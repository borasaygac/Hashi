# This file is for parsing the input files
import os
def parse_input_field(input_no):
    folder = os.path.join(os.getcwd(), 'project_1')
    file = f'{folder}/test{input_no}.txt' 
    contents = [] 

    with open(file) as t:
        size_info = t.readline().split()  
        x_size = int(size_info[0]) 
        y_size = int(size_info[1])

        print(f"Dimensions are {x_size}, {y_size}\n")
        # add buffer edge around input
        contents = [('.' * (y_size+2))]
        read = t.readlines()
        readLines = ['.'+ string[:-1] + '.' + string[-1] for string in read]
        print(readLines)
        contents.extend(readLines)
        contents.extend([('.' * (y_size+2))])
        print(contents)
    return x_size+2, y_size+2, contents




