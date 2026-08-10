// Copyright (c) 2026, spa and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Special Price Approval", {
// 	refresh(frm) {

// 	},
// });

frappe.ui.form.on("Special Price Approval", {
    setup(frm) {
        frm.set_query("sales_person", function () {
            if (!frm.doc.customer) {
                return {
                    filters: {
                        enabled: 1
                    }
                };
            }

            return {
                query: "spa.spa.doctype.special_price_approval.special_price_approval.get_sales_persons",
                filters: {
                    customer: frm.doc.customer
                }
            };
        });
    },

    customer(frm) {
        frm.set_value("sales_person", null);
    }
});