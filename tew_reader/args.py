import argparse


class Args():
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='TEW2020 Reader')
        self.parser.add_argument('--tew-home', '-th',
                                 help='The path to the TEW2020 folder.')
        self.parser.add_argument('--tew-db', '-td',
                                 help='The name of the TEW2020 database to query.')
        self.parser.add_argument('--tew-save', '-ts',
                                 help='The name of the TEW2020 save to use.')
        self.parser.add_argument('--initials', '-i', required=True,
                                 help='The initials of the company to search.')
        self.parser.add_argument('--sort', '-s', default='overness',
                                 help='The value used to sort the workers.')
        self.parser.add_argument('--output', '-o', default='table', choices=['csv', 'table'],
                                 help='The format that the data should be outputted in.')
        self.parser.add_argument('--type', '-t', default='complex', choices=['simple', 'complex'],
                                 help='The values to return in the output; simple has less values returned.')
        __group = self.parser.add_mutually_exclusive_group()
        __group.add_argument('--asc', dest='reverse', default=True, action='store_false',
                             help='Sort values in ascending order.')
        __group.add_argument('--desc', dest='reverse', default=True, action='store_true',
                             help='Sort values in descending order.')

    def parse_args(self, args=None):
        return self.parser.parse_args(args=args)


args = Args()
