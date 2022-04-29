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
    help="Long and short name of the process, separated with : in the string",
)
parser.add_argument(
    "--type-string", required=True, help="Particular type of the limit result presented"
)
parser.add_argument(
    "--output-file", required=True, help="Basename of the output .yaml file"
)
parser.add_argument(
    "--output-directory",
    required=True,
    help="Main output directory name for submission to HEPData",
)

args = parser.parse_args()


# Setting up templates
limit_template_1D_main = {
    "dependent_variables": [],
    "independent_variables": [
        {
            "header": {"name": r"Mass $m_\phi$", "units": "GeV"},
            "values": [],
        }
    ],
}

limit_template_1D_individual = {
    "header": {
        "name": r"95% CL limit on $\sigma(PROCESS)\cdot B(\phi\rightarrow\tau\tau)$",
        "units": "pb",
    },
    "qualifiers": [
        {"name": r"Centre-of-mass energy $\sqrt{s}$", "units": "GeV", "value": 13000},
        {"name": r"Integrated luminosity", "units": "fb$^{-1}$", "value": 138},
        {"name": r"Higgs boson production", "value": "PROCESS_LABEL"},
        {"name": r"Limit", "value": "RESULT"},
        {"name": r"Type", "value": "TYPE"},
    ],
    "values": [],
}

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
label, short = args.process.split(":")

## Put masses in
mass_dict = None
for v in output["independent_variables"]:
    if "Mass" in v["header"]["name"]:
        mass_dict = v
        break
for m in masses:
    mass_dict["values"].append({"value": m})

## Include observed
obs = copy.deepcopy(limit_template_1D_individual)
obs["header"]["name"] = obs["header"]["name"].replace("PROCESS", short)

### Replace placeholders
for q in obs["qualifiers"]:
    if "production" in q["name"]:
        q["value"] = q["value"].replace(
            "PROCESS_LABEL", " ".join([label, "$" + short + "$"])
        )
    elif "Limit" in q["name"]:
        q["value"] = q["value"].replace("RESULT", "Observed")
    elif "Type" in q["name"]:
        q["value"] = q["value"].replace("TYPE", args.type_string)

### Fill in limit results
for m in masses:
    obs["values"].append({"value": results[str(m)]["obs"]})
output["dependent_variables"].append(obs)

## Include Expected +/-68 %
exp68 = copy.deepcopy(limit_template_1D_individual)
exp68["header"]["name"] = exp68["header"]["name"].replace("PROCESS", short)

### Replace placeholders
for q in exp68["qualifiers"]:
    if "production" in q["name"]:
        q["value"] = q["value"].replace(
            "PROCESS_LABEL", " ".join([label, "$" + short + "$"])
        )
    elif "Limit" in q["name"]:
        q["value"] = q["value"].replace("RESULT", "Expected $\pm68\%$")
    elif "Type" in q["name"]:
        q["value"] = q["value"].replace("TYPE", args.type_string)

### Fill in limit results
for m in masses:
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
output["dependent_variables"].append(exp68)

## Include Expected +/-95 %
exp95 = copy.deepcopy(limit_template_1D_individual)
exp95["header"]["name"] = exp95["header"]["name"].replace("PROCESS", short)

### Replace placeholders
for q in exp95["qualifiers"]:
    if "production" in q["name"]:
        q["value"] = q["value"].replace(
            "PROCESS_LABEL", " ".join([label, "$" + short + "$"])
        )
    elif "Limit" in q["name"]:
        q["value"] = q["value"].replace("RESULT", "Expected $\pm95\%$")
    elif "Type" in q["name"]:
        q["value"] = q["value"].replace("TYPE", args.type_string)

### Fill in limit results
for m in masses:
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
output["dependent_variables"].append(exp95)

with open(os.path.join(args.output_directory, args.output_file), "w") as out:
    yaml.dump(output, out)
