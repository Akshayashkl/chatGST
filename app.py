import pandas as pd

# Step 1: Load data
gst_compliant_df = pd.read_excel(r'D:\ChatGST\gst_compliant_invoices.csv.xlsx')
gstr_2a_df = pd.read_excel(r'dummy_GSTR_2A.xlsx')

# Step 2: Normalize column names
gst_compliant_df.columns = gst_compliant_df.columns.str.strip().str.lower()
gstr_2a_df.columns = gstr_2a_df.columns.str.strip().str.lower()

# Step 3: Rename columns in GSTR-2A
gstr_2a_df.rename(columns={
    'invoice number': 'invoice_number',
    'invoice date': 'invoice_date',
    'gstin of supplier': 'supplier_gstin',
    'taxable value': 'taxable_value'
}, inplace=True)

# Step 4: Convert dates
gst_compliant_df['invoice_date'] = pd.to_datetime(gst_compliant_df['invoice_date'], dayfirst=True)
gstr_2a_df['invoice_date'] = pd.to_datetime(gstr_2a_df['invoice_date'], dayfirst=True)

# Step 5: Reconciliation merge (matched invoices)
reconciled = pd.merge(
    gst_compliant_df,
    gstr_2a_df,
    on=['invoice_number', 'invoice_date', 'supplier_gstin', 'taxable_value'],
    how='inner'
)

# Step 6: Identify unmatched invoices (all unmatched in gst_compliant_df)
unmatched = pd.concat([gst_compliant_df, reconciled]).drop_duplicates(keep=False)

# Step 7: Classify unmatched invoices
in_compliant_not_in_2a = pd.merge(
    gst_compliant_df,
    reconciled,
    on=['invoice_number', 'invoice_date', 'supplier_gstin', 'taxable_value'],
    how='left',
    indicator=True
).query('_merge == "left_only"').drop(columns=['_merge'])

in_2a_not_in_compliant = pd.merge(
    gstr_2a_df,
    reconciled,
    on=['invoice_number', 'invoice_date', 'supplier_gstin', 'taxable_value'],
    how='left',
    indicator=True
).query('_merge == "left_only"').drop(columns=['_merge'])

# Step 8: Export to Excel files
reconciled.to_excel("matched_invoices.xlsx", index=False)
unmatched.to_excel("unmatched_invoices.xlsx", index=False)
in_compliant_not_in_2a.to_excel("in_compliant_not_in_2a.xlsx", index=False)
in_2a_not_in_compliant.to_excel("in_2a_not_in_compliant.xlsx", index=False)

# Step 9: Generate summary report
summary = {
    "Total GST Compliant Invoices": len(gst_compliant_df),
    "Total GSTR-2A Invoices": len(gstr_2a_df),
    "Matched Invoices": len(reconciled),
    "Unmatched in Compliant Only": len(in_compliant_not_in_2a),
    "Unmatched in GSTR-2A Only": len(in_2a_not_in_compliant)
}

summary_df = pd.DataFrame(list(summary.items()), columns=["Metric", "Count"])
summary_df.to_excel("gst_reconciliation_summary.xlsx", index=False)

# Step 10: Done
print("GST Reconciliation complete. Results saved as Excel files.")
