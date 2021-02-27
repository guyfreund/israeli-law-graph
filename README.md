# LawGraph
#### A mapping of the Israeli legalisation.
This repository is the implementation of a final project in Digital Sciences course taken by Guy Freund & David Ziegler from The department of Computer Science, Ben-Gurion University, Israel.
This project is jointly guided by the Ben-Gurion University and the Israeli Ministry of Justice.
The project's goal is to create a mapping of all the laws in the Israeli legalisation. The data being used is given by the Israeli Ministry of Justice.

## Database Format
Each law is structured as an XML file in [AKN format](http://docs.oasis-open.org/legaldocml/ns/akn/3.0) and contains several ref elements. Each ref element stores a string reference that points to a specific law and to a specific element nested in the this law's XML file. Each such ref element represents a connection between law, such as:
- Amendment of a section in another law
- Reference to a definition contained in another law
- Reliance on a provision appearing in another law

This program creates the graph from the Israeli Ministry of Justice's database that contains all the laws. Each law's path is of the `$LAW_GRAPH_REPO_ROOT/akn/il/$LEG_TYPE/$DATE/$FRBRWORKURI/he@/main.xml` format, where:
- `LAW_GRAPH_REPO_ROOT`: The root of the LawGraph repository.
- `LEG_TYPE`: The type of legalisation. Currently: PrimaryLegislation, SecondaryLegislation or PrimaryOrSecondaryLegislation.
- `DATE`: A date of format YYYY-MM-DD.
- `FRBRWORKURI`: The element's value stored in each law in path `akomaNtoso/act/meta/identification/FRBRWork/FRBRthis/FRBRuri`.

## Graph Creation Logic:
For each reference: from_law, from_vertex, to_law & to_vertex vertexes are created. from_law => from_vertex, from_vertex => to_vertex, to_law => to_vertex edges are created.

<img src=https://github.com/guyfreund/LawGraph/blob/master/graph_logic.jpg width=600>


## Neo4j Implementation:

#### Spinning up the database: Method 1
For automatic upload to neo4j, use the following command options:
"-auto <username> <password> <url:port>"
Url and port are optional, if not specified, "bolt://localhost:7687" will be used.

#### Spinning up the database: Method 2
Create Nodes.csv and Edges.csv files, copy them into the DB 'Import' folder, 
and run 'create_all.cypher' to load them into the DB.
Notice that nodes have ID used for connecting relationships, than the IDs are removed.
To use this method execute using the following command options:
"-csv"

#### Spinning up the database: Method 3
Create Nodes.csv and Edges.csv files, copy them into a newly created DB 'Import' folder. 
Run the command in the 'command' file in the DB's Terminal.
To use this method execute using the following command options:
"--csv-import"

## Repository's Files:
- `generate_graph.py`: Generates the Pythonic graph.
- `classes.py`: Contains all Python Classes used across the program.
- `utils.py`: Gathers all util functions used to build the Pythonic graph.
- `constans.py`: Gathers all constants used to build the Pythonic graph.
- `error.py`: Contains all error handling functions.
- `errors.json`: The errors file, contains 5 different types errors and is being built during runtime.
- `law_graph_logs.log`: The log file. The program logs to this file during runtime.
- `requirements.txt`: The requirements file.
- `validate_class_uniqueness.py`: Validates that all class's elements can be 1to1 identified. 
- `validate_graph.py`: Validates the graph correctness.


- `neo4j` : Folder with Cyphers and import command.
  - `command` : Import command to be used in a DB terminal to import csv files.
  - `create_all.cypher` : Run delete_all, create_nodes, create_edges, remove_id in a row.
  - `create_edges.cypher` : Create relationships from csv file.
  - `create_nodes.cypher` : Create nodes from csv file.
  - `delete_all.cypher` : Delete all nodes and relationships from DB.
  - `merge_all.cypher` : Merge data from Nodes.csv and Edges.csv into DB.
  - `merge_edges.cypher` : Merge Edges.csv into DB.
  - `merge_nodes.cypher` : Merge Nodes.csv into DB.
  - `remove_id.cypher` : Remove ID property from all objects in DB.
  - `example1_preambles_with_references_to_other_laws.cypher` : Example Cypher query. Find all Preambles that reference laws other than the one the belong to.
  - `example2_nodes_with_no_in_edges.cypher` : Example Cypher query. Find all nodes that has no incoming relationships.


## Running the Program:
1. Install Python (version>=3.9.0)
2. Download neo4j https://neo4j.com/download/?ref=try-neo4j-lp
3. Run: `pip install -r requirements.txt`
4. Follow preferred method from above.

