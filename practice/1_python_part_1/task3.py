"""
Write function which receives list of text lines (which is space separated words) and word number.
It should enumerate unique words from each line and then build string from all words of given number.
Restriction: word_number >= 0
Examples:
    >>> build_from_unique_words('a b c', '1 1 1 2 3', 'cat dog milk', word_number=1)
    'b 2 dog'
    >>> build_from_unique_words('a b c', '', 'cat dog milk', word_number=0)
    'a cat'
    >>> build_from_unique_words('1 2', '1 2 3', word_number=10)
    ''
    >>> build_from_unique_words(word_number=10)
    ''
"""
from typing import Iterable


def build_from_unique_words(*lines: Iterable[str], word_number: int):
    #Convert input tuple into list
    list(lines)
    unordered_list = []
    ordered_list = []
    my_str = []

    #Check if the list has values if not return ''
    if any(lines):
        for elem in lines:
            unordered_list.append(elem.split(" "))

    #We get rid of duplicated values
    for lists in unordered_list:
        ordered_list.append(list(dict.fromkeys(lists)))

    #Check if the word_numbers it's greater than 0 and lower than our len(list)
    if word_number >= 0 and word_number <= len(ordered_list):
        for value in ordered_list:
            if value[word_number] != '':
                my_str.append(value[word_number:word_number+1])
    else:
        my_str.append('\'\'')

    return " ".join([elem for subelem in my_str for elem in subelem])


print(build_from_unique_words('a b c', '1 1 1 2 3', 'cat dog milk', word_number=1))
print(build_from_unique_words('a b c', '', 'cat dog milk', word_number=0))
print(build_from_unique_words('1 2', '1 2 3', word_number=10))
print(build_from_unique_words(word_number=10))