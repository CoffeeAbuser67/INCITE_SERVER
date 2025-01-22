
from apps.agricultura.models import AgricultureData  

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from .services import getTop10, getTop10TimeSeries   

import logging
logger = logging.getLogger(__name__)


# ★ FilterView
class FilterView(APIView):
    def get(self, request):
        # Get query parameters
    
        year = request.query_params.get('year')
        area = request.query_params.get('area')
        variable = request.query_params.get('variable')
        fetchType = request.query_params.get('fetchType')

        # Validate parameters
        if not year or not area or not variable or not fetchType:
            raise ValidationError("Missing required parameters: 'year', 'area', fetchType' and  'variable'.")

        # Filters
        try:
            year = int(year)  # Ensure year is an integer
        except ValueError:
            raise ValidationError("'year' must be a valid integer.")


        INSUMOS = [field.name for field in AgricultureData._meta.fields]
        filters = ['area', 'year', 'total', 'variable', 'muni_id', 'cafe_em_grao_total']
        for word in filters:
            INSUMOS.remove(word)

        if fetchType == 'common':
            R = getTop10(year, area, variable, INSUMOS)
        
        elif fetchType == 'timeSeries':
            data1 = getTop10(year ,area, variable, INSUMOS)
            data2 = getTop10TimeSeries(area, variable, INSUMOS)

            R = {
                "top10": data1,
                "timeSeries": data2
            }


        return Response(R, status=200)
    
# ── ⋙── ── ── ── ── ── ── ──➤ 
