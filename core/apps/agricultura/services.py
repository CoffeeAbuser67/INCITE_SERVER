from apps.agricultura.models import AgricultureData
from django.db.models import Avg, Q
from typing import List, Dict
from rest_framework.exceptions import ValidationError

# HERE Services
# ── ⋙── ── ── ── ── ── ── ──➤


#  <✪> getTopValues
def getTopValues(year: int, area: str, variable: str, type:str, INSUMOS: List[str]) -> Dict[str, Dict[str, float]]:
    
    VARIABLES = [variable, f"{variable}_percentual"]

    D = {}
    
    for var in VARIABLES:   
        queryset = AgricultureData.objects.filter(
            name_id=area,
            year=year,
            variable=var,
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
        
        D[var] = filtered_data

    # Get the percent of other elements that doesn't appear in the top values
    target = VARIABLES[1]
    total  = sum(D[target].values())
    
    # Only get others if it is greather than at leas 0.01%
    if total < 99.9 :
        outros = 100 - total
        D[target]['outros'] = outros
        
    return D
# ── ⋙── ── ── ── ── ── ── ──➤


#  <✪> getTop10TimeSeries
def getTop10TimeSeries (area: str, variable: str, INSUMOS: List[str]) -> List[Dict[str, float]]:

    
    queryset = AgricultureData.objects.filter(
        muni_id='ilheus', variable='valor da producao'
    )
    
    
    INSUMOS = [field.name for field in AgricultureData._meta.fields]
    filters = ['pkid','area', 'year', 'variable', 'muni_id', 'total', 'cafe_em_grao_total']
    for word in filters:
        INSUMOS.remove(word)
        
    
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
