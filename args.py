import argparse

__parser = argparse.ArgumentParser(description='TEW2020 Reader')
__parser.add_argument('--tew-home', '-th')
__parser.add_argument('--tew-db', '-td')
__parser.add_argument('--tew-save', '-ts')
__parser.add_argument('--initials', '-i', required=True)
__parser.add_argument('--sort', '-s', default='overness')
__group = __parser.add_mutually_exclusive_group()
__group.add_argument('--asc', dest='reverse', default=True, action='store_false')
__group.add_argument('--desc', dest='reverse', default=True, action='store_true')

args = __parser.parse_args()
