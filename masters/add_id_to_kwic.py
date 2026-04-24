import sys


def main(args):
    file_path = args[0]
    file_name = file_path.split('.')[0]
    file_extension = file_path.split('.')[1]
    with open(file_path, 'r') as f, open(file_name + '_new.' + file_extension, 'w') as new:
        j = 0
        for line in f:
            new.write(line.strip() + f'\t{j}\n')
            j += 1

if __name__ == '__main__':
    main(sys.argv[1:])