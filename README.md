---
# About the project
This repository contains program with simple graphical interface based on WX. Task of this program is to create dotplot from FASTA sequences.


Program has been created as part of completing my study subject.

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
Interface is launched from gui.py file. To start program you need to load fasta sequences by clicking "Wczytaj sekwencje" button. You can find example fasta files in NCBI base. When data is loaded you have to choose which 2 sequences (they can be the same sequences) do you wanna use to make dot plot by "Dodaj do dot-plota" button. Then u have to set basic parameters as a size of window and threshold (for short seqences <1000 bp, size of window=3 and threshold=3 should be good). When these parameters are set you can start the program by clicking "Stwórz dot-plot" button.
