---
# About the project
This repository contains a program with simple graphical interface based on WX. Task of this program is to create a dotplot from FASTA sequences.


Program has been created as a part of completing my study subject.

---
# Requirements
Program requires the following libraries:
- csv
- datetime
- math
- matplotlib
- os
- wxPython

---
# How to run program
![menu](/readme_imgs/menu.png)

The interface is launched from the 'gui.py' file. To start the program, you need to load FASTA sequences by clicking button number 3. Properly loaded sequences should appear in list number 1. You can delete them from the program by pressing button number 4. Example FASTA files can be found in the NCBI database.

Once the data is loaded, you need to set the analysis parameters in section number 5. First, set the basic parameters such as the window size (1st parameter) and the threshold (2nd parameter). For short sequences <1000 bp a window size of 3 and a threshold of 3 should work well. The 3rd parameter denotes the number of the first nucleotide to be aligned from the first sequence, and the 4th parameter is the number of the first nucleotide to be aligned from the second sequence.

In section number 6, you can change the alignment method. Section number 7 allows you to activate and configure serial analysis, enabling multiple analyses after a single launch, generating varied settings for window size and threshold each time. Next, select the two sequences (which can be the same) to create a dot plot by clicking button number 8. To reverse this action, use button number 9.

Once everything is configured, start the program by clicking button number 10.
