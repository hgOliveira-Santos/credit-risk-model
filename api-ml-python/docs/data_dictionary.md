# Dicionário de Dados - Projeto de Risco de Crédito

## Informações Gerais

- **Nome do Dataset:** Statlog (German Credit Data)
- **Fonte Original:** [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/144/statlog+german+credit+data)
- **Data de Acesso:** 27 de Setembro de 2025
- **Descrição:** Este conjunto de dados classifica 1000 indivíduos, descritos por um conjunto de 20 atributos, como "bom" ou "mau" risco de crédito. O objetivo é construir um modelo preditivo para essa classificação.

---

## Descrição das Colunas (Atributos)

| Nome da Coluna | Tipo de Dado | Descrição | Valores Possíveis |
| :--- | :--- | :--- | :--- |
| `checking_account_status` | Categórico | Status da conta corrente existente. | `A11`: < 0 DM <br> `A12`: 0 <= ... < 200 DM <br> `A13`: >= 200 DM <br> `A14`: Nenhuma conta corrente |
| `duration_in_month` | Numérico | Duração do crédito solicitada, em meses. | Inteiro |
| `credit_history` | Categórico | Histórico de crédito do cliente. | `A30`: Nenhum crédito/todos pagos <br> `A31`: Todos os créditos neste banco pagos em dia <br> `A32`: Créditos existentes pagos em dia até agora <br> `A33`: Atraso no pagamento no passado <br> `A34`: Conta crítica/outros créditos existentes |
| `purpose` | Categórico | Propósito do empréstimo. | `A40`: Carro (novo) <br> `A41`: Carro (usado) <br> `A42`: Móveis/Equipamentos <br> `A43`: Rádio/Televisão <br> `A44`: Eletrodomésticos <br> `A45`: Reparos <br> `A46`: Educação <br> `A48`: Retreinamento <br> `A49`: Negócios <br> `A410`: Outros |
| `credit_amount` | Numérico | Valor total do crédito solicitado. | Inteiro |
| `savings_account_bonds` | Categórico | Saldo em conta poupança/títulos. | `A61`: < 100 DM <br> `A62`: 100 <= ... < 500 DM <br> `A63`: 500 <= ... < 1000 DM <br> `A64`: >= 1000 DM <br> `A65`: Desconhecido/sem conta poupança |
| `present_employment_since` | Categórico | Tempo no emprego atual. | `A71`: Desempregado <br> `A72`: < 1 ano <br> `A73`: 1 <= ... < 4 anos <br> `A74`: 4 <= ... < 7 anos <br> `A75`: >= 7 anos |
| `installment_rate_percent` | Numérico | Taxa de parcelamento em % da renda disponível. | Inteiro |
| `personal_status_and_sex` | Categórico | Estado civil e sexo do cliente. | `A91`: Masculino: Divorciado/Separado <br> `A92`: Feminino: Divorciada/Separada/Casada <br> `A93`: Masculino: Solteiro <br> `A94`: Masculino: Casado/Viúvo |
| `other_debtors_guarantors` | Categórico | Indica a existência de outros devedores ou fiadores. | `A101`: Nenhum <br> `A102`: Co-requerente <br> `A103`: Fiador |
| `present_residence_since` | Numérico | Tempo de residência no endereço atual (em anos). | Inteiro |
| `property` | Categórico | Principal propriedade do cliente. | `A121`: Imóvel <br> `A122`: Seguro de vida/poupança para construção <br> `A123`: Carro <br> `A124`: Nenhuma propriedade/Desconhecido |
| `age_in_years` | Numérico | Idade do cliente em anos. | Inteiro |
| `other_installment_plans` | Categórico | Outros planos de pagamento/parcelamento. | `A141`: Em outros bancos <br> `A142`: Em lojas <br> `A143`: Nenhum |
| `housing` | Categórico | Situação de moradia. | `A151`: Aluguel <br> `A152`: Própria <br> `A153`: De favor (gratuita) |
| `number_of_existing_credits`| Numérico | Número de créditos existentes neste banco. | Inteiro |
| `job` | Categórico | Tipo de trabalho/ocupação. | `A171`: Não qualificado/não residente <br> `A172`: Não qualificado/residente <br> `A173`: Qualificado/funcionário <br> `A174`: Altamente qualificado/gerência/autônomo |
| `number_of_dependents` | Numérico | Número de dependentes financeiros do cliente. | Inteiro |
| `telephone` | Categórico | Se o cliente possui um telefone registrado em seu nome. | `A191`: Não <br> `A192`: Sim |
| `foreign_worker` | Categórico | Se o cliente é um trabalhador estrangeiro. | `A201`: Sim <br> `A202`: Não |
| `risk` | Categórica (Alvo)| **Variável Alvo:** Classificação de risco de crédito. | `1`: Bom Risco <br> `2`: Mau Risco |

---
