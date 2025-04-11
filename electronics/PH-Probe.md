**The E-201-C sensor is not suitable for continous depployment**, it should only be used to sporadicaly measure PH when refining water.

The PH-Probe has to be calibrated using `calibrate_ph.py`\
1. connect the probe to the normalizer board
2. connect the normalizer board to the control-PCB
3. Run the `calibrate_ph.py` skript on the controler
4. Put the probe into a solution with a known PH
5. Use the potentiometer on the normalizer board to adjust the PH output to matcht the solutions PH