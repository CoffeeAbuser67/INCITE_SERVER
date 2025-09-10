# -*- coding: utf-8 -*-
"""
_PIN_ 🦀 
@author: HM
"""
import os
import django
import logging
logger = logging.getLogger(__name__)

import io 
from faker import Faker
import requests
import time
from PIL import Image

# CurrentWorkDirectory = os.getcwd()
# sys.path.append(CurrentWorkDirectory)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true" #WARN Disable when not working with spyder


# Now set up Django
django.setup()

fake = Faker('pt_BR')
print(f"Django Version: {django.get_version()}")


# logger.info(django.get_version())
# from django.contrib.auth import get_user_model
# User = get_user_model()'
# print(User._meta.get_fields())  


# ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
#  ø●○● ○○○○ ●●●● ○○○○ ●●●● ○○○○ ●●●● ○○○○ ●●●● ○○○○ ●●●● ○○○○ ●●●● ○○○○ ●●●● ○○○○ ●●●● ○○○○ ●●●● ○○○○ ●●●● ○○○ø ║                                                                                 ║
# ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╝
# ┌───────┐
# │ UTILS │
# └───────┘

# (●) timer
def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(
            f"Function {func.__name__} took {end_time - start_time:.6f} seconds to execute."
        )
        return result

    return wrapper
# ── ⋙── ── ── ── ── ── ── ──➤

# ◯⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫸
# ┌────────────┐
# │ MyUSerTest │
# └────────────┘

# (✪) MyUSerTest
class MyUSerTest:
    
    # (●) mountAuthHeader
    @staticmethod
    def mountAuthHeader(cookies):
        cookies = [
            f"access-token={cookies.get('access-token')};",
            f"refresh-token={cookies.get('refresh-token')};"
        ]
        cookie_str = " ".join(cookies)
        return {"Cookie": cookie_str}
    
    
    # (●) read_user
    @staticmethod
    def get_user(custom_header, _prefix="http://127.0.0.1:8000/api/v1"):
        url = _prefix + "/auth/user/"
        response = requests.get(url, headers=custom_header)
        print(f"Status code: {response.status_code}")
        print(f"Response body: {response.json()}")
        
        return response


    # (●) login
    @staticmethod
    def login(sample: dict, _prefix="http://127.0.0.1:8000/api/v1"):
        url = _prefix + "/auth/login/"
        response = requests.post(url, json=sample)
        print(f"Status code: {response.status_code}")
        print(f"Response body: {response.json()}")
        auth_header = MyUSerTest.mountAuthHeader(response.cookies)
        return response, auth_header


    # (●) subscribe
    @staticmethod
    def subscribe(sample: dict, _prefix="http://127.0.0.1:8000/api/v1"):
        url = _prefix + "/auth/registration/"
        response = requests.post(url, json=sample)
        print(f"Status code: {response.status_code}")
        print(f"Response body: {response.json()}")
        return response
    
    

    
    # (●) logout
    @staticmethod
    def logout(_prefix="http://127.0.0.1:8000/api/v1"):
        url = _prefix + "/auth/logout/"
        body = {}
        response = requests.post(url, json=body)
        print(f"Status code: {response.status_code}")
        print(f"Response body: {response.json()}")
# ── ⋙── ── ── ── ── ── ── ──➤

# ◯⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫸


# ┌────────────────┐
# │ InciteAPITests │
# └────────────────┘

# ┌────────────────┐
# │ InciteAPITests │
# └────────────────┘

