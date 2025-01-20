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
#  TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST ║                                                                                                  ║
# ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╝


# from apps.agricultura.models import AgricultureData   # Replace 'your_app' with your actual app name
# ilheus = list(AgricultureData.objects.filter(muni_id = 'ilheus', year = 2023).values())
# bahia = list(AgricultureData.objects.filter(muni_id = 'bahia', year = 2023, variable = 'area plantada').values())


# ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
#  TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST TEST ║                                                                                                  ║
# ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════╝


# Filter and get the 9 largest values. (percentage)


from apps.agricultura.models import AgricultureData  
import math

INSUMOS = [field.name for field in AgricultureData._meta.fields]
filters = ['pkid','area', 'year', 'total', 'variable', 'muni_id', 'cafe_em_grao_total']
for word in filters:
    INSUMOS.remove(word)


# Filters
year = 2023
area = 'bahia'
variable = 'area colhida percentual total'




queryset = AgricultureData.objects.filter(
    muni_id=area,
    year=year,
    variable=variable
).values(*INSUMOS)  


if queryset.exists():
    entry = queryset.first()  

    # Drop nan values and convert to numeric
    filtered_data = {k: float(v) for k, v in entry.items() if v is not None}

    # Get the top 9 largest values
    filtered_data = sorted(filtered_data.items(), key=lambda item: item[1], reverse=True)[:9]
    

else:
    print("No matching data found.")
















