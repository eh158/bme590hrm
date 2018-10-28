# bme590hrm

The file HRM.py simulates a heart rate monitor. It takes the input of a .csv file containing ECG information and generates a dictionary named metrics containg the mean heart rate per minute, voltage extremes, time duration, the number of beats, and the times at which each beat occurred.  This information is then output as a .json file with the same name as the original .csv file.

To use this program, please set up a virtual environment with the packages specified in the requirements.txt file. After that, the file will be able to run. When running, the program will ask for a file name and a time interval to calculate mean heart rate. The program will keep prompting the user until the user enters a .csv file that is in the same directory and a positive time value. It will then process the .csv file and store the information in a .json file that will be saved in the same directory.
