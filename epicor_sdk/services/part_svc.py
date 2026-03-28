from typing import Dict, Any, Optional
from .client import EpicorClient

class PartSvc:
    def __init__(self, client: EpicorClient):
        self.client = client
        self.svc_name = "Erp.BO.PartSvc"

    def PartSvc_POST(self, part_num: str, description: str, optional_fields: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create a new Part via OData POST to PartSvc."""
        payload = {
            "PartNum": part_num,
            "PartDescription": description,
            "Company": self.client.company
        }
        if optional_fields:
            payload.update(optional_fields)
            
        return self.client.post(self.svc_name, "PartSvc", payload)

    def PartSvc_GET(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get Part data via OData GET from PartSvc."""
        return self.client.get(self.svc_name, "PartSvc", params=params)

    def PartWhses_GET(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get Part Warehouse data via OData."""
        return self.client.get(self.svc_name, "PartWhses", params=params)

    def PartPlants_POST(self, part_num: str, plant_id: str, prim_whse: str, optional_fields: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create a new Part Site (PartPlant) record via OData POST to PartPlants."""
        payload = {
            "PartNum": part_num,
            "Plant": plant_id,
            "PrimWhse": prim_whse,
            "Company": self.client.company
        }
        if optional_fields:
            payload.update(optional_fields)
            
        return self.client.post(self.svc_name, "PartPlants", payload)

    def PartPlants_GET(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get Part Site data via OData."""
        return self.client.get(self.svc_name, "PartPlants", params=params)

    def PartRevs_GET(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get Part Revision data via OData."""
        return self.client.get(self.svc_name, "PartRevs", params=params)
