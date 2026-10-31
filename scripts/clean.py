"""Step 1 - data preparation.

Reads the original DataHub file and writes the cleaned CSV used for triplification:
  * keeps 10 of the 14 columns (52-week low/high, price/sales and price/book dropped),
  * renames columns to snake_case,
  * adds the 8-digit GICS sub-industry code by matching the 'Sector' column
    (which actually holds GICS *sub-industries*, not sectors) to the GICS structure,
  * leaves missing financial values empty (they are omitted in the RDF, never set to 0).

Usage:  python scripts/clean.py
"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
src = ROOT / "data/original/constituents-financials.csv"
gics = pd.read_csv(ROOT / "data/cleaned/gics-structure.csv", dtype=str)
df = pd.read_csv(src)

keep = {
    "Symbol": "ticker",
    "Name": "name",
    "Sector": "gics_sub_industry",
    "Price": "share_price_usd",
    "Price/Earnings": "price_earnings_ratio",
    "Dividend Yield": "dividend_yield",
    "Earnings/Share": "earnings_per_share_usd",
    "Market Cap": "market_cap_usd",
    "EBITDA": "ebitda_usd",
    "SEC Filings": "sec_filings_url",
}
out = df[list(keep)].rename(columns=keep)
out["name"] = out["name"].str.strip()

code = dict(zip(gics.sub_industry, gics.sub_industry_code))
out.insert(3, "gics_sub_industry_code", out["gics_sub_industry"].map(code))
assert out["gics_sub_industry_code"].notna().all(), "unmatched GICS sub-industry"

for c in ["market_cap_usd", "ebitda_usd"]:
    out[c] = out[c].astype("Int64")

dst = ROOT / "data/cleaned/sp500-financials-cleaned.csv"
out.to_csv(dst, index=False)
print(f"{len(out)} rows, {out.shape[1]} columns -> {dst.relative_to(ROOT)}")
print("rows without any financial values:", int(out['share_price_usd'].isna().sum()))
