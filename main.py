import timeit
from src.parse_input import parse_input_field
from src.initialize_field import initialise_field
from src.build_constraints import build_constraints
from src.print import print_to_txt
from src.solve import solve
import os
import sys

# Global variable for deciding which text file to use, if they are from the given set by,
# the tutorial management.
num = 1
from_gui = False


def main(gui=False, numbr=1):
    global num
    if len(sys.argv) > 1:
        num = int(sys.argv[1])
        print(f"Running solver on test {num}.......")
        folder = os.path.join(os.getcwd(), 'Project_1')
        file = f'{folder}\\test{num}.txt'
    elif gui:
        print(
            f"Running solver on the file generated from GUI. File Name: input_man{numbr}.txt")
        folder = os.path.join(os.getcwd(), 'Project_1')
        file = f'{folder}\input_man{numbr}.txt'
        num = numbr
    else:
        print(f"Running solver on test {num}.......")
        folder = os.path.join(os.getcwd(), 'project_1')
        file = f'{folder}/test{num}.txt'

    field_info = parse_input_field(file)
    field, neighbours = initialise_field(
        field_info[0], field_info[1], field_info[2])
    nodes, vpool, formula = build_constraints(field, neighbours)
    output_folder = os.path.join(os.getcwd(), 'DIMACS')
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    with open(f"{output_folder}/{'man_input' if gui else 'test'}{num}.cnf", 'w') as file:
        file.write(formula.to_dimacs())
    model = solve(vpool, formula, neighbours, field_info[1])
    print_to_txt(nodes, model, num, gui)


if __name__ == "__main__":
    main()
    print(timeit.repeat(lambda: main(), repeat=5, number=1))
