import os
import time
import pandas as pd
from dotenv import load_dotenv
from neo4j import GraphDatabase
from scripts.benchmark_queries import QUERIES

load_dotenv()

driver = GraphDatabase.driver(
    os.getenv("COGNODB_URI"),
    auth=(
        os.getenv("COGNODB_USERNAME"),
        os.getenv("COGNODB_PASSWORD")
    )
)

results=[]

with driver.session(database="neo4j") as session:

    for name,query in QUERIES.items():

        start=time.perf_counter()

        session.run(query).consume()

        end=time.perf_counter()

        elapsed=(end-start)*1000

        print(name,round(elapsed,2),"ms")

        results.append([name,elapsed])

driver.close()

df=pd.DataFrame(results,columns=["Query","Execution_Time_ms"])

df.to_csv("results/cognodb_results.csv",index=False)

print(df)