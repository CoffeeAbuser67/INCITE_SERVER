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
# ┌────────────┐
# │DECLARATIONS│
# └────────────┘

import time
from unidecode import unidecode

# ⋙───timer ⏰──➤
def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        print(f"Function {func.__name__} start execution.")
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function {func.__name__} took {end_time - start_time:.6f} seconds to execute.")
        print("⋙── ── ── ── ── ── ── ── ── ── ── ── ──➤ 🦀")
        return result
    return wrapper


# {✪} OfficialNames
class OfficialNames:
    def __init__(self):
        self.territories_dict = {
            "Irecê" : ["América Dourada", "Barra do Mendes", "Barro Alto", "Cafarnaum", "Canarana", "Central", "Gentio do Ouro", "Ibipeba", "Ibititá", "Ipupiara", "Irecê", "Itaguaçu da Bahia", "João Dourado", "Jussara", "Lapão", "Mulungu do Morro", "Presidente Dutra", "Uibaí", "São Gabriel", "Xique-Xique"],
            "Velho Chico" : ["Barra", "Bom Jesus da Lapa", "Brotas de Macaúbas", "Carinhanha", "Feira da Mata", "Ibotirama", "Igaporã", "Malhada", "Matina", "Morpará", "Muquém do São Francisco", "Oliveira dos Brejinhos", "Paratinga", "Riacho de Santana", "Serra do Ramalho", "Sítio do Mato"],
            "Chapada Diamantina" : ["Abaíra", "Andaraí", "Barra da Estiva", "Boninal", "Bonito", "Ibicoara", "Ibitiara", "Iramaia", "Iraquara", "Itaeté", "Jussiape", "Lençóis", "Marcionílio Souza", "Morro do Chapéu", "Mucugê", "Nova Redenção", "Novo Horizonte", "Palmeiras", "Piatã", "Rio de Contas", "Seabra", "Souto Soares", "Utinga", "Wagner"],
            "Sisal" : ["Araci", "Barrocas", "Biritinga", "Candeal", "Cansanção", "Conceição do Coité", "Ichu", "Itiúba", "Lamarão", "Monte Santo", "Nordestina", "Queimadas", "Quijingue", "Retirolândia", "Santaluz", "São Domingos", "Serrinha", "Teofilândia", "Tucano", "Valente"],
            "Litoral Sul":  ["Almadina", "Arataca", "Aurelino Leal", "Barro Preto", "Buerarema", "Camacan", "Canavieiras", "Coaraci", "Floresta Azul", "Ibicaraí", "Ilhéus", "Itabuna", "Itacaré", "Itaju do Colônia", "Itajuípe", "Itapé", "Itapitanga", "Jussari", "Maraú", "Mascote", "Pau Brasil", "Santa Luzia", "São José da Vitória", "Ubaitaba", "Una", "Uruçuca"],
            "Baixo Sul" : ["Aratuípe", "Cairu", "Camamu", "Gandu", "Ibirapitanga", "Igrapiúna", "Ituberá", "Jaguaripe", "Nilo Peçanha", "Piraí do Norte", "Presidente Tancredo Neves", "Taperoá", "Teolândia", "Valença", "Wenceslau Guimarães"],
            "Extremo Sul" :["Alcobaça", "Caravelas", "Ibirapuã", "Itamaraju", "Itanhém", "Jucuruçu", "Lajedão", "Medeiros Neto", "Mucuri", "Nova Viçosa", "Prado", "Teixeira de Freitas", "Vereda"],
            "Médio Sudoeste da Bahia" : ["Caatiba", "Firmino Alves", "Ibicuí", "Iguaí", "Itambé", "Itapetinga", "Itarantim", "Itororó", "Macarani", "Maiquinique", "Nova Canaã", "Potiraguá", "Santa Cruz da Vitória"],
            "Vale do Jiquiriçá" :["Amargosa", "Brejões", "Cravolândia", "Elísio Medrado", "Irajuba", "Itaquara", "Itiruçu", "Jaguaquara", "Jiquiriçá", "Lafaiete Coutinho", "Laje", "Lajedo do Tabocal", "Maracás", "Milagres", "Mutuípe", "Nova Itarana", "Planaltino", "Santa Inês", "São Miguel das Matas", "Ubaíra"] ,
            "Sertão do São Francisco" :["Campo Alegre de Lourdes", "Canudos", "Casa Nova", "Curaçá", "Juazeiro", "Pilão Arcado", "Remanso", "Sento Sé", "Sobradinho", "Uauá"] ,
            "Bacia do Rio Grande" : ["Angical", "Baianópolis", "Barreiras", "Buritirama", "Catolândia", "Cotegipe", "Cristópolis", "Formosa do Rio Preto", "Luís Eduardo Magalhães", "Mansidão", "Riachão das Neves", "Santa Rita de Cássia", "São Desidério", "Wanderley"],
            "Bacia do Paramirim" :["Boquira", "Botuporã", "Caturama", "Érico Cardoso", "Ibipitanga", "Macaúbas", "Paramirim", "Rio do Pires"],
            "Sertão Produtivo" :["Brumado", "Caculé", "Caetité", "Candiba", "Contendas do Sincorá", "Dom Basílio", "Guanambi", "Ibiassucê", "Ituaçu", "Iuiú", "Lagoa Real", "Livramento de Nossa Senhora", "Malhada de Pedras", "Palmas de Monte Alto", "Pindaí", "Rio do Antônio", "Sebastião Laranjeiras", "Tanhaçu", "Tanque Novo", "Urandi"] ,
            "Piemonte do Paraguaçu" : ["Boa Vista do Tupim", "Iaçu", "Ibiquera", "Itaberaba", "Itatim", "Lajedinho", "Macajuba", "Mundo Novo", "Piritiba", "Rafael Jambeiro", "Ruy Barbosa", "Santa Terezinha", "Tapiramutá"],
            "Bacia do Jacuípe" :["Baixa Grande", "Capela do Alto Alegre", "Capim Grosso", "Gavião", "Ipirá", "Mairi", "Nova Fátima", "Pé de Serra", "Pintadas", "Quixabeira", "Riachão do Jacuípe", "São José do Jacuípe", "Serra Preta", "Várzea da Roça", "Várzea do Poço"] ,
            "Piemonte da Diamantina" :["Caém", "Jacobina", "Miguel Calmon", "Mirangaba", "Ourolândia", "Saúde", "Serrolândia", "Umburanas", "Várzea Nova"],
            "Semiárido Nordeste II" : ["Adustina", "Antas", "Banzaê", "Cícero Dantas", "Cipó", "Coronel João Sá", "Euclides da Cunha", "Fátima", "Heliópolis", "Jeremoabo", "Nova Soure", "Novo Triunfo", "Paripiranga", "Pedro Alexandre", "Ribeira do Amparo", "Ribeira do Pombal", "Santa Brígida", "Sítio do Quinto"],
            "Litoral Norte e Agreste Baiano": ["Acajutiba", "Alagoinhas", "Aporá", "Araças", "Aramari", "Cardeal da Silva", "Catu", "Conde", "Crisópolis", "Entre Rios", "Esplanada", "Inhambupe", "Itanagra", "Itapicuru", "Jandaíra", "Olindina", "Ouriçangas", "Pedrão", "Rio Real", "Sátiro Dias"],
            "Portal do Sertão": ["Água Fria", "Amélia Rodrigues", "Anguera", "Antônio Cardoso", "Conceição da Feira", "Conceição do Jacuípe", "Coração de Maria", "Feira de Santana", "Ipecaetá", "Irará", "Santa Bárbara", "Santanópolis", "Santo Estêvão", "São Gonçalo dos Campos", "Tanquinho", "Teodoro Sampaio", "Terra Nova"],
            "Sudoeste Baiano" : ["Anagé", "Aracatu", "Barra do Choça", "Belo Campo", "Bom Jesus da Serra", "Caetanos", "Cândido Sales", "Caraíbas", "Condeúba", "Cordeiros", "Encruzilhada", "Guajeru", "Jacaraci", "Licínio de Almeida", "Maetinga", "Mirante", "Mortugaba", "Piripá", "Planalto", "Poções", "Presidente Jânio Quadros", "Ribeirão do Largo", "Tremedal", "Vitória da Conquista"],
            "Recôncavo" : ["Cabaceiras do Paraguaçu", "Cachoeira", "Castro Alves", "Conceição do Almeida", "Cruz das Almas", "Dom Macedo Costa", "Governador Mangabeira", "Maragogipe", "Muniz Ferreira", "Muritiba", "Nazaré", "Salinas da Margarida", "Santo Amaro", "Santo Antônio de Jesus", "São Felipe", "São Félix", "Sapeaçu", "Saubara", "Varzedo"],
            "Médio Rio de Contas" :["Aiquara", "Apuarema", "Barra do Rocha", "Boa Nova", "Dário Meira", "Gongogi", "Ibirataia", "Ipiaú", "Itagi", "Itagibá", "Itamari", "Jequié", "Jitaúna", "Manoel Vitorino", "Nova Ibiá", "Ubatã"] ,
            "Bacia do Rio Corrente" :  ["Brejolândia", "Canápolis", "Cocos", "Coribe", "Correntina", "Jaborandi", "Santa Maria da Vitória", "Santana", "São Félix do Coribe", "Serra Dourada", "Tabocas do Brejo Velho"],
            "Itaparica" :["Abaré", "Chorrochó", "Glória", "Macururé", "Paulo Afonso", "Rodelas"],
            "Piemonte Norte do Itapicuru": ["Andorinha", "Antônio Gonçalves", "Caldeirão Grande", "Campo Formoso", "Filadélfia", "Jaguarari", "Pindobaçu", "Ponto Novo", "Senhor do Bonfim"],
            "Metropolitano de Salvador" : ["Camaçari", "Candeias", "Dias d'Ávila", "Itaparica", "Lauro de Freitas", "Madre de Deus", "Mata de São João", "Pojuca", "Salvador", "São Francisco do Conde", "São Sebastião do Passé", "Simões Filho", "Vera Cruz"],
            "Costa do Descobrimento": ["Belmonte", "Eunápolis", "Guaratinga", "Itabela", "Itagimirim", "Itapebi", "Porto Seguro", "Santa Cruz Cabrália"]
        }
    
        
    def clean_str(self, word : str) -> str :
        word = word.strip()
        word = word.lower()
        word = word.replace(' ', '_')
        word = word.replace('-', '_')
        word = word.replace("'", "_")
        word = unidecode(word)
        return(word)
    

    
    def get_regionList(self):
        return list(self.territories_dict.keys())
    
    
    
    def get_cleanMuniList(self):
        muni_list = []
        
        for _list in list(self.territories_dict.values()):
            muni_list =  muni_list + _list
        
        muni_list = [self.clean_str(el) for el in muni_list]
        return muni_list
    
    
    
    
    
    
    
    
    def get_cleanRegionList(self):
        region_list = list(self.territories_dict.keys())
        return [self.clean_str(el) for el in region_list]
        


    def get_clean_territories(self):
        clean_territories= {   
             self.clean_str(k) : [self.clean_str(el) for el in v] 
             for  k, v in self.territories_dict.items()
             }
        return clean_territories


