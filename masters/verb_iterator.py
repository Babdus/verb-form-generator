import sys
import verb_form_generator
import time


preverbs = [
    'და', 'შე', 'ჩა', 'ა', 'გა', 'წა', 'გადა', 'აღ', 'გან', 'მი', 'შთა', 'წარ', 'გარდა',
    'შემო', 'ჩამო', 'ამო', 'წამო', 'გადმო', 'აღმო', 'განმო', 'მიმო', 'შთამო', 'წარმო', 'გარდამო'
]

simple_preverbs = [
    'და'
]


def main(args):
    start_time = time.time()
    with open('data/layout_type_index.txt', 'r', encoding='utf-8') as f:
        lines = (line.strip() for line in f if line.strip())
        line_iter = iter(lines)
        result_verbs = []
        try:
            for line in line_iter:
                layout_with_valency, verbs = line.split('=')
                verbs = verbs.split(';')
                for verb in verbs:
                    result_verbs.append(verb.split(':')[0])
        except StopIteration:
            raise ValueError("Unexpected end of file while parsing.")

    count = 0
    last_time = start_time
    for verb in result_verbs:
        print(count, verb)
        for preverb in preverbs:
            verb_form_generator.generator(verb, preverb, unsafe=True, printable=False)
        count += 1
        curr_time = time.time()
        print(f'\r{count} {verb} {round(curr_time - last_time, 2)}s')
        last_time = curr_time
    print(f'{time.time() - start_time} seconds')

if __name__ == '__main__':
    main(sys.argv[1:])