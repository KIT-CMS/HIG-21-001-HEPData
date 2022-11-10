#! /usr/bin/env python3

import yaml
import copy
import json
import os
import ROOT as r
import numpy as np


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
parser.add_argument(
    "--max-deltaNLL", type=float, help="Maximim value of deltaNLL, that at least one category should not exceed too much. Default: %(default)s", default=12.0
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

# Adjust inputs to a proper range

range_indices_per_category = []
for data in inputs_dict.values():
    indices_above_margin = [ i for i, x in enumerate(data.values()) if x["deltaNLL"] and float(x["deltaNLL"]) >= 12]
    if indices_above_margin:
        range_indices_per_category.append(min(indices_above_margin)+1)
    else:
        range_indices_per_category.append(len(list(data.values())))

range_index = max(range_indices_per_category) if range_indices_per_category else -1

xcat = [k for k in inputs_dict.keys()][0]

# Setting up the .yaml file dict
output = copy.deepcopy(scan_vlq_1D_template_main)


x_values = [float(val) for val in inputs_dict[xcat].keys()][:range_index]
print(f"{x_label} range: {min(x_values)}, {max(x_values)}; number of points: {len(x_values)}")

x_width = (max(x_values) - min(x_values)) / (len(x_values) -1)
x_exponent = np.log10(x_width)

# Assuming, width is smaller than 1
x_precision = int(np.ceil(abs(x_exponent) + 1))
print(f"{x_label} width: {x_width}, derived exponent: {x_exponent}, precision: {x_precision}")

## Include x quantity
x = copy.deepcopy(scan_vlq_1D_template_individual)
x.pop("qualifiers")
x["header"]["name"] = x_label
x["header"]["units"] = x_units
x["values"] = [{"value": round(val, x_precision)} for val in x_values]
output["independent_variables"].append(x)

## Include deltaNLL
for categorization in inputs_dict:
    dNLL = copy.deepcopy(scan_vlq_1D_template_individual)
    dNLL["qualifiers"].append({"name": r"Categorization", "value": categorization})
    dNLL["header"]["name"] = r"$-\Delta\ln\mathcal{L}$"
    dNLL["header"]["units"] = ""
    dNLL["values"] = [{"value": round(float(val["deltaNLL"])/2, 3)} if val["deltaNLL"] else {"value": 0.0} for val in inputs_dict[categorization].values()][:range_index]
    output["dependent_variables"].append(dNLL)

with open(os.path.join(args.output_directory, args.output_file), "w") as out:
    yaml.dump(output, out)
