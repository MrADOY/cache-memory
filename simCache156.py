import sys
import argparse


def locate(cache, index, tag):
  for i, block in enumerate(cache[index]):
    if block['valid'] and block['tag'] is tag:
      return i


def read(cache, index, tag):
  if locate(cache, index, tag):
    return 1  # Hit

  # TODO:
  return 0  # Miss


def write(cache, index, tag):
  # TODO:
  pass


def simulate(cs, bs, assoc, trace):
  nbe = cs // bs * assoc
  cache = [[{'valid': False, 'tag': 0}
            for i in range(assoc)] for j in range(nbe)]
  with open(trace) as f:
    for line in f:
      instruction, address = line[:1], int(line[1:], 16)
      numbloc = address// bs
      index = numbloc % nbe
      tag = numbloc // nbe
      {'W': write, 'R': read}.get(instruction)(cache, index, tag)
      # TODO:


if __name__ == '__main__':
  if sys.version_info.major != 3:
    raise Exception("Python 3 must be used.")

  parser = argparse.ArgumentParser()
  for arg, arg_type in (('cs', int),
                        ('bs', int),
                        ('assoc', int),
                        ('trace', str)):
    parser.add_argument(arg, type=arg_type)
  simulate(**vars(parser.parse_args()))
