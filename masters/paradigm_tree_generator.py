import sys
from collections import defaultdict
from difflib import SequenceMatcher


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

    list_matching_layouts = []

    for i, screeves in enumerate(screeves_to_layouts):
        # print(i, screeves_to_layouts[screeves])
        list_matching_layouts.append({
            'screeves': screeves,
            'verbs': screeves_to_layouts[screeves]
        })

    # print(list_matching_layouts)

    with open('data/grouped_layouts_by_screeves.txt', 'w', encoding='utf-8') as f:
        for layout_type in list_matching_layouts:
            f.write(', '.join(layout_type['verbs']) + '\n')
    #
    # for i in range(len(list_matching_layouts)):
    #     for j in range(i+1, len(list_matching_layouts)):
    #         print(i, list_matching_layouts[i]['verbs'][0], j, list_matching_layouts[j]['verbs'][0])
    #         print(f"\033[91;1m{list_matching_layouts[i]['screeves']}\033[0m")
    #         print(f"\033[92;1m{list_matching_layouts[j]['screeves']}\033[0m")
    #
    #         screeves_1_as_string = "\n".join(list_matching_layouts[i]['screeves'])
    #         screeves_2_as_string = "\n".join(list_matching_layouts[j]['screeves'])
    #
    #         print(f"\033[31m{screeves_1_as_string}\033[0m")
    #         print(f"\033[32m{screeves_2_as_string}\033[0m")
    #
    #         matcher = SequenceMatcher(None, screeves_1_as_string, screeves_2_as_string)
    #         matching_blocks = matcher.get_matching_blocks()
    #         print(matching_blocks)
    #         for block in matching_blocks:
    #             pass
    #
    #         break
    #     break


if __name__ == "__main__":
    main(sys.argv[1:])