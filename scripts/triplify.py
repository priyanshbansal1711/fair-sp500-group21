"""Steps 5a/6a - apply the semantic data model and make the data linkable.

Produces
  * ontology/group21-ont.ttl and .owl : the mini ontology + the GICS concept scheme
  * data/rdf/sp500-financials.ttl     : the FAIRified dataset

Usage:  python scripts/triplify.py      (requires: pip install rdflib pandas)
"""
from pathlib import Path
import pandas as pd
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import DCTERMS, OWL, RDF, RDFS, SKOS, XSD

ROOT = Path(__file__).resolve().parent.parent
ONT = Namespace("https://w3id.org/FAIR-course-UT/2026/group21/ont#")
DATA = Namespace("https://w3id.org/FAIR-course-UT/2026/group21/data#")
SCHEMA = Namespace("https://schema.org/")
PROV = Namespace("http://www.w3.org/ns/prov#")

SNAPSHOT_DATE = "2026-10-23"   # 'last updated' date of the file on DataHub
RETRIEVED = "2026-10-24"


def bind(g):
    for p, ns in [("ont", ONT), ("data", DATA), ("schema", SCHEMA), ("skos", SKOS),
                  ("dct", DCTERMS), ("owl", OWL), ("xsd", XSD), ("prov", PROV)]:
        g.bind(p, ns)
    return g


# ---------------------------------------------------------------- ontology
ont = bind(Graph())
ont.parse(ROOT / "scripts/ontology-core.ttl")
gics = pd.read_csv(ROOT / "data/cleaned/gics-structure.csv", dtype=str)
levels = [("sector", ONT.GICSSector, None),
          ("industry_group", ONT.GICSIndustryGroup, "sector"),
          ("industry", ONT.GICSIndustry, "industry_group"),
          ("sub_industry", ONT.GICSSubIndustry, "industry")]
for _, r in gics.iterrows():
    for lvl, cls, parent in levels:
        c = ONT[f"gics-{r[lvl + '_code']}"]
        ont.add((c, RDF.type, cls))
        ont.add((c, RDF.type, SKOS.Concept))
        ont.add((c, SKOS.prefLabel, Literal(r[lvl], lang="en")))
        ont.add((c, SKOS.notation, Literal(r[lvl + "_code"])))
        ont.add((c, SKOS.inScheme, ONT.GICS))
        if parent:
            ont.add((c, SKOS.broader, ONT[f"gics-{r[parent + '_code']}"]))
        else:
            ont.add((ONT.GICS, SKOS.hasTopConcept, c))
ont.serialize(ROOT / "ontology/group21-ont.ttl", format="turtle")
ont.serialize(ROOT / "ontology/group21-ont.owl", format="xml")

# ---------------------------------------------------------------- data
df = pd.read_csv(ROOT / "data/cleaned/sp500-financials-cleaned.csv",
                 dtype={"gics_sub_industry_code": str})
g = bind(Graph())
measures = {
    "share_price_usd": ONT.sharePrice,
    "price_earnings_ratio": ONT.priceEarningsRatio,
    "dividend_yield": ONT.dividendYield,
    "earnings_per_share_usd": ONT.earningsPerShare,
    "market_cap_usd": ONT.marketCapitalization,
    "ebitda_usd": ONT.ebitda,
}
for _, r in df.iterrows():
    co = DATA[f"company-{r.ticker}"]
    g.add((co, RDF.type, SCHEMA.Corporation))
    g.add((co, SCHEMA.name, Literal(r["name"])))
    g.add((co, SCHEMA.tickerSymbol, Literal(r.ticker)))
    g.add((co, ONT.hasGICSSubIndustry, ONT[f"gics-{r.gics_sub_industry_code}"]))
    g.add((co, RDFS.seeAlso, URIRef(r.sec_filings_url)))

    if r[list(measures)].notna().any():
        sn = DATA[f"snapshot-{r.ticker}-{SNAPSHOT_DATE}"]
        g.add((co, ONT.hasFinancialSnapshot, sn))
        g.add((sn, RDF.type, ONT.FinancialSnapshot))
        g.add((sn, ONT.snapshotOf, co))
        g.add((sn, DCTERMS.date, Literal(SNAPSHOT_DATE, datatype=XSD.date)))
        g.add((sn, SCHEMA.priceCurrency, Literal("USD")))
        for col, prop in measures.items():
            v = r[col]
            if pd.notna(v):
                lex = str(int(v)) if col in ("market_cap_usd", "ebitda_usd") else repr(float(v))
                g.add((sn, prop, Literal(lex, datatype=XSD.decimal)))

g.serialize(ROOT / "data/rdf/sp500-financials.ttl", format="turtle")
print(f"ontology: {len(ont)} triples; data: {len(g)} triples, "
      f"{len(set(g.subjects(RDF.type, SCHEMA.Corporation)))} companies, "
      f"{len(set(g.subjects(RDF.type, ONT.FinancialSnapshot)))} snapshots")
