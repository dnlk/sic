from argparse import ArgumentParser


def parse_args():
    parser = ArgumentParser(description='Converts an image to sound')
    parser.add_argument('--image', help='The input jpeg file name', required=True)
    return parser.parse_args()
