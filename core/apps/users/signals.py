# your_app/signals.py

import logging

from django.apps import apps

from django.db.models.signals import post_migrate
from django.dispatch import receiver

from django.contrib.auth.models import Group


logger = logging.getLogger(__name__)

@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    Group = apps.get_model('auth', 'Group')
    roles = ['super', 'admin', 'staff', 'user']
    logger.info("post_migrate signal received.") # [LOG] signal 
    for role in roles:
        Group.objects.get_or_create(name=role)
    

    
# NOTE
#   Alternative code to create custom ids to the groups, more secure id roles
#   Not tested yet
#   maybe use a standalone script instead signals will be a safe approach 
#   

# import logging

# from django.apps import apps
# from django.db.models.signals import post_migrate
# from django.dispatch import receiver
# from django.contrib.auth.models import Group

# logger = logging.getLogger(__name__)

# @receiver(post_migrate)
# def create_default_groups(sender, **kwargs):
#     Group = apps.get_model('auth', 'Group')
#     roles_with_ids = [
#         {'name': 'super', 'id': 1},
#         {'name': 'admin', 'id': 2},
#         {'name': 'staff', 'id': 3},
#         {'name': 'user', 'id': 4},
#     ]
    
#     logger.info("post_migrate signal received.")  # [LOG] signal

#     for role in roles_with_ids:
#         group, created = Group.objects.get_or_create(name=role['name'])
#         if created:
#             # Assign the ID if the group was just created
#             group.id = role['id']
#             group.save()
#             logger.info(f"Created group '{role['name']}' with ID {role['id']}.")
#         else:
#             logger.info(f"Group '{role['name']}' already exists.")