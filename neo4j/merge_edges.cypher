LOAD CSV WITH HEADERS FROM "file:///Edges.csv" AS row
WITH row WHERE row.type = 'סעיף של חוק'
MATCH (n1 {title: row.from_title, law_uri:row.from_law_uri}), (n2 {title: row.to_title, law_uri:row.to_law_uri})
MERGE (n1)-[:`סעיף של חוק`]->(n2);

LOAD CSV WITH HEADERS FROM "file:///Edges.csv" AS row
WITH row WHERE row.type = 'תת-סעיף של סעיף'
MATCH (n1 {title: row.from_title, law_uri:row.from_law_uri}), (n2 {title: row.to_title, law_uri:row.to_law_uri})
MERGE (n1)-[:`תת-סעיף של סעיף`]->(n2);

LOAD CSV WITH HEADERS FROM "file:///Edges.csv" AS row
WITH row WHERE row.type = 'הפנייה לחוק אחר'
MATCH (n1 {title: row.from_title, law_uri:row.from_law_uri}), (n2 {title: row.to_title, law_uri:row.to_law_uri})
MERGE (n1)-[:`הפנייה לחוק אחר`]->(n2);

LOAD CSV WITH HEADERS FROM "file:///Edges.csv" AS row
WITH row WHERE row.type = 'הפנייה לסעיף של חוק אחר'
MATCH (n1 {title: row.from_title, law_uri:row.from_law_uri}), (n2 {title: row.to_title, law_uri:row.to_law_uri})
MERGE (n1)-[:`הפנייה לסעיף של חוק אחר`]->(n2);

LOAD CSV WITH HEADERS FROM "file:///Edges.csv" AS row
WITH row WHERE row.type = 'הקדמה לחוק'
MATCH (n1 {title: row.from_title, law_uri:row.from_law_uri}), (n2 {title: row.to_title, law_uri:row.to_law_uri})
MERGE (n1)-[:`הקדמה לחוק`]->(n2);

LOAD CSV WITH HEADERS FROM "file:///Edges.csv" AS row
WITH row WHERE row.type = 'סתמי'
MATCH (n1 {title: row.from_title, law_uri:row.from_law_uri}), (n2 {title: row.to_title, law_uri:row.to_law_uri})
MERGE (n1)-[:`סתמי`]->(n2);
