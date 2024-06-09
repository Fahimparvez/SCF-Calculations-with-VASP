import os
import shutil
import subprocess

def copy_input_files_to_folder(folder_name):
    try:
        shutil.copy('POTCAR', folder_name)
        shutil.copy('KPOINTS', folder_name)
        shutil.copy('INCAR', folder_name)
        print(f"Copied POTCAR, KPOINTS, and INCAR to {folder_name}")
    except FileNotFoundError as e:
        print(f"Error: {e}. Make sure the files exist in the root directory.")
        raise

def run_vasp_in_folder(folder_name, num_cores):
    # Change to the specified directory
    try:
        os.chdir(folder_name)
        print(f"Changed directory to {folder_name}")
    except FileNotFoundError:
        print(f"Error: Directory '{folder_name}' does not exist.")
        return

    # Check if the "COMPCAR" file exists
    if os.path.exists("COMPCAR"):
        print(f"Skipping {folder_name} because 'COMPCAR' file exists.")
        os.chdir('..')
        return

    # Run the VASP command using mpirun with the specified number of cores
    try:
        process = subprocess.Popen(['mpirun', '-np', str(num_cores), 'vasp'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Print the output in real-time
        print("Running VASP...")
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())

        # Capture and print any remaining output
        stdout, stderr = process.communicate()
        if stdout:
            print(stdout.strip())
        if stderr:
            print("Standard Error:\n", stderr.strip())
        
        if process.returncode == 0:
            print(f"VASP run completed successfully in folder: {folder_name}")

            # Create a "COMPCAR" file to indicate completion
            with open("COMPCAR", "w") as f:
                f.write("Calculation completed.")
            print(f"Created COMPCAR file in {folder_name}")
        else:
            print(f"VASP run failed in folder: {folder_name} with return code {process.returncode}")

    except Exception as e:
        print(f"An error occurred while running VASP in folder {folder_name}: {e}")

    finally:
        # Return to the original directory
        os.chdir('..')

def run_vasp_in_all_subfolders(num_cores):
    # Get the current directory (where the script is located)
    parent_directory = os.getcwd()
    print(f"Current directory: {parent_directory}")

    # List all subdirectories in the current directory
    subdirectories = [d for d in os.listdir('.') if os.path.isdir(d)]
    
    for subdir in subdirectories:
        print(f"Processing folder: {subdir}")
        
        # Copy input files to the subdirectory before running VASP
        try:
            copy_input_files_to_folder(subdir)
        except FileNotFoundError:
            print(f"Skipping folder: {subdir} due to missing input files.")
            continue
        
        run_vasp_in_folder(subdir, num_cores)

if __name__ == "__main__":
    # Ask the user for the number of cores
    num_cores = int(input("Enter the number of cores to use for VASP calculations: "))
    
    # Run the function in the current directory with the specified number of cores
    run_vasp_in_all_subfolders(num_cores)

