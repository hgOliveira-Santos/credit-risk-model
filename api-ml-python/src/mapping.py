MAPPINGS = {
    'checking_account_status': {
        'A11': 'negative_balance',
        'A12': 'low_balance',
        'A13': 'moderate_balance',
        'A14': 'no_account'
    },
    
    'credit_history': {
        'A30': 'no_credits_all_paid',
        'A31': 'all_paid_duly',
        'A32': 'existing_paid_duly',
        'A33': 'delay_in_past',
        'A34': 'critical_account'
    },
    
    'purpose': {
        'A40': 'car_new',
        'A41': 'car_used',
        'A42': 'furniture_equipment',
        'A43': 'radio_tv',
        'A44': 'domestic_appliances',
        'A45': 'repairs',
        'A46': 'education',
        'A48': 'retraining',
        'A49': 'business',
        'A410': 'others'
    },
    
    'savings_account_bonds': {
        'A61': 'very_low',
        'A62': 'low',
        'A63': 'moderate',
        'A64': 'high',
        'A65': 'unknown_none'
    },
    
    'present_employment_since': {
        'A71': 'unemployed',
        'A72': 'less_than_1yr',
        'A73': '1_to_4yrs',
        'A74': '4_to_7yrs',
        'A75': 'more_than_7yrs'
    },
    
    'personal_status_and_sex': {
        'A91': 'male_divorced_separated',
        'A92': 'female_divorced_separated_married',
        'A93': 'male_single',
        'A94': 'male_married_widowed'
    },
    
    'other_debtors_guarantors': {
        'A101': 'none',
        'A102': 'co_applicant',
        'A103': 'guarantor'
    },
    
    'property': {
        'A121': 'real_estate',
        'A122': 'life_insurance_savings',
        'A123': 'car',
        'A124': 'no_property_unknown'
    },
    
    'other_installment_plans': {
        'A141': 'bank',
        'A142': 'stores',
        'A143': 'none'
    },
    
    'housing': {
        'A151': 'rent',
        'A152': 'own',
        'A153': 'free'
    },
    
    'job': {
        'A171': 'unskilled_non_resident',
        'A172': 'unskilled_resident',
        'A173': 'skilled',
        'A174': 'highly_skilled_management'
    },
    
    'telephone': {
        'A191': 'no',
        'A192': 'yes'
    },
    
    'foreign_worker': {
        'A201': 'yes',
        'A202': 'no'
    },
}

def apply_mappings(df):    
    for column, mapping in MAPPINGS.items():
        if column in df.columns:
            df[column] = df[column].map(mapping)