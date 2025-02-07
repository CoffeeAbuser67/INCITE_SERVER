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
        D[var] = target

    #format Data 
    FD = {}
    for key in D.keys():
        target = [
            {"id" : k, "name" : INSUMOS_dict[k], 'v' : v }
            for k, v in D[key].items()
        ]
        FD[key] = target
        
    FD['var'] = VARIABLES['data']


    return FD
# ── ⋙── ── ── ── ── ── ── ──➤


#  <✪> getTopTimeSeries
def getTopTimeSeries (area, variable, type, INSUMOS):
    
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
    top10_field_names = [field for field, _ in top10_fields]
    top10_field_names.append('year')  # Include 'year' in the final result
    
    # Query the data for the top 10 fields
    F = queryset.values(*top10_field_names)
    
    return F
# ── ⋙── ── ── ── ── ── ── ──➤