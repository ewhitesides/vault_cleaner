# README

## Overview

- moves secrets from a kv2 mount VAULT_SOURCE_MOUNT older than VAULT_SOURCE_AGE days to another kv2 mount (VAULT_DESTINATION_MOUNT).

- after VAULT_DESTINATION_AGE days, secrets are deleted from VAULT_DESTINATION_MOUNT.

the use case for this code was password rotation, where machines would rotate their local passwords on a daily/weekly basis.  over time, if the path is no longer being written to, it is assumed that the machine no longer exists, and so this code creates a sort of 'recycle bin' system to prune old data.

this code was used in production with Vault v1.6.5, and should work with newer versions as well, but it has not been verified.

## development setup

the following assumes vscode and docker desktop are installed on your machine

- clone the repo:
    ```bash
    git clone <url>
    ```
- create a file '.env' at base of code folder
    ```bash
    VAULT_ADDR=
    VAULT_ROLE_ID=
    VAULT_SECRET_ID=
    VAULT_SOURCE_MOUNT=
    VAULT_SOURCE_AGE=
    VAULT_DESTINATION_MOUNT=
    VAULT_DESTINATION_AGE=
    ```
- in vscode, open the code folder and it should prompt to open as a container

## debugging

- press F9 to toggle a break point in code
- press F5 to run code in run.py
