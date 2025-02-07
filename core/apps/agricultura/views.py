
from apps.agricultura.models import AgricultureData  
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .services import getTopValues, getTopTimeSeries
import logging
logger = logging.getLogger(__name__)



# ★ TOPValuesView
class TOPValuesView(APIView):
    def get(self, request):
        # Get query parameters
    
        year = request.query_params.get('year')
        area = request.query_params.get('area')
        variable = request.query_params.get('variable')
        type = request.query_params.get('type')


        # Validate parameters
        if not year or not area or not variable or not type:
            raise ValidationError("Missing required parameters: 'year' or 'area' or  type' or  'variable'.")

        # Filters
        try:
            year = int(year)  # Ensure year is an integer
        except ValueError:
            raise ValidationError("'year' must be a valid integer.")


        INSUMOS = [field.name for field in AgricultureData._meta.fields]
        naoEInsumo = ['pkid','area','year', 'total','variable', 'cafe_em_grao_arabica', 'cafe_em_grao_canephora', 'name_id', 'type']
        for word in naoEInsumo:
            INSUMOS.remove(word)

        # (○) getTopValues
        R = getTopValues(year, area, variable, type,  INSUMOS)

        return Response(R, status=200)
# ── ⋙── ── ── ── ── ── ── ──➤ 


# ★ TopTimeSeriesView
class TopTimeSeriesView(APIView):
    def get(self, request):
        # Get query parameters

        area = request.query_params.get('area')
        variable = request.query_params.get('variable')
        type = request.query_params.get('type')

                # Validate parameters
        if not area or not variable or not type:
            raise ValidationError("Missing required parameters: 'area' or  type' or 'variable'.")

        INSUMOS = [field.name for field in AgricultureData._meta.fields]
        naoEInsumo = ['pkid','area','year', 'total','variable', 'cafe_em_grao_arabica', 'cafe_em_grao_canephora', 'name_id', 'type']
        for word in naoEInsumo:
            INSUMOS.remove(word)

        # (○) getTopTimeSeries
        R = getTopTimeSeries(area, variable, type,  INSUMOS)
        return Response(R, status=200)
# ── ⋙── ── ── ── ── ── ── ──➤ 



