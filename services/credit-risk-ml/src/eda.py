import pandas as pd
import numpy as np
import logging
import skrub

from src.credit_ingestor import CreditDataIngestion


class CreditRiskEDA:
    def __init__(self) -> None:
        self.data = None

    def load_data(self) -> pd.DataFrame:
        print("=" * 70)
        print("CARREGAMENTO DOS DADOS".center(70))
        print("=" * 70)

        data_loader = CreditDataIngestion()
        self.data = data_loader.ingest()

        print("✓ Dados carregados com sucesso!".center(70))
        print(
            f"✓ Shape: {self.data.shape[0]} linhas x {self.data.shape[1]} colunas".center(
                70
            )
        )
        print("\n")

        return self.data

    def overview(self):
        self.show_skrub_report()

    def analyze_target_variable(self):
        pass

    def show_skrub_report(self):
        """Gera e exibe o relatório do TableReport."""
        logging.getLogger().setLevel(logging.ERROR)
        skrub.TableReport(self.data).open()
        logging.getLogger().setLevel(logging.INFO)

    def run_full_analysis(self):
        """Executa a análise exploratória completa."""
        print("\n")
        print(("╔" + "═" * 68 + "╗").center(70))
        print(("║" + "ANÁLISE EXPLORATÓRIA DE DADOS".center(68) + "║").center(70))
        print(("╚" + "═" * 68 + "╝").center(70))
        print("\n")

        self.load_data()
        self.overview()
        self.analyze_target_variable()

        print("=" * 70)
        print("ANÁLISE CONCLUÍDA COM SUCESSO!".center(70))
        print("=" * 70)
        print("\n")
