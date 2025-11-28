import duckdb
import requests
import zipfile
from pathlib import Path
from typing import List

import src.config as cfg


class DuckDBCreditETL:
    def __init__(
        self,
        raw_dir: Path = cfg.RAW_DATA_DIR,
        processed_dir: Path = cfg.PROCESSED_DATA_DIR,
        column_names: List[str] = cfg.COLUMN_NAMES,
    ) -> None:
        self.raw_dir = raw_dir
        self.processed_dir = processed_dir
        self.column_names = column_names

        self._setup_directories()

    def _setup_directories(self):
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.processed_dir.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    etl = DuckDBCreditETL()
    etl.run_etl_pipeline()
