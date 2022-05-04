#! /usr/bin/env python3

import json
import yaml
import copy
import os
import ROOT as r

from argparse import ArgumentParser


# Parsing arguments
parser = ArgumentParser(
    description="Script to create HEPData .yaml file from 1D limit json files."
)
parser.add_argument(
    "--input", required=True, help="ROOT file containing all 6 TGraph2D CLs values"
)
parser.add_argument(
    "--type-string", required=True, help="Particular type of the limit result presented"
)
parser.add_argument(
    "--output-file", required=True, help="Basename of the output .yaml file"
)
parser.add_argument(
    "--x-quantity", required=True, help="Label:units of the x quantity"
)
parser.add_argument(
    "--y-quantity", required=True, help="Label:units of the y quantity"
)
parser.add_argument(
    "--output-directory",
    required=True,
    help="Main output directory name for submission to HEPData",
)
parser.add_argument(
    "--additional-qualifiers", nargs="*", help="A list of additional qualifiers, given as name:value", default=[] # Like the process label (long version)
)
parser.add_argument(
    "--min-n-points", required=True, type=int, help="Minimum number of points required for a contour"
)

args = parser.parse_args()

x_label, x_units = args.x_quantity.split(":")
y_label, y_units = args.y_quantity.split(":")


# Setting up templates
limit_template_main = {
    "dependent_variables": [],
    "independent_variables": [],
}

limit_template_individual = {
    "header": {},
    "qualifiers": [
        {"name": r"Centre-of-mass energy $\sqrt{s}$", "units": "GeV", "value": 13000},
        {"name": r"Integrated luminosity", "units": "fb$^{-1}$", "value": 138},
        {"name": r"Limit", "value": "RESULT"},
        {"name": r"Type", "value": "TYPE"},
    ],
    "values": [],
}

for q in args.additional_qualifiers:
    name,value = q.split(":")
    limit_template_individual["qualifiers"].append({"name": name, "value": value})

# Setup directory if it does not exist
if not os.path.isdir(args.output_directory):
    os.path.makedirs(args.output_directory)

results =  [
    "obs:Observed", 
    r"exp0:Expected at median of $f(\tilde{q}_\mu|\text{SM})$",
    r"exp-2:Expected at 2.5% quantile of $f(\tilde{q}_\mu|\text{SM})$",
    r"exp-1:Expected at 16% quantile of $f(\tilde{q}_\mu|\text{SM})$",
    r"exp+1:Expected at 84% quantile of $f(\tilde{q}_\mu|\text{SM})$",
    r"exp+2:Expected at 97.5% quantile of $f(\tilde{q}_\mu|\text{SM})$",
]

# Setting up the .yaml file dict for each CLs result
for result in results:
    output = copy.deepcopy(limit_template_main)
    r_name, r_label = result.split(":")

    ## Extract appropriate 2D Graph
    inputfile = r.TFile.Open(args.input, "read")
    graph = inputfile.Get(r_name)
    contours = graph.GetContourList(0.05)
    print(r_name,":",len(contours),"contours")
    x_values = []
    y_values = []
    for index, contour in enumerate(contours):
        if contour.GetN() < args.min_n_points:
            print("\tcontour:",index,"# points:",contour.GetN(),"excluded")
        else:
            print("\tcontour:",index,"# points:",contour.GetN(),"included")
            x_values += [val for val in contour.GetX()]
            y_values += [val for val in contour.GetY()]

    ## Put x-quantity in as independent variable
    x = copy.deepcopy(limit_template_individual)
    x.pop("qualifiers")
    x["header"]["name"] = x_label
    x["header"]["units"] = x_units
    x["values"] = [{"value": val} for val in x_values]
    output["independent_variables"].append(x)

    ## Put y-quantity in as dependent variable
    y = copy.deepcopy(limit_template_individual)
    y["header"]["name"] = y_label
    y["header"]["units"] = y_units

    ### Replace placeholders
    for q in y["qualifiers"]:
        if "Limit" in q["name"]:
            q["value"] = q["value"].replace("RESULT", r_label)
        elif "Type" in q["name"]:
            q["value"] = q["value"].replace("TYPE", args.type_string)

    ### Fill in limit results
    y["values"] = [{"value": val} for val in y_values]
    output["dependent_variables"].append(y)

    with open(os.path.join(args.output_directory, args.output_file.replace(".yaml", "_" + r_name + ".yaml")), "w") as out:
        yaml.dump(output, out)
