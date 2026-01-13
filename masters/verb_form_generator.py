import sys

from masters.translations import trad_screeves
from translations import geo
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation
from connection import engine, VerbForm, Base


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


rules = {
    'roots': [],
    'prefixes': [
        (('ვ:1_sbj.direct', 'გ:2_obj.direct'), 0),
        (('ვ:1_obj.inverse', 'გ:2_sbj.inverse'), 0),
        (('ი:Iturm.inverse', 'უ:3_sbj.Iturm.inverse'), 0),
        (('ი:Iturm_th.inverse', 'უ:3_sbj.Iturm_th.inverse'), 0),
        (('ი:vers.direct', 'უ:vers.3_obj.direct'), 0),
        (('ი:nonvers.direct', 'უ:nonvers.3_obj.direct'), 0),
        (('ი:vers.direct', 'ი:vers.3_obj.direct'), 0),
        (('ა:vers.direct', 'ა:vers.3_obj.direct'), 0),
        (('ვ:1_sbj.direct', 'ჰ:3_obj.direct'), 1),
        (('ვ:1_sbj.direct', 'ს:3_obj.direct'), 1),
        (('ვ:1_sbj.direct', 'ჰ:3_obj.nonvers.direct'), 1),
        (('ვ:1_sbj.direct', 'ს:3_obj.nonvers.direct'), 1),
        (('ვ:1_sbj.direct', 'ჰ:3_obj.IIIseries.direct'), 1),
        (('ვ:1_sbj.direct', 'ს:3_obj.IIIseries.direct'), 1)
    ],
    'suffixes': [
        (('ოდ:impf_sub_circ', 'დ:fut2_circ.impf_sub_circ'), 0),
        (('ს:3_sg_sbj.direct', 'ა:3_sg_sbj.pres.direct'), 0),
        (('ს:3_sg_sbj.direct', 'ა:3_sg_sbj.impf.direct'), 0),
        (('ს:3_sg_sbj.direct', 'ა:3_sg_sbj.cond.direct'), 0),
        (('ს:3_sg_sbj.direct', 'ა:3_sg_sbj.IIturm_impf.direct'), 0),
        (('ს:3_sg_sbj.direct', 'ა:3_sg_sbj.IIIsubj_impf.direct'), 0),
        (('ს:3_sg_sbj.direct', 'ა:3_sg_sbj.aor.direct'), 0),
        (('ს:3_sg_sbj.direct', 'ა:3_sbj.Iturm.direct'), 0),
        (('ს:3_sg_sbj.direct', 'ა:3_sbj.IIturm.direct'), 0),
        (('ა:3_sbj.IIturm.direct', 'ო:IIturm.3_sg_sbj.direct'), 0),
        (('ა:3_sbj.IIturm.direct', 'ვ:IIturm.3_pl_sbj.direct'), 0),
        (('ს:3_sg_sbj.direct', 'ო:3_sg_sbj.aor.direct'), 0),
        (('ს:3_sg_sbj.direct', 'თ:2_pl_obj.direct'), 0),
        (('ს:3_sg_sbj.direct', 'თ:3_pl_obj.3_sg_sbj.direct'), 0),
        (('თ:pl_sbj.direct', 'თ:2_pl_obj.direct'), 1),
        (('თ:pl_sbj.direct', 'ნენ:3_pl_sbj.direct'), 0),
        (('ნენ:3_pl_sbj.direct', 'ენ:3_pl_sbj.pres.direct'), 0),
        (('ნენ:3_pl_sbj.direct', 'ან:3_pl_sbj.pres.nonvers.direct'), 0),
        (('ნენ:3_pl_sbj.direct', 'ენ:3_pl_sbj.pres.vers.direct'), 0),
        (('ან:3_pl_sbj.pres.direct', 'ენ:3_pl_sbj.pres.vers.direct'), 0),
        (('ნენ:3_pl_sbj.direct', 'ან:3_pl_sbj.pres.direct'), 0),
        (('ნენ:3_pl_sbj.direct', 'ს:3_pl_sbj.pres_th.direct'), 0),
        (('ნენ:3_pl_sbj.direct', 'ეს:3_pl_sbj.aor.direct'), 0),
        (('ნენ:3_pl_sbj.direct', 'ნ:3_pl_sbj.IIsubj.direct'), 0),
        (('ნენ:3_pl_sbj.direct', 'ნ:3_pl_sbj.Iturm.direct'), 0),
        (('ნენ:3_pl_sbj.direct', 'ნ:3_pl_sbj.IIIsubj.direct'), 0),
        (('ი:IIIseries', 'ოდ:IIturm_impf_sub_circ'), 0),
        (('ი:pres', 'ა:3_sg_sbj.pres.direct'), 0),
        (('ი:pres.vers', 'ა:3_sg_sbj.pres.direct'), 0),
        (('ი:impf', 'ა:3_sg_sbj.impf.direct'), 0),
        (('ი:cond', 'ა:3_sg_sbj.cond.direct'), 0),
        (('ი:IIturm_impf', 'ა:3_sg_sbj.IIturm_impf.direct'), 0),
        (('ე:IIIsubj_impf', 'ა:3_sg_sbj.IIIsubj_impf.direct'), 0),
        (('ი:impf', 'ნენ:3_pl_sbj.direct'), 0),
        (('ი:cond', 'ნენ:3_pl_sbj.direct'), 0),
        (('ე:subj', 'ნენ:3_pl_sbj.direct'), 0),
        (('ი:IIturm_impf', 'ნენ:3_pl_sbj.direct'), 0),
        (('ე:IIIsubj_impf', 'ნენ:3_pl_sbj.direct'), 0),
        (('ე:aor', 'ა:3_sg_sbj.aor.direct'), 0),
        (('ე:aor', 'ო:3_sg_sbj.aor.direct'), 0),
        (('ე:aor', 'ეს:3_pl_sbj.aor.direct'), 0),
        (('ე:aor', 'ნენ:3_pl_sbj.direct'), 0),
        (('ი:aor', 'ნენ:3_pl_sbj.direct'), 0),
        (('ე:IIsubj', 'ნენ:3_pl_sbj.direct'), 0),
        (('ა:IIsubj', 'ნენ:3_pl_sbj.direct'), 0),
        (('ო:IIsubj', 'ნენ:3_pl_sbj.direct'), 0),
        (('ი:aor', 'ა:3_sg_sbj.aor.direct'), 0),
        (('ი:aor', 'ო:3_sg_sbj.aor.direct'), 0),
        (('ი:aor', 'ეს:3_pl_sbj.aor.direct'), 0),

        (('ს:3_obj.inverse', 'ა:3_obj.Iturm.inverse'), 0),
        (('ს:3_obj.inverse', 'ა:3_obj.IIturm.inverse'), 0),
        (('ს:3_obj.inverse', 'ო:3_obj.IIturm.inverse'), 0),
        (('ს:3_obj.inverse', 'თ:2_pl_sbj.inverse'), 0),
        (('თ:pl_obj.inverse', 'ა:3_obj.Iturm.inverse'), 0),
        (('თ:pl_obj.inverse', 'ა:3_obj.IIturm.inverse'), 0),
        (('თ:pl_obj.inverse', 'ს:3_obj.inverse'), 0),
        (('თ:pl_obj.inverse', 'თ:2_pl_sbj.inverse'), 1),
        (('თ:3_pl_sbj.3_obj.inverse', 'ს:3_obj.inverse'), 1),
        (('ე:IIturm', 'ა:3_obj.IIturm.inverse'), 0),
        (('ე:IIturm', 'ო:3_obj.IIturm.inverse'), 0),
        (('ი:IIturm', 'ა:3_obj.IIturm.inverse'), 0),
        (('ი:IIturm', 'ო:3_obj.IIturm.inverse'), 0),
        (('ი:IIIsubj', 'ა:3_obj.IIIsubj.inverse'), 0)
    ]
}

