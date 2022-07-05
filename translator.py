import os
import sys
import json

#creating folder for elementary CWL files
cwl_folder = 'elementary_cwl_files/'
code_folder = 'code/'
process_path = os.path.basename(code_folder) + '/'
yml_path = os.path.basename(cwl_folder) + '/'

#capturing path for elementary_cwl_files folder
if not os.path.exists(cwl_folder):
    os.makedirs(cwl_folder)

#input_key is the input parameter passed to the elementary CWL files
input_key = 'reference_file'

#input_value is the input parameter passed to the workflow.cwl 
input_value = 'reference'

#creating global variable for position in elementary files
position = 1


#creating YML file
def generate_yml(yml_file):
    print('Writing YML file...')
    with open(yml_file, 'w') as f:
        f.write(input_value + ':\n')
        f.write('  class: Directory\n')
        f.write('  path: ' + yml_path)
    print('YML file created ...')


#get_workflow_name will pull out the name from workflow.json
def get_workflow_name(json_file):
    
    with open(json_file) as f:
        json_var = json.load(f)
        
    return json_var['name']

#generating workflow.cwl
def generate_cwl(input_file):
    
    workflow_name = get_workflow_name(input_file)
    
    output_file = input_file.split('.')[0] + '.cwl'
    print('Output file:', output_file)
    
    print('Writing header...')
    write_header(output_file, workflow_name)
    print('Writing steps...')
    write_steps(input_file, output_file)
    
    print('CWL file written to', output_file)

#writing header for workflow.cwl 
def write_header(output_file, workflow_name):
    
    with open(output_file, 'w') as f:
        f.write('#!/usr/bin/env cwl-runner\n\n')
        f.write('cwlVersion: v1.0\n')
        f.write('class: Workflow\n')
        f.write('label: "' + workflow_name +'"\n\n')
        f.write('inputs:\n')
        f.write('  ' + input_value + ':\n')
        f.write('    type: Directory\n')
        f.write('    doc: Geoweaver workflow\n\n')
        f.write('outputs: []\n\n')
        f.write('steps: \n')


#creating elementary file header
def write_elementary_header(output_file):
    
    with open(output_file, 'w') as f:
        f.write('#!/usr/bin/env cwl-runner\n\n')
        f.write('class: CommandLineTool\n\n')
        f.write('cwlVersion: v1.0\n\n')


#writing steps in workflow.cwl by capturing the edges from workflow.json which is considered as process name
def write_steps(input_file, output_file):
    
    edges = get_edges(input_file)
    process_list = get_process_list(edges)
    
    
    with open(output_file, 'a') as f:
        for process in process_list:
            num_spaces = 2
            write_spaces(f, num_spaces)
            f.write(process + ':\n')
            num_spaces += 2
            write_spaces(f, num_spaces)
            f.write('run: ' + cwl_folder + process + '.cwl' + '\n')
            write_spaces(f, num_spaces)
            f.write('in:\n')
            num_spaces += 2
            write_spaces(f, num_spaces)
            f.write(input_key + ': ' + input_value + '\n')
            num_spaces -= 2
            write_spaces(f, num_spaces)
            f.write('out: []\n')
            
            create_elementary_file(process)



#creating elementary files body (calling the process name)
def create_elementary_file(process_name):
    
    global position
    
    file_name = cwl_folder + process_name + '.cwl'
    write_elementary_header(file_name)
    with open(file_name, 'a') as f:
        f.write('baseCommand: ["python", "'+ process_path + process_name + '.py"]\n\n')
        f.write('inputs:\n')
        f.write('  ' + input_key + ':\n')
        f.write('    type: Directory\n')
        f.write('    inputBinding:\n')
        f.write('      position: '+ str(position) +'\n')
        position += 1
        f.write('      prefix: --Output--\n\n')
        f.write('outputs: []\n\n')


def write_spaces(file_obj, num_spaces):
        for s in range(num_spaces):
            file_obj.write(' ')

#extracting the edges from json file
def get_edges(json_file):
    
    with open(json_file) as f:
        json_var = json.load(f)
    
    edges = json.loads(json_var['edges'])
    
    return edges

#writing the process name 
def get_process_list(edges):
    
    process_list, target_list = [], []
    for edge in edges:
        src_name = edge['source']['title']
        tgt_name = edge['target']['title']
        
        if src_name not in process_list:
            process_list.append(src_name)
            
        if src_name in target_list:
            target_list.remove(src_name)
                
        if tgt_name not in target_list:
            target_list.append(tgt_name)
            
    process_list += target_list
        
    return process_list


