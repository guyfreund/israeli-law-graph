MATCH (n)
WHERE NOT ()-[]->(n)
RETURN n limit 50

