import sys
import re

def main(args):
    file_path = args[0]
    with open(file_path, 'r') as read_file, open(f'{file_path}_new', 'w') as write_file:
        for line in read_file:
            word_form, word_form_id = line.split(',')
            if '(' in word_form:
                word_1 = re.sub(r'\((.+)\)', r'\1', word_form)
                word_2 = re.sub(r'\((.+)\)', '', word_form)
                write_file.write(f'{word_1},{word_form_id}')
                write_file.write(f'{word_2},{word_form_id}')
            else:
                write_file.write(line)

if __name__ == '__main__':
    main(sys.argv[1:])