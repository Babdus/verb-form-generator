import sys
from collections import defaultdict


def read_file(word):
    file_path = f'data/paradigm_types/{word}.txt'
    result = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = (line.strip() for line in f if line.strip())

        line_iter = iter(lines)

        screeves = []

        for key in line_iter:
            if key == 'screeves':
                n = int(next(line_iter))
                # print('n:', n)
                values = []
                for _ in range(n):
                    line = next(line_iter)
                    screeves.append(line)
    return tuple(screeves)



def main(args):

    screeves_to_layouts = defaultdict(list)
    layout_to_screeves = {}

    layout_file_path = 'data/layout_type_index.txt'
    with open(layout_file_path, 'r', encoding='utf-8') as f:
        lines = (line.strip() for line in f if line.strip())
        line_iter = iter(lines)
        for line in line_iter:
            layout_with_valency, verbs = line.split('=')
            layout, valency = layout_with_valency.split(':')
            # print(layout, valency)
            screeves = read_file(layout)
            screeves_to_layouts[screeves].append(layout)
            layout_to_screeves[layout] = screeves

    for i, screeves in enumerate(screeves_to_layouts):
        print(i, screeves_to_layouts[screeves])


if __name__ == "__main__":
    main(sys.argv[1:])