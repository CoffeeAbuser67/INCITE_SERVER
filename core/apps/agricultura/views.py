
from apps.agricultura.models import AgricultureData  

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

import logging
logger = logging.getLogger(__name__)



# ★ FilterView
class FilterView(APIView):
    def get(self, request):
        # Get query parameters
    
        year = request.query_params.get('year')
        area = request.query_params.get('area')
        variable = request.query_params.get('variable')

        logger.info(f" year : {year}, area: {area}, variable: {variable}") # [LOG] 


        # Validate parameters
        if not year or not area or not variable:
            raise ValidationError("Missing required parameters: 'year', 'area', and 'variable'.")

        # Filters
        try:
            year = int(year)  # Ensure year is an integer
        except ValueError:
            raise ValidationError("'year' must be a valid integer.")


        INSUMOS = [field.name for field in AgricultureData._meta.fields]
        filters = ['area', 'year', 'total', 'variable', 'muni_id', 'cafe_em_grao_total']
        for word in filters:
            INSUMOS.remove(word)


        queryset = AgricultureData.objects.filter(
            muni_id=area,
            year=year,
            variable=variable
        ).values(*INSUMOS)  # Fetch only the required fields (INSUMOS)


        if not queryset.exists():
            return Response({"message": "No matching data found."}, status=404)

        entry = queryset.first()  
    
        # Drop nan values and convert to numeric
        filtered_data = {k: float(v) for k, v in entry.items() if v is not None}

        # Get the top 9 largest values
        largest_values = sorted(filtered_data.items(), key=lambda item: item[1], reverse=True)[:9]

        response_data = dict(largest_values)
        return Response(response_data, status=200)
    
# ── ⋙── ── ── ── ── ── ── ──➤ 
