# FAIRness assessment - before and after

Scale: yes / partially / no. "Before" = the original DataHub file and its `datapackage.json`.
"After" = the FAIRified RDF data, its DCAT metadata records (published as RDF with w3id identifiers) and the w3id identifiers.

## Data

| Principle | Criterion | Before | After | Note |
|---|---|---|---|---|
| F1 | Globally unique identifier | partially | yes | Before: DataHub download URL, unique but not a PID. After: `w3id.org/.../group21/data`; every company and snapshot has its own URI |
| F1 | Persistent identifier | no | yes | w3id redirect (course relay, rules in `luizbonino/pid-relay`) decouples identifier from file location |
| F2 | Has metadata | yes | yes | |
| F2 | Has rich metadata | partially | yes | Before: title, description, column descriptions; no keywords, theme, date; `Sector` mis-described |
| F3 | Data identifier in metadata | partially | yes | Before: relative path `data/constituents-financials.csv` |
| F3 | Data identifier with clear predicate | no | yes | `dcat:downloadURL` |
| F4 | Indexed in a searchable resource | yes | partially | The original stays indexed on DataHub; the FAIRified version is in a public GitHub repository but not registered in a FAIR Data Point or catalogue |
| A1 | Resolution protocol | yes | yes | HTTPS |
| A1.1 | Open, free, universally implementable | yes | yes | HTTPS |
| A1.2 | Supports authentication/authorisation | yes | yes | Supported by HTTPS; not needed (public-domain data) |
| A2 | Metadata persist longer than data | no | partially | Metadata records are separate files with their own identifiers, but stored in the same repository as the data |
| I1 | Formal knowledge-representation language | no | yes | CSV with free-text headers -> RDF |
| I2 | FAIR vocabularies | no | yes | schema.org, SKOS, Dublin Core; own terms published under w3id |
| I3 | Qualified references to other data | no | partially | `rdfs:seeAlso` SEC EDGAR, `skos:broader` GICS hierarchy; no Wikidata links yet |
| R1 | Rich, accurate attributes | partially | yes | Units, datatypes and definitions in the ontology |
| R1.1 | Clear licence | yes | yes | Licence URI in metadata |
| R1.2 | Detailed provenance | partially | yes | Sources, snapshot date, `prov:wasDerivedFrom`, scripts |
| R1.3 | Domain community standards | partially | partially | GICS + schema.org; no finance ontology (FIBO) |

## Metadata

| Principle | Criterion | Before | After | Note |
|---|---|---|---|---|
| F1 | Globally unique identifier | no | yes | Before: `datapackage.json` has no identifier of its own. After: each metadata record has its own w3id IRI |
| F1 | Persistent identifier | no | yes | Each record has a w3id PID (`.../group21/metadata/dataset` etc.) |
| F2 | Rich metadata | partially | yes | DCAT dataset (14 properties) and 2 distributions (9 properties each) |
| F3 | Includes data identifier | partially | yes | `dcat:distribution`, `dcat:downloadURL` |
| F4 | Indexed | yes | no | Records are public on GitHub, but not registered in a FAIR Data Point or index |
| A1 / A1.1 | Standard open protocol | yes | yes | HTTPS |
| A2 | Available when data are gone | no | partially | Separate files with their own identifiers, but in the same repository as the data |
| I1 | Formal language | partially | yes | JSON (Frictionless) -> RDF |
| I2 | FAIR vocabularies | no | yes | DCAT 2, Dublin Core, PROV-O, FOAF, EU data themes |
| I3 | Qualified references | no | yes | `dct:source`, `prov:wasDerivedFrom`, `dct:conformsTo` |
| R1.1 | Licence | yes | yes | `dct:license` IRI |
| R1.2 | Provenance | partially | yes | Creator, publisher, sources, dates |
| R1.3 | Community standards | partially | yes | W3C DCAT validated with SHACL |
