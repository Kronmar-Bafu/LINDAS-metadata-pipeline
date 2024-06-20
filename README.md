# LINDAS-metadata-pipeline
A simple python script which transforms the metadata description of a dataset entered into a  corresponding yaml file and transforms it into RDF triples which conform to the LINDAS Governance rules and the required opendata.swiss metadata.

## Instructions
Fill information into the yaml files as instructed by the comments.  
If only LINDAS metadata is needed, the ODS file can be ignored or left empty.  
Opendata.swiss metadata will only be written if the ODS yaml file contains a value for the identifier.  

Execute the python file in the same folder as the two yaml files. Warnings will be displayed for missing or incorrectly formatted data.  
A turtle file (named according to the dataset name) will be saved in the same folder.  
If the data has to be adjusted simply rerun the script to overwrite the turtle file.  

## Dependencies
Python Modules
- RDFlib
- yaml
- datetime
- dateutil

To install these requirements, you can use `pip install -r requirements.txt`
