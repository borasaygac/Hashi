from src.parse_input import parse_input_field
from src.initialize_field import initialise_field
from src.build_constraints import build_constraints
from src.print import print_to_txt
from src.solve import solve
import sys

# Global variable for deciding which text file to use, if they are from the given set by,
# the tutorial management.
num = 1

def main():
    global num
    if len(sys.argv) > 1:
        num = int(sys.argv[1])
    print(f"Running solver on test {num}.......")
    field_info = parse_input_field(num)
    field, neighbours = initialise_field(field_info[0], field_info[1], field_info[2])
    nodes, vpool, formula = build_constraints(field)
    model = solve(vpool, formula)
    print_to_txt(nodes, model, num)


if __name__ == "__main__":
    main()
