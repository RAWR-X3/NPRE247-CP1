# NPRE247-Computer Project 1
### Contents:
- Instruction Manual (README.md)
- Assignment (NPRE247 ComProj 1 Instructions.pdf)
- Code (NPRE247 ComProj 1 Code.py)
- Input CSV (kepdecayinput.csv)
- Output CSV (kepdecayoutput.csv)

### How to use the code:
1. Download the Input CSV, Output CSV, and Code to your C: drive.
- To change the tfinal value (determines how long to simulate decay):
  Edit tfinal in line 2 of the Input CSV.
- To change the iterlength value (determines how many timesteps per unit of time, I.E 10 steps per 1 hour vs 1 step per 1 hour):
  Edit iterlength in line 31 (under the #config section) of the Code.
2. Run the code twice with desired values as I was unable to isolate the error causing it to seemingly finish outputting early before it finished graphing all values.
  (this was worked around by using r+ to write the file such that the next run using the same value can read the finished previous run's finished results)
