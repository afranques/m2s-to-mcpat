import sys
import re

# regexp to find the title of a section, like "[ Config.General ]"
section_title_regex = re.compile( r"\[ ([^\s\]]+) \]" )

def parser( line, results_sections ):
    section_title = section_title_regex.match( line )
    if section_title:
        print section_title.group(1)
    else:
        try:
            param_name, param_value = line.split("=")
        except ValueError:
            pass
        else:
            print param_name.strip(), param_value.strip()









if __name__ == '__main__': #this is how the main function is called in python
    # Command to execute this code: shell> python <nameOfThisFile>.py <m2sInputFile> <mcpatTemplateFile> <mcpatOutputFile>
    # This program takes a Multi2Sim results file, it reads the components it needs for McPat, it makes a copy of the mcpat template file
    # and it overwrites that copy with the components indicated.
    filename = sys.argv[1] #the argument of the python call will be the name of the source code file
    results_sections = {}
    with open(filename) as infile:
        for line in infile:
            parser(line, results_sections)
