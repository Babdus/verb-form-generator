import sys
import verb_form_generator


preverbs = [
    'და', 'შე', 'ჩა', 'ა', 'გა', 'წა', 'გადა', 'აღ', 'გან', 'მი', 'შთა', 'წარ', 'გარდა',
    'შემო', 'ჩამო', 'ამო', 'წამო', 'გადმო', 'აღმო', 'განმო', 'მიმო', 'შთამო', 'წარმო', 'გარდამო'
]


def main(args):
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

    for verb in result_verbs:
        for preverb in preverbs:
            verb_form_generator.generator(verb, preverb)


if __name__ == '__main__':
    main(sys.argv[1:])