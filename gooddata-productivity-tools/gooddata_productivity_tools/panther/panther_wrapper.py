import os
from typing import Self

from gooddata_productivity_tools.panther.panther_api import MethodsAPI
from gooddata_productivity_tools.panther.panther_sdk import MethodsSDK
from gooddata_sdk.sdk import GoodDataSdk


class PantherWrapper(MethodsSDK, MethodsAPI):
    """Wrapper class for the GoodData SDK."""

    def __init__(self, domain: str, token: str) -> None:
        self.panther_domain: str = domain
        self.panther_token: str = token

        # Initialize the GoodData SDK
        self.sdk = GoodDataSdk.create(self.panther_domain, self.panther_token)

        # Set up utils for direct API interaction
        self.base_url = self.get_base_url(self.panther_domain)
        self.headers: dict = {
            "Authorization": f"Bearer {self.panther_token}",
            "Content-Type": "application/vnd.gooddata.api+json",
        }

    @classmethod
    def get_client_from_env(cls) -> Self:
        """Creates a PantherWrapper instance using environment variables."""
        # TODO: is there a sdk method working with env variables? if so, at least unite the env variable names
        domain = os.getenv("PANTHER_DOMAIN")
        token = os.getenv("PANTHER_TOKEN")

        if not domain:
            raise ValueError("PANTHER_DOMAIN environment variable is not set")

        if not token:
            raise ValueError("PANTHER_TOKEN environment variable is not set")

        return cls(domain=domain, token=token)

    # TODO: create from profile

    # TODO: create from sdk instance

    # TODO: allow the user to initiate provisioning with a profile/ (host, token) pair or a GoodDataSdk instance
    # That way the user will not have to create another instance of custom class -> will be easier to use
    # - basically put these "create" class methods into the Provisioning class
