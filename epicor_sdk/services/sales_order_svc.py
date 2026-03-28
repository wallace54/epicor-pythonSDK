from typing import Dict, Any, Optional
from .client import EpicorClient

class SalesOrderSvc:
    def __init__(self, client: EpicorClient):
        self.client = client
        self.svc_name = "Erp.BO.SalesOrderSvc"

    def SalesOrder_POST(self, customer_num: int, optional_fields: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create a Sales Order head via OData POST to SalesOrder."""
        payload = {
            "CustNum": customer_num,
            "Company": self.client.company
        }
        if optional_fields:
            payload.update(optional_fields)
            
        return self.client.post(self.svc_name, "SalesOrder", payload)

    def SalesOrder_GET(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get Sales Order headers via OData."""
        return self.client.get(self.svc_name, "SalesOrder", params=params)

    def OrderDtls_POST(self, order_num: int, part_num: str, qty: float, line_desc: Optional[str] = None, optional_fields: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Add a Sales Order line via OData POST to OrderDtls."""
        payload = {
            "OrderNum": order_num,
            "PartNum": part_num,
            "LineDesc": line_desc or part_num,
            "SellingQuantity": qty,
            "Company": self.client.company
        }
        if optional_fields:
            payload.update(optional_fields)
            
        return self.client.post(self.svc_name, "OrderDtls", payload)

    def OrderDtls_GET(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get Sales Order lines via OData."""
        return self.client.get(self.svc_name, "OrderDtls", params=params)

    def OrderRels_POST(self, order_num: int, order_line: int, qty: float, optional_fields: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create a Sales Order release via OData POST to OrderRels."""
        payload = {
            "OrderNum": order_num,
            "OrderLine": order_line,
            "SellingReqQty": qty,
            "Company": self.client.company
        }
        if optional_fields:
            payload.update(optional_fields)
            
        return self.client.post(self.svc_name, "OrderRels", payload)

    def OrderRels_GET(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get Sales Order releases via OData."""
        return self.client.get(self.svc_name, "OrderRels", params=params)

    def OrderMiscs_POST(self, order_num: int, misc_code: str, misc_amt: float, order_line: int = 0, optional_fields: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Add a miscellaneous charge to a Sales Order via OData POST to OrderMiscs."""
        payload = {
            "OrderNum": order_num,
            "OrderLine": order_line,
            "MiscCode": misc_code,
            "MiscAmt": misc_amt,
            "Company": self.client.company
        }
        if optional_fields:
            payload.update(optional_fields)
            
        return self.client.post(self.svc_name, "OrderMiscs", payload)

    def OrderMiscs_GET(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get Sales Order miscellaneous charges via OData."""
        return self.client.get(self.svc_name, "OrderMiscs", params=params)
