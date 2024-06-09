# SCF-Calculations-with-VASP

To calculate SCF calculation by VASP, please follow the instructions:

Step 1: Create several folders with associated POSCAR files in each folder. Place all these folders in a new directory, which will serve as the root directory.
Step 2: Copy "vasp_scf.py" into the root directory.
Step 3: Also, place the "INCAR," "KPOINTS," and "POTCAR" files into the root directory. The "vasp_scf" script will automatically copy these files into the subdirectories.
Step 4: Run the Python script in the root directory. It will prompt you to input the number of cores you wish to utilize for your calculation.
Step 5: Upon completing each subdirectory SCF calculation, a file named "COMPCAR" will be generated to confirm the completion of the calculation.
