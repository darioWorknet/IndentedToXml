file = 'test.txt'   # File to be read
level = 0           # Starting level
xml_str = ''        # Output string
not_closed = []     # LIFO list
levels = dict()     # To store the level of each label
separator = ' --- ' # To be printed between labels


def leading_spaces(s):
    ''' Count leading spaces in string '''
    return len(s) - len(s.lstrip())


def to_xml(str, close=False, aligned=False):
    ''' Given a string converts it to xml format '''
    if close:
        n = levels[str.strip()]
        if aligned:
            return separator + "</" + str.strip() + ">"
        return (' ' * n) + "</" + str.strip() + ">"

    return (' ' *level) + "<" + str.strip() + ">"





if __name__ == '__main__':
    # Open file and iterate lines
    with open(file, 'r') as f:
        for line in f:

            # If line empty go to next iteration
            if line.strip() == "":
                continue
            
            # Store level
            level = leading_spaces(line)
            levels[line.strip()] = level

            # MAIN LOGIC =========================================================
            # If it is the first item -> add line to output and append to not_closed
            if level == 0:
                xml_str += to_xml(line) + '\n'
                not_closed.append(line)

            # If entering a level -> add prev line to output, add line to output
            # and append it to not_closed
            elif level > prev_level:
                xml_str += to_xml(line) + '\n'
                not_closed.append(line)

            # If we are in the same level -> close previous level
            elif level == prev_level:
                xml_str = xml_str[:-1]
                prev = not_closed.pop()
                xml_str += to_xml(prev, close=True, aligned=True) + '\n'

                xml_str += to_xml(line) + '\n'

                not_closed.append(line)

            # If we exit the level -> check how many levels have we exited
            # close them all. Add line to output and append to not_closed
            elif level < prev_level:
                xml_str = xml_str[:-1]
                align = True
                for i in range((prev_level - level) // 4 + 1):
                    prev = not_closed.pop()
                    xml_str += to_xml(prev, close=True, aligned=align) + '\n'
                    align = False

                xml_str += to_xml(line) + '\n'

                not_closed.append(line)

            # Store previous level
            prev_level = leading_spaces(line)


    # Close last opened labels
    xml_str = xml_str[:-1]
    align = True
    for label in reversed(not_closed):
        xml_str += to_xml(label, close=True, aligned=align) + '\n'
        align = False 

    # Final output
    print(xml_str)