# {●} INSUMOS_dict
INSUMOS_dict = {
    "abacate": "Abacate",
    "abacaxi": "Abacaxi",
    "acai": "Açaí",
    "alfafa_fenada": "Alfafa Fenada",
    "algodao_arboreo_em_caroco": "Algodão Arbóreo em Caroço",
    "algodao_herbaceo_em_caroco": "Algodão Herbáceo em Caroço",
    "alho": "Alho",
    "amendoim_em_casca": "Amendoim em Casca",
    "arroz_em_casca": "Arroz em Casca",
    "aveia_em_grao": "Aveia em Grão",
    "azeitona": "Azeitona",
    "banana_cacho": "Banana (Cacho)",
    "batata_doce": "Batata Doce",
    "batata_inglesa": "Batata Inglesa",
    "borracha_latex_coagulado": "Borracha (Látex Coagulado)",
    "borracha_latex_liquido": "Borracha (Látex Líquido)",
    "cacau_em_amendoa": "Cacau em Amêndoa",
    "cafe_em_grao_total": "Café em Grão (Total)",
    "caju": "Caju",
    "cana_de_acucar": "Cana-de-Açúcar",
    "cana_para_forragem": "Cana para Forragem",
    "caqui": "Caqui",
    "castanha_de_caju": "Castanha de Caju",
    "cebola": "Cebola",
    "centeio_em_grao": "Centeio em Grão",
    "cevada_em_grao": "Cevada em Grão",
    "cha_da_india_folha_verde": "Chá-da-Índia (Folha Verde)",
    "coco_da_baia": "Coco-da-Baía",
    "dende_cacho_de_coco": "Dendê (Cacho de Coco)",
    "erva_mate_folha_verde": "Erva-Mate (Folha Verde)",
    "ervilha_em_grao": "Ervilha em Grão",
    "fava_em_grao": "Fava em Grão",
    "feijao_em_grao": "Feijão em Grão",
    "figo": "Figo",
    "fumo_em_folha": "Fumo em Folha",
    "girassol_em_grao": "Girassol em Grão",
    "goiaba": "Goiaba",
    "guarana_semente": "Guaraná (Semente)",
    "juta_fibra": "Juta (Fibra)",
    "laranja": "Laranja",
    "limao": "Limão",
    "linho_semente": "Linhaça (Semente de Linho)",
    "maca": "Maçã",
    "malva_fibra": "Malva (Fibra)",
    "mamao": "Mamão",
    "mamona_baga": "Mamona (Baga)",
    "mandioca": "Mandioca",
    "manga": "Manga",
    "maracuja": "Maracujá",
    "marmelo": "Marmelo",
    "melancia": "Melancia",
    "melao": "Melão",
    "milho_em_grao": "Milho em Grão",
    "noz_fruto_seco": "Noz (Fruto Seco)",
    "palmito": "Palmito",
    "pera": "Pera",
    "pessego": "Pêssego",
    "pimenta_do_reino": "Pimenta-do-Reino",
    "rami_fibra": "Rami (Fibra)",
    "sisal_ou_agave_fibra": "Sisal ou Agave (Fibra)",
    "soja_em_grao": "Soja em Grão",
    "sorgo_em_grao": "Sorgo em Grão",
    "tangerina": "Tangerina",
    "tomate": "Tomate",
    "trigo_em_grao": "Trigo em Grão",
    "triticale_em_grao": "Triticale em Grão",
    "tungue_fruto_seco": "Tungue (Fruto Seco)",
    "urucum_semente": "Urucum (Semente)",
    "uva": "Uva",
    "outros": "Outros",
}



# ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
# ×●●●× ○○○○ ●●●● ○○○○ ●●●● ○○○○ ●●●● ○○○○ ●●●● ○○○○ ●●●● ○○○○ ●●●● ○○○○ ●●●● ○○○○ ●●●● ○○○○ ●●●● ○○○○ ●●●● ○○○○ ║                                                                                                  ║
# ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╝
# ── ⋙── ── ── ── ── ── ── ── ── ── ── ──➤
#       ┌──────┐┌────────┐
#       │DJANGO││SERVICES│
#       └──────┘└────────┘

from apps.agricultura.models import AgricultureData
from django.db.models import Avg

#  <✪> getTop10
def getTop10(year, area, variable, type, INSUMOS):

    VARIABLES = {'data' : variable,  'percent_data':  f"{variable}_percentual"}

    D = {}
    
    for key in VARIABLES.keys():   
        queryset = AgricultureData.objects.filter(
            name_id=area,
            year=year,
            variable=VARIABLES[key],
            type = type
        ).values(*INSUMOS)  
        
        if not queryset.exists():
            print("No matching data found.")
            
        entry = queryset.first()  
        # Drop nan values and convert to numeric
        filtered_data = {k: float(v) for k, v in entry.items() if v is not None}
        # Get the top 9 largest values
        filtered_data = sorted(filtered_data.items(), key=lambda item: item[1], reverse=True)[:10]
        filtered_data = dict(filtered_data)

        filtered_data = {k: v for k, v in filtered_data.items() if v != 0} #Remove 0's
        
        D[key] = filtered_data

    # Get the percent of other elements that doesn't appear in the top values

    total  = sum(D['percent_data'].values())
    
    # Only get others if it is greather than at leas 0.01%
    if total < 99.9 :
        outros = 100 - total
        D['percent_data']['outros'] = outros
        

    VARIABLES2 = ['quantidade_produzida','rendimento_medio_da_producao'] # <●> VARIABLES2
    D2 = {}
    cols_to_fetch = list(D['data'].keys())

    for var in VARIABLES2:

        queryset = AgricultureData.objects.filter(
            name_id=area,
            year=year,
            variable=var,
            type = type
        ).values(*INSUMOS)  
    
        if not queryset.exists():
            print("No matching data found.")
            
        entry = queryset.first()  
            
        target = {col: entry[col] for col in cols_to_fetch }
        D2[var] = target


    FD2 =  [ 
        {
            'id' : col,
            'name' : INSUMOS_dict[col],
            'qp' : D2[VARIABLES2[0]][col],
            'rm' : D2[VARIABLES2[1]][col],
        }
        for col in cols_to_fetch
    ]

    #format Data 
    FD = {}
    for key in D.keys():
        target = [
            {"id" : k, "name" : INSUMOS_dict[k], 'v' : v }
            for k, v in D[key].items()
        ]
        FD[key] = target
    FD['var'] = VARIABLES['data']
    FD['QP_RM'] = FD2
    
    return FD
