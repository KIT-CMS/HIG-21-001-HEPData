#! /usr/bin/env python3

import json
import yaml
import copy
import os
import ROOT as r

from argparse import ArgumentParser


# Parsing arguments
parser = ArgumentParser(
    description="Script to create HEPData .yaml file from prefit shape distributions."
)
parser.add_argument(
    "--input", required=True, help="Input ROOT file with prefit shapes and their uncertainties"
)
parser.add_argument(
    "--analysis-configuration",
    required=True,
    help="Configuration in .yaml format related to analysis-specific labelling.",
)
parser.add_argument(
    "--output-file", required=True, help="Basename of the output .yaml file"
)
parser.add_argument(
    "--distribution-quantity", required=True, help="Label:units of the distribution quantity"
)
parser.add_argument(
    "--category", required=True, help="Name of the considered category"
)
parser.add_argument(
    "--output-directory",
    required=True,
    help="Main output directory name for submission to HEPData",
)
parser.add_argument(
    "--min-bin-content", required=True, type=float, help="Minimum meaningful number in a bin, lower values are set to 0"
)

args = parser.parse_args()

# Load analysis configuration
config = yaml.load(open(args.analysis_configuration, "r"), Loader=yaml.FullLoader)

d_label, d_units = args.distribution_quantity.split(":")


# Setting up templates
distribution_template_main = {
    "dependent_variables": [],
    "independent_variables": [],
}

distribution_template_individual = {
    "header": {},
    "qualifiers": [
        {"name": r"Centre-of-mass energy $\sqrt{s}$", "units": "GeV", "value": 13000},
        {"name": r"Integrated luminosity", "units": "fb$^{-1}$", "value": 138},
        {"name": r"Category", "value": config["categories"][args.category]},
    ],
    "values": [],
}

event_template_values = {
    "value": 0.0,
    "errors": [],
}

# Setup directory if it does not exist
if not os.path.isdir(args.output_directory):
    os.path.makedirs(args.output_directory)

# Setting up the .yaml file dict
output = copy.deepcopy(distribution_template_main)

# Load ROOT file and extract information from it
inputfile = r.TFile.Open(args.input, "read")

## Determine processes
processes = [k.GetName() for k in inputfile.GetListOfKeys()]
backgrounds = set(processes).intersection(set(config["backgrounds"]))
signals = set(processes).difference(backgrounds).difference(set("data_obs"))

## Extract information on binning from data_obs histogram
data_obs = inputfile.Get("data_obs/data_obs")
n_bins = data_obs.GetNbinsX()
low_edges = [data_obs.GetBinLowEdge(i+1) for i in range(n_bins)]
high_edges = [data_obs.GetBinLowEdge(i+1) + data_obs.GetBinWidth(i+1) for i in range(n_bins)]

## Define variable distribution
distribution = copy.deepcopy(distribution_template_individual)
distribution.pop("qualifiers")
distribution["header"]["name"] = args.distribution_quantity
for low, high in zip(low_edges, high_edges):
    distribution["values"].append({"low": low, "high": high})

output["independent_variables"].append(distribution)

## Put observation into yaml file
data_events = copy.deepcopy(distribution_template_individual)
data_events["header"]["name"] = "Events"
data_events["qualifiers"].append({"name": "Process", "value": config["data_obs"]})
data_events["values"] = [{"value": int(round(data_obs.GetBinContent(i+1)))} for i in range(n_bins)]
output["dependent_variables"].append(data_events)

## Extract information on backgrounds
for bg in backgrounds:
    bg_dir = inputfile.Get(bg)
    ### Get nominal shape
    nominal_shape = bg_dir.Get(bg)
    ### Determine systematic names
    systnames = set([k.GetName().replace("_Up","").replace("_Down","").replace(bg+"_","") for k in bg_dir.GetListOfKeys() if "Up" in k.GetName() or "Down" in k.GetName()])
    bg_events = copy.deepcopy(distribution_template_individual)
    bg_events["header"]["name"] = "Events"
    bg_events["qualifiers"].append({"name": "Process", "value": config["backgrounds"][bg]})
    ### Nominal bin content + all systematic variations
    for i in range(n_bins):
        value = copy.deepcopy(event_template_values)
        central = nominal_shape.GetBinContent(i+1) if nominal_shape.GetBinContent(i+1) > args.min_bin_content else 0
        value["value"] = central
        for syst in systnames:
            up = bg_dir.Get(bg+"_"+syst+"_Up")
            up_val = up.GetBinContent(i+1) if up.GetBinContent(i+1) > args.min_bin_content else 0
            down = bg_dir.Get(bg+"_"+syst+"_Down")
            down_val = down.GetBinContent(i+1) if down.GetBinContent(i+1) > args.min_bin_content else 0
            if sum([central, down_val, up_val]) != 0:
                error = {"label" : syst}
                error["asymerror"] = {
                    "minus" : down_val - central,
                    "plus" : up_val - central,
                }
                value["errors"].append(error)
        bg_events["values"].append(value)
    output["dependent_variables"].append(bg_events)

with open(os.path.join(args.output_directory, args.output_file), "w") as out:
    yaml.dump(output, out)
