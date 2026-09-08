import os, sys
import xml.etree.ElementTree as ET
if not hasattr(ET.ElementTree, 'getiterator'):
    ET.ElementTree.getiterator = lambda self, tag=None: self.iter(tag)

import pandas as pd

PY = "/Users/temu/.workbuddy/binaries/python/envs/default/bin/python"
FILES = {
    "C_xls": "/Users/temu/Downloads/产品库存(2).xls",
    "A_xlsx": "/Users/temu/Downloads/2026-09-01_bizWarehouseProductInventoryExport6409.xlsx",
    "B_xlsx": "/Users/temu/Downloads/ProductInventory-1788234957397-556059.xlsx",
    "master": "/Users/temu/Downloads/导出产品-按SKU-953261488470130688.xlsx",
}

def norm(s):
    return "".join(ch for ch in str(s).lower() if ch.isalnum())

# ---- Warehouse C .xls ----
print("="*70)
print("WAREHOUSE C (.xls)")
try:
    df = pd.read_excel(FILES["C_xls"], header=2, dtype=str)
    print("shape:", df.shape)
    print("columns:", list(df.columns))
    # find sku-ish column
    sku_col = None
    for c in df.columns:
        if norm(c) in ("产品sku","sku","产品条码"):
            sku_col = c; break
    cust_col = None
    for c in df.columns:
        if norm(c) in ("客户","仓库"):
            cust_col = c; break
    print("sku_col:", sku_col, "cust_col:", cust_col)
    # sample
    print(df.head(3).to_string())
    if sku_col:
        vals = df[sku_col].dropna().astype(str)
        c3950 = vals[vals.str.upper().str.startswith("C3950-")]
        print("C3950- prefixed SKU count:", len(c3950))
        print("sample C3950 SKUs:", c3950.head(10).tolist())
    if cust_col:
        print("customer values:", df[cust_col].dropna().unique()[:10])
except Exception as e:
    print("ERR C:", repr(e))

# ---- Warehouse A ----
print("="*70)
print("WAREHOUSE A (.xlsx)")
try:
    df = pd.read_excel(FILES["A_xlsx"], dtype=str)
    print("shape:", df.shape)
    print("columns:", list(df.columns))
    sku_col=None
    for c in df.columns:
        if norm(c) in ("sku","产品条码","自定义编码","产品sku"):
            sku_col=c; break
    print("sku_col:", sku_col)
    if sku_col:
        vals = df[sku_col].dropna().astype(str)
        c3950 = vals[vals.str.upper().str.startswith("C3950-")]
        print("C3950- count:", len(c3950))
        print(c3950.head(5).tolist())
except Exception as e:
    print("ERR A:", repr(e))

# ---- Warehouse B ----
print("="*70)
print("WAREHOUSE B (.xlsx)")
try:
    df = pd.read_excel(FILES["B_xlsx"], dtype=str)
    print("shape:", df.shape)
    print("columns:", list(df.columns))
    sku_col=None
    for c in df.columns:
        if norm(c) in ("sku","自定义编码","产品条码","产品sku"):
            sku_col=c; break
    print("sku_col:", sku_col)
    if sku_col:
        vals = df[sku_col].dropna().astype(str)
        c3950 = vals[vals.str.upper().str.startswith("C3950-")]
        print("C3950- count:", len(c3950))
        print(c3950.head(5).tolist())
except Exception as e:
    print("ERR B:", repr(e))

# ---- Master ----
print("="*70)
print("PRODUCT MASTER")
try:
    df = pd.read_excel(FILES["master"], sheet_name="产品", dtype=str)
    print("shape:", df.shape)
    print("columns:", list(df.columns))
    sku_col = "*SKU" if "*SKU" in df.columns else df.columns[0]
    spu_col = "SPU" if "SPU" in df.columns else None
    vals = df[sku_col].dropna().astype(str)
    c3950 = vals[vals.str.upper().str.startswith("C3950-")]
    print("master C3950- SKU count:", len(c3950))
    print("sample:", c3950.head(8).tolist())
except Exception as e:
    print("ERR master:", repr(e))
