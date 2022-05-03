"""
init
"""

from vault_cleaner.kv2 import (
    get_age_filtered_paths,
    get_current_secret_data,
    write_secret_data,
    delete_path
)

def copy_kv2_secrets(source_mount: str, destination_mount: str, age: int):
    """
    Summary:
        get kv2 secrets older than $age days and copies them from source to destination

    Parameters:
        source_mount (str): the source kv2 engine
        destination_mount (str): the destination kv2 engine
        age (int): number of days to filter on

    Returns:
        none
    """

    #get paths to copy from source_mount
    int_age=int(age)
    paths = get_age_filtered_paths(source_mount, int_age)

    #get current version of secret, and copy to destination
    for path in paths:
        secret_data = get_current_secret_data(source_mount, path)
        write_secret_data(destination_mount, path, secret_data)


def clean_kv2_paths(mount: str, age: int):
    """
    Summary:
        get kv2 secrets older than $age days and deletes the path/subpath from mount

    Parameters:
        mount (str): the kv2 engine mount to check
        age (int): number of days to filter on

    Returns:
        none
    """

    #get old paths
    int_age=int(age)
    paths = get_age_filtered_paths(mount, int_age)

    #delete the path and it's contents
    for path in paths:
        delete_path(mount, path)
