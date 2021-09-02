import os

# Config
file = 'IMO.txt'   # File to be read

# Global variables
prev_level = -1     # Starts at -1, so that it could be considered entering a level in the first line
level = 0           # Starting level
xml_str = ''        # Output string
not_closed = []     # LIFO list
levels = dict()     # To store the level of each label
SEPARATOR = ' --- ' # To be printed between labels
values = dict()     # To store values of each label
variables = dict()  # To store variables of each line



def leading_spaces(line):
    ''' Count leading spaces in string '''
    return len(line) - len(line.lstrip())


def open_xml(label):
    ''' Returns label between angle brackets.
    If label has variables, insert them between brackets too '''
    if variables[label]:
        var = ' ' + variables[label]
    else:
        var = ''
    return (' ' *level) + "<" + label + var + ">"


def close_xml(label, aligned=False):
    ''' Returns label between closing angle brackets.
    If  closing label goes in the same line of it's label pair, it admits values between labels.
    Otherwise, it goes alone in the next line and will be indented to the specified level '''
    global levels
    n = levels[label]
    if aligned:
        if values[label]:
            value = ' ' + values[label] + ' '
        else:
            value = SEPARATOR
        return value + "</" + label + ">"
    # If next line -> indent
    return (' ' * n) + "</" + label + ">"


def get_vars_vals(line, label):
    ''' Updates global dictionaries with values and variables '''
    global variables, values
    line_lst = line.split(' ')
    line_vals = []
    line_vars = []
    for l in line_lst[1:]: # Discard the first element, which is the label
        if '=' not in l and len(l)>1: # Its a value
            line_vals.append(l)
        elif len(l)>1:
            line_vars.append(l)

    values[label] = ' '.join(line_vals)
    variables[label] = ' '.join(line_vars)


def iterate_lines(file):
    ''' Yield each line of the file '''
    with open(file) as f:
        for line in f:
            yield line


def switch_extension(file, new_extension):
    ''' Return the filename with the new extension '''
    return os.path.splitext(file)[0] + new_extension




if __name__ == '__main__':

    for line in iterate_lines(file):

        # If line empty go to next line
        if line.strip() == "":
            continue
        
        # Store label and level
        label = line.strip().split()[0]
        level = leading_spaces(line)
        levels[label] = level

        # Storing variables and values
        get_vars_vals(line.strip(), label)

        # MAIN LOGIC =========================================================
        # If entering a level -> add label to output
        if level > prev_level:
            xml_str += open_xml(label) + '\n'

        # If we are in the same level -> close previous label
        elif level == prev_level:
            xml_str = xml_str[:-1]
            prev = not_closed.pop()
            xml_str += close_xml(prev, aligned=True) + '\n'

            xml_str += open_xml(label) + '\n'

        # If we exit the level -> check how many levels have we exited
        # close them all. Add label to output and append it to not_closed
        elif level < prev_level:
            xml_str = xml_str[:-1]
            align = True
            for i in range((prev_level - level) // 4 + 1):
                prev = not_closed.pop()
                xml_str += close_xml(prev, aligned=align) + '\n'
                align = False

            xml_str += open_xml(label) + '\n'

        # Store previous label and level
        prev_level = level
        not_closed.append(label)


    # Close last opened labels
    xml_str = xml_str[:-1]
    align = True
    for label in reversed(not_closed):
        xml_str += close_xml(label, aligned=align) + '\n'
        align = False 

    # Store in file
    new_file = switch_extension(file, '.xml')
    with open(new_file, 'w') as f:
        f.write(xml_str)

    # Delete extension from file
    os.rename('output.xml', file[:-4] + '.xml')

    # Final output
    print(xml_str)