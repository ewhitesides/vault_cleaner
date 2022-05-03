"""
client
"""

import os
import hvac

class CustomHvacClient(hvac.Client):
    """
    hvac client wrapper object with enter and exit methods for use in 'with' statements

    examples of creating class object with enter/exit
        https://www.python.org/dev/peps/pep-0343/
        https://stackoverflow.com/questions/1984325/explaining-pythons-enter-and-exit

    examples of class with inheritance
        https://www.askpython.com/python/oops/python-class-constructor-init-function

    example of login/logout method on hvac.Client object
        https://hvac.readthedocs.io/en/latest/usage/auth_methods/index.html
    """

    def __init__(self):

        #super = parent class hvac.Client
        super().__init__(
            timeout=60 #sometimes get timeout errors with default 30
        )

    def __enter__(self):

        #load in url from env
        self.url=os.environ['VAULT_ADDR']

        #use role-id, secret-id to login
        self.auth.approle.login(
            role_id=os.environ['VAULT_ROLE_ID'],
            secret_id=os.environ['VAULT_SECRET_ID']
        )

        #assert returns AssertionError if is_authenticated() returns False
        assert self.is_authenticated()

        #output
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logout()
