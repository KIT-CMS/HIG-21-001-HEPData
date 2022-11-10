#! /usr/bin/env python3

import yaml
import copy
import os
import pandas as pd

from argparse import ArgumentParser

# Parsing arguments
parser = ArgumentParser(
    description="Script to create HEPData .yaml file from .csv correlation files"
)
parser.add_argument(
    "--input", required=True, help=".csv input file with three columns. First to columns contain parameter names, third the correlation coefficient in percent"
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

args = parser.parse_args()

# Setting up templates
sm_ggh_frac_template_main = {
    "dependent_variables": [],
    "independent_variables": [],
}

sm_ggh_frac_template_individual = {
    "header": {},
    "qualifiers": [
        {"name": r"Centre-of-mass energy $\sqrt{s}$", "units": "GeV", "value": 13000},
        {"name": r"Integrated luminosity", "units": "fb$^{-1}$", "value": 138},
    ],
    "values": [],
}
for q in args.additional_qualifiers:
    name,value = q.split(":")
    sm_ggh_frac_template_individual["qualifiers"].append({"name": name, "value": value})

# Setup directory if it does not exist
if not os.path.isdir(args.output_directory):
    os.path.makedirs(args.output_directory)

# Obtain desired information from ROOT file
df = pd.read_csv(args.input)

frac_labels = {
    "ggh_t_frac": '$gg\phi$ t-only',
    "ggh_b_frac": '$gg\phi$ b-only',
    "ggh_i_frac": '$gg\phi$ tb-interference',
}

# Setting up the .yaml file dict
output = copy.deepcopy(sm_ggh_frac_template_main)

## Include mass parameter
mass = copy.deepcopy(sm_ggh_frac_template_individual)
mass.pop("qualifiers")
mass["header"]["name"] = '$m_\phi$'
mass["header"]["units"] = "GeV"
mass["values"] = [{"value": val} for val in df["MH"]]
output["independent_variables"].append(mass)

## Include correlation coefficient
for frac in frac_labels:
    fracinfo = copy.deepcopy(sm_ggh_frac_template_individual)
    fracinfo["header"]["name"] = 'Fraction of the cross-section $\sigma(gg\phi)$ as expected from SM'
    fracinfo["header"]["units"] = ''
    fracinfo["qualifiers"].append({"name": r"Contribution", "value": frac_labels[frac]})
    fracinfo["values"] = [{"value": round(val, 6)} for val in df[frac]]
    output["dependent_variables"].append(fracinfo)

with open(os.path.join(args.output_directory, args.output_file), "w") as out:
    yaml.dump(output, out)
