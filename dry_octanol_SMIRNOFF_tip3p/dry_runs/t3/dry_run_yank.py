#!/bin/bash
import os
import sys
import glob
import json
from simtk.openmm.app import *

from yank.experiment import ExperimentBuilder


# Specify directory in RESULTS_DIR
RESULTS_DIR = os.path.join('.','dry_yank_results') #where the json file will be stored
MOLECULES_DONE_FILEPATH = os.path.join(RESULTS_DIR, 'dry_yank_mols_done.json') #this json file keeps track of molecule that are done

OUTPUT_DIR = os.path.join('.','dry_yank_outputs')# where the yank results/output will be stored

def print_and_flush(msg):
    """On the cluster, printing may not always appear if not flushed."""
    print(msg)
    sys.stdout.flush()

def read_status():
    if os.path.exists(MOLECULES_DONE_FILEPATH):
        print_and_flush('Node {}: Resuming from {}'.format(job_id, MOLECULES_DONE_FILEPATH))
        with open(MOLECULES_DONE_FILEPATH, 'r') as f:
            molecules_data = set(json.load(f))
    else:
        molecules_data = set()
    return molecules_data


def update_status(new_element):
    if not os.path.exists(RESULTS_DIR):
        os.makedirs(RESULTS_DIR)
    molecules_data = read_status()
    molecules_data.add(new_element)
    with open(MOLECULES_DONE_FILEPATH, 'w') as f:
        json.dump(list(molecules_data), f)

def run_yank(job_id, n_jobs):
    # Direct path to where the input PDBs are
    pdb_dir = "./t3_dry_oct_pdbs"
    # Direct path to where the input XML system files are (will need to change according to what trial directory you're working in)
    openmm_system_dir = "./t3_dry_oct_XMLs"
    
    # Path to YANK template script (YAML file)
    yank_script_template_filepath = 'dry_yank.yaml' #don't need to change this

    # Read in YANK template script.
    with open(yank_script_template_filepath, 'r') as f:
        script_template = f.read()

    # Load cached status calculations.
    molecules_done = read_status()

    # Find all the molecules to run
    # Make a list of JUST the solute/octanol mixures (excludes the solute in water mixtures that are in the same pdb directory as the solute/octanol mixures)
    molecules_files_pattern = os.path.join(pdb_dir, '*_octanol_0.0_1.0_SMIRNOFF_tip3p_equil.pdb')
    molecule_ids = [os.path.basename(molecule_file)[:-4] for molecule_file in glob.glob(molecules_files_pattern)] # makes a list of just the system IDs (ie SM13_octanol_0.0_1.0_SMIRNOFF_tip3p_equil instead of SM13_octanol_0.0_1.0_SMIRNOFF_tip3p_equil.pdb)

    # Sort molecules so that parallel nodes won't make the same calculation.
    molecule_ids = sorted(molecule_ids)

    # Loop through the list of the phase 1 files, which are the solute/octanol mixtures
    # The phase 1 file name will be used to grab the corresponding phase 2 file
    # Create input files.
    for i, molecule_id in enumerate(molecule_ids):
        # Check if the job is assigned to this script and/or if we
        # have already completed this.
        if (i % n_jobs != job_id - 1 or molecule_id in molecules_done):
            print_and_flush('Node {}: Skipping {}'.format(job_id, molecule_id))
            continue

        # specify phase one, which will be the solute in just octanol
        phase1_molecule_id = molecule_id
        # specify phase two, which will be the solute in just water
        phase2_molecule_id = phase1_molecule_id.replace("_octanol_0.0_1.0_SMIRNOFF_tip3p_equil", "_water_0.0_1.0_SMIRNOFF_tip3p_equil")

        # Specify the PDB and XML filepaths
        phase1_PDB_filepath = os.path.join(pdb_dir, phase1_molecule_id + '.pdb') #solute in octanol
        phase2_PDB_filepath = os.path.join(pdb_dir, phase2_molecule_id + '.pdb') #solute in water

        phase1_xml_filepath = os.path.join(openmm_system_dir, phase1_molecule_id[:-6] + '.xml') #solute in octanol/water
        phase2_xml_filepath = os.path.join(openmm_system_dir, phase2_molecule_id[:-6] + '.xml') #solute in water

        # Create yank script.
        phase1_path = str([phase1_xml_filepath, phase1_PDB_filepath])
        phase2_path = str([phase2_xml_filepath, phase2_PDB_filepath])
        
        # Load the PDB and XML files into yank
        script = script_template.format(experiment_dir=molecule_id,
                                        phase1_path=phase1_path,
                                        phase2_path=phase2_path)

        # Run YANK.
        print_and_flush('Node {}: Running {}'.format(job_id, molecule_id))
        yaml_builder = ExperimentBuilder(script)
        yaml_builder.run_experiments()

        # Update completed molecules.
        update_status(molecule_id)

if __name__ == '__main__':
    
    print("Started running dry_run_yank.py ...")
    
    job_id = int(sys.argv[1])
    n_jobs = int(sys.argv[2])
    assert 0 < job_id <= n_jobs
    run_yank(job_id=job_id, n_jobs=n_jobs)

    print("Done running dry_run_yank.py!")
