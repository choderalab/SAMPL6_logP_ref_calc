# Activate environment
source activate SAMPL6_logP

# Create output directory for dcd files
    output_directory_name="t1_dcd_files"
    echo "$output_directory_name"
    mkdir "$output_directory_name"

# Create dcd file for each phase of each trajectoru
for d in ../t1/dry_yank_output/* ; do
    echo "$d"

    # Extract system name
    system_name="$(cut -d'/' -f4 <<<"$d")"
    echo "$system_name"
    path_to_output_system_directory="$output_directory_name/$system_name"

    # Create system subdirectory in output directory and move dcd files to output direct
    mkdir "$path_to_output_system_directory"

    # Convert nc to dcd
    yank analyze extract-trajectory --trajectory="$path_to_output_system_directory/anti_trial1_solvent1.dcd" --netcdf="$d/solvent1.nc" --state=0
    yank analyze extract-trajectory --trajectory="$path_to_output_system_directory/anti_trial1_solvent2.dcd" --netcdf="$d/solvent2.nc" --state=0
done

# Create tar.gz bundle of the output directory
tar -czvf "$output_directory_name.tar.gz" "$output_directory_name"

echo "Done!"
