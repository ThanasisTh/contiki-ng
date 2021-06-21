import os

def replace_string_in_file(file, identifying_phrase, new_value, split_index, separator=" "):
    new_file_content = ""

    reading_file = open(file, "r")
    for line in reading_file:
        replacement_line = line
        if identifying_phrase in line:
            replacement_line = line.replace(line.split(separator)[split_index], str(new_value)+'\n')
        new_file_content += replacement_line
    reading_file.close()

    writing_file = open(file, "w")
    writing_file.write(new_file_content)
    writing_file.close()



def rename_file(path):
    path = "./logs/"

    for root, dirs, files in os.walk(path):
        print(files)
        for i in files:
            if i.split(":")[0] == "Best result":
                os.rename(os.path.join(root, i), os.path.join(root, i.split(":")[0] + " for minimal: " + i.split(":")[1]))

