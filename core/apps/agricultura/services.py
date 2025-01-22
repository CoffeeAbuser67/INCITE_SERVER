from apps.agricultura.models import AgricultureData
from django.db.models import Avg, Q
from typing import List, Dict
from rest_framework.exceptions import ValidationError

# HERE Services
# ── ⋙── ── ── ── ── ── ── ──➤


#  <✪> getTop10
def getTop10(year: int, area: str, variable: str, INSUMOS: List[str]) -> Dict[str, Dict[str, float]]:
    
    queryset = AgricultureData.objects.filter(
        muni_id=area,
        year=year,
        variable=variable
    ).values(*INSUMOS)  
    

    if not queryset.exists():
        raise ValidationError("No matching data found.")
        
    entry = queryset.first()  
    # Drop nan values and convert to numeric
    filtered_data = {k: float(v) for k, v in entry.items() if v is not None}
    # Get the top 9 largest values
    filtered_data = sorted(filtered_data.items(), key=lambda item: item[1], reverse=True)[:10]
    filtered_data = dict(filtered_data)

    
    variable_percent = f"{variable} percentual total"
        
    
    queryset = AgricultureData.objects.filter(
        muni_id=area,
        year=year,
        variable=variable_percent
    ).values(*INSUMOS)  


    if not queryset.exists():
        raise ValidationError("No matching data found.")
            
    
    entry = queryset.first()  
    # Drop nan values and convert to numeric
    percent_data = {k: float(v) for k, v in entry.items() if v is not None}
    # Get the top 9 largest values
    percent_data = sorted(percent_data.items(), key=lambda item: item[1], reverse=True)[:10]
    percent_data = dict(percent_data)
    
    
    D = {
        "values" : filtered_data,
        "percent_values" : percent_data
    }


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