# ── ⋙── ── ── ── ── ── ── ──➤


#  <✪> getTopTimeSeries
def getTopTimeSeries (area, variable, type, INSUMOS):

    FD = {}
    
    queryset = AgricultureData.objects.filter(
        name_id=area,
        variable=variable,
        type = type
    ).values(*INSUMOS)  


    # Calculate average for each column in INSUMOS
    averages = (
        queryset.aggregate(
            **{field: Avg(field) for field in INSUMOS}
        )
    )
    
    
    # Drop null averages
    filtered_averages = {k: v for k, v in averages.items() if v is not None}
    
    # Get top 10 columns by average value
    top10_fields = sorted(filtered_averages.items(), key=lambda x: x[1], reverse=True)[:10]
    top10_field_keys = [field for field, _ in top10_fields]
    
    FD['keys'] = top10_field_keys
    
    top10_field_keys.append('year')  # Include 'year' in the final result
    
    # Query the data for the top 10 fields
    F = queryset.values(*top10_field_keys)
    
    if not F.exists():
        print("No matching data found.")
    
    FD['data'] = sorted(F, key=lambda x: x['year'])
    
    

    # NECESSARIO PQ O RECHART QUEBRA COM VALORES ONDE Y = 0 
    # TO CONVERTENDO VALORES DE 0 PARA 0.0001 
    # QUE MERDA VUH! BIBLIOTECA PODRE
    for item in FD['data'] :
        for key, value in item.items():
            if value == 0.0:
                item[key] = 0.0001


    return FD
