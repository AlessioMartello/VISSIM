# VISSIM

A Python program to automate the analysis of output data from [PTV VISSIM](https://www.ptvgroup.com/en/solutions/products/ptv-vissim/) traffic simulation software.

## Description

Data analyis is currently performed on .lsa .rsz and .aXX files, output by VISSIM. The program yields three separate .xlsx files, saved in the respective /data/outputs folder. 

## Getting Started

### Dependencies

* Python 3.8
* Windows 10 OS
* For libraries see requirements.txt
* Recommended using Spyder (Anaconda) for all dependencies readily available.

### Installing

* Download the program.
* Modify the file VISSIM/data/inputs/excel/"Demand_dependancy.xlsx" according to the instructions inside the file.
* Put all the data outputs from VISSIM into the  VISSIM/data/inputs directory.

## Executing the program

* Navigate to gui.py
* Execute file.

### Usage
* Select the desired analyses from the checkboxes.
* If Saturation flow anlysis is to be performed, enter the maximum acceptable headway in the entry box.
* Locate the folder containing the appropriate data.
* Click run.
* Results will be output into the "outputs" folder.

## Help

* If the demand dependency output returns populated with 0's, ensure the Demand_dependency.xlsx is correctly populated, with your chosen Demand Dependant stages (see point two of "Installing" section above)

## Authors

Alessio Martello

## Contributions

Pull requests welcome.

## License

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

*[MIT license](http://opensource.org/licenses/mit-license.php)*
* See LICENSE.md for details.

## References 
* For details of VISSIM Data see: https://www.et.byu.edu/~msaito/CE662MS/Labs/VISSIM_530_e.pdf