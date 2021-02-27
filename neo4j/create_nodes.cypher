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

