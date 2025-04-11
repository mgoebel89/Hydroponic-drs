# This folder contains source files for different usecases

- `time_control.py` is ment to periodicaly fill the container and let it empty out.
  - the time it takes to fill and empty have to be measured and updated in the code manually.
  - `time_on` should be just over the time it takes for the container to start draining.
  - `time_off` should be set to the time it takes for the system to drain added to the time you want between system flushes
  - sugested flush timing, once every 30 minutes
- `calibrate_ph.py` for usage see [PH-Probe](../parts/PH-Probe.md)
- `fill_sense_control.py` is a more sophisticated version of `time_control.py` that detects waterlevel and automatically fills the container when it is empty and stops when it is full.
  - for instructions on how to set up the sensor see [FillSense](../construction/FillSense.md)