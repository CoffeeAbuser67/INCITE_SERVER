
# -*- coding: utf-8 -*-
"""
_PIN_ 🦀 
@author: henry # 
"""
import os
import django
import sys
import logging
logger = logging.getLogger(__name__)


# CurrentWorkDirectory = os.getcwd()
# sys.path.append(CurrentWorkDirectory)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true" #WARN Disable when not working with spyder

# Now set up Django
django.setup()

print(django.get_version())
# logger.info(django.get_version())


# ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
# ×●●●× ○○○○ ●●●● ○○○○ ●●●● ○○○○ ●●●● ○○○○ ●●●● ○○○○ ●●●● ○○○○ ●●●● ○○○○ ●●●● ○○○○ ●●●● ○○○○ ●●●● ○○○○ ●●●● ○○○○ ║                                                                                                  ║
# ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╝


import requests
import json
from pprint import pprint # Para imprimir o JSON de forma bonita

# URL base da nossa API
BASE_URL = "http://127.0.0.1:8000/api/v1/"

# Headers padrão para requisições com JSON
JSON_HEADERS = {
    'Content-Type': 'application/json'
}

# ✪ create_instituicao
def create_instituicao(data):
    """Cria uma nova instituição (POST)."""
    print("--- 1. CRIANDO UMA NOVA INSTITUIÇÃO ---")
    try:
        response = requests.post(
            f"{BASE_URL}instituicoes/", 
            data=json.dumps(data), 
            headers=JSON_HEADERS
        )
        response.raise_for_status()  # Lança um erro se a requisição falhar (status != 2xx)
        created_data = response.json()
        print("Instituição criada com sucesso!")
        pprint(created_data)
        return created_data
    except requests.exceptions.RequestException as e:
        print(f"Erro ao criar instituição: {e}")
        if e.response:
            print("Detalhes:", e.response.json())
        return None

# ✪ get_all_instituicoes
def get_all_instituicoes():
    """Busca todas as instituições (GET)."""
    print("\n--- 2. LISTANDO TODAS AS INSTITUIÇÕES ---")
    try:
        response = requests.get(f"{BASE_URL}instituicoes/")
        response.raise_for_status()
        pprint(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Erro ao listar instituições: {e}")

# ✪ update_instituicao
def update_instituicao(instituicao_id, data):
    """Atualiza uma instituição existente (PUT)."""
    print(f"\n--- 3. ATUALIZANDO A INSTITUIÇÃO ID={instituicao_id} ---")
    try:
        response = requests.put(
            f"{BASE_URL}instituicoes/{instituicao_id}/",
            data=json.dumps(data),
            headers=JSON_HEADERS
        )
        response.raise_for_status()
        updated_data = response.json()
        print("Instituição atualizada com sucesso!")
        pprint(updated_data)
        return updated_data
    except requests.exceptions.RequestException as e:
        print(f"Erro ao atualizar instituição: {e}")
        if e.response:
            print("Detalhes:", e.response.json())
        return None

# ✪ delete_instituicao
def delete_instituicao(instituicao_id):
    """Deleta uma instituição (DELETE)."""
    print(f"\n--- 4. DELETANDO A INSTITUIÇÃO ID={instituicao_id} ---")
    try:
        response = requests.delete(f"{BASE_URL}instituicoes/{instituicao_id}/")
        response.raise_for_status()
        # DELETE bem-sucedido retorna status 204 No Content
        if response.status_code == 204:
            print("Instituição deletada com sucesso!")
        else:
            print(f"Resposta inesperada: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Erro ao deletar instituição: {e}")


# ── ◯⫘⫘⫘⫘ MAIN ⫘⫘⫘⫘⫘⫸


instituicao_mock = {
    "nome": "Instituto de Testes Avançados (ITA)",
    "cidade": "São José dos Campos",
    "coordenador_responsavel": "Dr. Elara Vance",
    "email": "elara.vance@ita.br",
    "telefone": "(12) 99999-8888",
    "quantidade_pesquisadores": 5
}



# Executa o ciclo CRUD
created_instituicao = create_instituicao(instituicao_mock)

if created_instituicao:
    instituicao_id = created_instituicao['id']

    get_all_instituicoes()
    
    # Dados para atualização
    update_mock = instituicao_mock.copy()
    update_mock['nome'] = "Instituto de Testes Avançados - Atualizado (ITA)"
    update_instituicao(instituicao_id, update_mock)

    delete_instituicao(instituicao_id)

    get_all_instituicoes()