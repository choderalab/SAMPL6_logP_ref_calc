import json
from phase_grab import *

#from tools import *
import glob
import os
import numpy as np
import pickle
import warnings
warnings.filterwarnings("ignore")

# Replicate runs
trials = [1, 2, 3]

for trial_number in trials:
    #update this line according to dry yank output directory (1,2 and 3) 
    trials = glob.glob("/data/chodera/misik/SAMPL6_logP_ref_calc/wet_octanol_GAFF_tip3p/t{}/wet_yank_output/".format(trial_number))
    all_mols = []
    for idx in range(len(trials)):
        #Grab the names of all the folders/molecules
        directory_mol_list = list()
        for root, dirs, files in os.walk(str(trials[idx]), topdown=False):
            for name in dirs:
                if "oct" in name:
                    directory_mol_list.append(name)

        for mol in range(len(directory_mol_list)):
            experiment_dir = trials[idx] + directory_mol_list[mol]
            DeltaF = analyze_directory(experiment_dir)
            #print(DeltaF)

            dict = {'trial':idx, str(directory_mol_list[mol]): DeltaF}
            all_mols.append(dict)
            print("{}% of trial {} collected..".format(round(float(mol/len(directory_mol_list)*100),2),idx))
    
    #update output file name for trial 1, 2, and 3
    filename = "trial{}_wet_octanol_GAFF_tip3p.pickle".format(trial_number)

    with open(filename, 'wb') as handle:
        pickle.dump(all_mols, handle, protocol=pickle.HIGHEST_PROTOCOL)
