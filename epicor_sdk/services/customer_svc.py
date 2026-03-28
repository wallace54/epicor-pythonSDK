from typing import Dict, Any, Optional
from .client import EpicorClient

class CustomerSvc:
    def __init__(self, client: EpicorClient):
        self.client = client
        self.svc_name = "Erp.BO.CustomerSvc"

    def Customers_POST(self, cust_id: str, name: str, optional_fields: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create a new Customer via OData POST to Customers."""
        payload = {
            "CustID": cust_id,
            "Name": name,
            "Company": self.client.company
        }
        if optional_fields:
            payload.update(optional_fields)
            
        return self.client.post(self.svc_name, "Customers", payload)

    def Customers_GET(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get Customer data via OData."""
        return self.client.get(self.svc_name, "Customers", params=params)

    def CustShipTos_GET(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get Customer ShipTo data via OData."""
        return self.client.get(self.svc_name, "CustShipTos", params=params)

    def CustBillTos_GET(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get Customer BillTo data via OData."""
        return self.client.get(self.svc_name, "CustBillTos", params=params)
