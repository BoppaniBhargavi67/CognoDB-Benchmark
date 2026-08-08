# Benchmark Cypher Queries

QUERIES = {
    "point_lookup": """
        MATCH (p:Page {id: $id})
        RETURN p
""",
    "indexed_lookup": """
    MATCH (p:Page {page_type: $page_type})
    RETURN count(p) AS total
""",

    "one_hop": """
        MATCH (p:Page {id: $id})-[:LINKS_TO]->(n)
        RETURN count(n) AS neighbors
""",

    "two_hop": """
        MATCH (p:Page {id: $id})-[:LINKS_TO]->()-[:LINKS_TO]->(n)
        RETURN count(n) AS neighbors
""",

    "three_hop": """
        MATCH (p:Page {id: $id})
        -[:LINKS_TO]->()
        -[:LINKS_TO]->()
        -[:LINKS_TO]->(n)
        RETURN count(n) AS neighbors
""",

    "aggregation": """
        MATCH (p:Page)
        RETURN p.page_type AS page_type,
               count(*) AS total
    """
}