persons = ['1', '2', '3']
numbers = ['sg', 'pl']


def make_affixes(params, direction, param_priority, category_to_parameter):
    affixes = set()
    for param in params:
        if param in category_to_parameter[direction]:
            for sub_param in category_to_parameter[direction][param]:
                if sub_param['categories'] <= params or 'FORCE' in sub_param['categories']:
                    affixes.add(sub_param['param'])

    for condition, result in rules[direction]:
        if condition[0] in affixes and condition[1] in affixes:
            if result == 2:
                continue
            affixes.remove(condition[result])
    affixes = list(affixes)
    affixes.sort(key=lambda x: param_priority[direction][x])
    return affixes


def replace_layout_elements(line, roots, affixes, preverbs):
    if ':' in line:  # replace [***] with roots or affixes
        surface_form = line.split(':')[0]
        if surface_form.startswith('[') and surface_form.endswith(']'):
            surface_form = surface_form[1:-1]
            if surface_form.split('.')[0] == 'root':
                choosing_list = roots
            elif surface_form.split('.')[0] == 'affix':
                choosing_list = affixes
            elif surface_form.split('.')[0] == 'preverb':
                choosing_list = preverbs
            else:
                raise ValueError(f"Unidentified {surface_form.split('.')[0]}")
            index = int(surface_form.split('.')[1]) if '.' in surface_form else 1
            # print(surface_form, index, choosing_list)
            replacer = choosing_list[index - 1].split('.')[0]
            line = replacer + ':' + ':'.join(line.split(':')[1:])
            # print(line)
    return line


