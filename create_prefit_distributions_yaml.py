#! /usr/bin/env python3

import json
import yaml
import copy
import os
import ROOT as r
import re

from argparse import ArgumentParser

def sorted_nicely(l):
    """ Sort the given iterable in the way that humans expect: alphanumeric sort (in bash, that's 'sort -V')"""
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    return sorted(l, key = alphanum_key)

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
parser.add_argument(
    "--signal-pattern", required=True, help="Regular expression to match signal and avoid e.g. masses via groups. Should contain a group for process name and for mass"
)
parser.add_argument(
    "--mode", required=True, choices=["grouped", "individual"], help="Determines, how to process individual processes in terms of nominal shapes and systematic uncertainties"
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

## Extract information on processes
def create_info_for_proc(process, is_signal, signal_pattern, inputfile, mode, analysis_configuration):
    events = copy.deepcopy(distribution_template_individual)
    events["header"]["name"] = "Events"
    procs = [k.GetName() for k in inputfile.GetListOfKeys()]
    if mode == "individual" or is_signal == True or (is_signal == False and process in procs):
        proc_dir = inputfile.Get(process)
        name, mass = process, None
        if is_signal:
            ### Determine name and mass from regex
            matching = re.match(signal_pattern, process)
            name, mass = matching.groups()
        ### Get nominal shape
        nominal_shape = proc_dir.Get(process)
        n_bins_proc = nominal_shape.GetNbinsX()
        systnames = set([k.GetName().replace("_Up","").replace("_Down","").replace(process+"_","") for k in proc_dir.GetListOfKeys() if "Up" in k.GetName() or "Down" in k.GetName()])
        if is_signal:
            events["qualifiers"].append({"name": "Process", "value": config["signals"][name].replace("@MASS@",mass)})
        else:
            events["qualifiers"].append({"name": "Process", "value": config["backgrounds"][name]})
        ### Nominal bin content + all systematic variations
        for i in range(n_bins_proc):
            value = copy.deepcopy(event_template_values)
            central = nominal_shape.GetBinContent(i+1) if abs(nominal_shape.GetBinContent(i+1)) > args.min_bin_content else 0
            value["value"] = central
            for syst in sorted_nicely(systnames):
                up = proc_dir.Get(process+"_"+syst+"_Up")
                up_val = up.GetBinContent(i+1) if abs(up.GetBinContent(i+1)) > args.min_bin_content else 0
                down = proc_dir.Get(process+"_"+syst+"_Down")
                down_val = down.GetBinContent(i+1) if abs(down.GetBinContent(i+1)) > args.min_bin_content else 0
                if sum([central, down_val, up_val]) != 0:
                    error = {"label" : syst}
                    error["asymerror"] = {
                        "minus" : down_val - central,
                        "plus" : up_val - central,
                    }
                    if abs(error["asymerror"]["plus"])  > args.min_bin_content or abs(error["asymerror"]["minus"]) > args.min_bin_content:
                        value["errors"].append(error)
            events["values"].append(value)
    elif mode == "grouped":
        proc_type = "signals" if is_signal else "backgrounds"
        config_procs = set(analysis_configuration[proc_type][process]["members"])
        considered_procs = list(config_procs.intersection(set(procs)))
        if is_signal:
            events["qualifiers"].append({"name": "Process", "value": config["signals"][process]["name"].replace("@MASS@",mass)})
        else:
            events["qualifiers"].append({"name": "Process", "value": config["backgrounds"][process]["name"]})
        ### Get nominal shape
        nominal_shape = inputfile.Get(considered_procs[0]).Get(considered_procs[0]).Clone()
        for p in considered_procs[1:]:
            nominal_shape.Add(inputfile.Get(p).Get(p))
        n_bins_proc = nominal_shape.GetNbinsX()
        ### Setup systematics determinations
        systematics = {}
        systematics_per_proc = {}
        for p in considered_procs:
            pdir = inputfile.Get(p)
            systematics_per_proc[p] = set([k.GetName().replace("_Up","").replace("_Down","").replace(p+"_","") for k in pdir.GetListOfKeys() if "Up" in k.GetName() or "Down" in k.GetName()])
            for syst in systematics_per_proc[p]:
                systematics[syst] = { "Up": None, "Down": None}
        systematics_notype = set([syst.replace("norm_", "").replace("shape", "") for syst in systematics])
        systematics_shape_and_norm = set()
        if len(systematics) != len(systematics_notype):
            print(f"WARNING: encountered systematics which are both shape & norm for processes within on grouped process {process}")
            systematics_shape_and_norm = set([syst for syst in systematics_notype for syst_with_type in systematics if re.match(syst, syst_with_type)])
            print("\t",systematics_shape_and_norm)
        ### Determine systematic variations for grouped process
        for syst in systematics:
            for direction in systematics[syst]:
                for p in systematics_per_proc.keys():
                    if systematics[syst][direction]:
                        pdir = inputfile.Get(p)
                        hist_name = ""
                        if syst in systematics_per_proc[p]: # process has the considered systematic uncertainty
                            hist_name = p + "_" + syst + "_" + direction
                        else:
                            hist_name = p
                        #print(f"\tAdding to systematic {syst} for direction {direction} histogram {hist_name}")
                        systematics[syst][direction].Add(pdir.Get(hist_name))
                    else:
                        pdir = inputfile.Get(p)
                        hist_name = ""
                        if syst in systematics_per_proc[p]: # process has the considered systematic uncertainty
                            hist_name = p + "_" + syst + "_" + direction
                        else:
                            hist_name = p 
                        #print(f"\tInitiating systematic {syst} for direction {direction} with {hist_name}")
                        systematics[syst][direction] = pdir.Get(hist_name).Clone()
        ### Clean up the case, if a systematic is both norm and shape across different processes
        for syst in systematics_shape_and_norm:
            for direction in systematics["shape_"+syst]:
                systematics["shape_"+syst][direction].Add(systematics["norm_"+syst][direction])
            systematics.pop("norm_"+syst)
        ### Nominal bin content + all systematic variations
        for i in range(n_bins_proc):
            value = copy.deepcopy(event_template_values)
            central = nominal_shape.GetBinContent(i+1) if abs(nominal_shape.GetBinContent(i+1)) > args.min_bin_content else 0
            value["value"] = central
            for syst in sorted_nicely(systematics):
                up_val = systematics[syst]["Up"].GetBinContent(i+1) if abs(systematics[syst]["Up"].GetBinContent(i+1)) > args.min_bin_content else 0
                down_val = systematics[syst]["Down"].GetBinContent(i+1) if abs(systematics[syst]["Down"].GetBinContent(i+1)) > args.min_bin_content else 0
                if sum([central, down_val, up_val]) != 0:
                    error = {"label" : syst}
                    error["asymerror"] = {
                        "minus" : down_val - central,
                        "plus" : up_val - central,
                    }
                    if abs(error["asymerror"]["plus"])  > args.min_bin_content or abs(error["asymerror"]["minus"]) > args.min_bin_content:
                        value["errors"].append(error)
            events["values"].append(value)
    return events

# Setup directory if it does not exist
if not os.path.isdir(args.output_directory):
    os.path.makedirs(args.output_directory)

# Setting up the .yaml file dict
output = copy.deepcopy(distribution_template_main)

# Load ROOT file and extract information from it
inputfile = r.TFile.Open(args.input, "read")

## Determine processes
processes = [k.GetName() for k in inputfile.GetListOfKeys()]
backgrounds = set()
signals = set()
if args.mode == "individual":
    backgrounds = set(processes).intersection(set(config["backgrounds"]))
    signals = set([proc for proc in processes for sig in set(config["signals"]) if re.match(sig, proc)])
elif args.mode == "grouped":
    for bg in config["backgrounds"]:
        if isinstance(config["backgrounds"][bg], str):
            if bg in processes:
                backgrounds.add(bg)
        elif isinstance(config["backgrounds"][bg], dict):
            for bg_procs in config["backgrounds"][bg]["members"]:
                if bg_procs in processes:
                    backgrounds.add(bg)
                    break
    for sig in config["signals"]:
        if isinstance(config["signals"][sig], str):
            for proc in processes:
                if re.match(sig, proc):
                    signals.add(proc)
        elif isinstance(config["signals"][sig], dict):
            print("ERROR: grouping of signals not supported due to possibility of several mass hypotheses")
            exit(1)

## Extract information on binning from data_obs histogram
data_obs = inputfile.Get("data_obs/data_obs")
n_bins = data_obs.GetNbinsX()
low_edges = [data_obs.GetBinLowEdge(i+1) for i in range(n_bins)]
high_edges = [data_obs.GetBinLowEdge(i+1) + data_obs.GetBinWidth(i+1) for i in range(n_bins)]

## Define variable distribution
distribution = copy.deepcopy(distribution_template_individual)
distribution.pop("qualifiers")
distribution["header"]["name"] = d_label
distribution["header"]["units"] = d_units
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
for bg in sorted_nicely(backgrounds):
    output["dependent_variables"].append(create_info_for_proc(bg, False, None, inputfile, args.mode, config))

## Extract information on signals
for sig in sorted_nicely(signals):
    output["dependent_variables"].append(create_info_for_proc(sig, True, args.signal_pattern, inputfile, args.mode, config))

with open(os.path.join(args.output_directory, args.output_file), "w") as out:
    yaml.dump(output, out)
