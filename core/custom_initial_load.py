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


import pandas as pd


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true" #WARN Disable when not working with spyder

# Now set up Django
django.setup()

print(django.get_version(), '↯')
# logger.info(django.get_version())

df = pd.read_excel('lavouras_temp&perm_output33.xlsx')

# Preencher valores NaN com None para evitar problemas ao inserir no banco
df = df.astype(object).where(pd.notnull(df), None)



from django.db import transaction
from apps.agricultura.models import AgricultureData  


# Criar lista de objetos do modelo
objects = [
    AgricultureData(
        muni_id=row['muni_id'],
        year=row['year'],
        area=row['area'],
        variable = row['variable'],
        total=row['total'],
        abacate=row['abacate'],
        abacaxi=row['abacaxi'],
        acai=row['acai'],
        alfafa_fenada=row['alfafa_fenada'],
        algodao_arboreo_em_caroco=row['algodao_arboreo_em_caroco'],
        algodao_herbaceo_em_caroco=row['algodao_herbaceo_em_caroco'],
        alho=row['alho'],
        amendoim_em_casca=row['amendoim_em_casca'],
        arroz_em_casca=row['arroz_em_casca'],
        aveia_em_grao=row['aveia_em_grao'],
        azeitona=row['azeitona'],
        banana_cacho=row['banana_cacho'],
        batata_doce=row['batata_doce'],
        batata_inglesa=row['batata_inglesa'],
        borracha_latex_coagulado=row['borracha_latex_coagulado'],
        borracha_latex_liquido=row['borracha_latex_liquido'],
        cacau_em_amendoa=row['cacau_em_amendoa'],
        cafe_em_grao_total=row['cafe_em_grao_total'],
        cafe_em_grao_arabica=row['cafe_em_grao_arabica'],
        cafe_em_grao_canephora=row['cafe_em_grao_canephora'],
        caju=row['caju'],
        cana_de_acucar=row['cana_de_acucar'],
        cana_para_forragem=row['cana_para_forragem'],
        caqui=row['caqui'],
        castanha_de_caju=row['castanha_de_caju'],
        cebola=row['cebola'],
        centeio_em_grao=row['centeio_em_grao'],
        cevada_em_grao=row['cevada_em_grao'],
        cha_da_india_folha_verde=row['cha_da_india_folha_verde'],
        coco_da_baia=row['coco_da_baia'],
        dende_cacho_de_coco=row['dende_cacho_de_coco'],
        erva_mate_folha_verde=row['erva_mate_folha_verde'],
        ervilha_em_grao=row['ervilha_em_grao'],
        fava_em_grao=row['fava_em_grao'],
        feijao_em_grao=row['feijao_em_grao'],
        figo=row['figo'],
        fumo_em_folha=row['fumo_em_folha'],
        girassol_em_grao=row['girassol_em_grao'],
        goiaba=row['goiaba'],
        guarana_semente=row['guarana_semente'],
        juta_fibra=row['juta_fibra'],
        laranja=row['laranja'],
        limao=row['limao'],
        linho_semente=row['linho_semente'],
        maca=row['maca'],
        malva_fibra=row['malva_fibra'],
        mamao=row['mamao'],
        mamona_baga=row['mamona_baga'],
        mandioca=row['mandioca'],
        manga=row['manga'],
        maracuja=row['maracuja'],
        marmelo=row['marmelo'],
        melancia=row['melancia'],
        melao=row['melao'],
        milho_em_grao=row['milho_em_grao'],
        noz_fruto_seco=row['noz_fruto_seco'],
        palmito=row['palmito'],
        pera=row['pera'],
        pessego=row['pessego'],
        pimenta_do_reino=row['pimenta_do_reino'],
        rami_fibra=row['rami_fibra'],
        sisal_ou_agave_fibra=row['sisal_ou_agave_fibra'],
        soja_em_grao=row['soja_em_grao'],
        sorgo_em_grao=row['sorgo_em_grao'],
        tangerina=row['tangerina'],
        tomate=row['tomate'],
        trigo_em_grao=row['trigo_em_grao'],
        triticale_em_grao=row['triticale_em_grao'],
        tungue_fruto_seco=row['tungue_fruto_seco'],
        urucum_semente=row['urucum_semente'],
        uva=row['uva']
    )
    for _, row in df.iterrows()
]


# Inserção em massa no banco de dados
with transaction.atomic():
    AgricultureData.objects.bulk_create(objects, batch_size=2000)  # Ajuste o batch_size conforme necessário