def read_file(word, roots, affixes, preverbs):
    file_path = f'data/paradigm_types/{word}.txt'
    result = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = (line.strip() for line in f if line.strip())

        line_iter = iter(lines)

        try:
            for key in line_iter:
                # print('key:', key)
                n = int(next(line_iter))
                # print('n:', n)
                values = []
                for _ in range(n):
                    line = next(line_iter)
                    # print('line:', line)
                    if ', ' in line:
                        values.append(tuple(line.split(', ')))
                    else:
                        line = replace_layout_elements(line, roots, affixes, preverbs)
                        values.append(line)
                result[key] = values
        except StopIteration:
            raise ValueError("Unexpected end of file while parsing.")

    return result


def choose_file(root):
    layout_file_path = 'data/layout_type_index.txt'
    candidate_files = []
    with open(layout_file_path, 'r', encoding='utf-8') as f:
        lines = (line.strip() for line in f if line.strip())
        line_iter = iter(lines)
        try:
            for line in line_iter:
                layout_with_valency, verbs = line.split('=')
                layout, valency = layout_with_valency.split(':')
                verbs = verbs.split(';')
                for verb in verbs:
                    if ':' in verb:
                        verb, params = verb.split(':')
                        roots = [root for root in params.split(',') if '.' not in root]
                        affixes = [param for param in params.split(',') if '.' in param]
                    else:
                        roots = [verb]
                        affixes = []
                    if verb == root:
                        candidate_files.append((layout, valency, roots, affixes))
        except StopIteration:
            raise ValueError("Unexpected end of file while parsing.")
    if len(candidate_files) == 0:
        print(f'\033[31m{root}\033[0m ვერ მოიძებნა პარადიგმის ყალიბებში')
        exit()
    return candidate_files

def make_param_priority(parameters):
    return {
        'roots': {param: i for i, param in enumerate(parameters['roots'])},
        'prefixes': {param: i for i, param in enumerate(parameters['prefixes'])},
        'suffixes': {param: i for i, param in enumerate(parameters['suffixes'])}
    }


def make_category_to_parameter(parameters):
    category_to_parameter = {'roots': {}, 'prefixes': {}, 'suffixes': {}}

    for direction in ['roots', 'prefixes', 'suffixes']:
        for param in parameters[direction]:
            value, gloss = param.split(':')
            categories = gloss.split('.')
            for category in categories:
                if category in category_to_parameter[direction]:
                    category_to_parameter[direction][category].append({'param': param, 'categories': set(categories)})
                else:
                    category_to_parameter[direction][category] = [{'param': param, 'categories': set(categories)}]
    return category_to_parameter


def generator(verb, preverb, unsafe=False, highlight=None, printable=True):
    return main([verb, preverb, '1'], highlight, unsafe, printable)


