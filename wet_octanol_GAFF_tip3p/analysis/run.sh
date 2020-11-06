# Activate conda environment
source activate SAMPL6_logP

# Extract free energy of transfer as JSON files
python test_extra_molecules.py
python test_SAMPL6_molecules.py
