from typing import Dict, Any, Optional
from .client import EpicorClient

class ARInvoiceSvc:
    def __init__(self, client: EpicorClient):
        self.client = client
        self.svc_name = "Erp.BO.ARInvoiceSvc"

    def create_invoice(self, order_num: int, optional_fields: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Generate an AR Invoice via OData POST to InvcHeads."""
        payload = {
            "Company": self.client.company,
            "OrderNum": order_num
        }
        if optional_fields:
            payload.update(optional_fields)
            
        return self.client.post(self.svc_name, "InvcHeads", payload)
