
geoweaver_cwl
=============
geoweaver_cwl is a python tool wrapper for translating Geoweaver AI - workflows into Common Workflow Language (CWL). CWL is an open standard for describing how to run command-line tools and connect them to create workflows. Tools and workflows described using CWL are portable across a variety of platforms that support the CWL standards. Researchers who are using Geoweaver can use it to translate their workflows and get the formatted CWL files for the existing workflows.

The code is written in Python 3.

Installation
=========
For installation use the following command:

    pip install geoweaver_cwl


Example Usage
=============
Import the package

    from geoweaver_cwl import translator as tr

The json file will be converted to CWL format using generate_cwl function. It will also create a subdirectory called elementary_cwl_files, which will translate all the python files used in the workflow to CWL.

    tr.generate_cwl('workflow.json')


The output should look like this and you should be able to see a workflow.cwl file and elementary_cwl_files in the folder:

    Output file: workflow.cwl
    Writing header...
    Writing steps...
    CWL file written to workflow.cwl

The generate_yml function produces a YML file, which you should see in the exiting directory.
*Note: specify the name you want to give to your yml file in the function; in our example, we've called it "input."

    tr.generate_yml('input.yml')

The output should look like this and you should be able to see a YML file in the folder:
    
    Writing YML file...
    YML file created ...

