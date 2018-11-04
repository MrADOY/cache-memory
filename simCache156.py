import sys
import argparse


def read_address(address):
  # TODO:
  pass


def write_address(address):
  # TODO:
  pass


def simulate(cs, bs, assoc, trace):
  with open(trace) as f:
    for line in f:
      instruction, address = line[:1].lower(), line[1:].strip()
      {'w': write_address, 'r': read_address}.get(instruction)(address)
      # TODO:


if __name__ == '__main__':
  if sys.version_info[0] != 3:
    print("WARNING: You do not seem to use Python 3.")

  parser = argparse.ArgumentParser()
  for arg, arg_type in (('cs', int),
                        ('bs', int),
                        ('assoc', int),
                        ('trace', str)):
    parser.add_argument(arg, type=arg_type)
  simulate(**vars(parser.parse_args()))