class InciteAPITests:
    
    @staticmethod
    @timer
    def create_instituicao(auth_header, _prefix="http://127.0.0.1:8000/api/v1"):
        print("\n--- ❶ Testando: Criar Instituição (POST) ---")
        url = _prefix + "/instituicoes/"
        
        instituicao_data = {
            'nome': f"Instituição de Teste - {fake.company()}",
            'coordenador_responsavel': fake.name(),
            'email': fake.unique.email(),
            'telefone': fake.phone_number()
        }
        
        image_buffer = io.BytesIO()
        image = Image.new('RGB', (100, 100), 'blue') # Mudei a cor para azul para diferenciar
        image.save(image_buffer, format='PNG')
        image_buffer.seek(0)
        
        files = {'marcador_logo': ('logo.png', image_buffer, 'image/png')}
        
        response = requests.post(url, headers=auth_header, data=instituicao_data, files=files)
        
        print(f"Status code: {response.status_code}")
        print(f"Response body: {response.json()}")
        return response

    @staticmethod
    @timer
    def list_instituicoes(auth_header, _prefix="http://127.0.0.1:8000/api/v1"):
        print("\n--- ❷ Testando: Listar Instituições (GET) ---")
        url = _prefix + "/instituicoes/"
        response = requests.get(url, headers=auth_header)
        
        print(f"Status code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Encontradas {len(data)} instituições.")
        else:
            print(f"Response body: {response.text}")
        return response

    # ▼▼▼ NOVOS MÉTODOS ADICIONADOS AQUI ▼▼▼

    @staticmethod
    @timer
    def retrieve_instituicao(auth_header, instituicao_id, _prefix="http://127.0.0.1:8000/api/v1"):
        print(f"\n--- ❸ Testando: Detalhar Instituição ID:{instituicao_id} (GET) ---")
        url = f"{_prefix}/instituicoes/{instituicao_id}/"
        response = requests.get(url, headers=auth_header)
        
        print(f"Status code: {response.status_code}")
        if response.ok:
            print(f"Response body: {response.json()}")
        return response

    @staticmethod
    @timer
    def update_instituicao(auth_header, instituicao_id, _prefix="http://127.0.0.1:8000/api/v1"):
        print(f"\n--- ❹ Testando: Atualizar Instituição ID:{instituicao_id} (PATCH) ---")
        url = f"{_prefix}/instituicoes/{instituicao_id}/"
        
        update_payload = {
            'nome': f"NOME ATUALIZADO - {fake.company()}",
            'informacoes_adicionais': "Este campo foi atualizado pelo script de teste."
        }
        
        response = requests.patch(url, headers=auth_header, json=update_payload)
        
        print(f"Status code: {response.status_code}")
        if response.ok:
            print(f"Response body: {response.json()}")
        return response

    @staticmethod
    @timer
    def delete_instituicao(auth_header, instituicao_id, _prefix="http://127.0.0.1:8000/api/v1"):
        print(f"\n--- ❺ Testando: Deletar Instituição ID:{instituicao_id} (DELETE) ---")
        url = f"{_prefix}/instituicoes/{instituicao_id}/"
        response = requests.delete(url, headers=auth_header)
        
        print(f"Status code: {response.status_code}")
        # Uma deleção bem-sucedida retorna 204 No Content, que não tem corpo
        if response.status_code == 204:
            print("Instituição deletada com sucesso.")
        return response

# ◯⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫘⫸


# ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
#  TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST ║                                                                                                  ║
# ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╝
    
# ┌──────────────────┐
# │ PEFORM SUBSCRIBE │
# └──────────────────┘

sample = {
    "first_name": 'nengue2',
    "last_name": 'M',
    "email": "teste02@gmail.com",
    "password1": "123Querty",
    "password2": "123Querty",
    "user_group": 1  
}

# (○) subscribe(sample)
res = MyUSerTest.subscribe(sample)

# ┌──────────────┐
# │ PEFORM LOGIN │
# └──────────────┘
sample = {"email": 'teste02@gmail.com', "password": '123Querty'}
login_res, auth_header = MyUSerTest.login(sample)


login_res.cookies.items()


# ┌────────────────────────┐
# │ PEFORM GET ACTIVE USER │
# └────────────────────────┘
res = MyUSerTest.get_user(auth_header)


