# NPRE247-Computer Project 1
### Contents:
- Instruction Manual (README.md)
- Project report (NPRE247 ComProj 1.pdf)
- Assignment requirements (NPRE247 ComProj 1 Instructions.pdf)
- Code (NPRE247 ComProj 1 Code.py)
- Input CSV (kepdecayinput.csv)
- Output CSVs ('kepdecayoutput.csv','kepdecayoutput_t0.5.csv','kepdecayoutput_t0.1.csv')

### How to use the code:
1. Download the Input CSV, Output CSVs, and Code to the same folder.
- To change the tfinal value (determines how long to simulate decay):
  Edit tfinal in line 2 of the Input CSV.
- To change the iterlength value (determines how many timesteps per unit of time, I.E 10 steps per 1 hour vs 1 step per 1 hour):
  Edit iterlength in line 2 of the Input CSV.
2. Run the code <ins>from the folder it is located in</ins> with desired values.
The code has three modes of operation:
- Graphing Numerical: graphs the numerical solution (press n when it asks).
- Graphing N_B trials: graphs the N_B deltaT trials normally (press y then n when it asks).
- Graphing N_Bmax trials: graphs the N_B max trials (press y both times it asks).
