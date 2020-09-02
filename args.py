import argparse

__parser = argparse.ArgumentParser(description='TEW2020 Reader')
__parser.add_argument('--tew-home', '-th',
                      help='The path to the TEW2020 folder.')
__parser.add_argument('--tew-db', '-td',
                      help='The name of the TEW2020 database to query.')
__parser.add_argument('--tew-save', '-ts',
                      help='The name of the TEW2020 save to use.')
__parser.add_argument('--initials', '-i', required=True,
                      help='The initials of the company to search.')
__parser.add_argument('--sort', '-s', default='overness',
                      help='The value used to sort the workers.')
__parser.add_argument('--output', '-o', default='table', choices=['csv', 'table'],
                      help='The format that the data should be outputted in.')
__group = __parser.add_mutually_exclusive_group()
__group.add_argument('--asc', dest='reverse', default=True, action='store_false',
                     help='Sort values in ascending order.')
__group.add_argument('--desc', dest='reverse', default=True, action='store_true',
                     help='Sort values in descending order.')

args = __parser.parse_args()
