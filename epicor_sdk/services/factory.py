from typing import Dict, Any, Optional
from .client import EpicorClient

class JobEntrySvc:
    def __init__(self, client: EpicorClient):
        self.client = client
        self.svc_name = "Erp.BO.JobEntrySvc"

    def create_job(self, part_num: str, qty: float, order_num: Optional[int] = None, order_line: Optional[int] = None) -> Dict[str, Any]:
        """Create a new Job via OData POST to JobHeads."""
        # Note: In Epicor, jobs often have JobNum manual or auto-assigned. 
        # For OData, we just POST the fields.
        payload = {
            "PartNum": part_num,
            "ProdQty": qty,
            "Company": self.client.company,
            "JobEngineered": True,
            "JobReleased": True
        }
        return self.client.post(self.svc_name, "JobHeads", payload)

class CustShipSvc:
    def __init__(self, client: EpicorClient):
        self.client = client
        self.svc_name = "Erp.BO.CustShipSvc"

    def create_shipment(self, order_num: int) -> Dict[str, Any]:
        """Create a Customer Shipment via OData POST to ShipHeads."""
        payload = {
            "Company": self.client.company,
            "OrderNum": order_num
        }
        return self.client.post(self.svc_name, "ShipHeads", payload)

class ARInvoiceSvc:
    def __init__(self, client: EpicorClient):
        self.client = client
        self.svc_name = "Erp.BO.ARInvoiceSvc"

    def create_invoice(self, order_num: int) -> Dict[str, Any]:
        """Generate an AR Invoice via OData POST to InvcHeads."""
        payload = {
            "Company": self.client.company,
            "OrderNum": order_num
        }
        return self.client.post(self.svc_name, "InvcHeads", payload)
