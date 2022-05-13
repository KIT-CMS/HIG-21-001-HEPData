#! /usr/bin/env python3

import yaml
import copy
import os
import pandas as pd
import numpy as np

from argparse import ArgumentParser

# Parsing arguments
parser = ArgumentParser(
    description="Script to create HEPData .yaml file from .csv correlation files. Correlations given in percent in the output file"
)
parser.add_argument(
    "--input", required=True, help=".csv input file with three columns. First to columns contain parameter names, third the correlation coefficient"
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
    "--additional-qualifiers", nargs="*", help="A list of additional qualifiers, given as name:value. Default: %(default)s", default=[]
)
parser.add_argument(
    "--min-correlation", type=float, help="Minimum correlation (absolute value) to be considered. Default: %(default)s", default=0.01
)

args = parser.parse_args()

# Setting up templates
correlation_2D_template_main = {
    "dependent_variables": [],
    "independent_variables": [],
}

correlation_2D_template_individual = {
    "header": {},
    "qualifiers": [
        {"name": r"Centre-of-mass energy $\sqrt{s}$", "units": "GeV", "value": 13000},
        {"name": r"Integrated luminosity", "units": "fb$^{-1}$", "value": 138},
    ],
    "values": [],
}
for q in args.additional_qualifiers:
    name,value = q.split(":")
    correlation_2D_template_individual["qualifiers"].append({"name": name, "value": value})

# Setup directory if it does not exist
if not os.path.isdir(args.output_directory):
    os.path.makedirs(args.output_directory)

# Obtain desired information from ROOT file
df = pd.read_csv(args.input)
df = df[np.absolute(df["Correlation"]) >= args.min_correlation]

# Setting up the .yaml file dict
output = copy.deepcopy(correlation_2D_template_main)

## Include x parameter
x = copy.deepcopy(correlation_2D_template_individual)
x.pop("qualifiers")
x["header"]["name"] = "Nuisance parameter (x)"
x["header"]["units"] = ""
x["values"] = [{"value": val} for val in df.iloc[:, 0].values]
output["independent_variables"].append(x)

## Include y quantity
y = copy.deepcopy(correlation_2D_template_individual)
y.pop("qualifiers")
y["header"]["name"] = "Nuisance parameter (y)"
y["header"]["units"] = ""
y["values"] = [{"value": val} for val in df.iloc[:, 1].values]
output["independent_variables"].append(y)

## Include correlation coefficient
corr = copy.deepcopy(correlation_2D_template_individual)
corr["header"]["name"] = "Correlation coefficient"
corr["header"]["units"] = '%'
corr["values"] = [{"value": round(val * 100.0)} for val in df.iloc[:, 2].values]
output["dependent_variables"].append(corr)

with open(os.path.join(args.output_directory, args.output_file), "w") as out:
    yaml.dump(output, out)
