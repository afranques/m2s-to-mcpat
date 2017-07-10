import sys
import re

# regexp to find the title of a section, like "[ Config.General ]"
section_title_regex = re.compile( r"\[ ([^\s\]]+) \]" )

# global variable to keep track of what section are we parsing now
current_section = None

def parser( line, m2s_sections ):
    global current_section

    # if we find a section title
    section_title = section_title_regex.match( line )
    if section_title:
        # DEBUG: print section_title.group(1)
        # we create a new pair into the m2s_sections dictionary, where
        # the key is the section title and the value is another dictionary,
        # which will contain all pairs of parameters/values for that section
        m2s_sections[section_title.group(1).strip()] = {}
        current_section = section_title.group(1).strip() # we update the current section name
    # otherwise we are still inside a section
    else:
        try:
            # this will fail if there's no pair of "param = value" in the line
            param_name, param_value = line.split("=")
        except ValueError:
            pass
        else:
            # DEBUG: print param_name.strip(), param_value.strip()
            if current_section is not None:
                # we define a new entry where the key is the name of the parameter, and we also assign its value
                m2s_sections[current_section][param_name.strip()] = param_value.strip()










if __name__ == '__main__': #this is how the main function is called in python
    # Command to execute this code: shell> python <nameOfThisFile>.py <m2sInputFile> <mcpatTemplateFile> <mcpatOutputFile>
    # This program takes a Multi2Sim results file, it reads the components it needs for McPat, it makes a copy of the mcpat template file
    # and it overwrites that copy with the components indicated.

    filename = sys.argv[1] # first argument is m2sInputFile
    m2s_sections = {} # this dictionary will contain one row per every section in the m2s results file

    # we read m2sInputFile one line at a time (this will automatically close the file at the end)
    with open(filename) as infile:
        for line in infile:
            parser(line, m2s_sections)
