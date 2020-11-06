#/usr/local/bin/env python

import os
import json
import logging

import numpy as np
from scipy.stats import linregress


# A validation test fails when its Z-score exceeds this threshold.
#MAX_Z_SCORE = 6
#ANALYSIS_FILEPATH = os.path.join('..', 'results', 'analysis_done.json')
MOLECULES_DONE_FILEPATH = os.path.join('Molecules_collected.json')
# ANALYSIS_FILEPATH = os.path.join('..', 'results', 'analysis_done_torsions.json')
# MOLECULES_DONE_FILEPATH = os.path.join('..', 'results', 'molecules_done_torsions.json')

# Set logger verbosity level.
logging.basicConfig(level=logging.DEBUG)


def analyze_directory(experiment_dir):
    """Return free energy and error of a single experiment.
    Parameters
    ----------
    experiment_dir : str
        The path to the directory storing the nc files.
    Return
    ------
    DeltaF : simtk.unit.Quantity
        Difference in free energy between the end states in kcal/mol.
    """
    import yaml
    from simtk import unit
    from yank.analyze import get_analyzer

    analysis_script_filepath = os.path.join(experiment_dir, 'analysis.yaml')

    # Load sign of alchemical phases.
    with open(analysis_script_filepath, 'r') as f:
        analysis_script = yaml.load(f)


    # Generate analysis object.
    analysis = {}
    for phase_name, sign in analysis_script:
        phase_path = os.path.join(experiment_dir, phase_name + '.nc')
        analyzer = get_analyzer(phase_path)

        analysis[phase_name] = analyzer.analyze_phase()
        print("analysis[phase_name]", analysis[phase_name])
        kT = analyzer.kT
        n_samples = len(analyzer.reporter._storage_dict['analysis'].dimensions['iteration']) - 1
        assert n_samples == 5000, '{}'.format(n_samples)

    # Compute free energy.
    free_energy_diff = 0.0
    for phase_name, sign in analysis_script:
        free_energy_diff -= sign * (analysis[phase_name]['free_energy_diff'] + analysis[phase_name]['free_energy_diff_standard_state_correction'])

    # Convert from kT units to kcal/mol
    unit_conversion = kT / unit.kilocalories_per_mole
    return free_energy_diff * unit_conversion

#def save_analysis(experiment_name, data, filepath):
#    info = {experiment_name : data}
#    with open(filepath, 'w') as f:
#        json.dump(info, f)
