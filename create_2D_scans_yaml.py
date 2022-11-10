#! /usr/bin/env python3

import yaml
import copy
import os
import ROOT as r
import numpy as np


r.EnableImplicitMT()
from argparse import ArgumentParser

# Parsing arguments
parser = ArgumentParser(
    description="Script to create HEPData .yaml file from 1D limit json files."
)
parser.add_argument(
    "--input", required=True, help="ROOT file input of 2D deltaNLL scan. Assuming, that TTree 'limit' is contained in file"
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
    "--x-quantity", required=True, help="Name:label:units of the x-axis quantity"
)
parser.add_argument(
    "--y-quantity", required=True, help="Name:label:units of the y-axis quantity"
)
parser.add_argument(
    "--mass-hypothesis", required=True, type=float, help="Float number for mass hypothesis"
)
parser.add_argument(
    "--upper-value", required=True, type=float, help="Float number for a maximum considered deltaNLL to avoid outliers"
)
# Assuming, that deltaNLL is contained in the file as z-xis quantity


args = parser.parse_args()
x_name, x_label, x_units = args.x_quantity.split(":")
y_name, y_label, y_units = args.y_quantity.split(":")

# Setting up templates
scan_2D_template_main = {
    "dependent_variables": [],
    "independent_variables": [],
}

scan_2D_template_individual = {
    "header": {},
    "qualifiers": [
        {"name": r"Centre-of-mass energy $\sqrt{s}$", "units": "GeV", "value": 13000},
        {"name": r"Integrated luminosity", "units": "fb$^{-1}$", "value": 138},
        {"name": r"Mass hypothesis", "units": "GeV", "value": args.mass_hypothesis},
    ],
    "values": [],
}

# Setup directory if it does not exist
if not os.path.isdir(args.output_directory):
    os.path.makedirs(args.output_directory)

# Obtain desired information from ROOT file
df = r.RDataFrame("limit", args.input, [x_name, y_name, "deltaNLL", "quantileExpected"])
df_bestFit = df.Filter("quantileExpected == -1 and deltaNLL == 0")
df = df.Filter("quantileExpected > -1 && deltaNLL < " + str(args.upper_value)) # problematic values
print(df.Max("deltaNLL").GetValue())
print(df.Min("deltaNLL").GetValue())
print(df.Count().GetValue())
scan_2d_values = df.AsNumpy([x_name, y_name, "deltaNLL"])
scan_2d_values_bestfit = df_bestFit.AsNumpy([x_name, y_name, "deltaNLL"])

for k in scan_2d_values_bestfit:
    scan_2d_values_bestfit[k] = set([float(val) for val in scan_2d_values_bestfit[k]])
    if len(scan_2d_values_bestfit[k]) > 1:
        print("ERROR: multiple bestfits in results")
        exit(1)

# Setting up the .yaml file dict
output = copy.deepcopy(scan_2D_template_main)

# Get Ranges for x- and y- axis
x_min, x_max = df.Min(x_name).GetValue(), df.Max(x_name).GetValue()
y_min, y_max = df.Min(y_name).GetValue(), df.Max(y_name).GetValue()
x_points = set(scan_2d_values[x_name])
y_points = set(scan_2d_values[y_name])

n_x_points = len(x_points)
n_y_points = len(y_points)

if "Yt" in args.output_file or "qqphi" in args.output_file:
    x_max = x_min + (x_max - x_min) / n_x_points * (n_x_points + 1)
    n_x_points += 1

print(f"{x_name} range: {x_min}, {x_max} with {n_x_points} points")
print(f"{y_name} range: {y_min}, {y_max} with {n_y_points} points")

x_width = (x_max - x_min) / n_x_points
y_width = (y_max - y_min) / n_y_points

x_exponent = np.log10(x_width)
y_exponent = np.log10(y_width)

# Assuming, width is smaller than 1
x_precision = int(np.ceil(abs(x_exponent) + 2))
y_precision = int(np.ceil(abs(y_exponent) + 2))

print(f"{x_name} width: {x_width}, derived exponent: {x_exponent}, precision: {x_precision}")
print(f"{y_name} width: {y_width}, derived exponent: {y_exponent}, precision: {y_precision}")


## Include x quantity
x = copy.deepcopy(scan_2D_template_individual)
x.pop("qualifiers")
x["header"]["name"] = x_label
x["header"]["units"] = x_units
x["values"] = [{"value": round(float(val), x_precision)} for val in scan_2d_values[x_name]] + [{"value": round(float(val), x_precision)} for val in scan_2d_values_bestfit[x_name]]
output["independent_variables"].append(x)

## Include y quantity
y = copy.deepcopy(scan_2D_template_individual)
y.pop("qualifiers")
y["header"]["name"] = y_label
y["header"]["units"] = y_units
y["values"] = [{"value": round(float(val), y_precision)} for val in scan_2d_values[y_name]] + [{"value": round(float(val), y_precision)} for val in scan_2d_values_bestfit[y_name]]
output["independent_variables"].append(y)

## Include deltaNLL (up to 5th digit after comma)
dNLL = copy.deepcopy(scan_2D_template_individual)
dNLL["header"]["name"] = r"$-\Delta\ln\mathcal{L}$"
dNLL["header"]["units"] = ""
dNLL["values"] = [{"value": round(float(val), 3)} for val in scan_2d_values["deltaNLL"]] + [{"value": round(float(val), 3)} for val in scan_2d_values_bestfit["deltaNLL"]]
output["dependent_variables"].append(dNLL)

with open(os.path.join(args.output_directory, args.output_file), "w") as out:
    yaml.dump(output, out)
