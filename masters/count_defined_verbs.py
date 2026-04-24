def main():
    layout_file_path = 'data/layout_type_index.txt'
    all_verbs = []
    with open(layout_file_path, 'r', encoding='utf-8') as f:
        lines = (line.strip() for line in f if line.strip())
        line_iter = iter(lines)
        for line in line_iter:
            layout_with_valency, verbs = line.split('=')
            layout, valency = layout_with_valency.split(':')
            verbs = sorted(list(map(lambda x: (layout, x.split(':')[0]), verbs.split(';'))))
            all_verbs += verbs
    all_verbs = sorted(all_verbs, key=lambda x: x[0])
    for verb in all_verbs:
        print(f'{verb[0]},{verb[1]}')
    # print(sorted(all_verbs))
    print(len(all_verbs))


if __name__ == '__main__':
    main()