# ┌───────────────┐
# │ REFRESH TOKEN │
# └───────────────┘
_prefix="http://127.0.0.1:8000/api/v1"
url = _prefix + "/auth/token/refresh/"
response = requests.post(url, headers=auth_header, json={})
response.cookies.items()
refreshed_auth_header = MyUSerTest.mountAuthHeader(response.cookies)
print(f"Status code: {response.status_code}")
print(f"Response body: {response.json()}")


# ┌───────────────┐
# │ PEFORM LOGOUT │
# └───────────────┘
res = MyUSerTest.logout()



# ══════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
#  TEST FLOW - INSTITUIÇÕES CRUD                                                                                ║
# ══════════════════════════════════════════════════════════════════════════════════════════════════════════════╝


# ┌──────────────────────────┐
# │  Bloco 1: CREATE & LIST  │
# └──────────────────────────┘
create_res = InciteAPITests.create_instituicao(auth_header)
assert create_res.status_code == 201, "Falha ao criar instituição!"

# Extrai o ID da instituição que acabamos de criar para usar nos próximos testes
created_instituicao_id = create_res.json()['id']
print(f"--> ID da Instituição criada para os testes: {created_instituicao_id}")

list_res = InciteAPITests.list_instituicoes(auth_header)
assert list_res.status_code == 200, "Falha ao listar instituições!"
assert len(list_res.json()) > 0, "A lista de instituições está vazia."


# ┌────────────────────────────────────┐
# │ Bloco 2: RETRIEVE, UPDATE & DELETE │
# └────────────────────────────────────┘

# Teste de Retrieve (Detalhe)
retrieve_res_before = InciteAPITests.retrieve_instituicao(auth_header, created_instituicao_id)
assert retrieve_res_before.status_code == 200, "Falha ao buscar detalhes da instituição!"

# Teste de Update (Atualização)
update_res = InciteAPITests.update_instituicao(auth_header, created_instituicao_id)
assert update_res.status_code == 200, "Falha ao atualizar a instituição!"

# Verificação do Update: busca o mesmo objeto de novo e confere se os dados mudaram
print("\n--- Verificando se a atualização foi salva ---")
retrieve_res_after = InciteAPITests.retrieve_instituicao(auth_header, created_instituicao_id)
updated_data = retrieve_res_after.json()
assert "NOME ATUALIZADO" in updated_data['nome'], "O nome da instituição não foi atualizado corretamente."
assert updated_data['informacoes_adicionais'] is not None, "As informações adicionais não foram atualizadas."
print("--> Verificação de Update bem-sucedida!")

# Teste de Delete (Remoção)
delete_res = InciteAPITests.delete_instituicao(auth_header, created_instituicao_id)
assert delete_res.status_code == 204, "Falha ao deletar a instituição!"

# Verificação do Delete: tenta buscar a instituição de novo e espera um erro 404
print("\n--- Verificando se a deleção foi efetiva ---")
retrieve_res_deleted = InciteAPITests.retrieve_instituicao(auth_header, created_instituicao_id)
assert retrieve_res_deleted.status_code == 404, "A instituição ainda existe após a deleção, o que não deveria acontecer."
print("--> Verificação de Delete bem-sucedida!")

print("\n✅ Todos os testes de CRUD para Instituições foram executados com sucesso!")


















# ┌─────────────────────┐
# │ PesquisadorAPITests │
# └─────────────────────┘

