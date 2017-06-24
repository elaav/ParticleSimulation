# ParticleSimulation
This project was writen in order to make the particles simulation
for TAU lab C easier, and concentrate on the physics.

## Pre-installation
Connect to your TAU linux shell from the "MobaXterm" application
in https://remoteapp.tau.ac.il.
Then connect to the physics server with the following command:
```
$ ssh -X gp.tau.ac.il
```
Create the gimel folder as specified in the lab instructions:
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
#### Calibration
In order produce calibration measurements with electron:
```
$ python calibration_injects.py -p electron
```
#### General Injects
In order to inject k0 short:
```
$ python injects.py -p k-short
```