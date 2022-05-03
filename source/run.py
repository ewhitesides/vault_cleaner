"""
high level script to call functions from init
"""

import os
from dotenv import load_dotenv
import vault_cleaner

#load in environment data
load_dotenv()

vault_cleaner.copy_kv2_secrets(
    source_mount = os.getenv('VAULT_SOURCE_MOUNT'),
    destination_mount = os.getenv('VAULT_DESTINATION_MOUNT'),
    age = os.getenv('VAULT_SOURCE_AGE')
)

vault_cleaner.clean_kv2_paths(
    mount = os.getenv('VAULT_SOURCE_MOUNT'),
    age = os.getenv('VAULT_SOURCE_AGE')
)

vault_cleaner.clean_kv2_paths(
    mount = os.getenv('VAULT_DESTINATION_MOUNT'),
    age = os.getenv('VAULT_DESTINATION_AGE')
)
