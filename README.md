# Convert Multi2Sim results into McPAT configuration
## Quick summary
 - **Purpose of the script**: take one or multiple statistics output files obtained after simulating a certain application with Multi2Sim, and convert them into McPAT XML input configuration format
 - **Input files**: `<McPATTemplateFile.xml>` to define the structure of the desired McPAT configuration file, `<m2sInputFileN>` to provide the statistics obtained from Multi2Sim
 - **Output file**: `<McPATOutputFile.xml>` is the McPAT XML configuration file, which is ready to be passed as argument in a McPAT simulation
 - **How to execute**: `python m2s-to-McPAT.py <McPATTemplateFile.xml> <McPATOutputFile.xml> <m2sInputFile1> [<m2sInputFile2> ... <m2sInputFileN>]`

## Motivation: why do we need this script?
Multi2Sim (also referred as m2s) has been adapted to provide some of the statistics that McPAT requires in its input file. The correspondence between the Multi2Sim statistics and McPAT input parameters is given in Appendix II of the Multi2Sim (v4.2) manual. However, Multi2Sim does not provide any tool to generate the McPAT input file automatically, which means that for every simulation we ought to manually copy the values from the m2s result file to the McPAT input configuration file; **this process should be automatized**.

## The solution: how does this script work?
### Step 1: obtaining from Multi2Sim
When we run a simulation on m2s we can indicate to save the output results into different files, i.e. processor, memory and network. Each of these contains different sections (usually one per component simulated, plus some global statistics), and every section contains multiple pairs of parameters/values. Example (from a processor output):

    [ Global ]
    Cycles = 251285895
    Time = 18604.76
    CyclesPerSecond = 13507
    MemoryUsed = 45395968
    ...
    Dispatch.Total = 5572371475
    ...

    [ Config.BranchPredictor ]
    Kind = TwoLevel
    BTB.Sets = 256
    BTB.Assoc = 4
    ...

    [ ... ]
    ...

In our script, the first thing we do is parse all the m2s results files provided, and separate them into sections. Additionally, every section is also separated into the multiple pairs of parameters/values. This structure is saved using a dictionary inside another dictionary, and the process is defined in the function `parser()` of the code.

### Step 2: converting to McPAT
McPAT requires an XML configuration file to run a simulation, which looks like this:

    <component id="system.core0" name="core0">
    	<param name="clock_rate" value="1000"/>
    	...
    	<stat name="total_instructions" value="400000"/>
    	<stat name="int_instructions" value="200000"/>
    	...
    <component id="system.core0.icache" name="icache">
    	...
    	<stat name="read_accesses" value="200000"/>
    	<stat name="read_misses" value="100000"/>
    	...
    <component id="system.core0.dcache" name="dcache">
    	...
    	<stat name="read_accesses" value="200000"/>
    	<stat name="read_misses" value="1000000"/>
    	...

As we explained before, the problem is that changing the value of every `stat` in the file at every execution of m2s is arduous.
So, in our second step, and now that all the values that we are trying to export from m2s into McPAT are saved and organized into memory, we have to fill the McPAT configuration template with them.
To do that, we check every line of the McPAT template file, and if it contains a `stat` we look for its correspondence parameter name into a translation table called `corresp_McPAT_to_m2s` (previously defined by the user in the code). If there is a match, we search the translated parameter name in the dictionary created during the parsing process (Step 1), we save the value into a temporal variable, and we use it to write the line into the output McPAT configuration file, using the same format as in the template; which is:

    <stat name="corresponding name from m2s" value="value from m2s"/>
The rest of the lines from the template (the ones not containing a `stat`), are copied verbatim from the template to the output file.

### Usage
*(if argument files are in different folder than current working directory, make sure to specify the path to each of them)*

	shell> python m2s-to-McPAT.py <McPATTemplateFile.xml> ...
			<McPATOutputFile.xml> <m2sInputFile1> [<m2sInputFile2> ...
			<m2sInputFileN>]

The script `m2s-to-McPAT.py` takes at least 3 arguments when executed:

 - `McPATTemplateFile.xml` is the actual configuration template that we are planning to use as input to McPAT. This file must contain all the components, parameters and stats that we plan to simulate on McPAT. *This file will not be modified by this script.*
 - `McPATOutputFile.xml` will be the resulting configuration file after the template is filled with all the values from the Multi2Sim results file. ***This is the file that we can later use to run McPAT.***
 - `m2sInputFileN` contains the different sections and parameter values that Multi2Sim provides at the end of each simulation. *If multiple files are provided, they will all be treated as a single file, so **make sure that there are no duplicated sections between them.***

### Example
This example shows a possible case where we might have run the Raytrace benchmark on Multi2Sim, and saved the results of the processor and memory components into `m2s_raytrace_results_proc.txt` and `m2s_raytrace_results_mem.txt`; which could look something like this,

