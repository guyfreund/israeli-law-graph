LOAD CSV WITH HEADERS FROM 'file:///Nodes.csv' AS row
with row WHERE row.type = 'Law' 
MERGE (l:Law {title:row.title, law_uri:row.law_uri});

LOAD CSV WITH HEADERS FROM 'file:///Nodes.csv' AS row
with row WHERE row.type = 'Chapter' 
MERGE (l:Chapter {title:row.title, law_uri:row.law_uri});

LOAD CSV WITH HEADERS FROM 'file:///Nodes.csv' AS row
with row WHERE row.type = 'Point'
MERGE (l:Point {title:row.title, body:row.body, law_uri:row.law_uri});

LOAD CSV WITH HEADERS FROM 'file:///Nodes.csv' AS row
with row WHERE row.type = 'Section'
MERGE (l:Section {title:row.title, body:row.body, law_uri:row.law_uri});

LOAD CSV WITH HEADERS FROM 'file:///Nodes.csv' AS row
with row WHERE row.type = 'Part' 
MERGE (l:Part {title:row.title, law_uri:row.law_uri});

LOAD CSV WITH HEADERS FROM 'file:///Nodes.csv' AS row
with row WHERE row.type = 'Appendix' 
MERGE (l:Appendix {title:row.title, law_uri:row.law_uri});

LOAD CSV WITH HEADERS FROM 'file:///Nodes.csv' AS row
with row WHERE row.type = 'Preamble' 
MERGE (l:Preamble {title:row.title, law_uri:row.law_uri});

LOAD CSV WITH HEADERS FROM 'file:///Nodes.csv' AS row
with row WHERE row.type = 'Subtitle' 
MERGE (l:Subtitle {title:row.title, law_uri:row.law_uri});

LOAD CSV WITH HEADERS FROM 'file:///Nodes.csv' AS row
with row WHERE row.type = 'WrapUp' 
MERGE (l:WrapUp {title:row.title, law_uri:row.law_uri});

LOAD CSV WITH HEADERS FROM "file:///Edges.csv" AS row
WITH row WHERE row.type = 'סעיף של חוק'
MATCH (n1 {title: row.from_title, law_uri:row.from_law_uri}), (n2 {title: row.to_title, law_uri:row.to_law_uri})
MERGE (n1)-[:'סעיף של חוק']->(n2);

LOAD CSV WITH HEADERS FROM "file:///Edges.csv" AS row
WITH row WHERE row.type = 'תת-סעיף של סעיף'
MATCH (n1 {title: row.from_title, law_uri:row.from_law_uri}), (n2 {title: row.to_title, law_uri:row.to_law_uri})
MERGE (n1)-[:'תת-סעיף של סעיף']->(n2);

LOAD CSV WITH HEADERS FROM "file:///Edges.csv" AS row
WITH row WHERE row.type = 'הפנייה לחוק אחר'
MATCH (n1 {title: row.from_title, law_uri:row.from_law_uri}), (n2 {title: row.to_title, law_uri:row.to_law_uri})
MERGE (n1)-[:'הפנייה לחוק אחר']->(n2);

LOAD CSV WITH HEADERS FROM "file:///Edges.csv" AS row
WITH row WHERE row.type = 'הפנייה לסעיף של חוק אחר'
MATCH (n1 {title: row.from_title, law_uri:row.from_law_uri}), (n2 {title: row.to_title, law_uri:row.to_law_uri})
MERGE (n1)-[:'הפנייה לסעיף של חוק אחר']->(n2);

LOAD CSV WITH HEADERS FROM "file:///Edges.csv" AS row
WITH row WHERE row.type = 'הקדמה לחוק'
MATCH (n1 {title: row.from_title, law_uri:row.from_law_uri}), (n2 {title: row.to_title, law_uri:row.to_law_uri})
MERGE (n1)-[:'הקדמה לחוק']->(n2);

LOAD CSV WITH HEADERS FROM "file:///Edges.csv" AS row
WITH row WHERE row.type = 'סתמי'
MATCH (n1 {title: row.from_title, law_uri:row.from_law_uri}), (n2 {title: row.to_title, law_uri:row.to_law_uri})
MERGE (n1)-[:'סתמי']->(n2);
