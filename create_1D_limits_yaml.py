#! /usr/bin/env python3

import json
import yaml
import copy
import os

from argparse import ArgumentParser


# Parsing arguments
parser = ArgumentParser(
    description="Script to create HEPData .yaml file from 1D limit json files."
)
parser.add_argument(
    "--inputs", required=True, nargs="+", help="A list of 1D limit .json files"
)
parser.add_argument(
    "--process",
    required=True,
    help="Short name of the process in Latex",
)
parser.add_argument(
    "--type-string", required=True, help="Particular type of the limit result presented"
)
parser.add_argument(
    "--output-file", required=True, help="Basename of the output .yaml file"
)
parser.add_argument(
    "--mass-quantity", required=True, help="Label:units of the mass quantity"
)
parser.add_argument(
    "--limit-quantity", required=True, help="Label:units of the limit quantity"
)
parser.add_argument(
    "--output-directory",
    required=True,
    help="Main output directory name for submission to HEPData",
)
parser.add_argument(
    "--additional-qualifiers", nargs="*", help="A list of additional qualifiers, given as name:value. Default: %(default)s", default=[] # Like the process label (long version)
)
parser.add_argument("--limit-name-replacement", help="A different qualifier name instead of 'Limit'. Default: %(default)s", default=None)

args = parser.parse_args()

m_label, m_units = args.mass_quantity.split(":")
l_label, l_units = args.limit_quantity.split(":")


# Setting up templates
limit_template_1D_main = {
    "dependent_variables": [],
    "independent_variables": [],
}

limit_template_1D_individual = {
    "header": {},
    "qualifiers": [
        {"name": r"Centre-of-mass energy $\sqrt{s}$", "units": "GeV", "value": 13000},
        {"name": r"Integrated luminosity", "units": "fb$^{-1}$", "value": 138},
        {"name": args.limit_name_replacement if args.limit_name_replacement else r"Limit", "value": "RESULT"},
        {"name": r"Type", "value": "TYPE"},
    ],
    "values": [],
}

for q in args.additional_qualifiers:
    name,value = q.split(":")
    limit_template_1D_individual["qualifiers"].append({"name": name, "value": value})

limit_template_expvalues = {
    "value": 0.0,
    "errors": [],
}

# Setup directory if it does not exist
if not os.path.isdir(args.output_directory):
    os.path.makedirs(args.output_directory)


# Creating a dict from .json files
results = {}

for i in args.inputs:
    results.update(json.load(open(i, "r")))

masses = sorted([float(m) for m in results.keys()])


# Setting up the .yaml file dict
output = copy.deepcopy(limit_template_1D_main)
short = args.process

## Put masses in
mass = copy.deepcopy(limit_template_1D_individual)
mass.pop("qualifiers")
mass["header"]["name"] = m_label
mass["header"]["units"] = m_units
for m in masses:
    mass["values"].append({"value": m})
output["independent_variables"].append(mass)

## Include observed
obs = copy.deepcopy(limit_template_1D_individual)
obs["header"]["name"] = l_label
obs["header"]["units"] = l_units

### Replace placeholders
for q in obs["qualifiers"]:
    if "Limit" in q["name"] or (args.limit_name_replacement and args.limit_name_replacement in q["name"]):
        q["value"] = q["value"].replace("RESULT", "Observed")
    elif "Type" in q["name"]:
        q["value"] = q["value"].replace("TYPE", args.type_string)

### Fill in limit results
for m in masses:
    obs["values"].append({"value": results[str(m)]["obs"]})
output["dependent_variables"].append(obs)

## Include Expected +/-68 %
exp68 = copy.deepcopy(limit_template_1D_individual)
exp68["header"]["name"] = l_label
exp68["header"]["units"] = l_units

### Replace placeholders
for q in exp68["qualifiers"]:
    if "Limit" in q["name"]:
        q["value"] = q["value"].replace("RESULT", "Expected $\pm68\%$")
    elif "Type" in q["name"]:
        q["value"] = q["value"].replace("TYPE", args.type_string)

### Fill in limit results
for m in masses:
    if "exp0" in results[str(m)]:
        value = copy.deepcopy(limit_template_expvalues)
        central = results[str(m)]["exp0"]
        value["value"] = central
        error = {}
        error["asymerror"] = dict(
            minus=results[str(m)]["exp-1"] - central,
            plus=results[str(m)]["exp+1"] - central,
        )
        value["errors"].append(error)
        exp68["values"].append(value)
if exp68["values"]:
    output["dependent_variables"].append(exp68)

## Include Expected +/-95 %
exp95 = copy.deepcopy(limit_template_1D_individual)
exp95["header"]["name"] = l_label
exp95["header"]["units"] = l_units

### Replace placeholders
for q in exp95["qualifiers"]:
    if "Limit" in q["name"]:
        q["value"] = q["value"].replace("RESULT", "Expected $\pm95\%$")
    elif "Type" in q["name"]:
        q["value"] = q["value"].replace("TYPE", args.type_string)

### Fill in limit results
for m in masses:
    if "exp0" in results[str(m)]:
        value = copy.deepcopy(limit_template_expvalues)
        central = results[str(m)]["exp0"]
        value["value"] = central
        error = {}
        error["asymerror"] = dict(
            minus=results[str(m)]["exp-2"] - central,
            plus=results[str(m)]["exp+2"] - central,
        )
        value["errors"].append(error)
        exp95["values"].append(value)
if exp95["values"]:
    output["dependent_variables"].append(exp95)

with open(os.path.join(args.output_directory, args.output_file), "w") as out:
    yaml.dump(output, out)
