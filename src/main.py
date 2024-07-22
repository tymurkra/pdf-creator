import os.path

from json_to_pdf import json_to_pdf

OUTPUT_PATH = 'output'
OUTPUT_FILENAME = 'output.pdf'

TEMPLATE_PATH = 'templates'
TEMPLATE_NAME = 'test.mustache'
TEMPLATE_DATA = 'test.json'


def test():
    out = json_to_pdf(os.path.join(TEMPLATE_PATH, TEMPLATE_DATA),
                      os.path.join(TEMPLATE_PATH, TEMPLATE_NAME),
                      os.path.join(OUTPUT_PATH, OUTPUT_FILENAME))
    if out is not None:
        print(f'PDF successfully created: {os.path.abspath(out)}')
    else:
        print('Error!')


if __name__ == '__main__':
    test()
