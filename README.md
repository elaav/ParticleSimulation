# ParticleSimulation
This project was writen in order to make the particles simulation
for TAU lab C easier, and concentrate on the physics.

## Pre-installation
Connect to your TAU linux shell and create the gimel folder as
specified in the lab instructions:
```
$ /var/misc/phys/setup
```

## Installation
Copy all files in this project to the gimel directory.
The main scripts are "calibration_injects.py" and "injects.py",
and both of them have a very helpful help menu:
```
$ python injects.py -h
```

## Examples
In order produce calibration measurements with electron:
```
$ python calibration_injects.py -p electron
```

In order to inject k0 short:
```
$ python injects.py -p k-short
```