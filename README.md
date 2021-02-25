# LawGraph
#### A mapping of the Israeli legalisation.
This repository is the implementation of a final project in Digital Sciences course taken by Guy Freund & David Ziegler from The department of Computer Science, Ben-Gurion University, Israel.
This project is in jointly guided by the Ben-Gurion University and the Israeli Ministry of Justice.
The project's goal is to create a mapping of all the law's in the Israeli legalisation. The data being used is given by the Israeli Ministry of Justice.

## Database Format
Each law is structured as an XML file in [AKN format](http://docs.oasis-open.org/legaldocml/ns/akn/3.0) and contains several `ref` elements. Each `ref` element contains a string reference that points to a specific law and to a specific element nested in the this law's XML file. Each such `ref` element represents a connection between law, such as:
- Amendment of a section in another law
- Reference to a definition contained in another law
- Reliance on a provision appearing in another law

This program creates the graph from a law's database. Each law's path is of the `$LAW_GRAPH_REPO_ROOT/akn/il/$LEG_TYPE/$DATE/$FRBRWORKURI/he@/main.xml` format, where:
- `$LAW_GRAPH_REPO_ROOT`: The root of the LawGraph repository.
- `$LEG_TYPE`: The type of legalisation. Currently: PrimaryLegislation, SecondaryLegislation or PrimaryOrSecondaryLegislation.
- `$DATE`: A date of format YYYY-MM-DD.
- `$FRBRWORKURI`: The element's value stored in each law in path `akomaNtoso/act/meta/identification/FRBRWork/FRBRthis/FRBRuri`.

## Graph Creation Logic:
- For each reference: from_law, from_vertex, to_law & to_vertex vertexes are created. from_law => from_vertex, from_vertex => to_vertex, to_law => to_vertex edges are created.
<img src=https://github.com/guyfreund/LawGraph/blob/master/graph_logic.jpg width=600>


## Neo4j Implementation:
@TODO: elaborate on what we did.

#### Spinning up the database: Method 1
@TODO: elaborate on how to spin up.

#### Spinning up the database: Method 2
@TODO: elaborate on how to spin up.

#### Spinning up the database: Method 3
@TODO: elaborate on how to spin up.


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


## Running the Program:
1. Install Python (version>=3.9.0)
2. @TODO: Add Neo4j installation insturctions.
3. Run: `pip install -r requirements.txt`
4. @TODO: Add running the program instructions (in the main way out of the 3 possible).

