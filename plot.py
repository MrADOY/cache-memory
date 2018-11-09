from simCache156 import simulate
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('bs', type=int)
parser.add_argument('trace', type=str)
args = vars(parser.parse_args())


x_axis = [pow(2, x) << 10 for x in range(4)]
for assoc in (pow(2, i) for i in range(4)):
  results = []
  for x in x_axis:
    misses, reads, writes = simulate(cs=x, assoc=assoc,
                                     **args)
    miss_percentage = misses / (reads + writes) * 100
    results.append(miss_percentage)
  plt.plot(x_axis, results, label=assoc)

plt.xticks(x_axis)

plt.xlabel('Taille du cache (octet)')
plt.ylabel('Défauts de cache (%)')
plt.title('Taille des blocs: {} octets'.format(args['bs']))
plt.legend(title="Associativité", loc='best')

plt.savefig("test.png")
plt.show()
