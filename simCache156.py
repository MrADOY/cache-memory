import sys
import argparse
import time
import itertools
import threading


def print_infinite_loader():
  for char in itertools.cycle(('\\', '|', '/', '-')):
    print('Computing...', char, '\r', end='')
    time.sleep(.1)


def locate(cache, index, tag):
  for i, block in enumerate(cache[index]):
    if block['valid'] and block['tag'] == tag:
      return i


def replace_block(cache, index, tag):
  block_to_replace = None
  for block in cache[index]:
    if not block['valid']:
      # A block is free
      block_to_replace = block
      break
  else:
    # No block is free, so we have to find the oldest one
    block_to_replace = max(cache[index], key=lambda block: block['counter'])
  block_to_replace.update({'valid': True, 'tag': tag, 'counter': 0})

  # Increment every counter from the cache line
  for block in cache[index]:
    block['counter'] += 1


def read(cache, index, tag):
  if locate(cache, index, tag) is not None:
    return 0  # Hit

  replace_block(cache, index, tag)
  return 1  # Miss


def write(cache, index, tag):
  # TODO: Is this part done?
  if locate(cache, index, tag) is not None:
    return 0  # Hit
  replace_block(cache, index, tag)
  return 1  # Miss


def simulate(cs, bs, assoc, trace):
  nbe = cs // (bs * assoc)
  cache = [[{'valid': False, 'tag': 0, 'counter': 0}
            for i in range(assoc)] for j in range(nbe)]
  misses = 0
  requests = {'W': 0, 'R': 0}
  with open(trace) as f:
    for line in f:
      instruction, address = line[:1], int(line[1:], 16)
      numbloc = address // bs
      index = numbloc % nbe
      tag = numbloc // nbe
      misses += {'W': write, 'R': read}.get(instruction)(cache, index, tag)
      requests[instruction] += 1

  writes, reads = requests.values()
  return misses, reads, writes


if __name__ == '__main__':
  if sys.version_info.major != 3:
    raise Exception("Python 3 must be used.")

  parser = argparse.ArgumentParser()
  for arg, arg_type in (('cs', int),
                        ('bs', int),
                        ('assoc', int),
                        ('trace', str)):
    parser.add_argument(arg, type=arg_type)

  loader_thread = threading.Thread(target=print_infinite_loader, daemon=True)
  loader_thread.start()
  misses, reads, writes = simulate(**vars(parser.parse_args()))
  loader_thread.join(timeout=0)

  nb_requests = reads + writes
  print('{} reads, {} writes ({} total)'.format(reads, writes, nb_requests),
        '{} cache misses ({}%)'.format(misses, misses / nb_requests * 100),
        sep='\n')