def save_to_db(
        word_form,
        verb,
        screeve,
        trad_screeve,
        subject_number,
        subject_person,
        object_number,
        object_person,
        preverb,
        blueprint,
        unsafe=False
) -> bool:
    new_verb_form = VerbForm(
        word_form=word_form,
        verb=verb,
        screeve=screeve,
        trad_screeve=trad_screeve,
        subject_person=subject_person,
        subject_number=subject_number,
        object_person=object_person,
        object_number=object_number,
        preverb=preverb,
        blueprint=blueprint,
    )
    session.add(new_verb_form)
    if unsafe:
        return True
    try:
        session.commit()
        return True
    except IntegrityError as e:
        session.rollback()
        if isinstance(e.orig, UniqueViolation):
            return False
        else:
            raise e


def main(args, highlight=None, unsafe=False, printable=True):
    root = args[0]
    preverbs = [args[1]] if len(args) > 1 and args[1] != 'nopv' else []
    no_save = '--no-save' in args
    preverb = preverbs[0] if len(preverbs) > 0 else ""

    cell_width = len(root) + len(preverb) + 8

    candidate_files = choose_file(root)
    for layout, valency, roots, affixes in candidate_files:
        if printable:
            print(f'\033[37;1m{preverb}\033[32;1m{root}\033[0m\n')

        valency = int(valency)

        parameters = read_file(layout, roots, affixes, preverbs)
        param_priority = make_param_priority(parameters)
        category_to_parameter = make_category_to_parameter(parameters)
        screeves = parameters['screeves']

        for screeve in screeves:
            screeve_params = set(screeve[1].split('.'))
            if printable:
                print(f'\033[33;1m{geo[screeve[0]]}\033[0m')
                print(f'\033[91;2;3m{trad_screeves[screeve[2]]}\033[0m')
            for sbj_num in numbers:
                for sbj_pers in persons:
                    for obj_num in numbers if valency > 1 else ['sg']:
                        for obj_pers in persons if valency > 1 else ['3']:
                            if sbj_pers in {'1', '2'} and sbj_pers == obj_pers:
                                if printable:
                                    print(f'{"":{cell_width}}', end='')
                                continue
                            pers_params = {
                                f'{sbj_pers}_sbj',
                                f'{sbj_num}_sbj',
                                f'{sbj_pers}_{sbj_num}_sbj',
                                f'{obj_pers}_obj',
                                f'{obj_num}_obj',
                                f'{obj_pers}_{obj_num}_obj'
                            }

                            params = screeve_params | pers_params | {'ALL'}

                            prefixes = make_affixes(params, 'prefixes', param_priority, category_to_parameter)
                            roots = make_affixes(params, 'roots', param_priority, category_to_parameter)
                            suffixes = make_affixes(params, 'suffixes', param_priority, category_to_parameter)

                            prefix_form = "".join([morpheme.split(':')[0] for morpheme in prefixes])
                            root_form = "".join([morpheme.split(':')[0] for morpheme in roots])
                            suffix_form = "".join([morpheme.split(':')[0] for morpheme in suffixes])
                            word_form = f'{prefix_form}{root_form}{suffix_form}'

                            color_start = ''
                            color_end = ''

                            if not no_save:
                                response = save_to_db(
                                    word_form=word_form,
                                    verb=root,
                                    screeve=screeve[0],
                                    trad_screeve=trad_screeves[screeve[2]],
                                    subject_person=int(sbj_pers),
                                    subject_number=sbj_num,
                                    object_person=int(obj_pers),
                                    object_number=obj_num,
                                    preverb=preverb,
                                    blueprint=layout,
                                    unsafe=unsafe
                                )
                                if not response:
                                    color_start = '\033[90;3m'
                                    color_end = '\033[0m'

                            if highlight == word_form:
                                color_start = '\033[91;3m'
                                color_end = '\033[0m'
                            if printable:
                                print(f'{color_start}{word_form:<{cell_width}}{color_end}', end='')
                    if printable:
                        print()
            if printable:
                print()
    if unsafe and not no_save:
        try:
            session.commit()
        except IntegrityError as e:
            session.rollback()


if __name__ == "__main__":
    main(sys.argv[1:])