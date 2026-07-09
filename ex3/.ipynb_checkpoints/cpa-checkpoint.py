####################################################################################################
############################# Hardware Oriented Security - CPA Exercise ############################
####################################################################################################

# Imports and Setup
# from load import load_io, load_traces
from bokeh.plotting import figure, show
from bokeh.models import HoverTool
import time
import logging
import numpy as np
from ham_w import ham_w
from env import  plaintexts_path_npy,ciphertexts_path_npy,traces_path_npy
logging.basicConfig(level=logging.INFO)

# SBox
SBOX=[6,11,5,4,2,14,7,10,9,13,15,12,3,1,0,8]
SBOX = np.array(SBOX)

# Global Parameters
n_traces = 30000
n_nibbles = 16
trace_len = 100012
scale = 3
m_off = 0

# Load Data (Run once)
plaintexts = np.load(plaintexts_path_npy, mmap_mode="c")
ciphertexts = np.load(ciphertexts_path_npy,mmap_mode="c")

tic = time.perf_counter()
traces = np.load(traces_path_npy, mmap_mode="c")
toc = time.perf_counter()
logging.info(f"Loaded the power traces in {toc - tic:0.4f} seconds")

# Scale traces (Run once)
for i in range(n_traces):
    for j in range(n_nibbles):
        traces[i, j] = ((traces[i, j]/127)*4) * scale + m_off

# CPA Parameters
nibbleStart = 0;
nibbleEnd = 16;
keyCandidateStart = 0
keyCandidateStop = 15
solvedKey = np.zeros((1,nibbleEnd))

##################################################
########### Exercise 1 - Area Selection ##########
##################################################

# Plotting - Full Trace
power_traces_plot = figure(title="Power Consumption of an Encryption", 
                           x_axis_label="Time", 
                           y_axis_label="Power (mW)",
                           width=1200, height=600)
power_traces_plot.line(x=[i for i in range(traces.shape[1])], y=traces[1,:], 
                       legend_label="Power Trace", 
                       line_width=2)
hover = HoverTool(tooltips=[("Time", "$x"), ("Power", "$y")])
power_traces_plot.add_tools(hover)
show(power_traces_plot)

# Plotting - Reduced Trace
offset_initial = 10     # Change this value
segmentLength = 10      # Change this value
traces_red = traces[:, offset_initial:offset_initial+segmentLength]

reduced_power_traces_plot = figure(title="Selected Power Consumption", 
                           x_axis_label="Time", 
                           y_axis_label="Power (mW)",
                           width=1200, height=600)
reduced_power_traces_plot.line(x=[i for i in range(traces_red.shape[1])], y=traces_red[1,:], 
                       legend_label="Power Trace", 
                       line_width=2)
hover = HoverTool(tooltips=[("Time", "$x"), ("Power", "$y")])
reduced_power_traces_plot.add_tools(hover)
show(reduced_power_traces_plot)

##################################################
############ EXERCISE 2 - Key Recovery ###########
##################################################

# CPA Steps:
    # Key Guess
    # Hypothesis (compute intermediate value)
    # Correlation
    # Correct Key byte (highest correlation)

tic = time.perf_counter()
logging.info("Starting CPA")

# Your CPA goes here

toc = time.perf_counter()
logging.info(f"CPA done in {toc - tic:0.4f} seconds")
logging.info(f"Solved Key: {solvedKey}")
# Key in hex
print([hex(int(s)) for s in solvedKey[0]])