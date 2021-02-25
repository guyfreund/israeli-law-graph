# LawGraph
#### Generates a Graph that maps laws and their references.
This repository is the implementation of a final project in Digital Science course taken by Guy Freund & David Ziegler from Ben-Gurion University.
This project is in jointly guided by the Ben-Gurion University and the Israeli. Ministry of Justice

חוקים מפנים פעמים רבות לחוקים אחרים, מסיבות שונות (לעתים סעיף מפנה לחוק אחר באופן כללי, ולעתים סעיף מפנה ישירות לסעיף מסוים בחוק אחר). המשימה היא יצירת מפת קשרים של כלל ההפניות בין חוקים, יחד עם מידע על סוג ההפניה (תיקון של סעיף בחוק אחר, הפניה להגדרה שנמצאת בחוק אחר, הסתמכות על הוראה שמופיעה בחוק אחר וכו').



The project's goal is to create a mapping of all the law's in the Israeli legalisation. The data being used is given by the Ministry of Justice.

## Database Format
Each law is structured by an XML file in [AKN format](http://docs.oasis-open.org/legaldocml/ns/akn/3.0) contains several `ref` elements. Each `ref` element contains a string reference that point to a law and to a specific element nested in the law's XML file.

This program creates the graph from a law's database. Each law's path is of the `$LAW_GRAPH_REPO_ROOT/akn/il/$LEG_TYPE/$DATE/$FRBRWORKURI/he@/main.xml` format, where:
- `$LAW_GRAPH_REPO_ROOT` is the root of the `LawGraph` repository.
- `$LEG_TYPE` is the type of legalisation. Currently: PrimaryLegislation, SecondaryLegislation or PrimaryOrSecondaryLegislation.
- `$DATE` is a date of format YYYY-MONTH-DAY.
- `$FRBRWORKURI` the element's value stored in each law in path `akomaNtoso/act/meta/identification/FRBRWork/FRBRthis/FRBRuri`

## Graph Creation Logic:
- For each reference: `from_law, from_vertex, to_law & to_vertex` vertexes are created. `from_law => from_vertex, from_vertex => to_vertex, to_law => to_vertex` edges are created.
![Alt text](graph_logic.jpg?raw=true "Title")


## Repository's Files:
- `generate_graph.py`: Generates the Pythonic graph.
- `classes.py`: Contains all Python Classes used across the program.
- `utils.py`: Gathers all util functions used to build the Pythonic graph.
- `constans.py`: Gathers all constants used to build the Pythonic graph.
- `error.py`: Contains all error handling functions.
- `errors.json`: The errors file, contains 5 different types errors and is being built during runtime.
- `law_graph_logs.log`: The log file. The program logs to this file during runtime.
- `requirements.txt`: The requirements file. To install all the program's dependencies run: `pip install -r requirements.txt`.
- `validate_class_uniqueness.py`: Validates that all class's elements can be 1to1 identified. 
- `validate_graph.py`: Validates the graph correctness.
