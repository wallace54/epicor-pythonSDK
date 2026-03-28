from typing import Dict, Any, Optional
from .client import EpicorClient

class QuoteSvc:
    def __init__(self, client: EpicorClient):
        self.client = client
        self.svc_name = "Erp.BO.QuoteSvc"

    def get_new_quote(self) -> Dict[str, Any]:
        """Initialize a new Quote dataset."""
        return self.client.post(self.svc_name, "GetNewQuote", {"ds": {}})

    def create_quote(self, customer_num: int, territory_id: Optional[str] = None) -> Dict[str, Any]:
        """Create a quote head via OData POST to QuoteHeads."""
        payload = {
            "CustNum": customer_num,
            "TerritoryID": territory_id or "",
            "Company": self.client.company
        }
        return self.client.post(self.svc_name, "QuoteHeads", payload)

    def add_quote_line(self, quote_num: int, part_num: str, qty: float, optional_fields: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Add a line to an existing quote via OData POST to QuoteDtls."""
        payload = {
            "QuoteNum": quote_num,
            "PartNum": part_num,
            "OrderQty": qty,
            "Company": self.client.company
        }
        if optional_fields:
            payload.update(optional_fields)
            
        return self.client.post(self.svc_name, "QuoteDtls", payload)
