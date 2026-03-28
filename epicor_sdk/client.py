import requests
import json
import logging
from typing import Dict, Any, Optional

class EpicorClient:
    def __init__(self, server_url: str, company: str, api_key: str, username: str, password: str):
        self.server_url = server_url.rstrip('/')
        self.company = company
        self.api_key = api_key
        self.username = username
        self.password = password
        
        self.session = requests.Session()
        self.session.auth = (username, password)
        self.session.headers.update({
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-API-Key": api_key
        })
        
        self.base_odata_url = f"{self.server_url}/api/v2/odata/{self.company}"
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("EpicorClient")

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        try:
            response.raise_for_status()
            if response.status_code == 204:
                return {}
            return response.json()
        except requests.exceptions.HTTPError as e:
            self.logger.error(f"HTTP Error: {response.status_code} - {response.text}")
            raise e
        except json.JSONDecodeError:
            self.logger.error(f"Failed to decode JSON from response: {response.text}")
            return {"raw_text": response.text}

    def get(self, service: str, method: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = f"{self.base_odata_url}/{service}/{method}"
        response = self.session.get(url, params=params)
        return self._handle_response(response)

    def post(self, service: str, method: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Call a Business Object's RPC-style method (e.g. GetNewQuote, Update)"""
        url = f"{self.base_odata_url}/{service}/{method}"
        response = self.session.post(url, json=data)
        return self._handle_response(response)

    def update_ext(self, service: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Call UpdateExt for simpler CRUD operations."""
        return self.post(service, "UpdateExt", data)

    def patch(self, service: str, key_params: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Standard OData PATCH for direct record updates"""
        url = f"{self.base_odata_url}/{service}({key_params})"
        response = self.session.patch(url, json=data)
        return self._handle_response(response)
