from typing import Dict, Any, Optional
from .client import EpicorClient

class QuoteSvc:
    def __init__(self, client: EpicorClient):
        self.client = client
        self.svc_name = "Erp.BO.QuoteSvc"

    def Quotes_POST(self, customer_num: int, optional_fields: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create a new Quote head via OData POST to Quotes."""
        payload = {
            "CustNum": customer_num,
            "Company": self.client.company
        }
        if optional_fields:
            payload.update(optional_fields)
            
        return self.client.post(self.svc_name, "Quotes", payload)

    def Quotes_GET(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get Quote headers via OData."""
        return self.client.get(self.svc_name, "Quotes", params=params)

    def QuoteDtls_POST(self, quote_num: int, part_num: str, qty: float, line_desc: Optional[str] = None, optional_fields: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Add a line to an existing quote via OData POST to QuoteDtls."""
        payload = {
            "QuoteNum": quote_num,
            "PartNum": part_num,
            "LineDesc": line_desc or part_num,
            "OrderQty": qty,
            "Company": self.client.company
        }
        if optional_fields:
            payload.update(optional_fields)
            
        return self.client.post(self.svc_name, "QuoteDtls", payload)

    def QuoteDtls_GET(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get Quote lines via OData."""
        return self.client.get(self.svc_name, "QuoteDtls", params=params)

    def QuoteQties_POST(self, quote_num: int, quote_line: int, qty: float, optional_fields: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Add a Sales Quote quantity break via OData POST to QuoteQties."""
        payload = {
            "QuoteNum": quote_num,
            "QuoteLine": quote_line,
            "OurQuantity": qty,
            "Company": self.client.company
        }
        if optional_fields:
            payload.update(optional_fields)
            
        return self.client.post(self.svc_name, "QuoteQties", payload)

    def QuoteQties_GET(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get Quote quantities via OData."""
        return self.client.get(self.svc_name, "QuoteQties", params=params)
