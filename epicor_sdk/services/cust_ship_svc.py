from typing import Dict, Any, Optional
from .client import EpicorClient

class CustShipSvc:
    def __init__(self, client: EpicorClient):
        self.client = client
        self.svc_name = "Erp.BO.CustShipSvc"

    def create_shipment(self, order_num: int, optional_fields: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create a Customer Shipment via OData POST to ShipHeads."""
        payload = {
            "Company": self.client.company,
            "OrderNum": order_num
        }
        if optional_fields:
            payload.update(optional_fields)
            
        return self.client.post(self.svc_name, "ShipHeads", payload)
