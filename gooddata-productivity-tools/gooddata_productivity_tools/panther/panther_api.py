import json
from typing import Any

import requests

TIMEOUT = 60
PANTHER_REQUEST_PAGE_SIZE = 250
PANTHER_API_VERSION = "v1"


class MethodsAPI:
    headers: dict[str, str]
    base_url: str

    @staticmethod
    def get_base_url(domain: str) -> str:
        """Returns the root endpoint for the Panther API."""
        # if the domain ends with a slash, remove it
        if domain[-1] == "/":
            domain = domain[:-1]

        # Handle missing protocol
        if not domain.startswith("https://") and not domain.startswith("http://"):
            domain = f"https://{domain}"

        if domain.startswith("http://") and not domain.startswith("https://"):
            domain = domain.replace("http://", "https://")

        return f"{domain}/api/{PANTHER_API_VERSION}"

    def get_custom_application_setting(
        self, workspace_id: str, setting_id: str
    ) -> requests.Response:
        """Sends a GET request to the server."""
        url = f"/entities/workspaces/{workspace_id}/customApplicationSettings/{setting_id}"
        return self._get(url)

    def put_custom_application_setting(
        self, workspace_id: str, setting_id: str, data: dict[str, Any]
    ) -> requests.Response:
        url = f"/entities/workspaces/{workspace_id}/customApplicationSettings/{setting_id}"
        return self._put(url, data, self.headers)

    def post_custom_application_setting(
        self, workspace_id: str, data: dict[str, Any]
    ) -> requests.Response:
        """Posts a custom application setting to the server."""
        url = f"/entities/workspaces/{workspace_id}/customApplicationSettings/"
        return self._post(url, data, self.headers)

    def get_all_workspace_data_filters(self, workspace_id: str) -> requests.Response:
        """Gets all workspace data filters for a given workspace."""
        url = f"/entities/workspaces/{workspace_id}/workspaceDataFilters"
        return self._get(url)

    def get_workspace_data_filter_settings(
        self, workspace_id: str
    ) -> requests.Response:
        """Gets all workspace data filter settings for a given workspace."""
        url = f"/entities/workspaces/{workspace_id}/workspaceDataFilterSettings?include=workspaceDataFilters"

        return self._get(url)

    def get_workspace_data_filter_setting(
        self, workspace_id: str, wdf_id: str
    ) -> requests.Response:
        """Gets a single workspace data filter setting for a given workspace."""
        url = (
            f"/entities/workspaces/{workspace_id}/workspaceDataFilterSettings/{wdf_id}"
        )

        return self._get(url)

    def put_workspace_data_filter_setting(
        self,
        workspace_id: str,
        wdf_setting: dict[str, Any],
    ) -> requests.Response:
        wdf_setting_id = wdf_setting["data"]["id"]
        endpoint = f"/entities/workspaces/{workspace_id}/workspaceDataFilterSettings/{wdf_setting_id}"
        return self._put(
            endpoint,
            wdf_setting,
            self.headers,
        )

    def post_workspace_data_filter_setting(
        self,
        workspace_id: str,
        wdf_setting: dict[str, Any],
    ) -> requests.Response:
        endpoint = f"/entities/workspaces/{workspace_id}/workspaceDataFilterSettings/"
        return self._post(
            endpoint,
            wdf_setting,
            self.headers,
        )

    def delete_workspace_data_filter_setting(
        self,
        workspace_id: str,
        wdf_setting_id: str,
    ) -> requests.Response:
        endpoint = f"/entities/workspaces/{workspace_id}/workspaceDataFilterSettings/{wdf_setting_id}"
        return self._delete(
            endpoint,
        )

    def get_user_data_filters(self, workspace_id: str) -> requests.Response:
        """Gets all user data filters for a given workspace."""
        endpoint = f"/layout/workspaces/{workspace_id}/userDataFilters"
        return self._get(endpoint)

    def get_automations(self, workspace_id: str) -> requests.Response:
        """Gets all automations for a given workspace."""
        endpoint = f"/entities/workspaces/{workspace_id}/automations?include=ALL"
        return self._get(endpoint)

    def post_workspace_data_filter(
        self, workspace_id: str, data: dict[str, Any]
    ) -> requests.Response:
        """Creates a workspace data filter for a given workspace."""
        endpoint = f"/entities/workspaces/{workspace_id}/workspaceDataFilters"
        return self._post(endpoint, data, self.headers)

    def _get(self, endpoint: str) -> requests.Response:
        """Sends a GET request to the server and returns JSON object."""
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, headers=self.headers, timeout=TIMEOUT)
        return response

    def _post(
        self,
        endpoint: str,
        data: Any,
        headers: dict | None = None,
    ) -> requests.Response:
        """Sends a POST request to the server with a given JSON object."""
        if not headers:
            request_headers = self.headers
        else:
            request_headers = headers

        url = f"{self.base_url}{endpoint}"
        data_json = json.dumps(data)
        response = requests.post(
            url, data=data_json, headers=request_headers, timeout=TIMEOUT
        )
        return response

    def _put(
        self,
        endpoint: str,
        data: Any,
        headers: dict | None = None,
    ) -> requests.Response:
        """Sends a POST request to the server with a given JSON object."""
        if not headers:
            request_headers = self.headers
        else:
            request_headers = headers

        url = f"{self.base_url}{endpoint}"

        data_json = json.dumps(data)

        response = requests.put(
            url, data=data_json, headers=request_headers, timeout=TIMEOUT
        )
        return response

    def _delete(
        self,
        endpoint: str,
    ) -> requests.Response:
        """Sends a DELETE request to the server."""
        url = f"{self.base_url}{endpoint}"

        response = requests.delete(url, headers=self.headers, timeout=TIMEOUT)

        return response
