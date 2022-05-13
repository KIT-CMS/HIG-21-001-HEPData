#! /usr/bin/env python3

import yaml
import copy
import json
import os
import ROOT as r


r.EnableImplicitMT()
from argparse import ArgumentParser

# Parsing arguments
parser = ArgumentParser(
    description="Script to create HEPData .yaml file from 1D VLQ likelihood scans from .json files."
)
parser.add_argument(
    "--inputs", required=True, nargs="+", help="A list of 1D VLQ likelihood scans .json files, in the format filename:categorization"
)
parser.add_argument(
    "--output-file", required=True, help="Basename of the output .yaml file"
)
parser.add_argument(
    "--output-directory",
    required=True,
    help="Main output directory name for submission to HEPData",
)
parser.add_argument(
    "--x-quantity", required=True, help="Label:units of the x-axis quantity"
)
parser.add_argument(
    "--mass-hypothesis", required=True, type=float, help="Float number for mass hypothesis"
)
parser.add_argument(
    "--additional-qualifiers", nargs="*", help="A list of additional qualifiers, given as name:value. Default: %(default)s", default=[]
)
# Assuming, that deltaNLL is contained in the file as y-axis quantity


args = parser.parse_args()
x_label, x_units = args.x_quantity.split(":")

# Setting up templates
scan_vlq_1D_template_main = {
    "dependent_variables": [],
    "independent_variables": [],
}

scan_vlq_1D_template_individual = {
    "header": {},
    "qualifiers": [
        {"name": r"Centre-of-mass energy $\sqrt{s}$", "units": "GeV", "value": 13000},
        {"name": r"Integrated luminosity", "units": "fb$^{-1}$", "value": 138},
        {"name": r"Mass hypothesis", "units": "TeV", "value": args.mass_hypothesis},
    ],
    "values": [],
}

for q in args.additional_qualifiers:
    name,value = q.split(":")
    scan_vlq_1D_template_individual["qualifiers"].append({"name": name, "value": value})

# Setup directory if it does not exist
if not os.path.isdir(args.output_directory):
    os.path.makedirs(args.output_directory)

# Obtain desired information from .json files
inputs_dict = {}

for inputname in args.inputs:
    fname, category = inputname.split(":")
    inputs_dict[category] = json.load(open(fname, "r"))

xcat = [k for k in inputs_dict.keys()][0]

# Setting up the .yaml file dict
output = copy.deepcopy(scan_vlq_1D_template_main)

## Include x quantity
x = copy.deepcopy(scan_vlq_1D_template_individual)
x.pop("qualifiers")
x["header"]["name"] = x_label
x["header"]["units"] = x_units
x["values"] = [{"value": float(val)} for val in inputs_dict[xcat].keys()]
output["independent_variables"].append(x)

## Include deltaNLL
for categorization in inputs_dict:
    dNLL = copy.deepcopy(scan_vlq_1D_template_individual)
    dNLL["qualifiers"].append({"name": r"Categorization", "value": categorization})
    dNLL["header"]["name"] = r"$-\Delta\ln\mathcal{L}$"
    dNLL["header"]["units"] = ""
    dNLL["values"] = [{"value": float(val["deltaNLL"])} for val in inputs_dict[categorization].values()]
    output["dependent_variables"].append(dNLL)

with open(os.path.join(args.output_directory, args.output_file), "w") as out:
    yaml.dump(output, out)
