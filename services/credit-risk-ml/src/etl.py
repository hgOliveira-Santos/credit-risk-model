import duckdb
import requests
import zipfile
from pathlib import Path
from typing import List

import src.config as cfg


class CreditETL:
    def __init__(
        self,
        raw_dir: Path = cfg.RAW_DATA_DIR,
        processed_dir: Path = cfg.PROCESSED_DATA_DIR,
        file_url: str = cfg.GERMAN_CREDIT_ZIP_URL,
        file_name: str = cfg.CREDIT_DATA,
        column_names: List[str] = cfg.COLUMN_NAMES,
    ) -> None:
        self.raw_dir = raw_dir
        self.processed_dir = processed_dir
        self.file_url = file_url
        self.column_names = column_names

        self.destiny_path = raw_dir / file_name

        self._setup_directories()

    def _setup_directories(self):
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.processed_dir.mkdir(parents=True, exist_ok=True)

    def _download_file(self):
        print(f"[EXTRACT] Baixando de {self.file_url} ...")

        try:
            res = requests.get(self.file_url, timeout=60, stream=True)
            res.raise_for_status()

            with open(self.destiny_path, "wb") as f:
                for chunk in res.iter_content(chunk_size=8192):
                    f.write(chunk)

            print(f"[OK] Download salvo em: {self.destiny_path}")
            return

        except Exception as e:
            print(f"[ERRO] Falha no download: {e}")
            raise e

    def _extract_zip(self):

        print(f"[EXTRACT] Descompactando {self.file_url}...")

        try:
            pass
        except Exception as e:
            print(f"[ERRO] Falha na extração do arquivo ZIP: {e}")
            raise e

    def run_etl_pipeline(self):
        self._download_file()


if __name__ == "__main__":
    etl = CreditETL()
    etl.run_etl_pipeline()
