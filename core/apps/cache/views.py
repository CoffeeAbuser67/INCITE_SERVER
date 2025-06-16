from django.shortcuts import render
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


# ★ Temp_cache_view 
class Temp_cache_view(APIView):

    def post(self, request, format=None):
        data = request.data
        # Save data to cache with a unique key
        cache.set('cached_data', data, timeout=600)  # timeout in seconds # 10 min
        print(data)
        return Response("Data saved in cache", status=status.HTTP_201_CREATED)


    def get(self, request, format=None):
        # Retrieve data from cache
        data = cache.get('cached_data')
        if data is not None:
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response("No data found", status=status.HTTP_404_NOT_FOUND)

# ── ⋙ ── ── ── ── ── ── ── ──➤