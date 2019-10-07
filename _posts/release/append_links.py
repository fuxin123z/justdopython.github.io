import os


root = os.getcwd()
ignore_list = ["2019-09-16-python-web-014.md",
                "2019-09-24-python-web-jinjia-020.md",
                ]

def get_filelists(file_dir):
    list_direction = os.listdir()
    filelists = []
    for direction in list_direction:
        if(os.path.isfile(direction)):
            filelists.append(direction)
    return filelists

if __name__ == "__main__":
    filelists = get_filelists(root)
    insertStrings = ["\n\n> 示例代码：[Python-100-days-", 0, 0, 0, 0]
    insertStrings[2] = "](https://github.com/JustDoPython/python-100-day/tree/master/"
    insertStrings[4] = ")\n\n"
    for file_name in filelists:
        if(file_name[-6] == "0" and file_name not in ignore_list):
            # file_name[-6:-2] 为日期编号

            with open(file_name, encoding='utf-8') as f:
                cons = f.readlines()
                insertStrings[1] = "day" + file_name[-6:-3]
                insertStrings[3] = "day" + "-" + file_name[-6:-3]
                insertString = ''.join(insertStrings)
                insertIndex = cons[1:].index("---\n") + 2
                cons.insert(insertIndex, insertString)

            with open(file_name, 'w', encoding='utf-8') as f:
                f.writelines(cons)

