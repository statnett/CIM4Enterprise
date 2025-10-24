**Description**

`CimToBsddTransformer.py` is a command line app to create bSDD dictionary from CIM ontology in GraphDB repository. The resulting dictionary is stored in `/../../cim-bsdd.json` after installing dependencies and running the script with arguments in this directory.

**To install dependencies**:

1. Create Python=>3.10 virtual environment in this directory
2. activate the virtual environment
3. run `pip install -r requirements.txt`

**To produce CIM bSDD**:

run `python CimToBsddTransformer.py -gdb {graphDB URL} -u {username} -p {passowrd} -r {repository na,e}`



