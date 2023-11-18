from parse_input_field import parse_input_field, num
from initialize_field import initialise_field
from constraint_building import build_constraints
from print_to_txt import print_to_txt
import sys


def main():
    if len(sys.argv) > 1:
        parse_input_field.num = int(sys.argv[1])

    field_info = parse_input_field(num)
    field = initialise_field(field_info[0], field_info[1], field_info[2])
    model_infos = build_constraints(field)
    n = model_infos[0]
    model = model_infos[1]
    print_to_txt(n, model)


if __name__ == "__main__":
    main()
