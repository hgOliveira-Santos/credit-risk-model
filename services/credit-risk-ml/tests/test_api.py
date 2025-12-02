# Script de teste para a API de predição de risco de crédito
import requests
import json

# URL base da API
BASE_URL = "http://localhost:8001"


def test_health():
    """Testa o endpoint de health check"""
    print("=" * 50)
    print("Testando endpoint /health")
    print("=" * 50)

    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        print("✓ Health check passou!\n")
        return True
    except Exception as e:
        print(f"✗ Erro no health check: {e}\n")
        return False


def test_predict(age, credit_amount, duration, description):
    """Testa o endpoint de predição"""
    print("=" * 50)
    print(f"Teste: {description}")
    print("=" * 50)

    payload = {"age": age, "credit_amount": credit_amount, "duration": duration}

    print(f"Payload: {json.dumps(payload, indent=2)}")

    try:
        response = requests.post(f"{BASE_URL}/predict", json=payload)
        print(f"Status Code: {response.status_code}")
        result = response.json()
        print(f"Response: {json.dumps(result, indent=2)}")
        print("✓ Predição realizada com sucesso!\n")
        return True
    except Exception as e:
        print(f"✗ Erro na predição: {e}\n")
        return False


def main():
    """Executa todos os testes"""
    print("\n" + "=" * 50)
    print("TESTES DA API DE PREDIÇÃO DE RISCO DE CRÉDITO")
    print("=" * 50 + "\n")

    # Teste 1: Health check
    if not test_health():
        print("❌ A API não está respondendo. Verifique se o servidor está rodando.")
        return

    # Teste 2: Caso de baixo risco (jovem, valor baixo, duração curta)
    test_predict(
        age=25,
        credit_amount=2000,
        duration=12,
        description="Baixo risco: jovem, valor baixo, duração curta",
    )

    # Teste 3: Caso de alto risco (jovem, valor alto, duração longa)
    test_predict(
        age=20,
        credit_amount=15000,
        duration=48,
        description="Alto risco: jovem, valor alto, duração longa",
    )

    # Teste 4: Caso intermediário (idade média, valor médio, duração média)
    test_predict(
        age=40,
        credit_amount=5000,
        duration=24,
        description="Risco intermediário: idade média, valor médio, duração média",
    )

    # Teste 5: Caso de pessoa mais velha (menor risco)
    test_predict(
        age=65,
        credit_amount=8000,
        duration=36,
        description="Risco baixo: pessoa mais velha",
    )

    # Teste 6: Caso extremo de alto risco
    test_predict(
        age=18,
        credit_amount=20000,
        duration=60,
        description="Alto risco: muito jovem, valor muito alto, duração muito longa",
    )

    print("=" * 50)
    print("TESTES CONCLUÍDOS")
    print("=" * 50)


if __name__ == "__main__":
    main()
