MATCH (n: Preamble)
WITH n
MATCH p=(n)-[r: `הקדמה לחוק`]->()
WITH count(r) as cntr, n
WHERE cntr>2
WITH n
MATCH p=(n)-[: `הפנייה לחוק אחר`]->()
RETURN p LIMIT 50
