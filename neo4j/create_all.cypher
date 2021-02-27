MATCH (n) DETACH DELETE n;

LOAD CSV WITH HEADERS FROM 'file:///Nodes.csv' AS row
with row WHERE row.type = 'Law' 
CREATE (l:Law {id:toInteger(row.Id), title:row.title, law_uri:row.law_uri});

LOAD CSV WITH HEADERS FROM 'file:///Nodes.csv' AS row
with row WHERE row.type = 'Chapter' 
CREATE (l:Chapter {id:toInteger(row.Id), title:row.title, law_uri:row.law_uri});

LOAD CSV WITH HEADERS FROM 'file:///Nodes.csv' AS row
with row WHERE row.type = 'Point'
CREATE (l:Point {id:toInteger(row.Id), title:row.title, body:row.body, law_uri:row.law_uri});

LOAD CSV WITH HEADERS FROM 'file:///Nodes.csv' AS row
with row WHERE row.type = 'Section'
CREATE (l:Section {id:toInteger(row.Id), title:row.title, body:row.body, law_uri:row.law_uri});

LOAD CSV WITH HEADERS FROM 'file:///Nodes.csv' AS row
with row WHERE row.type = 'Part' 
CREATE (l:Part {id:toInteger(row.Id), title:row.title, law_uri:row.law_uri});

LOAD CSV WITH HEADERS FROM 'file:///Nodes.csv' AS row
with row WHERE row.type = 'Appendix' 
CREATE (l:Appendix {id:toInteger(row.Id), title:row.title, law_uri:row.law_uri});

LOAD CSV WITH HEADERS FROM 'file:///Nodes.csv' AS row
with row WHERE row.type = 'Preamble' 
CREATE (l:Preamble {id:toInteger(row.Id), title:row.title, law_uri:row.law_uri});

LOAD CSV WITH HEADERS FROM 'file:///Nodes.csv' AS row
with row WHERE row.type = 'Subtitle' 
CREATE (l:Subtitle {id:toInteger(row.Id), title:row.title, law_uri:row.law_uri});

LOAD CSV WITH HEADERS FROM 'file:///Nodes.csv' AS row
with row WHERE row.type = 'WrapUp' 
CREATE (l:WrapUp {id:toInteger(row.Id), title:row.title, law_uri:row.law_uri});

LOAD CSV WITH HEADERS FROM "file:///Edges.csv" AS row
WITH row WHERE row.type = 'סעיף של חוק'
MATCH (n1 {id: toInteger(row.from_id)}), (n2 {id: toInteger(row.to_id)})
create (n1)-[:`סעיף של חוק`]->(n2);

LOAD CSV WITH HEADERS FROM "file:///Edges.csv" AS row
WITH row WHERE row.type = 'תת-סעיף של סעיף'
MATCH (n1 {id: toInteger(row.from_id)}), (n2 {id: toInteger(row.to_id)})
create (n1)-[:`תת-סעיף של סעיף`]->(n2);

LOAD CSV WITH HEADERS FROM "file:///Edges.csv" AS row
WITH row WHERE row.type = 'הפנייה לחוק אחר'
MATCH (n1 {id: toInteger(row.from_id)}), (n2 {id: toInteger(row.to_id)})
create (n1)-[:`הפנייה לחוק אחר`]->(n2);

LOAD CSV WITH HEADERS FROM "file:///Edges.csv" AS row
WITH row WHERE row.type = 'הפנייה לסעיף של חוק אחר'
MATCH (n1 {id: toInteger(row.from_id)}), (n2 {id: toInteger(row.to_id)})
create (n1)-[:`הפנייה לסעיף של חוק אחר`]->(n2);

LOAD CSV WITH HEADERS FROM "file:///Edges.csv" AS row
WITH row WHERE row.type = 'הקדמה לחוק'
MATCH (n1 {id: toInteger(row.from_id)}), (n2 {id: toInteger(row.to_id)})
create (n1)-[:`הקדמה לחוק`]->(n2);

LOAD CSV WITH HEADERS FROM "file:///Edges.csv" AS row
WITH row WHERE row.type = 'סתמי'
MATCH (n1 {id: toInteger(row.from_id)}), (n2 {id: toInteger(row.to_id)})
create (n1)-[:`סתמי`]->(n2);

MATCH (n) Remove n.id;
