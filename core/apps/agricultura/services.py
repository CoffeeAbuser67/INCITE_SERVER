from apps.agricultura.models import AgricultureData
from django.db.models import Avg, Q
from typing import List, Dict

from .helpers import INSUMOS_dict  



#  <✪> getTopValues
def getTopValues(year: int, area: str, variable: str, type:str, INSUMOS: List[str]) -> Dict[str, Dict[str, float]]:
    
    # VARIABLES = [variable, f"{variable}_percentual"] # <●> VARIABLES

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
    top10_fields = sorted(filtered_averages.items(), key=lambda x: x[1], reverse=True)[:6]
    top10_field_keys = sorted([key for key, _ in top10_fields])  

    FD['keys'] = {key : INSUMOS_dict[key]  for key in top10_field_keys}

    # FD['keys'] = top10_field_keys.copy()
    # FD['names'] = [INSUMOS_dict[key] for key in top10_field_keys]

    top10_field_keys.append('year')  # Include 'year' in the final result
    F = queryset.values(*top10_field_keys) 
    
    if not F.exists():
        print("No matching data found.")

    FD['data'] = sorted(F, key=lambda x: x['year'])

    # NECESSARIO PQ O RECHART QUEBRA COM VALORES ONDE Y = 0 
    # TO CONVERTENDO VALORES DE 0 PARA None
    # AFF! BIBLIOTECA PODRE!
    for item in FD['data'] :
        for key, value in item.items():
            if value == 0.0:
                item[key] = None

    return FD
# ── ⋙── ── ── ── ── ── ── ──➤


#  <✪> getTotalValues
def getTotalValues (region, year, variable):

    queryset = AgricultureData.objects.filter(
        region = region,
        year = year,
        variable= variable,
    ).values('total', 'name_id')  

    R = {el['name_id']: el['total'] for el in queryset}

    return R
# ── ⋙── ── ── ── ── ── ── ──➤