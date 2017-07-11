# Convert Multi2Sim results into McPAT configuration
## The problem
Multi2Sim (sometimes referred as m2s) has been adapted to provide some of the statistics that McPAT requires in its input file. The correspondence between the multi2sim statistics and mcpat input parameters is given in Appendix II of the Multi2Sim (v4.2) manual, however Multi2Sim does not provide any tool to generate the McPAT input file automatically, which means that for every simulation we should manually copy the values from the m2s result file to the mcpat input configuration file; this process should be automatized.

## The solution
The script m2s-to-mcpat.py takes at least 3 arguments when executed

Convert Multi2Sim results files into McPat XML input format
