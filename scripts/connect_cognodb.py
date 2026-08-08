from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Read credentials
URI = os.getenv("COGNODB_URI")
USERNAME = os.getenv("COGNODB_USERNAME")
PASSWORD = os.getenv("COGNODB_PASSWORD")

# Create driver
driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)

try:
    # Open a session
    with driver.session(database="neo4j") as session:

        # Run a simple Cypher query
        result = session.run("RETURN 'Connected to CognoDB Successfully!' AS message")

        # Print result
        print(result.single()["message"])

    print("Database connection successful!")

except Exception as e:
    print("Connection Failed!")
    print(e)

finally:
    driver.close()