import sys
import time
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation
from connection import engine, VerbForm, Base, Concordance, Context, WordForm, OptionalWordForm, PartOfSpeech, ContextWord


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def get_optional_word_forms(optional_word_forms_path):
    optional_word_forms = {}
    with open(optional_word_forms_path, 'r') as f:
        counter = 0
        for line in f:
            # print(f'\033[33m{line}\033[0m')
            counter += 1
            if counter == 1:
                continue
            word_form, word_form_id = line.split(',')
            word_form = word_form.strip()
            word_form_id = int(word_form_id.strip())
            if not word_form in optional_word_forms:
                optional_word_forms[word_form] = word_form_id
            else:
                print(f'\033[31m{word_form}, {word_form_id}\033[0m')
    return optional_word_forms


def split_line(line):
    line = line.strip()
    parts = line.split('\t')
    left_words = [('+'.join(word.split('+')[:-1]), word.split('+')[-1]) for word in parts[0].split(' ') if '+' in word]
    left_words.reverse()
    right_words = [('+'.join(word.split('+')[:-1]), word.split('+')[-1]) for word in parts[2].split(' ') if '+' in word]
    query_word = ('+'.join(parts[1].split('+')[:-1]), parts[1].split('+')[-1])
    return left_words, right_words, query_word


def store_pos(file_path):
    parts_of_speech = set()
    with open(file_path, 'r') as f:
        i = 0
        for line in f:
            try:
                left_words, right_words, query_word = split_line(line)
                parts_of_speech.add(query_word[1])
                parts_of_speech |= {word[1] for word in left_words}
                parts_of_speech |= {word[1] for word in right_words}
            except IndexError:
                print(f'\033[91m{i}, {line}\033[0m')
                return None
            i += 1
    for pos in parts_of_speech:
        new_pos = PartOfSpeech(
            part_of_speech=pos
        )
        session.add(new_pos)
    try:
        session.commit()
        return True
    except IntegrityError as e:
        session.rollback()
        raise e


def get_pos():
    result = session.query(PartOfSpeech.part_of_speech, PartOfSpeech.id).all()
    result = {pos[0]: pos[1] for pos in result}
    return result


def main(args):
    start_time = time.time()
    file_path = args[0]
    optional_word_forms_path = args[1]
    optional_word_forms = get_optional_word_forms(optional_word_forms_path)

    # store_pos(file_path)
    parts_of_speech = get_pos()
    print(parts_of_speech)

    with open(file_path, 'r') as f:
        j = 0
        for line in f:
            try:
                print(f'\033[92m{j}, \033[94m{time.time() - start_time:.2f}\033[0m', end='\r')
                j += 1
                left_words, right_words, query_word = split_line(line)

                query_pos_id = parts_of_speech[query_word[1]]

                concordance = Concordance(
                    query_word=query_word[0],
                    query_part_of_speech_id=query_pos_id,
                    optional_word_form_id=optional_word_forms[query_word[0]],
                )

                left_context = Context(direction='left')
                right_context = Context(direction='right')

                for i, word in enumerate(left_words):
                    left_context.context_words.append(
                        ContextWord(
                            word=word[0],
                            position=i,
                            part_of_speech_id=parts_of_speech[word[1]]
                        )
                    )

                for i, word in enumerate(right_words):
                    right_context.context_words.append(
                        ContextWord(
                            word=word[0],
                            position=i,
                            part_of_speech_id=parts_of_speech[word[1]]
                        )
                    )

                concordance.contexts.append(left_context)
                concordance.contexts.append(right_context)
                session.add(concordance)
                session.commit()
            except IntegrityError as e:
                session.rollback()
                print()
                print(f'\033[96m{line}\033[0m')
                print(f'\033[91m{e}\033[0m')

if __name__ == '__main__':
    main(sys.argv[1:])