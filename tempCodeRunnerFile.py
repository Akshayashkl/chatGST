# Classify unmatched invoices: in GSTR-2A but missing in gst_compliant_df
import pandas as pd
import app

in_2a_not_in_compliant = pd.merge(
    gstr_2a_df,
    reconciled,
    on=['invoice_number', 'invoice_date', 'supplier_gstin', 'taxable_value'],
    how='left',
    indicator=True
).query('_merge == "left_only"').drop(columns=['_merge'])

# Export unmatched sets
in_compliant_not_in_2a.to_excel("in_compliant_not_in_2a.xlsx", index=False)
in_2a_not_in_compliant.to_excel("in_2a_not_in_compliant.xlsx", index=False)

# Generate summary report
summary = {
    "Total GST Compliant Invoices": len(gst_compliant_df),
    "Total GSTR-2A Invoices": len(gstr_2a_df),
    "Matched Invoices": len(reconciled),
    "Unmatched in Compliant Only": len(in_compliant_not_in_2a),
    "Unmatched in GSTR-2A Only": len(in_2a_not_in_compliant)
}

summary_df = pd.DataFrame(list(summary.items()), columns=["Metric", "Count"])
summary_df.to_excel("gst_reconciliation_summary.xlsx", index=False)