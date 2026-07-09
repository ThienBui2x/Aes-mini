# Correlation Power Analysis Attack — Python Implementation

#### This project provides a Python-based implementation of a **Correlation Power Analysis (CPA) attack**

---
## Setup your python environment

### Python Version
```bash
python3.12
```

### Python Virtual Environment 
```bash
python3.12 -m venv <name-your-virtual-env>
```
### Activate the virtual environment 
```bash
source <name-your-virtual-env>/bin/activate
```
### Install the necessary python libraries
```bash
pip install numpy

pip install bokeh
```
# Options you may run the code either in terminal, or spyder

## Before you run ensure the project structure to look like this
```text
cpa/
│
├── cpa.py       # Main script for performing the CPA attack
├── load.py      # Module for loading power traces and plaintext data
├── ham_w.py     # Module for computing Hamming weights (Lookup table)
├── env.py       # Python file that has the paths to the traces,plaintexts,ciphertexts
├── traces/      # (Optional) Directory containing input trace and 
└── README.md    # Documentation (this file)
```
## Running the code in terminal (option 1)
```bash
python cpa.py 
```
## Running the code on spyder (option 2)
```bash
# Spyder lets you view the variable data stored during/after completion of the running of code (Similar to the idea of workspace in MATLAB)
# First install spyder
pip install spyder

# Launch Spyder
spyder
```

1. Navigate to the folder containing the cpa.py file
2.  Hit on run file or f5

## Output
1. Power Traces plots 
2. Solved Key

## Deactivate Virtual Environment
When finished, deactivate the environment:
```bash
deactivate
```