# ── ⋙── ── ── ── ── ── ── ──➤


# ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
#  TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST ║                                                                                                  ║
# ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╝

if '🦀' == '🦀':

    INSUMOS = [field.name for field in AgricultureData._meta.fields]
    _filters = ['pkid','area','year', 'region', 'total','variable', 'cafe_em_grao_arabica', 'cafe_em_grao_canephora', 'name_id', 'type']
    for word in _filters:
        INSUMOS.remove(word)
    year = 2023
    area = 'bahia'
    variable = "valor_da_producao"
    type = 'regiao'
    
    X = getTop10(year, area, variable, type, INSUMOS)
#  ── ⋙── ── ── ── ── ── ── ──➤

# ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
#  TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST ║                                                                                                  ║
# ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╝

if '🦀' == '🦀':
    INSUMOS = [field.name for field in AgricultureData._meta.fields]
    _filters = ['pkid','area','year', 'region', 'total','variable', 'cafe_em_grao_arabica', 'cafe_em_grao_canephora', 'name_id', 'type']
    for word in _filters:
        INSUMOS.remove(word)
    
    _area = 'irece'
    _variable = "valor_da_producao"
    _type = 'municipio'

    X = getTopTimeSeries (_area, _variable, _type, INSUMOS)
#  ── ⋙── ── ── ── ── ── ── ──➤

# ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
#  TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST ║                                                                                                  ║
# ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╝

# ⋙════#════#═════════════════════════════════════➤
#   ╔══#════#══╗
#   ║ ANALYSIS ║
#   ╚══════════╝

#     ┌─────┐
#     │TOP10│
#     └─────┘

if '🦀' == '🦀':
    M = OfficialNames()
    Munis = M.get_cleanMuniList()
    
    Regions = M.get_cleanRegionList()
    Regions = Regions + ['brasil', 'bahia']
    
    INSUMOS = [field.name for field in AgricultureData._meta.fields]
    _filters = ['pkid','area','year', 'region', 'total','variable', 'cafe_em_grao_arabica', 'cafe_em_grao_canephora', 'name_id', 'type']
    for word in _filters:
        INSUMOS.remove(word)
    
    
    resultsR = []
    for region in Regions:
        area = region
        year = 2000
        variable = 'area_colhida'
        _type = "regiao"
        X = getTop10(year, area, variable, _type, INSUMOS)
        resultsR.append(X)
    
    
    resultsM = []
    for muni in Munis:
        area = muni
        year = 2000
        variable = 'area_colhida'
        _type = "municipio"
        X = getTop10(year, area, variable, _type, INSUMOS)
        resultsM.append(X)
#  ── ⋙── ── ── ── ── ── ── ──➤



# ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
#  TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST ║                                                                                                  ║
# ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╝


# def get_total_values(area, year, variable):

region = 'bahia'
year = 2023
variable = 'valor_da_producao'

queryset = AgricultureData.objects.filter(
    region = region,
    year = year,
    variable= variable,
).values('total', 'name_id')  


X = list(queryset)



# def get_thermometer_color(value: float, start: float, end: float, colors: list[str]) -> str:
#     step_size = (end - start) / len(colors)
#     index = min(max(int((value - start) / step_size), 0), len(colors) - 1)
#     return colors[index]



# ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
#  TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST ║                                                                                                  ║
# ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╝


