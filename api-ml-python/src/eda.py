import pandas as pd


class CreditRiskEDA:
    def __init__(self, data_path: str) -> None:
        self.data_path = data_path
        self.data = None

    def load_data(self) -> pd.DataFrame:
        print("=" * 70)
        print("CARREGAMENTO DOS DADOS")
        print("=" * 70)

        self.data = pd.read_csv(self.data_path)

        print(f"✓ Dados carregados com sucesso!")
        print(f"✓ Shape: {self.data.shape[0]} linhas x {self.data.shape[1]} colunas\n")

        return self.data
