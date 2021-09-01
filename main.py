file = 'test.txt'
level = 0
xml_str = ''
not_closed = [] # LIFO list

def count_spaces(str):
    for i, c in enumerate(str):
        if c != " ":
            return i

def to_xml(str, close=False, aligned=False):

    if close:
        n = levels[str.strip()]
        if aligned:
            return (' --- ') + "</" + str.strip() + ">"
        return (' ' * n) + "</" + str.strip() + ">"

    return (' ' *level) + "<" + str.strip() + ">"



levels = dict()


with open(file, 'r') as f:
    for line in f:
        # If line empty go to next iteration
        if line.strip() == "":
            continue

        level = count_spaces(line)
        levels[line.strip()] = level

        # If we exit the level
        if level == 0:
            xml_str += to_xml(line) + '\n'
            not_closed.append(line)

        # If we exit the level
        elif level < prev_level:
            xml_str = xml_str[:-1]
            align = True
            for i in range((prev_level - level) // 4 + 1):
                prev = not_closed.pop()
                xml_str += to_xml(prev, close=True, aligned=align) + '\n'
                align = False
            # New one open
            xml_str += to_xml(line) + '\n'
            # Append to list
            not_closed.append(line)


        # If we enter the level -> print actual line and append it to the list
        elif level > prev_level:
            xml_str += to_xml(line) + '\n'
            not_closed.append(line)

        # If we are in the same level
        elif level == prev_level:
            # Close previous at the same level
            xml_str = xml_str[:-1]
            prev = not_closed.pop()
            xml_str += to_xml(prev, close=True, aligned=True) + '\n'
            # Print new one
            xml_str += to_xml(line) + '\n'
            # Not closed this one yet
            not_closed.append(line)

        prev_level = count_spaces(line)




# Close opened labels
xml_str = xml_str[:-1]
align = True
for label in reversed(not_closed):
    xml_str += to_xml(label, close=True, aligned=align) + '\n'
    align = False 

print(xml_str)