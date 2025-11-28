import duckdb
import requests
import zipfile
from pathlib import Path
from typing import List

# Importamos o módulo inteiro para evitar "from ... import A, B, C, D"
import src.config as cfg

class DuckDBCreditETL:
    def __init__(
        self, 
        raw_dir: Path = cfg.RAW_DATA_DIR, 
        processed_dir: Path = cfg.PROCESSED_DATA_DIR,
        column_names: List[str] = cfg.COLUMN_NAMES
    ) -> None:
        """
        Inicializa o ETL com caminhos e configurações.
        Permite sobrescrever caminhos para testes (Dependency Injection).
        """
        self.raw_dir = raw_dir
        self.processed_dir = processed_dir
        self.column_names = column_names
        
        # Garante que as pastas existem na inicialização
        self._setup_directories()

    def _setup_directories(self):
        """Cria a estrutura de pastas se não existir."""
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.processed_dir.mkdir(parents=True, exist_ok=True)

    def _download_file(self, url: str, dest_path: Path) -> Path:
        """Baixa o arquivo ZIP e retorna o caminho salvo."""
        print(f"[EXTRACT] Baixando de {url}...")
        
        try:
            res = requests.get(url, timeout=60, stream=True)
            res.raise_for_status()
            
            with open(dest_path, "wb") as f:
                for chunk in res.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"[OK] Download salvo em: {dest_path}")
            return dest_path
            
        except requests.exceptions.RequestException as e:
            print(f"[ERRO] Falha no download: {e}")
            raise e

    def _extract_zip(self, zip_path: Path) -> Path:
        """
        Extrai o ZIP e retorna o caminho do arquivo .data.
        Procura especificamente pelo arquivo 'german.data' dentro do zip.
        """
        print(f"[EXTRACT] Descompactando {zip_path.name}...")
        
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(self.raw_dir)
            
        # O arquivo dentro do zip da UCI geralmente se chama 'german.data'
        # Vamos procurar por qualquer arquivo .data extraído
        extracted_file = next(self.raw_dir.glob("*.data"), None)
        
        if not extracted_file:
            raise FileNotFoundError("Nenhum arquivo .data encontrado após descompactação.")
            
        return extracted_file

    def _data_to_parquet(self, source_data_path: Path) -> Path:
        """
        Lê o arquivo .data bruto (sem header), aplica nomes de colunas
        e salva como Parquet otimizado usando DuckDB.
        """
        output_parquet = self.processed_dir / "credit_risk.parquet"
        print(f"[TRANSFORM] Convertendo {source_data_path.name} para Parquet...")

        # Monta a query SQL dinamicamente para renomear column0 -> checking_account, etc.
        # O read_csv_auto do DuckDB gera colunas genéricas quando não há header.
        select_clause = ", ".join(
            [f"column{i} AS {name}" for i, name in enumerate(self.column_names)]
        )

        con = duckdb.connect()
        
        # O dataset German Credit usa ESPAÇO como separador e não tem header
        query = f"""
            COPY (
                SELECT {select_clause}
                FROM read_csv('{source_data_path}', header=False, delim=' ', auto_detect=True)
            ) TO '{output_parquet}' (FORMAT 'PARQUET', CODEC 'ZSTD');
        """

        try:
            con.sql(query)
            print(f"[LOAD] Arquivo salvo com sucesso: {output_parquet}")
            return output_parquet
        except Exception as e:
            print(f"[ERRO] Falha na conversão DuckDB: {e}")
            raise e
        finally:
            con.close()

    def run_etl_pipeline(self):
        """Orquestra o pipeline completo."""
        print("-" * 50)
        print("INICIANDO PIPELINE DE DADOS (ETL)")
        print("-" * 50)

        # 1. Definir caminhos temporários
        zip_destiny = self.raw_dir / "temp_data.zip"

        # 2. Extract (Download + Unzip)
        self._download_file(url=cfg.GERMAN_CREDIT_ZIP_URL, dest_path=zip_destiny)
        raw_data_file = self._extract_zip(zip_destiny)

        # 3. Transform & Load (Data -> Parquet)
        final_path = self._data_to_parquet(raw_data_file)
        
        # 4. Limpar o zip e o .data bruto
        zip_destiny.unlink()
        
        print("-" * 50)
        print(f"PIPELINE CONCLUÍDO. DADOS EM: {final_path}")

if __name__ == "__main__":
    etl = DuckDBCreditETL()
    etl.run_etl_pipeline()