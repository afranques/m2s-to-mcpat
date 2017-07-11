# Convert Multi2Sim results into McPAT configuration
## The problem
Multi2Sim (sometimes referred as m2s) has been adapted to provide some of the statistics that McPAT requires in its input file. The correspondence between the multi2sim statistics and mcpat input parameters is given in Appendix II of the Multi2Sim (v4.2) manual, however Multi2Sim does not provide any tool to generate the McPAT input file automatically, which means that for every simulation we should manually copy the values from the m2s result file to the mcpat input configuration file; this process should be automatized.

## The solution
### Step 1
When we run a simulation on m2s we can indicate to save the output results into different files, i.e. processor, memory and network. Each of these contains different sections (usually one per component simulated, plus some global statistics), and every section contains multiple pairs of parameters/values. Example (from a processor output):

    [ Global ]
    Cycles = 251285895
    ROI Cycles = 159082946
     (from 92147509 to 251230455)
    Time = 18604.76
    CyclesPerSecond = 13507
    MemoryUsed = 45395968
    MemoryUsedMax = 271998976
    ...

    [ Config.BranchPredictor ]
    Kind = TwoLevel
    BTB.Sets = 256
    BTB.Assoc = 4
    Bimod.Size = 1024
    ...

    [ ... ]
    ...

In our script, the first thing we do is parse all the m2s results files provided, and separate them into sections. Additionally, every section is also separated into the multiple pairs of parameters/values. This structure is saved using a dictionary.

### Step 2


### Example
The script m2s-to-mcpat.py takes at least 3 arguments when executed:

 - `m2sInputFileN` contains the different sections and parameter values that multi2sim provides at the end of each simulation. If multiple files are provided as arguments, they will all be treated as a single file, so make sure that there are no duplicated sections between them.
 - `mcpatTemplateFile.xml` is the actual configuration template that we are planning to use as input to mcpat. This file must contain all the components, parameters and stats that we plan to simulate on mcpat. *This file will not be modified by this script.*
 - `mcpatOutputFile.xml` will be the resulting configuration file after the template is filled with all the values from the multi2sim results file. *This is the file that we can later use to run mcpat.*

### Implementation details
talk about the dictionary inside a dictionary, the global variables, etc.


> Written with [StackEdit](https://stackedit.io/).
