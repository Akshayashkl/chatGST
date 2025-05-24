import pandas as pd

# Load data
gst_compliant_df = pd.read_excel(r'D:\ChatGST\gst_compliant_invoices.csv.xlsx')
gstr_2a_df = pd.read_excel(r'dummy_GSTR_2A.xlsx')

# Normalize columns: strip spaces and lowercase
gst_compliant_df.columns = gst_compliant_df.columns.str.strip().str.lower()
gstr_2a_df.columns = gstr_2a_df.columns.str.strip().str.lower()

# Rename gstr_2a_df columns to match gst_compliant_df
gstr_2a_df.rename(columns={
    'invoice number': 'invoice_number',
    'invoice date': 'invoice_date',
    'gstin of supplier': 'supplier_gstin',
    'taxable value': 'taxable_value'
}, inplace=True)

# Convert invoice_date columns to datetime with dayfirst=True
gst_compliant_df['invoice_date'] = pd.to_datetime(gst_compliant_df['invoice_date'], dayfirst=True)
gstr_2a_df['invoice_date'] = pd.to_datetime(gstr_2a_df['invoice_date'], dayfirst=True)

# Perform reconciliation merge
reconciled = pd.merge(
    gst_compliant_df,
    gstr_2a_df,
    on=['invoice_number', 'invoice_date', 'supplier_gstin', 'taxable_value'],
    how='inner'
)

# Identify unmatched invoices
unmatched = pd.concat([gst_compliant_df, reconciled]).drop_duplicates(keep=False)

# Export results
reconciled.to_excel("matched_invoices.xlsx", index=False)
unmatched.to_excel("unmatched_invoices.xlsx", index=False)

print("Reconciliation complete. Results saved.")
