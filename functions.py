#!/usr/bin/env python

#extract the water molecules from the pdb
def filter(pdb):
    temp = []
    for i in pdb:
        if len(str.split(str(i))) == 11:
            if str.split(str(i))[3] == 'SOL' and str.split(str(i))[2] == 'OW':
                temp.append([str.split(str(i))[4],str.split(str(i))[5],str.split(str(i))[6],str.split(str(i))[7]])
            else:
                continue
        else:
            continue
    return temp

#assign temporary positions to the water molecules based on their coordinates
def state(arr):
    for i in arr:
        temp = ""
        if float(i[3]) > 50.2:
            temp += "Right"
        elif float(i[3]) < 23.2:
            temp += "Left"
        elif float(i[1]) >= 31.2 and float(i[1]) < 43.2 and float(i[2]) >= 29.5 and float(i[2]) < 41.5 and float(i[3]) >= 23.2 and float(i[3]) < 50.2:
            temp += "Centre"
        else:
            temp += "Intermediate"
        i.append(temp)
    return arr

#create an array with complete trajectory of each water molecule at all times
def path(arr, solvent):
    final_arr = []
    for m in range(0,solvent):
        temp=[]
        for n in range(len(arr)):
            temp.append([])
        final_arr.append(temp)

    for i in range(0,solvent):
        #print(arr[0][1][0])
        final_arr[i][0] = arr[0][i][0]
        for j in range(len(arr)-1):
            #print(final_arr[i][j+1])
            final_arr[i][j+1].append([j+1,arr[j][i][4]])
    return final_arr

#group the positions and output compressed trajectory with time stamps
def time_stamp(arr):
    temp_loc = arr[1][0][1]
    #print(temp_loc)
    output = [arr[0],arr[1]]
    for i in range(1,len(arr)):
        if arr[i][0][1]==temp_loc:
            continue
        else:
            temp_loc=arr[i][0][1]
            output.append(arr[i])
    return output

#check if they pass through the center
def center(arr):
    output=[]
    for i in range(0, len(arr)):
        output.append(0)
    for i in range(0,len(arr)):
        for j in range(1,len(arr[i])):
            if 'Centre' in arr[i][j][0][1]:
                output[i]=arr[i]
            else:
                continue
    return output

#extract the water molecules going through the centre from top to bottom
def through(arr):
    through=[]
    time_through=[]
    #print(arr[0])
    for i in range(0,len(arr)):
        #print(arr[])
        for j in range(1,len(arr[i])-2):
            temp=arr[i]
            #print(temp[j])
            if 'Left' in temp[j][0][1] and 'Centre' in temp[j+1][0][1] and 'Right' in temp[j+2][0][1]:
                #through.append(arr[i])
                time_through.append([arr[i][0], temp[j][0], temp[j+1][0], temp[j+2][0]])
            else:
                continue
    return time_through

#extract molecules going through the centre from bottom to top
def reverse_through(arr):
    through=[]
    time_through=[]
    #print(arr[0])
    for i in range(0,len(arr)):
        #print(arr[])
        for j in range(1,len(arr[i])-2):
            temp=arr[i]
            #print(temp[j])
            if 'Right' in temp[j][0][1] and 'Centre' in temp[j+1][0][1] and 'Left' in temp[j+2][0][1]:
                #through.append(arr[i])
                time_through.append([arr[i][0], temp[j][0], temp[j+1][0], temp[j+2][0]])
            else:
                continue
    return time_through

#extract water molecules bouncing back from the centre
def bounce(arr):
    bounce=[]
    #print(arr[0])
    for i in range(0,len(arr)):
        #print(arr[])
        for j in range(1,len(arr[i])-2):
            temp=arr[i]
            #print(temp[j])
            if 'Left' in arr[i][j][0][1] and 'Centre' in arr[i][j+1][0][1] and 'Left' in arr[i][j+2][0][1]:
                bounce.append(arr[i])
            else:
                continue
    return bounce

#extract molecules passing through the centre (via Intermediate) with a distorted trajectory
def through2(arr):
    through=[]
    #print(arr[0])
    for i in range(0,len(arr)):
        #print(arr[])
        for j in range(1,len(arr[i])-3):
            temp=arr[i]
            #print(temp[j])
            if 'Left' in temp[j][0][1] and 'Centre' in temp[j+1][0][1] and 'Intermediate' in temp[j+2][0][1] \
                    and 'Right' in temp[j+3][0][1]:
                through.append(arr[i])
            else:
                continue
            if 'Right' in temp[j][0][1] and 'Centre' in temp[j+1][0][1] and 'Intermediate' in temp[j+2][0][1] \
                    and 'Left' in temp[j+3][0][1]:
                through.append(arr[i])
            else:
                continue
    return through