from typing import Dict, Any, Optional
from .client import EpicorClient

class PartSvc:
    def __init__(self, client: EpicorClient):
        self.client = client
        self.svc_name = "Erp.BO.PartSvc"

    def create_part(self, part_num: str, description: str, part_type: str = "P", optional_fields: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create a new Part via OData POST to Parts."""
        payload = {
            "PartNum": part_num,
            "PartDescription": description,
            "TypeCode": part_type, # P = Purchased, M = Manufactured
            "Company": self.client.company
        }
        if optional_fields:
            payload.update(optional_fields)
            
        return self.client.post(self.svc_name, "Parts", payload)

    def get_part(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get Part data via OData."""
        return self.client.get(self.svc_name, "Parts", params=params)

    def get_part_warehouses(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get Part Warehouse data via OData."""
        return self.client.get(self.svc_name, "PartWhses", params=params)

    def get_part_revisions(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get Part Revision data via OData."""
        return self.client.get(self.svc_name, "PartRevs", params=params)