`m2s_raytrace_results_proc.txt`:

    [ Global ] <--- Information relative to all cores
    Cycles = 251285895 <--- we want this parameter
    Time = 18604.76
    CyclesPerSecond = 13507
    ...

    [ c0 ] <--- Information relative to the first core
    ...
    Dispatch.Total = 5572371475 <--- we want this parameter
    ...

    [ ... ]
    ...

`m2s_raytrace_results_mem.txt`:

    [ il1-0 ] <--- L1 instruction cache
    Sets = 256
	Assoc = 2
	...
	Reads = 3016215 <--- we want this parameter
	...

	[ l1-0 ] <--- L1 data cache
    Sets = 256
	Assoc = 2
	...
	Reads = 3897354 <--- we want this parameter
	...
Notice that in each file, some of the sections contain the parameters that we want to convert to McPAT. Specifically, in this case we want the parameter `Cycles` from the `Global` section, the `Dispatch.Total` from `c0`, and the L1 instruction and data `Reads` from `il1-0` and `l1-0` respectively.
The value of these parameters will fill their corresponding `stat`, on a McPAT template that might look like this,

`McPAT_xeon_template.xml`:

    <component id="system" name="system">
    	<param name="number_of_cores" value="4"/>
    	<param name="temperature" value="380"/>
    	...
    	<stat name="total_cycles" value=""/> <--- we want to fill this stat
    	...
    <component id="system.core0" name="core0">
    	...
    	<stat name="total_instructions" value=""/> <--- we want to fill this stat
    	...
    <component id="system.core0.icache" name="icache">
    	...
    	<stat name="read_accesses" value=""/> <--- we want to fill this stat
    	...
    <component id="system.core0.dcache" name="dcache">
    	...
    	<stat name="read_accesses" value=""/> <--- we want to fill this stat
    	...

Once the McPAT template is ready we make sure that the `corresp_McPAT_to_m2s` translation table (found at the beginning of `m2s-to-McPAT.py`) has the pairs corresponding to our example, which are:

    corresp_McPAT_to_m2s = {
	    "system->total_cycles":               "Global->Cycles",
	    "system.core0->total_instructions":   "c0->Dispatch.Total",
	    "system.core0.icache->read_accesses": "il1-0->Reads",
	    "system.core0.dcache->read_accesses": "l1-0->Reads"
	    }
Notice that for every entry, the "component->stat_name" in the left column refers to a stat in the McPAT template, and the "section->param_name" in the right column refers to its corresponding parameter in the m2s results file.

**NOTE: If a stat is not defined in the McPAT template (e.g. `<stat name="XX" value "">`), it will not be imported from m2s it even if it has an entry in `corresp_McPAT_to_m2s`**. This is because the template is what determines what stats should be simulated, and the script should not overwrite that structure.

**NOTE: If a stat has no entry in `corresp_McPAT_to_m2s`, it will not be imported from m2s**. This is because the conversion between m2s and McPAT is ought to be defined in the script, therefore if there is no translation entry for that `stat` we can assume that the user does not want to import that value from m2s (and potentially use the one defined in the template instead).

Now everything is ready, so we execute the script:

	shell> python m2s-to-McPAT.py McPAT_xeon_template.xml ...
			McPAT_xeon_raytrace.xml m2s_raytrace_results_proc.txt ...
			m2s_raytrace_results_mem.txt
*(assuming all argument files are within the same folder, which is the current working directory)*

This results into the creation of a file called `McPAT_xeon_raytrace.xml`, which will be the one used as input to McPAT, and has the following structure,
`McPAT_xeon_raytrace.xml`:

    <component id="system" name="system">
    	<param name="number_of_cores" value="4"/>
    	<param name="temperature" value="380"/>
    	...
    	<stat name="total_cycles" value="251285895"/> <--- value obtained from m2s
    	...
    <component id="system.core0" name="core0">
    	...
    	<stat name="total_instructions" value="5572371475"/> <--- value obtained from m2s
    	...
    <component id="system.core0.icache" name="icache">
    	...
    	<stat name="read_accesses" value="3016215"/> <--- value obtained from m2s
    	...
    <component id="system.core0.dcache" name="dcache">
    	...
    	<stat name="read_accesses" value="3897354"/> <--- value obtained from m2s
    	...
**NOTE: after executing the script, check the shell/terminal for any possible errors.** The most common error will say something like `ERROR: Section->Parameter not found in m2s dictionary`, which means that there was a McPAT `stat` whose translation did not match with any of the parameters obtained from the m2s result files. Make sure that the corresponding entry in `corresp_McPAT_to_m2s` is correct and the parameter actually exist in the m2s input file.
<!--### Implementation details
talk about the dictionary inside a dictionary, the global variables, etc.-->


> Written with [StackEdit](https://stackedit.io/).
