
import sets
from sets import Set, ImmutableSet

def add (graph, i, j=None, weight=1, undirected=True, noselfloops=True):
    """Add a vertex or edge to a graph."""
    if j is None:
        if i not in graph.keys():
            graph[i] = {}
    else:
        if (i==j) and noselfloops:
            return
        if i not in graph:
            graph[i] = {}
        if j not in graph:
            graph[j] = {}
        graph[i][j] = weight
        #print "Weight:"
        #print weight
        #print graph[i][j]
        #print i,j,graph
        if undirected:
            graph[j][i] = weight
            
   # print "graph in geaphFunctions:"
   # print graph

def weight (graph, i, j):
    """Return weight of edge (i,j)."""
    return graph[i][j]

def degree (graph, i):
    """Degree of vertex i.
    """
    return len(graph[i])

def edges (graph, undirected=True):
    """Returns Set of edges."""
    edges = sets.Set()
    seen = sets.Set()
    for key in graph.keys():
        for other in graph[key]:
            if undirected:
                keyother = Set([key,other])
                if keyother not in seen:
                    edges.add((key,other))
                    seen.add(keyother)                
            else:
                edges.add((key,other))
    return edges


def subgraph (graph, vertices):
    """Get the subgraph determined by the given vertices.
    """
    sub = {}
    for v in vertices:
        sub[v] = {}
        for other in Set(graph[v]) & Set(vertices):
            sub[v][other] = graph[v][other]
    return sub

def neighbors (graph, i, k=1):
    """Returns (k)neighbors of vertex i.
    
    The k-neighbors of i are all vertices no more than k steps away from i.
    """
    if k == 1:
        return Set(graph[i].keys())
    else:
        neigh = Set(neighbors(graph, i))
        for other in list(neigh):
            neigh |= neighbors(graph, other, k-1)
    try:
        neigh.remove(i)
    except KeyError:
        pass
    return neigh

def deledge (graph, i, j, undirected=True):
    """Delete edge (i,j) from the graph."""
    del graph[i][j]
    if undirected: del graph[j][i]