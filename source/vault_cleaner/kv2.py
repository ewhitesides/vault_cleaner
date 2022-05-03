"""
kv2
"""

from datetime import datetime
from typing import List, Dict
from vault_cleaner.logger import logger
from vault_cleaner.client import CustomHvacClient

def _get_full_paths(client: CustomHvacClient, mount_point: str) -> List[str]:
    """
    Summary:
        gets list of paths from mount point
        in a path may be one or more subpaths
        so we return the complete "{path}{subpath}"

    Parameters:
        client (CustomHvacClient): the custom hvac client object
        mount_point (str): the name of the kv2 engine mount

    Returns:
        output (List[str]): list of full paths
    """

    output=[]

    #get paths on mount_point (e.g. mycomputer1)
    paths = client.secrets.kv.v2.list_secrets(
        mount_point=mount_point,
        path=''
    )['data']['keys']

    #get subpaths on each path (e.g. root)
    for path in paths:
        subpaths = client.secrets.kv.v2.list_secrets(
            mount_point=mount_point,
            path=path
        )['data']['keys']

        #return complete paths (e.g. mycomputer1/root)
        for subpath in subpaths:
            output.append(f"{path}{subpath}")

    msg = f"retrieved {len(output)} paths from mount {mount_point}"
    logger.info(msg)
    return output


def _is_old(client: CustomHvacClient, mount_point: str, path: str, age: int) -> bool:
    """
    Summary:
        checks updated_time property in metadata,
        and returns True if older than days var

    Parameters:
        client (CustomHvacClient): the custom hvac client object
        mount_point (str): the name of the kv2 engine mount
        path (str): the path/subpath on mount_point
        age (int): number of days

    Returns
        output (bool): True if older than age var, False if not
    """

    output = False

    response = client.secrets.kv.v2.read_secret_metadata(
        mount_point=mount_point,
        path=path
    )

    #convert date such as '2021-03-09T21:07:09.406443746Z' to object
    last_update_time=response['data']['updated_time']
    last_update_time_without_microseconds=last_update_time.split('.')[0]
    last_update_time_datetimeobj = datetime.strptime(
        last_update_time_without_microseconds, '%Y-%m-%dT%H:%M:%S'
    )

    #return True if age is greater than days variable, else return False
    #vault logs in UTC time, so we need 'now' in utc
    now = datetime.utcnow()
    days_diff = (now - last_update_time_datetimeobj).days

    if days_diff > age:
        msg=f"on mount {mount_point}, path {path} is {days_diff} days old"
        logger.info(msg)
        output = True

    return output


def get_age_filtered_paths(mount_point: str, age: int) -> List[str]:
    """
    Summary:
        get list of paths older than $age

    Parameters:
        mount_point (str): the name of the kv2 engine mount
        age (int): number of days

    Returns:
        output (List[str]): list of paths
    """

    try:
        with CustomHvacClient() as client:
            #initial variables
            output = []

            #loop through paths on mount point
            full_paths = _get_full_paths(client, mount_point)
            for full_path in full_paths:

                #if age of path is over $age days old, append to output
                old = _is_old(client, mount_point, full_path, age)
                if old:
                    output.append(full_path)

            msg = f"retrieved {len(output)} paths older than {age} days from mount {mount_point}"
            logger.info(msg)
            return output

    except Exception as err:
        msg = f"Exception occurred getting paths from mount {mount_point}: {err}"
        logger.error(msg)
        raise


def get_current_secret_data(mount_point: str, path: str) -> Dict:
    """
    Summary:
        gets the current secret data for given mount_point/path/subpath

    Parameters:
        mount_point (str): the mount point
        path (str): the path/subpath on mount_point

    Returns:
        output (Dict): the secret data
    """

    try:
        with CustomHvacClient() as client:
            #get current version
            version = client.secrets.kv.v2.read_secret_metadata(
                mount_point=mount_point,
                path=path
            )['data']['current_version']

            #return data for that current version
            output = client.secrets.kv.v2.read_secret_version(
                mount_point=mount_point,
                path=path,
                version=version
            )['data']['data']

            msg = f"retrieved secret from mount {mount_point}, path {path}"
            logger.info(msg)
            return output

    except Exception as err:
        msg = f"Exception occurred getting secret from mount {mount_point}, path {path}: {err}"
        logger.error(msg)
        raise


def write_secret_data(mount_point: str, path: str, secret: dict):
    """
    Summary:
        write secret to mount_point/path/subpath

    Parameters:
        mount_point (str): the name of the kv2 engine mount
        path (str): the path/subpath on mount_point
        secret (dict): the secret data

    Returns:
        none
    """

    try:
        with CustomHvacClient() as client:
            #write to target mount_point/path
            #created_time is not really used except to validate write was successful
            #should create KeyError if ['data']['created_time'] does not exist
            _ = client.secrets.kv.v2.create_or_update_secret(
                mount_point=mount_point,
                path=path,
                secret=secret
            )['data']['created_time']

            msg = f"secret written to mount {mount_point}, path {path}"
            logger.info(msg)

    except Exception as err:
        msg = f"Exception occurred when writing secret to mount {mount_point}, path {path}: {err}"
        logger.error(msg)
        raise


def delete_path(mount_point: str, path: str):
    """
    Summary:
        delete all versions and metadata for a given path/subpath

    Parameters:
        mount_point (str): the name of the kv2 engine mount
        path (str): the path/subpath on mount_point

    Returns:
        none
    """

    try:
        with CustomHvacClient() as client:
            response = client.secrets.kv.v2.delete_metadata_and_all_versions(
                mount_point=mount_point,
                path=path
            )

            #raise error if response is not 200-level
            response.raise_for_status()

            msg = f"deleted path {path} at mount {mount_point}"
            logger.info(msg)

    except Exception as err:
        msg = f"Exception occurred when deleting path {path} on mount {mount_point}: {err}"
        logger.error(msg)
        raise
