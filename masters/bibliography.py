import os
import sys
import re


def read_file(file_path, folder_path):
    dictionary = {}
    key = None
    with open(file_path, 'r') as f:
        for line in f.readlines():
            if line.startswith('######'):
                key = line.replace('######', '').strip()
            elif key is not None:
                if key == 'author':
                    dictionary[key] = read_authors(line, folder_path)
                elif key == 'publisher':
                    dictionary[key] = read_publisher(line, folder_path)
                elif key == 'book':
                    dictionary[key] = read_book(line, folder_path)
                else:
                    value = re.sub(r"\[\[([^\[^\]]+)\|([^\[^\]]+)]]", r"\2", line).strip()
                    value = re.sub(r"\[\[([^\[^\]]+)]]", r"\1", value).strip()
                    dictionary[key] = value
    return dictionary


def read_authors(line, folder_path):
    author_dicts = []
    author_links = line.split(', ')
    for author_link in author_links:
        author_filename = re.sub(r"\[\[([^\[^\]]+)\|([^\[^\]]+)]]", r"\1", author_link).strip()
        author_filename = re.sub(r"\[\[([^\[^\]]+)]]", r"\1", author_filename).strip()
        author_file_path = os.path.join(folder_path, 'authors', author_filename + '.md')
        author_dict = read_file(author_file_path, folder_path)
        if len(author_dict) == 0:
            author = re.sub(r"\[\[([^\[^\]]+)\|([^\[^\]]+)]]", r"\2", author_link).strip()
            author = re.sub(r"\[\[([^\[^\]]+)]]", r"\1", author).strip()
            names = author.split(' ')
            author_dict['first name'] = names[0]
            if len(names) > 1:
                author_dict['last name'] = names[1]
            if len(names) > 2:
                raise ValueError
        author_dicts.append(author_dict)
    return author_dicts


def generate_author_string(author_dicts, language, first_element=True):
    author_string = ''
    for i, author_dict in enumerate(author_dicts):
        if i == 0 and first_element:
            if 'last name' in author_dict:
                author_string += author_dict['last name']
            elif 'last initial' in author_dict:
                author_string += author_dict['last initial']
            author_string += ', '
            if 'first name' in author_dict:
                author_string += author_dict['first name']
            elif 'first initial' in author_dict:
                author_string += author_dict['first initial']
            if 'middle name' in author_dict:
                author_string += ' ' + author_dict['middle name']
            elif 'middle initial' in author_dict:
                author_string += ' ' + author_dict['middle initial']
        else:
            if i != 0 and (i != len(author_dicts) - 1 or len(author_dict) > 2):
                author_string += ', '
            elif i != 0:
                author_string += ' '
            # print(i, len(author_dicts), language)
            if i != 0 and i == len(author_dicts) - 1:
                if language == 'English':
                    author_string += 'and '
                elif language == 'Georgian':
                    author_string += 'და '
            if 'first name' in author_dict:
                author_string += author_dict['first name']
            elif 'first initial' in author_dict:
                author_string += author_dict['first initial']
            author_string += ' '
            if 'middle name' in author_dict:
                author_string += author_dict['middle name'] + ' '
            elif 'middle initial' in author_dict:
                author_string += author_dict['middle initial'] + ' '
            if 'last name' in author_dict:
                author_string += author_dict['last name']
            elif 'last initial' in author_dict:
                author_string += author_dict['last initial']
    # print(f'\033[93m{author_string}\033[0m')
    return author_string


def generate_publisher_string(publisher_dict, resource):
    publisher_string = ''
    if 'place' in resource:
        publisher_string += resource['place'] + ': '
    elif 'place' in publisher_dict:
        publisher_string += publisher_dict['place'] + ': '
    publisher_string += publisher_dict['title']
    return publisher_string


def generate_book_string(book_dict, author_dict):
    book_string = ''
    title = book_dict['title']
    if book_dict['language'] == 'English':
        book_string += 'In '
    elif book_dict['language'] == 'Georgian':
        book_string += 'წიგნში '
    book_string += '_' + title
    if 'volume' in book_dict:
        book_string += ' ' + book_dict['volume']
    book_string += '_'
    if book_dict['author'] != author_dict:
        if book_dict['language'] == 'English':
            book_string += ' ed. '
        elif book_dict['language'] == 'Georgian':
            book_string += ' რედ. '
        book_string += generate_author_string(book_dict['author'], book_dict['language'], first_element=False)
    book_string += ','
    return book_string


