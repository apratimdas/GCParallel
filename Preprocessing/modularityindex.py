
import networkx as nx
import sys

from modularity_maximization.community_newman import partition
from modularity_maximization.utils import get_modularity

karate = nx.Graph(nx.read_pajek(sys.argv[1]))

print(nx.info(karate))
comm_dict = partition(karate)

# for comm in set(comm_dict.values()):
#     print("Community %d"%comm)
#     print(', '.join([node for node in comm_dict if comm_dict[node] == comm]))

from modularity_maximization.utils import get_modularity
print('Modularity of such partition for karate is %.3f' % get_modularity(karate, comm_dict))