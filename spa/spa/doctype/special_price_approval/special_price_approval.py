# Copyright (c) 2026, spa and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class SpecialPriceApproval(Document):
    pass

@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_sales_persons(doctype, txt, searchfield, start, page_len, filters):
    customer = filters.get("customer")

    if not customer:
        return frappe.db.get_all(
            "Sales Person",
            filters={
                "enabled": 1
            },
            fields=["name"],
            limit_start=start,
            limit_page_length=page_len
        )

    return frappe.db.sql(
        """
        SELECT
            sp.name
        FROM
            `tabSales Person` sp
        INNER JOIN
            `tabSales Team` st
            ON st.sales_person = sp.name
        WHERE
            st.parent = %(customer)s
            AND st.parenttype = 'Customer'
            AND sp.enabled = 1
            AND sp.name LIKE %(txt)s
        ORDER BY
            sp.name
        LIMIT %(start)s, %(page_len)s
        """,
        {
            "customer": customer,
            "txt": f"%{txt}%",
            "start": start,
            "page_len": page_len
        }
    )

def create_sales_order(doc, method=None):

    # Only HO-approved requests can create Sales Orders
    if doc.status != "HO Approved":
        return

    # Prevent duplicate Sales Orders
    if doc.sales_order_reference:
        return

    sales_order = frappe.get_doc({
        "doctype": "Sales Order",
		"customer": doc.customer,
        "special_price_approval": doc.name,
        "territory": doc.territory,
        "delivery_date": frappe.utils.today(),
        "items": []
    })

    for item in doc.items:
        sales_order.append("items", {
            "item_code": item.item_code,
            "qty": item.quantity,
            "rate": item.approved_rate or item.requested_rate
        })

    sales_order.insert()

    doc.db_set(
        "sales_order_reference",
        sales_order.name
    )

    frappe.msgprint(
        f"Sales Order {sales_order.name} created successfully."
    )