def read_publisher(line, folder_path):
    publisher_filename = re.sub(r"\[\[([^\[^\]]+)\|([^\[^\]]+)]]", r"\1", line).strip()
    publisher_filename = re.sub(r"\[\[([^\[^\]]+)]]", r"\1", publisher_filename).strip()
    publisher_file_path = os.path.join(folder_path, 'publishers', publisher_filename + '.md')
    publisher_dict = read_file(publisher_file_path, folder_path)
    if len(publisher_dict) == 0:
        publisher = re.sub(r"\[\[([^\[^\]]+)\|([^\[^\]]+)]]", r"\2", line).strip()
        publisher = re.sub(r"\[\[([^\[^\]]+)]]", r"\1", publisher).strip()
        publisher_dict['title'] = publisher
    return publisher_dict


def read_book(line, folder_path):
    book_filename = re.sub(r"\[\[([^\[^\]]+)\|([^\[^\]]+)]]", r"\1", line).strip()
    book_filename = re.sub(r"\[\[([^\[^\]]+)]]", r"\1", book_filename).strip()
    book_file_path = os.path.join(folder_path, 'books', book_filename + '.md')

    book_dict = read_file(book_file_path, folder_path)
    return book_dict


def main(args):
    folder_path = args[0]
    resource_filenames = os.listdir(os.path.join(folder_path, 'resources'))
    resources = []
    bibliographies = []

    for resource_filename in resource_filenames:
        resource_path = os.path.join(folder_path, 'resources', resource_filename)
        dictionary = read_file(resource_path, folder_path)
        if 'type' not in dictionary:
            print(f"\033[93;1m{resource_path}\033[0;33m has no type\033[0m")
        if 'title' not in dictionary:
            print(f"\033[94;1m{resource_path}\033[0;34m has no title\033[0m")
        resources.append(dictionary)

    for resource in resources:
        if 'type' not in resource:
            continue
        if 'title' not in resource:
            continue

        print(resource['title'])
        # print(resource)
        if resource['type'] == 'book':
            author_string = generate_author_string(resource['author'], resource['language'])
            year = resource['year']
            title = resource['title']
            bibliography = author_string + '. ' + year + '. _' + title + '_'

            if 'volume' in resource:
                bibliography += '. '
                if resource['language'] == 'English':
                    bibliography += 'Vol. '
                elif resource['language'] == 'Georgian':
                    bibliography += 'ტ. '
                bibliography += resource['volume']

            if 'series' in resource:
                bibliography += '. ' + resource['series']

                if 'series no' in resource:
                    bibliography += ' ' + resource['series no']

            if 'publisher' in resource:
                bibliography += '. ' + generate_publisher_string(resource['publisher'], resource)

            # print(f'\033[96m{bibliography}\033[0m')
            # print()
        elif resource['type'] == 'chapter':
            author_string = generate_author_string(resource['author'], resource['language'])
            year = resource['year']
            title = resource['title']
            bibliography = author_string + '. ' + year + '. ' + title

            bibliography += '. ' + generate_book_string(resource['book'], resource['author'])

            bibliography += ' ' + resource['page']

            if 'publisher' in resource['book']:
                bibliography += '. ' + generate_publisher_string(resource['book']['publisher'], resource['book'])
            # print(f'\033[95m{bibliography}\033[0m')
            # print()

        elif resource['type'] == 'article':
            author_string = generate_author_string(resource['author'], resource['language'])
            year = resource['year']
            title = resource['title']
            bibliography = author_string + '. ' + year + '. ' + title

            bibliography += '. _' + resource['journal'] + '_'

            if 'volume' not in resource and 'issue' not in resource:
                print(f'\033[91m{bibliography}\033[0m')

            if 'volume' in resource:
                bibliography += ' ' + resource['volume']

            if 'issue' in resource:
                bibliography += ', '
                if resource['language'] == 'English':
                    bibliography += 'no. '
                elif resource['language'] == 'Georgian':
                    bibliography += '№'
                bibliography += resource['issue']

                bibliography += ': ' + resource['page']

            # print(f'\033[92m{bibliography}\033[0m')
            # print()
        elif resource['type'] == 'dissertation':
            if 'publisher' not in resource:
                continue
            author_string = generate_author_string(resource['author'], resource['language'])
            year = resource['year']
            title = resource['title']
            bibliography = author_string + '. ' + year + '. ' + title
            bibliography += '. PhD diss.,'

            bibliography += generate_publisher_string(resource['publisher'], resource)
        else:
            continue
        bibliographies.append(bibliography + '.')
    bibliographies = sorted(bibliographies)
    with open(os.path.join(folder_path, 'Bibliography.md'), 'w') as bibliography_file:
        for i, bibliography in enumerate(bibliographies):
            bibliography_file.write(f'{i+1}. {bibliography}\n')


if __name__ == '__main__':
    main(sys.argv[1:])