class PesquisadorAPITests:
    
    @staticmethod
    @timer
    def create_pesquisador(auth_header, instituicao_id, _prefix="http://127.0.0.1:8000/api/v1"):
        print(f"\n---  criando pesquisador para a Instituição ID:{instituicao_id} (POST) ---")
        url = _prefix + "/pesquisadores/"
        
        payload = {
            "nome": fake.name(),
            "area_atuacao": fake.job(),
            "desligado": False,
            "bolsista": fake.pybool(),
            "instituicao": instituicao_id  # Associamos à instituição criada anteriormente
        }
        
        response = requests.post(url, headers=auth_header, json=payload)
        
        print(f"Status code: {response.status_code}")
        print(f"Response body: {response.json()}")
        return response

    @staticmethod
    @timer
    def list_pesquisadores(auth_header, _prefix="http://127.0.0.1:8000/api/v1"):
        print("\n--- Listando todos os pesquisadores (GET) ---")
        url = _prefix + "/pesquisadores/"
        response = requests.get(url, headers=auth_header)
        
        print(f"Status code: {response.status_code}")
        if response.ok:
            print(f"Encontrados {len(response.json())} pesquisadores no total.")
        return response

    @staticmethod
    @timer
    def update_pesquisador(auth_header, pesquisador_id, _prefix="http://127.0.0.1:8000/api/v1"):
        print(f"\n--- Atualizando Pesquisador ID:{pesquisador_id} (PATCH) ---")
        url = f"{_prefix}/pesquisadores/{pesquisador_id}/"
        
        payload = {
            "area_atuacao": "Especialista em Testes Automatizados",
            "desligado": True
        }
        
        response = requests.patch(url, headers=auth_header, json=payload)
        
        print(f"Status code: {response.status_code}")
        print(f"Response body: {response.json()}")
        return response

    @staticmethod
    @timer
    def delete_pesquisador(auth_header, pesquisador_id, _prefix="http://127.0.0.1:8000/api/v1"):
        print(f"\n--- Deletando Pesquisador ID:{pesquisador_id} (DELETE) ---")
        url = f"{_prefix}/pesquisadores/{pesquisador_id}/"
        response = requests.delete(url, headers=auth_header)
        
        print(f"Status code: {response.status_code}")
        if response.status_code == 204:
            print("Pesquisador deletado com sucesso.")
        return response







# ══════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
#  TEST FLOW - PESQUISADORES CRUD                                                                               ║
# ══════════════════════════════════════════════════════════════════════════════════════════════════════════════╝

# ┌───────────────────────────┐
# │ Bloco 3: PESQUISADOR CRUD │
# └───────────────────────────┘

print("\n\n--- INICIANDO TESTES DE CRUD PARA PESQUISADORES ---")

# Criar um pesquisador associado à instituição que já criamos
create_pesq_res = PesquisadorAPITests.create_pesquisador(auth_header, created_instituicao_id)
assert create_pesq_res.status_code == 201, "Falha ao criar pesquisador!"



# Extrair o ID do pesquisador recém-criado
created_pesquisador_id = create_pesq_res.json()['id']
print(f"--> ID do Pesquisador criado para os testes: {created_pesquisador_id}")

# Listar todos os pesquisadores para confirmar que o nosso está lá
list_pesq_res = PesquisadorAPITests.list_pesquisadores(auth_header)
assert list_pesq_res.status_code == 200, "Falha ao listar pesquisadores!"


# Atualizar o pesquisador que criamos
update_pesq_res = PesquisadorAPITests.update_pesquisador(auth_header, created_pesquisador_id)
assert update_pesq_res.status_code == 200, "Falha ao atualizar pesquisador!"
assert update_pesq_res.json()['desligado'] is True, "O campo 'desligado' não foi atualizado."

# Deletar o pesquisador
delete_pesq_res = PesquisadorAPITests.delete_pesquisador(auth_header, created_pesquisador_id)
assert delete_pesq_res.status_code == 204, "Falha ao deletar pesquisador!"

# Verificar se o pesquisador foi realmente deletado
print("\n--- Verificando se a deleção do pesquisador foi efetiva ---")
retrieve_instituicao_after_delete = InciteAPITests.retrieve_instituicao(auth_header, created_instituicao_id)
pesquisadores_da_instituicao = retrieve_instituicao_after_delete.json()['pesquisadores']
assert len(pesquisadores_da_instituicao) == 0, "O pesquisador ainda está associado à instituição após ser deletado."
print("--> Verificação de Delete do pesquisador bem-sucedida!")

print("\n✅ Todos os testes de CRUD para Pesquisadores foram executados com sucesso!")












