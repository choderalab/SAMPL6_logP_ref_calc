import json
from tools import *
import glob
import os
import numpy as np

trials = glob.glob("/data/chodera/misik/SAMPL6_logP_ref_calc/wet_octanol_SMIRNOFF_tip3p/t*/wet_yank_output/")

for idx in range(len(trials)):
    # Trial number
    # trial_num = trials[idx].split("/")[-3]
    trial_num = "t2"
    
    # Grab the names of all the folders/molecules
    directory_mol_list = list()
    for root, dirs, files in os.walk(str(trials[idx]), topdown=False):
        for name in dirs:
            if name[0:2] == "SM" and "_SMIRNOFF_tip3p_equil" in name:
                directory_mol_list.append(name)

    all_mols = []
    for mol in range(len(directory_mol_list)):
        print("\n STARTING TO ANALYZE {} {}... \n".format(mol,str(directory_mol_list[mol])))
        experiment_dir = trials[idx] + directory_mol_list[mol]
        try:
            DeltaF = analyze_directory(experiment_dir)
        except:
            DeltaF = np.NaN
        dict = {str(directory_mol_list[mol]): float(DeltaF)}
        all_mols.append(dict)

    # Added to see the results of partial analysis before errror
        trial_num = trials[idx].split("/")[-3]
        filename = "SAMPL6_mols_trial_" + trial_num + "_SMIRNOFF_tip3p_wetoct.json"
        with open(filename, 'w') as f:
            json.dump(all_mols, f)

# Summary of all analysis
    trial_num = trials[idx].split("/")[-3]
    filename = "SAMPL6_mols_trial_" + trial_num + "_SMIRNOFF_tip3p_wetoct.json"
    with open(filename, 'w') as f:
        json.dump(all_mols, f)
