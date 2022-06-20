"""
Read files from ./files and extract values from them.
Write one file with all values separated by commas.

Example:
    Input:

    file_1.txt (content: "23")
    file_2.txt (content: "78")
    file_3.txt (content: "3")

    Output:

    result.txt(content: "23, 78, 3")
"""


def read_files(files):
    result = []
    for file in files:
        with open(file, 'r') as f:
            result.append(f.read())
    with open('file.txt', 'w') as file:
        file.write(','.join(result))

print(read_files(['./files/file_1.txt', './files/file_2.txt', './files/file_3.txt']))