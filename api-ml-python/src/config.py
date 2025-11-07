from pathlib import Path
import os

# URL do arquivo zip do German Credit Data
GERMAN_CREDIT_ZIP_URL = "https://archive.ics.uci.edu/static/public/144/statlog+german+credit+data.zip"

# Nome do arquivo .data que será salvo
GERMAN_CREDIT_DATA = "credit_data.data"

# --- Definição de Caminhos---
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / 'data'
RAW_DATA_DIR = DATA_DIR / 'raw'
PROCESSED_DATA_DIR = DATA_DIR / 'processed'

# Cria as pastas data, data/raw e data/processed se não existirem
def _create_directories():
    """
    Cria os diretórios necessários para armazenar os dados brutos e processados.
    """
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)

_create_directories()


# Renomeia as colunas de acordo com a documentação
COLUMN_NAMES = [
    'checking_account_status',
    'duration_in_month',
    'credit_history',
    'purpose',
    'credit_amount',
    'savings_account_bonds',
    'present_employment_since',
    'installment_rate_percent',
    'personal_status_and_sex',
    'other_debtors_guarantors',
    'present_residence_since',
    'property',
    'age_in_years',
    'other_installment_plans',
    'housing',
    'number_of_existing_credits',
    'job',
    'number_of_dependents',
    'telephone',
    'foreign_worker',
    'risk'
]

# --- Definição de Tipos de Colunas ---
# Colunas numéricas (valores contínuos e discretos)
NUMERIC_COLUMNS = [
    'duration_in_month',
    'credit_amount',
    'installment_rate_percent',
    'present_residence_since',
    'age_in_years',
    'number_of_existing_credits',
    'number_of_dependents'
]

# Colunas categóricas (valores categóricos/ordinais)
CATEGORICAL_COLUMNS = [
    'checking_account_status',
    'credit_history',
    'purpose',
    'savings_account_bonds',
    'present_employment_since',
    'personal_status_and_sex',
    'other_debtors_guarantors',
    'property',
    'other_installment_plans',
    'housing',
    'job',
    'telephone',
    'foreign_worker'
]

# Coluna target
TARGET_COLUMN = 'risk'
