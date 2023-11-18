from parse_input import parse_input_field
from initialize_field import initialise_field
from build_constraints import build_constraints
from print import print_to_txt
import sys

# Global variable for deciding which text file to use, if they are from the given set by,
# the tutorial management.
num = 1

def main():
    global num
    if len(sys.argv) > 1:
        num = int(sys.argv[1])
    field_info = parse_input_field(num)
    field = initialise_field(field_info[0], field_info[1], field_info[2])
    model_infos = build_constraints(field)
    n = model_infos[0]
    model = model_infos[1]
    print_to_txt(n, model, num)


if __name__ == "__main__":
    main()
