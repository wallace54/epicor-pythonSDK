from typing import Dict, Any, Optional
from .client import EpicorClient

class JobEntrySvc:
    def __init__(self, client: EpicorClient):
        self.client = client
        self.svc_name = "Erp.BO.JobEntrySvc"

    def create_job(self, part_num: str, qty: float, order_num: Optional[int] = None, order_line: Optional[int] = None, optional_fields: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
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
        if optional_fields:
            payload.update(optional_fields)
            
        return self.client.post(self.svc_name, "JobHeads", payload)
