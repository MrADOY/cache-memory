import sys
import argparse


def locate(cache, index, tag):
  for i, block in enumerate(cache[index]):
    if block['valid'] and block['tag'] == tag:
      return i


def replace_block(cache, index, tag):
  # a block is free.
  for block in cache[index]:
    if not block['valid']:
      block.update({'valid': True, 'tag': tag, 'counter' : 0})
      update_counter(cache)
      return
  # no block are free so we have to find the oldest.
  oldest_block = max(cache[index], key=lambda block: block['counter'])
  oldest_block.update({'valid': True, 'tag': tag, 'counter' : 0})
  update_counter(cache)

def read(cache, index, tag):
  if locate(cache, index, tag) is not None:
    return 0  # Hit

  replace_block(cache, index, tag)
  return 1  # Miss


def write(cache, index, tag):
  # TODO: Is this part done?
  if locate(cache, index, tag) is not None:
    return 0  # Hit
  return 1  # Miss

def update_counter(cache):
  for _set in cache:
    for block in _set:
      block['counter'] += 1


def simulate(cs, bs, assoc, trace):
  nbe = cs // bs * assoc
  cache = [[{'valid': False, 'tag': 0, 'counter' : 0}
            for i in range(assoc)] for j in range(nbe)]
  misses = 0
  with open(trace) as f:
    for line in f:
      instruction, address = line[:1], int(line[1:], 16)
      numbloc = address // bs
      index = numbloc % nbe
      tag = numbloc // nbe
      misses += {'W': write, 'R': read}.get(instruction)(cache, index, tag)
      # TODO:

  print(misses)


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
