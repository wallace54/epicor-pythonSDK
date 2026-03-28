import os
import logging
from dotenv import load_dotenv
from epicor_sdk.client import EpicorClient
from epicor_sdk.services.customer_svc import CustomerSvc
from epicor_sdk.services.part_svc import PartSvc
from epicor_sdk.services.quote_svc import QuoteSvc
from epicor_sdk.services.sales_order_svc import SalesOrderSvc
from epicor_sdk.services.job_entry_svc import JobEntrySvc
from epicor_sdk.services.cust_ship_svc import CustShipSvc
from epicor_sdk.services.ar_invoice_svc import ARInvoiceSvc

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("DemoDataFactory")

def main():
    # Load Environment
    load_dotenv()
    
    server_url = os.getenv("EPICOR_SERVER_URL")
    company = os.getenv("EPICOR_COMPANY")
    api_key = os.getenv("EPICOR_API_KEY")
    username = os.getenv("EPICOR_USERNAME")
    password = os.getenv("EPICOR_PASSWORD")
    
    if not all([server_url, company, api_key, username, password]):
        logger.error("Missing configuration in .env file (see .env.example)")
        return

    # Initialize Client & Services
    client = EpicorClient(server_url, company, api_key, username, password)
    customer_svc = CustomerSvc(client)
    part_svc = PartSvc(client)
    quote_svc = QuoteSvc(client)
    order_svc = SalesOrderSvc(client)
    job_svc = JobEntrySvc(client)
    ship_svc = CustShipSvc(client)
    inv_svc = ARInvoiceSvc(client)

    cust_id = f"DEMO-{os.urandom(2).hex().upper()}"
    part_num = f"DEMO-{os.urandom(2).hex().upper()}" # Unique demo part ID
    qty = 5.0

    try:
        # 0.1 Create a Customer
        logger.info(f"--- 0.1 Creating Customer {cust_id} ---")
        cust_resp = customer_svc.create_customer(cust_id, name="SDK Demo Customer")
        customer_num = cust_resp.get("CustNum")
        logger.info(f"Customer {cust_id} created successfully (CustNum: {customer_num})")

        # 0.2 Create a Part
        logger.info(f"--- 0.2 Creating Part {part_num} ---")
        part_svc.create_part(part_num, description="SDK Demo Product", part_type="M")
        logger.info(f"Part {part_num} created successfully")

        # 1. Create a Quote
        logger.info(f"--- 1. Creating Quote for CustNum {customer_num} ---")
        quote_resp = quote_svc.create_quote(customer_num)
        quote_num = quote_resp.get("QuoteNum")
        logger.info(f"Quote Created: {quote_num}")
        
        # Add a Quote Line
        logger.info(f"Adding line for part {part_num} to Quote {quote_num}")
        quote_line_resp = quote_svc.add_quote_line(quote_num, part_num, qty)
        logger.info("Quote Line added")

        # 2. Create Sales Order
        logger.info(f"--- 2. Creating Sales Order for Quote {quote_num} ---")
        order_resp = order_svc.create_order(customer_num, optional_fields={"QuoteNum": quote_num})
        order_num = order_resp.get("OrderNum")
        logger.info(f"Sales Order Created: {order_num}")
        
        # Add an Order Line (or it might have copied from Quote depending on Epicor settings)
        logger.info(f"Adding line for part {part_num} to Order {order_num}")
        order_line_resp = order_svc.add_order_line(order_num, part_num, qty, line_desc="Demo Demo Data")
        order_line = 1 # Assuming first line is 1
        logger.info(f"Order Line {order_line} added")

        # Explicitly Create/Update Order Release
        logger.info(f"Creating Order Release for Order {order_num}, Line {order_line}")
        order_rel_resp = order_svc.add_order_release(order_num, order_line, qty, optional_fields={"WarehouseCode": "Main"})
        logger.info("Order Release created/updated")

        # Create Order Misc Charges
        logger.info(f"Adding Miscellaneous Charges to Order {order_num}")
        
        # Header Charge (e.g. general handling fee)
        order_svc.add_order_misc(order_num, misc_code="HAND", misc_amt=10.0, order_line=0)
        logger.info("Header Misc charge added ($10.00)")

        # Line Charge (e.g. line-specific shipping fee)
        order_svc.add_order_misc(order_num, misc_code="SHIP", misc_amt=15.0, order_line=order_line)
        logger.info(f"Line {order_line} Misc charge added ($15.00)")

        # --- Verification Step using new GET functions ---
        logger.info("--- 2.5 Verification: Retrieving Order Data ---")
        filter_params = {"$filter": f"OrderNum eq {order_num}"}
        
        order_data = order_svc.get_order(params=filter_params)
        logger.info(f"Retrieved Order {order_num} successfully")
        
        lines_data = order_svc.get_order_lines(params=filter_params)
        logger.info(f"Lines found: {len(lines_data.get('value', []))}")
        
        releases_data = order_svc.get_order_releases(params=filter_params)
        logger.info(f"Releases found: {len(releases_data.get('value', []))}")
        
        miscs_data = order_svc.get_order_miscs(params=filter_params)
        logger.info(f"Misc Charges found: {len(miscs_data.get('value', []))}")

        # 3. Create a Job
        logger.info(f"--- 3. Creating Job for Part {part_num} ---")
        job_resp = job_svc.create_job(part_num, qty, order_num=order_num)
        job_num = job_resp.get("JobNum")
        logger.info(f"Job Created: {job_num}")

        # 4. Create Shipment
        logger.info(f"--- 4. Creating Customer Shipment for Order {order_num} ---")
        ship_resp = ship_svc.create_shipment(order_num)
        pack_num = ship_resp.get("PackNum")
        logger.info(f"Shipment Created (PackNum): {pack_num}")

        # 5. Create AR Invoice
        logger.info(f"--- 5. Creating AR Invoice for Order {order_num} ---")
        inv_resp = inv_svc.create_invoice(order_num)
        invoice_num = inv_resp.get("InvoiceNum")
        logger.info(f"Invoice Created: {invoice_num}")

        logger.info("--- Demo Data Generation Complete! ---")

    except Exception as e:
        logger.error(f"Error during flow: {e}")

if __name__ == "__main__":
    main()
