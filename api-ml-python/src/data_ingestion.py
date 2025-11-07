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


# ==============================================================================
# Configuração do Logger
# ==============================================================================

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)


# ==============================================================================
# Função Principal do Pipeline de Ingestão
# ==============================================================================
def ingest_credit_data(
    url: str = config.GERMAN_CREDIT_ZIP_URL, overwrite: bool = False
) -> pd.DataFrame:
    """
    Orquestra o pipeline completo de ingestão de dados de crédito.
    """
    logger.info(">>> INICIANDO O PIPELINE DE INGESTÃO DE DADOS <<<")

    # --- 1. Configuração de Caminhos ---
    raw_data_dir = config.RAW_DATA_DIR
    processed_data_dir = config.PROCESSED_DATA_DIR
    data_filename = config.GERMAN_CREDIT_DATA
    processed_filepath = os.path.join(processed_data_dir, data_filename)

    # --- 2. Verificação de Desempenho (Idempotência) ---
    if os.path.exists(processed_filepath) and not overwrite:
        logger.info(
            f"Arquivo de dados já existe em '{processed_filepath}'. Pulando a ingestão."
        )
        logger.info("Carregando dados existentes...")
        return load_data_file(processed_filepath)

    # --- 3. Execução do Pipeline ---
    try:
        # Etapa de Download
        download_success = download_zip_file(url, raw_data_dir)
        if not download_success:
            logger.error("Etapa de download falhou. Abortando o pipeline.")
            return pd.DataFrame()

        # Etapa de Extração
        extract_success = extract_data_file_from_zip(
            data_filename, raw_data_dir, processed_data_dir
        )
        if not extract_success:
            logger.error("Etapa de extração do arquivo falhou. Abortando o pipeline.")
            return pd.DataFrame()

        # Etapa de Carregamento
        df = load_data_file(processed_filepath)
        logger.info(">>> PIPELINE DE INGESTÃO DE DADOS CONCLUÍDO COM SUCESSO <<<")
        return df

    except Exception as e:
        logger.critical(f"Ocorreu um erro crítico e inesperado no pipeline: {e}")
        return pd.DataFrame()


# ==============================================================================
# Funções Auxiliares do Pipeline
# ==============================================================================
def download_zip_file(url: str, destination_folder: str) -> bool:
    logger.info(f"Iniciando download de {url}")
    try:
        os.makedirs(destination_folder, exist_ok=True)

        response = requests.get(url)
        response.raise_for_status()

        with zipfile.ZipFile(BytesIO(response.content)) as zip_ref:
            zip_ref.extractall(destination_folder)

        logger.info(f"Arquivos extraídos com sucesso para: {destination_folder}")
        return True

    except requests.exceptions.RequestException as e:
        logger.error(f"Erro de conexão durante o download: {e}")
        return False
    except zipfile.BadZipFile:
        logger.error("O arquivo baixado não é um ZIP válido ou está corrompido.")
        return False
    except Exception as e:
        logger.error(f"Ocorreu um erro inesperado em 'download_zip_file': {e}")
        return False


def extract_data_file_from_zip(
    filename: str,
    source_folder: str,
    destination_folder: str,
    file_extension: str = ".data",
) -> bool:
    logger.info(f"Procurando por arquivo '{file_extension}' em '{source_folder}'...")
    try:
        file_found = False
        for found_filename in os.listdir(source_folder):
            source_filepath = os.path.join(source_folder, found_filename)

            if found_filename.endswith(file_extension):
                file_found = True
                logger.info(f"Arquivo alvo encontrado: '{found_filename}'")

                renamed_filepath = os.path.join(source_folder, filename)
                final_destination_filepath = os.path.join(destination_folder, filename)

                if os.path.exists(renamed_filepath):
                    os.remove(renamed_filepath)
                os.rename(source_filepath, renamed_filepath)
                logger.info(f"Arquivo renomeado para: '{filename}'")

                os.makedirs(destination_folder, exist_ok=True)
                if os.path.exists(final_destination_filepath):
                    os.remove(final_destination_filepath)
                shutil.move(renamed_filepath, final_destination_filepath)
                logger.info(f"Arquivo movido para: '{destination_folder}'")

            elif os.path.isfile(source_filepath):
                os.remove(source_filepath)
                logger.info(f"Arquivo extra '{found_filename}' removido.")

        if not file_found:
            logger.warning(
                f"Nenhum arquivo com extensão '{file_extension}' foi encontrado em '{source_folder}'."
            )
            return False

        return True
    except Exception as e:
        logger.error(f"Ocorreu um erro ao extrair e mover o arquivo: {e}")
        return False


def load_data_file(
    data_filepath: str, column_names: List = config.COLUMN_NAMES
) -> pd.DataFrame:
    logger.info(f"Carregando dados de '{data_filepath}' para o DataFrame.")
    try:
        df = pd.read_csv(
            data_filepath,
            sep=r"\s+",
            header=None,
            names=column_names,
            encoding="latin1",
        )
        logger.info("DataFrame carregado com sucesso.")
        return df
    except FileNotFoundError:
        logger.error(f"Arquivo de dados não encontrado em: {data_filepath}")
        return pd.DataFrame()
    except Exception as e:
        logger.error(f"Ocorreu um erro ao carregar o arquivo CSV: {e}")
        return pd.DataFrame()
