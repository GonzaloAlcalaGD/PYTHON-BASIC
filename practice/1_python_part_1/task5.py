"""
Write function which receives line of space sepparated words.
Remove all duplicated words from line.
Restriction:
Examples:
    >>> remove_duplicated_words('cat cat dog 1 dog 2')
    'cat dog 1 2'
    >>> remove_duplicated_words('cat cat cat')
    'cat'
    >>> remove_duplicated_words('1 2 3')
    '1 2 3'
"""


def remove_duplicated_words(line: str):
    my_list = line.split()
    new_str = []
    for elem in list(dict.fromkeys(my_list)):
        new_str.append(elem)
    return " ".join(new_str)
print(remove_duplicated_words('cat cat dog 1 dog 2'))
print(remove_duplicated_words('cat cat cat'))
print(remove_duplicated_words('1 2 3'))