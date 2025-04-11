# PH Probe Instructions

**The E-201-C sensor is not suitable for continuous deployment**, it should only be used to sporadically measure PH when refining water.

The PH-Probe has to be calibrated using `calibrate_ph.py`\

1. Connect the probe to the normalizer board.
2. Connect the normalizer board to the control-PCB.
3. Run the `calibrate_ph.py` script on the controller.
4. Put the probe into a solution with a known PH.
5. Use the potentiometer on the normalizer board to adjust the PH output to match the solution's PH.
