"""
Created on Tue May 17 11:44:04 2022

@author: tyler

A short script to sample larger data sets to correlate with smaller ones 

MIT License

Copyright (c) 2023 Tyler Lott

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
import tkinter as tk
from tkinter import filedialog
import numpy as np 

root = tk.Tk()
root.withdraw()

run_filtering = input("Would you like to filter a larger linescan acquisition and adapt it to 318 data points (Talos 200)? ")
if run_filtering == "Y" or run_filtering == "Yes" or run_filtering == "yes" or run_filtering == "y":
    file_path = filedialog.askopenfilename()
    file_path = open(os.path.expanduser(file_path))
    thickness_array = []
    for i in file_path:
        thickness_array.append(i)
    
    thickness_array_stripped = []
    data = []
    ### Cleaning up the text files
    for i in thickness_array:
        i_stripped = i.strip('\n')
        thickness_array_stripped.append(i_stripped)
    
    for i in thickness_array_stripped:
        i_stripped2 = float(i.strip("'"))
        data.append(i_stripped2)
    
    data_selected = [] 
    data_selected.append(data[0])
    count = 0
    for i in data:
        count += 1
        if count % 26 == 0:    # Sampling factor, 26 for Titan 8192 point data
            data_selected.append(i)
    data_selected.append(data[-1])
    
    save_path = filedialog.asksaveasfilename()
    with open(str(save_path)+"_filtered_data.txt", "w") as output:
        for i in data_selected:
            output.write(str(i)+"\n")
            
    root.destroy()

### A nearest neighbours algorithm that can be utilized instead of other filters such as the Savitzky-Golay filter ###
run_averaging = input("Would you like to average the data? ")
if run_averaging == "Y" or run_averaging == "Yes" or run_averaging == "yes" or run_averaging == "y":
    file_path = filedialog.askopenfilename()
    file_path = open(os.path.expanduser(file_path))
    thickness_array = []
    for i in file_path:
        thickness_array.append(i)
    
    thickness_array_stripped = []
    data_selected = []
    ### Cleaning up the text files
    for i in thickness_array:
        i_stripped = i.strip('\n')
        thickness_array_stripped.append(i_stripped)
    
    for i in thickness_array_stripped:
        i_stripped2 = float(i.strip("'"))
        data_selected.append(i_stripped2)
    data_selected_averaged = []
    total_count = 0
    ### Averaging by the two nearest neighbours ###
    data_selected_averaged  = []
    total_count = 0
    ### Averaging by nearest neighbours on either side ###
    neighbours = int(input("Please enter an integer value for the averaging (number of neighbours on each side): "))
    neighbour_iteration = np.zeros(neighbours-2)
    
    if neighbours == 0:
        data_selected = data_selected
    elif neighbours == 1:
        for i in data_selected:
            if total_count == 0:
                val_sum = 0
                for i in data_selected[0:neighbours+1]:
                    val_sum += i 
                avg_point = val_sum / len(data_selected[0:neighbours+1])
                data_selected_averaged.append(avg_point)
                total_count +=1    
                
            elif total_count > neighbours-1 and total_count < len(data_selected)-neighbours:
                val_sum = 0
                for i in data_selected[total_count-1:total_count+2]:
                    val_sum += i 
                avg_point = val_sum / len(data_selected[total_count-1:total_count+2])
                data_selected_averaged.append(avg_point)
                total_count +=1

            elif total_count == len(data_selected)-neighbours:
                val_sum = 0
                for i in data_selected[total_count-neighbours:total_count+neighbours]:
                    val_sum += i 
                avg_point = val_sum / len(data_selected[total_count-neighbours:total_count+neighbours])
                data_selected_averaged.append(avg_point)
                total_count +=1

    elif neighbours == 2:
        for i in data_selected:
            if total_count == 0:
                val_sum = 0
                for i in data_selected[0:neighbours+1]:
                    val_sum += i 
                avg_point = val_sum / len(data_selected[0:neighbours+1])
                data_selected_averaged.append(avg_point)
                total_count +=1    

            elif total_count == 1:
                val_sum = 0
                for i in data_selected[0:neighbours+2]:
                    val_sum += i 
                avg_point = val_sum / len(data_selected[0:neighbours+2])
                data_selected_averaged.append(avg_point)
                total_count +=1

            elif total_count > neighbours-1 and total_count < len(data_selected)-neighbours:
                val_sum = 0
                for i in data_selected[total_count-neighbours:total_count+neighbours+1]:
                    val_sum += i 
                avg_point = val_sum / len(data_selected[total_count-neighbours:total_count+neighbours+1])
                data_selected_averaged.append(avg_point)
                total_count +=1

            elif total_count == len(data_selected)-neighbours:
                val_sum = 0
                for i in data_selected[total_count-neighbours:total_count+neighbours]:
                    val_sum += i 
                avg_point = val_sum / len(data_selected[total_count-neighbours:total_count+neighbours])
                data_selected_averaged.append(avg_point)
                total_count +=1

            elif total_count == len(data_selected)-1:
                val_sum = 0
                for i in data_selected[total_count-neighbours:total_count+1]:
                    val_sum += i 
                avg_point = val_sum / len(data_selected[total_count-neighbours:total_count+1])
                data_selected_averaged.append(avg_point)
                total_count +=1

    elif neighbours > 2:   
        for i in data_selected:
            if total_count == 0:
                val_sum = 0
                for i in data_selected[0:neighbours+1]:
                    val_sum += i 
                avg_point = val_sum / len(data_selected[0:neighbours+1])
                data_selected_averaged.append(avg_point)
                total_count +=1    

            elif total_count == 1:
                val_sum = 0
                for i in data_selected[0:neighbours+2]:
                    val_sum += i 
                avg_point = val_sum / len(data_selected[0:neighbours+2])
                data_selected_averaged.append(avg_point)
                total_count +=1

            elif total_count > 1 and total_count < neighbours:
                val_sum = 0      
                for i in data_selected[0:total_count+neighbours]:
                    val_sum += i 
                avg_point = val_sum / len(data_selected[0:total_count+neighbours])
                data_selected_averaged.append(avg_point)
                total_count +=1
                val_sum = 0 

            elif total_count >= neighbours and total_count < len(data_selected)-neighbours:
                val_sum = 0
                for i in data_selected[total_count-neighbours:total_count+neighbours+1]:
                    val_sum += i 
                avg_point = val_sum / len(data_selected[total_count-neighbours:total_count+neighbours+1])
                data_selected_averaged.append(avg_point)
                total_count +=1

            elif total_count == len(data_selected)-neighbours:
                val_sum = 0
                iteration_count = 0
                while iteration_count < len(neighbour_iteration)+1:         
                    for i in data_selected[total_count-neighbours:total_count+neighbours-iteration_count]:
                        val_sum += i 
                    avg_point = val_sum / len(data_selected[total_count-neighbours:total_count+neighbours-iteration_count])
                    data_selected_averaged.append(avg_point)
                    total_count +=1
                    iteration_count += 1
                    val_sum = 0 

            elif total_count == len(data_selected)-1:
                val_sum = 0
                for i in data_selected[total_count-neighbours:total_count+1]:
                    val_sum += i 
                avg_point = val_sum / len(data_selected[total_count-neighbours:total_count+1])
                data_selected_averaged.append(avg_point)
                total_count +=1

    save_path = filedialog.asksaveasfilename()            
    with open(str(save_path)+"_averaged_data.txt", "w") as output:
        for i in data_selected_averaged:
            output.write(str(i)+"\n")
print("END OF PROGRAM")
