# Copyright (c) 2026, spa and contributors
# For license information, please see license.txt

# import frappe
from pydoc import doc

from frappe.model.document import Document


class SpecialPriceApprovalItem(Document):
	pass

# def total_current_amount(doc, method=None):
# 	total_amount = 0

# 	for item in doc.Special Price Approval Item:
# 		rate = item.current_price 
# 		total_amount += rate * item.quantity

# 	doc.db_set(
# 		"total_wrt_current_price",
# 		total_amount
# 	)



