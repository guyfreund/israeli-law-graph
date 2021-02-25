# LawGraph

#### Generates a Graph that maps laws and their references.
---

Each law is structured by an XML file in [AKN format](http://docs.oasis-open.org/legaldocml/ns/akn/3.0) contains several `ref` elements. Each `ref` element contains a string reference that point to a law and to a specific element nested in the law's XML file.

This program creates the graph from a law's database. Each law's path is of the `$LAW_GRAPH_REPO_ROOT/akn/il/$LEG_TYPE/$DATE/$FRBRWORKURI/he@/main.xml` format, where:
- `$LAW_GRAPH_REPO_ROOT` is the root of the `LawGraph` repository.
- `$LEG_TYPE` is the type of legalisation. Currently: PrimaryLegislation, SecondaryLegislation or PrimaryOrSecondaryLegislation.
- `$DATE` is a date of format YYYY-MONTH-DAY.
- `$FRBRWORKURI` the element's value stored in each law in path `akomaNtoso/act/meta/identification/FRBRWork/FRBRthis/FRBRuri`

#### The logic to create a reference:
- For each reference: `from_law, from_vertex, to_law & to_vertex` vertexes are created. `from_law => from_vertex, from_vertex => to_vertex, to_law => to_vertex` edges are created.
![Alt text](graph_logic.jpg?raw=true "Title")
