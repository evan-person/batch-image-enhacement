import argparse
import os
import cv2
import importlib
from functools import reduce
import json
import importlib

# ARGUMENTS
parser = argparse.ArgumentParser(description='Summary script')
parser.add_argument("--pipeline", type=str, default=None)
parser.add_argument("--input_directory", type=str, default=None)
parser.add_argument("--output_directory", type=str, default=None)
parser.add_argument("--verbose", type=bool, default=False)
args = parser.parse_args()


# ERROR MESSAGES
if args.pipeline == None:
    print("Please specify an input json file")
    exit()

if args.input_directory == None:
    print("Please specify an input directory")
    exit()

if args.output_directory == None:
    print("Please specify an output directory")
    exit()

verbose_mode = args.verbose

# MAIN
with open(args.pipeline) as jsonFile:
    pipeline_json = json.load(jsonFile)
    jsonFile.close()

#set up script to go through directory of images
input_directory = args.input_directory
output_directory = args.output_directory

files = os.listdir(input_directory)

#check if output directory exists, if not create it
if not os.path.exists(output_directory):
    os.makedirs(output_directory)


#check if input directory exists, if not exit
if not os.path.exists(input_directory):
    print("Input directory does not exist")
    exit()

#check if compute_statistics_before flag in pipeline is true
if pipeline_json['compute_statistics_before'] == True:
    #compute statistics
    print("this is not yet implemented...")
   
#dynamic import of modules
steps = []
params = []
for step in pipeline_json['steps']:
    module = step['name']
    #import module from src folder modules.py file

    modules = importlib.import_module('src.processing')
    #use getattr to get the function from the modules as a function with the string name of the module being imported
    module = getattr(modules, module)

    # if step['params'] != None:
    #     module = module(**step['params'])
    params.append(step['params'])
    steps.append(module)

# img = cv2.imread(input_directory + '/' + files[0])
# step[0](img, **params[0], params[1])

# build pipeline using functool reduce
def apply_step(img, step_with_params):
    step, params = step_with_params
    return step(img, **params[0])

def pipeline(img):
    return reduce(apply_step, zip(steps, params), img)


#loop through files in directory
for file in files:
    if os.path.isfile(input_directory + '/' + file):
        #read in the image and go through processing steps
        img = cv2.imread(input_directory + '/' + file)

        output_img = pipeline(img)

        new_filename = file.split('.')[0] + '_processed.jpg'
        cv2.imwrite(os.path.join(output_directory,new_filename), output_img)

        if verbose_mode:
            print("Processed image: " + file)
        





#check if compute_statistics_after flag in pipeline is true
if pipeline_json['compute_statistics_after'] == True:
    #compute statistics
    print("this is not yet implemented...")
   
