from typing import List
import pandas as pd
import requests
import zipfile
import os
from io import BytesIO
from . import config
import shutil
import logging
import sys


class CreditDataIngestion:
    """
    Classe para orquestrar o pipeline completo de ingestão de dados de crédito.
    """

    def __init__(
        self,
        url: str = config.GERMAN_CREDIT_ZIP_URL,
        raw_data_dir: str = config.RAW_DATA_DIR,
        processed_data_dir: str = config.PROCESSED_DATA_DIR,
        data_filename: str = config.GERMAN_CREDIT_DATA,
        column_names: List = config.COLUMN_NAMES,
    ):
        self.url = url
        self.raw_data_dir = raw_data_dir
        self.processed_data_dir = processed_data_dir
        self.data_filename = data_filename
        self.processed_filepath = os.path.join(processed_data_dir, data_filename)
        self.column_names = column_names

        # Configuração do Logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        if not self.logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            handler.setLevel(logging.INFO)
            formatter = logging.Formatter(
                "%(asctime)s - %(levelname)s - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def ingest(self, overwrite: bool = False, mappings: dict = None) -> pd.DataFrame:
        """
        Orquestra o pipeline de ingestão.
        """
        self.logger.info(">>> INICIANDO O PIPELINE DE INGESTÃO DE DADOS <<<")

        if os.path.exists(self.processed_filepath) and not overwrite:
            self.logger.info(
                f"Arquivo de dados já existe em '{self.processed_filepath}'. Pulando a ingestão."
            )
            self.logger.info("Carregando dados existentes...")
            return self._load_data_file(self.processed_filepath, self.column_names)

        try:
            download_success = self._download_zip_file(self.url, self.raw_data_dir)
            if not download_success:
                self.logger.error("Etapa de download falhou. Abortando o pipeline.")
                return pd.DataFrame()

            extract_success = self._extract_data_file_from_zip(
                self.data_filename, self.raw_data_dir, self.processed_data_dir
            )
            if not extract_success:
                self.logger.error(
                    "Etapa de extração do arquivo falhou. Abortando o pipeline."
                )
                return pd.DataFrame()

            df = self._load_data_file(self.processed_filepath, self.column_names)

            if mappings:
                df = self._apply_mappings(df, mappings)

            self.logger.info(
                ">>> PIPELINE DE INGESTÃO DE DADOS CONCLUÍDO COM SUCESSO <<<"
            )
            return df

        except Exception as e:
            self.logger.critical(
                f"Ocorreu um erro crítico e inesperado no pipeline: {e}"
            )
            return pd.DataFrame()

    def _download_zip_file(self, url: str, destination_folder: str) -> bool:
        self.logger.info(f"Iniciando download de {url}")
        try:
            os.makedirs(destination_folder, exist_ok=True)

            response = requests.get(url)
            response.raise_for_status()

            with zipfile.ZipFile(BytesIO(response.content)) as zip_ref:
                zip_ref.extractall(destination_folder)

            self.logger.info(
                f"Arquivos extraídos com sucesso para: {destination_folder}"
            )
            return True

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Erro de conexão durante o download: {e}")
            return False
        except zipfile.BadZipFile:
            self.logger.error(
                "O arquivo baixado não é um ZIP válido ou está corrompido."
            )
            return False
        except Exception as e:
            self.logger.error(f"Ocorreu um erro inesperado em 'download_zip_file': {e}")
            return False

    def _extract_data_file_from_zip(
        self,
        filename: str,
        source_folder: str,
        destination_folder: str,
        file_extension: str = ".data",
    ) -> bool:
        self.logger.info(
            f"Procurando por arquivo '{file_extension}' em '{source_folder}'..."
        )
        try:
            file_found = False
            for found_filename in os.listdir(source_folder):
                source_filepath = os.path.join(source_folder, found_filename)

                if found_filename.endswith(file_extension):
                    file_found = True
                    self.logger.info(f"Arquivo alvo encontrado: '{found_filename}'")

                    renamed_filepath = os.path.join(source_folder, filename)
                    final_destination_filepath = os.path.join(
                        destination_folder, filename
                    )

                    if os.path.exists(renamed_filepath):
                        os.remove(renamed_filepath)
                    os.rename(source_filepath, renamed_filepath)
                    self.logger.info(f"Arquivo renomeado para: '{filename}'")

                    os.makedirs(destination_folder, exist_ok=True)
                    if os.path.exists(final_destination_filepath):
                        os.remove(final_destination_filepath)
                    shutil.move(renamed_filepath, final_destination_filepath)
                    self.logger.info(f"Arquivo movido para: '{destination_folder}'")

                elif os.path.isfile(source_filepath):
                    os.remove(source_filepath)
                    self.logger.info(f"Arquivo extra '{found_filename}' removido.")

            if not file_found:
                self.logger.warning(
                    f"Nenhum arquivo com extensão '{file_extension}' foi encontrado em '{source_folder}'."
                )
                return False

            return True
        except Exception as e:
            self.logger.error(f"Ocorreu um erro ao extrair e mover o arquivo: {e}")
            return False

    def _load_data_file(self, data_filepath: str, column_names: List) -> pd.DataFrame:
        self.logger.info(f"Carregando dados de '{data_filepath}' para o DataFrame.")
        try:
            df = pd.read_csv(
                data_filepath,
                sep=r"\s+",
                header=None,
                names=column_names,
                encoding="latin1",
            )
            self.logger.info("DataFrame carregado com sucesso.")
            return df
        except FileNotFoundError:
            self.logger.error(f"Arquivo de dados não encontrado em: {data_filepath}")
            return pd.DataFrame()
        except Exception as e:
            self.logger.error(f"Ocorreu um erro ao carregar o arquivo CSV: {e}")
            return pd.DataFrame()

    def _apply_mappings(self, df: pd.DataFrame, mappings: dict) -> pd.DataFrame:
        self.logger.info("Aplicando mapeamentos nas variáveis categóricas...")

        df_mapped = df.copy()

        for column, mapping in mappings.items():
            if column in df_mapped.columns:
                df_mapped[column] = df_mapped[column].map(mapping)
                self.logger.debug(f"Mapeamento aplicado na coluna '{column}'")
            else:
                self.logger.warning(f"Coluna '{column}' não encontrada no DataFrame")

        self.logger.info("Mapeamentos aplicados com sucesso")
        return df_mapped
