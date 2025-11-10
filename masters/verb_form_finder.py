import json
import sys

import verb_form_generator
from translations import geo


def print_entry(entry):
    print(f'\033[93m{"ზმნა:":<{16}}\033[32;1;3m{entry["verb"]}\033[0m')
    print(f'\033[33m{"მწკრივი:":<{16}}\033[33;1m{geo[entry["screeve"]]}\033[0m')
    print(f'\033[33m{"სუბიექტი:":<{16}}\033[33;1m{geo[entry["subject person"]]} {geo[entry["subject number"]]}\033[0m')
    print(f'\033[33m{"ობიექტი:":<{16}}\033[33;1m{geo[entry["object person"]]} {geo[entry["object number"]]}\033[0m')
    print(f'\033[33m{"ზმნისწინი:":<{16}}\033[37;1m{entry["preverb"]}\033[0m')
    print(f'\033[33m{"ყალიბი:":<{16}}\033[97;1m{entry["blueprint"]}\033[0m')
    print()


def main(args):
    word_form = args[0]
    with open('data/dictionary.json', 'r', encoding='utf-8') as f:
        dictionary = json.load(f)
    entries = dictionary.get(word_form)
    if entries is None:
        print('\033[31;1mNot found\033[0m')
        return 0
    paradigms = set()
    preverbs = []
    printed_entries = []
    print(f'\n\033[37m{"ფორმა:":<{16}}\033[97;1;3m{word_form}\n')
    for entry in entries:
        printed_entry = entry.copy()
        printed_entry.pop('preverb', None)
        if len(printed_entries) == 0 or printed_entry not in printed_entries:
            print_entry(entry)
        printed_entries.append(printed_entry)
        verb = entry['verb']
        preverb = entry['preverb']
        preverbs.append(preverb)
        paradigms.add(verb)
    for verb in paradigms:
        verb_form_generator.generator(verb, preverbs[0], dictionary=None, highlight=word_form)
    return 0


if __name__ == '__main__':
    main(sys.argv[1:])