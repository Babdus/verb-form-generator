def main():
    layout_file_path = 'data/layout_type_index.txt'
    all_verbs = []
    with open(layout_file_path, 'r', encoding='utf-8') as f:
        lines = (line.strip() for line in f if line.strip())
        line_iter = iter(lines)
        for line in line_iter:
            layout_with_valency, verbs = line.split('=')
            layout, valency = layout_with_valency.split(':')
            verbs = list(map(lambda x: x.split(':')[0], verbs.split(';')))
            all_verbs += verbs
    # print(all_verbs)
    print(len(all_verbs))


if __name__ == '__main__':
    main()