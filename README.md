# brakingtests_railways
This repository contains Python scripts for analyzing and visualizing standardized braking test performance in railway systems. The tool processes CSV data from braking tests, calculates key parameters according to industry standards (GMRT2045), and generates visual representations of test results 

## Features:
- Automatic processing of multiple CSV test files
- Calculation of critical braking parameters (distances, velocities)
- Statistical analysis of test dispersion
- Visualization of results against standard requirements
- Support for different braking systems (B7 and EB in EMUs)

## Requirements:
- Python 3.x
- Libraries: numpy, pandas, matplotlib

## Input Data Format
The tool requires CSV files with the following specifications:
- Delimiter: Semicolon (;)
- Encoding: Latin-1
- Required columns:
  - `Tiempo Pulsador`: Time values for braking events
  - `Velocity`: Speed values in km/h
  - `Distancia`: Distance values in meters
  - `CIL KPA`: Cylinder pressure in kPa (used to identify brake type)

The CSV files should be placed in a single directory. The tool will automatically categorize tests as either B7 or EB type based on the maximum pressure value.

## How to Use
1. Download or clone this repository
2. Place your CSV test files in a directory
3. Run the included `.bat` file
4. When prompted, enter the full path to the directory containing your CSV files
5. The script will process all valid CSV files and generate the analysis

## Output
The tool will generate:
- A graph named `GMRT2045_plot.png` in the directory of CSV files
- The plot includes:
  - Braking performance for both B7 and EB systems
  - Reference curves according to GMRT2045 standard
  - Tolerance bands for acceptable performance (15%)
  - Actual test results plotted against requirements

## Example
![GMRT2045_plot](https://github.com/user-attachments/assets/4ed12e78-87de-4658-ab19-0f7f77b7831c)
