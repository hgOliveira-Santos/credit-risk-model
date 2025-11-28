import duckdb
import requests
import zipfile
import os
from pathlib import Path

from src.config import RAW_DATA_DIR, PROCESSED_DATA_DIR


def _setup_directories():
    """Cria a estrutura de pastas se não existir."""
    print(f"[SETUP] Verificando diretórios...")
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)


def _download_file(url: str, file_dest: Path) -> bool:
    """Baixa o arquivo ZIP."""
    print(f"[EXTRACT] Baixando arquivo ZIP para: {file_dest}")

    try:
        res = requests.get(url, timeout=60, stream=True)
        res.raise_for_status()
        with open(file_dest, "wb") as f:
            for chunk in res.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    except Exception as e:
        print(f"Erro no download: {e}")
        return False


def _extract_zip(zip_path: Path, extract_to: Path):
    """Extrai o conteúdo do ZIP para a pasta raw."""
    print(f"[EXTRACT] Descompactando {zip_path}...")
    try:
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_to)
        print(f"Arquivos extraídos em {extract_to}")
    except Exception as e:
        print(f"Erro ao descompactar: {e}")
        raise e


def run_etl_pipeline():
    """
    Executa o pipeline ETL completo
    """

    _setup_directories()


if __name__ == "__main__":
    run_etl_pipeline()
