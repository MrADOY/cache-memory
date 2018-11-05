import sys
import argparse


def locate(cache, index, tag):
  for i, block in enumerate(cache[index]):
    if block['valid'] or block['tag'] is tag:
      return i


def read(cache, index, tag):
  if locate(cache, index, tag):
    return True # Hit

  # TODO:
  return False # Miss


def write(cache, index, tag):
  # TODO:
  pass


def simulate(cs, bs, assoc, trace):
  nbe = cs // bs * assoc
  cache = [[{'valid': False, 'tag': 0} for i in range(assoc)] for j in range(nbe)]
  with open(trace) as f:
    for line in f:
      instruction, address = line[:1].lower(), int(line[1:].strip(), 16)
      numbloc = address * 4 // bs
      index = numbloc % nbe
      tag = numbloc // nbe
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
