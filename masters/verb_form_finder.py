import json
import sys


def main(args):
    word_form = args[0]
    with open('data/dictionary.json', 'r', encoding='utf-8') as f:
        dictionary = json.load(f)
    entries = dictionary.get(word_form)
    if entries is None:
        print('\033[31;1mNot found\033[0m')
        return 0
    last_csv_file = None
    for entry in entries:
        print(entry)
        verb = entry['verb']
        preverb = entry['preverb']
        csv_file = f'data/temp/{preverb}_{verb}_1.csv'
        if csv_file != last_csv_file:
            with open(csv_file, 'r', encoding='utf-8') as f:
                lines = (line.strip() for line in f if line.strip())
                line_iter = iter(lines)
                try:
                    for line in line_iter:
                        print(line)
                except StopIteration:
                    raise ValueError("Unexpected end of file while parsing.")
            last_csv_file = csv_file
    return 0


if __name__ == '__main__':
    main(sys.argv[1:])