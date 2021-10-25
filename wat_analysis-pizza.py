#!/usr/bin/env python
from functions import *
import sys
import numpy as np
sys.path.append('/<path to the folder with protein files>/')

temp=[]
protein = "<name of protein directory>"
#read the GROMACS topology file to get total number of solvent molecules in the system
with open("%s/<topology file>"%protein, "r") as topol:
    num_water = int(topol.readlines()[-1:][0].split()[1])

#read the structure files and assign positions to solvent
for i in range(0,2501):
    # conf = structure files extracted at interval of 10ps from the trajectory
    with open('%s/conf%s.pdb' %(protein,i)) as f:
        temp.append(state(filter(f)))

#filter molecules going through centre at any point
final_array = path(temp, num_water)
grouped_path=[]
for i in final_array:
    grouped_path.append(time_stamp(i))
centre_arr = center(grouped_path)
centre_arr = [x for x in centre_arr if x != 0]

#save the array of all solvent molecules with assigned positions for further analysis
arr_final = np.array(final_array, dtype=object)
np.save("%straj_final.npy" % protein, arr_final)

#save the results to a file
with open("%s/all_results.txt" % protein, "w") as f:
    f.write("Number of water molecules flowing from top to bottom:" + str(len(through(centre_arr))) + "\n")
    f.write("Number of water molecules from bottom to top" + str(len(reverse_through(centre_arr))) + "\n")
    f.write("Bouncing back:" + str(len(bounce(centre_arr))) + "\n")

#extract residue IDs for water passing through the cavity
wat_through = through(centre_arr)
pdb_set1 = []
pdb_set2 = []
for i in range(0, len(wat_through) - 1):
    first = int(wat_through[i][0])
    second = int(wat_through[i + 1][0])
    if first < second:
        pdb_set1.append(wat_through[i][0])
    elif first > second:
        pdb_set1.append(wat_through[i][0])
        break

for i in range(len(pdb_set1), len(wat_through)):
    pdb_set2.append(wat_through[i][0])

#create a trajectory for storing the trajectory of water passing through
os.mkdir("%s/through" % protein)

#save the coordinates of the solvent passing through the cavity to visualise their trajectory
for i in range(0, len(pdb_set1)):
    wat_id = wat_through[i][0]
    left_t = int(wat_through[i][1][0])
    right_t = int(wat_through[i][3][0])
    if left_t >= 10:
        interval1 = left_t - 10
    else:
        interval1 = 0
    if right_t <= 2490:
        interval2 = right_t + 10
    else:
        interval2 = 2500
    a = 1
    for i in range(interval1, interval2):
        with open('%s/conf%s.pdb' % (protein, i), "r") as f:
            for line in f:
                if "OW  SOL  %s" % wat_id in line:
                    with open("%s/through/through_wat_%s.pdb" % (protein, wat_id), "a") as file:
                        new_line = line
                        new_line = new_line.replace("%s" % wat_id, "%s" % a)
                        file.write(new_line)
                    break
        a = a + 1