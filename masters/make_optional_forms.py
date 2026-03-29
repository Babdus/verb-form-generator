import sys
import re

def main(args):
    file_path = args[0]
    with open(file_path, 'r') as read_file, open(f'{file_path}_new', 'w') as write_file:
        for line in read_file:
            if '(' in line:
                word_1 = re.sub(r'\((.+)\)', r'\1', line)
                word_2 = re.sub(r'\((.+)\)', '', line)
                write_file.write(word_1)
                write_file.write(word_2)
            else:
                write_file.write(line)

if __name__ == '__main__':
    main(sys.argv[1:])