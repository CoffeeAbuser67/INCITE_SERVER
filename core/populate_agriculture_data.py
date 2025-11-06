# -*- coding: utf-8 -*-
import os
import django
import sys
import pandas as pd
import time

print(">>> Iniciando configuração do ambiente Django...")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

try:
    django.setup()
except ImportError as exc:
    raise ImportError(
        "Não foi possível importar o Django. Você tem certeza que ele está instalado e "
        "disponível na sua PYTHONPATH? Você esqueceu de ativar o ambiente virtual?"
    ) from exc

NOME_DO_ARQUIVO_XLSX = 'lavouras_temp&perm_OUTPUT_FINAL.xlsx'

from apps.agricultura.models import AgricultureData
from django.db import transaction

def run():
    """Função principal para executar a carga de dados."""
    
    # 1. Validação e Leitura do Arquivo
    if not os.path.exists(NOME_DO_ARQUIVO_XLSX):
        print(f"\nERRO: Arquivo '{NOME_DO_ARQUIVO_XLSX}' não encontrado na pasta raiz do projeto.")
        return

    print(f"\n>>> Lendo o arquivo '{NOME_DO_ARQUIVO_XLSX}'. Isso pode demorar...")
    start_time = time.time()
    df = pd.read_excel(NOME_DO_ARQUIVO_XLSX)
    end_time = time.time()
    print(f">>> Arquivo lido em {end_time - start_time:.2f} segundos. {len(df)} linhas encontradas.")

    # 2. Validação estrita das colunas
    print(">>> Validando colunas do arquivo...")
    model_fields = {f.name for f in AgricultureData._meta.concrete_fields if not f.primary_key}
    excel_columns = set(df.columns)

    if model_fields != excel_columns:
        missing = sorted(list(model_fields - excel_columns))
        extra = sorted(list(excel_columns - excel_columns))
        print("\nERRO: As colunas do Excel não batem com o modelo do Django.")
        if missing:
            print(f"  - Colunas FALTANDO no Excel: {missing}")
        if extra:
            print(f"  - Colunas EXTRAS no Excel: {extra}")
        return
    
    print(">>> Validação de colunas concluída com sucesso.")

    # 3. Limpeza e Preparação dos Dados
    df = df.astype(object).where(pd.notnull(df), None)
    objects_to_create = [AgricultureData(**row) for row in df.to_dict('records')]

    # 4. Inserção em Massa com Feedback de Progresso
    print(">>> Iniciando inserção dos dados no banco. Por favor, aguarde.")
    
    batch_size = 2000
    total_rows = len(objects_to_create)
    
    with transaction.atomic():
        created_count = 0
        for i in range(0, total_rows, batch_size):
            batch = objects_to_create[i:i + batch_size]
            AgricultureData.objects.bulk_create(batch)
            created_count += len(batch)
            
            # Lógica para imprimir o progresso na mesma linha
            progress = (created_count / total_rows) * 100
            # A string '\r' move o cursor para o início da linha
            # 'end=""' evita que o print pule para a próxima linha
            sys.stdout.write(f"\rProgresso: {created_count}/{total_rows} registros inseridos ({progress:.2f}%)")
            sys.stdout.flush() # Força a atualização do que é exibido no terminal

    print("\n\n>>> Carga de dados finalizada com SUCESSO!")
    print(f">>> Total de {total_rows} registros inseridos.")


# entrada do script
if __name__ == '__main__':
    run()