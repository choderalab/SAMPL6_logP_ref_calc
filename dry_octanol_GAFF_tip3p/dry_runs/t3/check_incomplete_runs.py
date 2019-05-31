from os import listdir
from os.path import isfile, join
import json

# Create a list of systems

PDB_DIR_PATH = "./t3_dry_oct_pdbs"

# Get list of file names
only_files = [f for f in listdir(PDB_DIR_PATH) if isfile(join(PDB_DIR_PATH, f))]

# Remove pdb extension from file names
system_list = []
for file_name in only_files:
    system_name = file_name.split(".pdb")[0]
    system_list.append(system_name)
# Remove "water" systems from the list
for system in system_list:
    if "_water_" in system:
        system_list.remove(system)
for system in system_list:
    if "water" in system:
        system_list.remove(system)
for system in system_list:
    if "water" in system:
        system_list.remove(system)

print("All systems to run:", system_list, "\n")


# Compare full system_list to done_list

# Read JSON file to get a list of completed YANK runs
DONE_JSON_PATH = "dry_yank_results/dry_yank_mols_done.json"

with open(DONE_JSON_PATH) as f:
    done_list = json.load(f)

print("Done systems:", done_list, "\n")

# Compare 2 lists to find the missing ones

def Diff(li1, li2): 
    return (list(set(li1) - set(li2))) 

incomplete_systems_list = Diff(system_list, done_list)
print("Incomplete systems:")
print(incomplete_systems_list)

# Write list of incomplete files
INCOMPLETE_JSON_PATH = "dry_yank_results/dry_yank_mols_incomplete.json"

with open(INCOMPLETE_JSON_PATH, 'w') as f:
    json.dump(list(incomplete_systems_list), f)

# Report ratio of completed jobs.
print("Completed: {}/{}".format(len(done_list), len(system_list)) )
