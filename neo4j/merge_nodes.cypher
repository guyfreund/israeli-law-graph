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

