# OxygraphAnalysis

#Analysis package for SBP with treatment of NADH, ADP, CCCP, Complex 1 Inhibitor. Sections slopes and allows for manual curve fitting. Exports figures for slope and excel sheet of slope values and basic statistical information. Graphs total Oxygraph after initial induction.

#Open OA2.py file and navigate to depository file that contains a file with all your data formated. Directory should look like ~/workingdir/Datadir and navigate to ~/workingdir .
See example excel sheet on how to format data. Please have data files as excel sheets, if not change pd.read_excel(name) to pd.read_csv(name). 

#Once script is opened it will prompt for the name of the data file and create figure directories in the working directory. Next the slopes of each section will occur. It will prompt for how many points to remove from the left and then the right. If you accept input 0 and 0 and the figure will save. Once the slope analysis has been performed on all slopes a bar chart of average values with standard error will be reported and saved. At this time there is no way to 'go back' if too many points are removed be cautious with your analysis.
