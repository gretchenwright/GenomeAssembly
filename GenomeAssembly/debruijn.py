from collections import deque
import random
from graphviz import Digraph

def drawGraph(black_edges, red_edges, start, end):
	C = Digraph(format='png')
	C.attr(rankdir = 'LR', size = '15', constraint='false')
	S = set(black_edges.keys())
	T = set(red_edges.keys())
	U = S.union(T)
	C.attr('node', shape='circle')
	for node in sorted(list(U)):
		if node in [start, end]:
			C.node(node, color = 'red', style='filled')
		else:
			C.node(node)
	for tail in black_edges:
		for head in black_edges[tail]:
			C.edge(tail, head)
	C.attr('edge', color='red')
	for tail in red_edges:
		for head in red_edges[tail]:
			C.edge(tail, head)
	return C

def eulerianCircuit(G): # G must be a connected and balanced (Eulerian) graph
	H = {k:v for k, v in G.items()}
	nEdges = sum(len(H[i]) for i in H)
	node = next(iter(H.keys()))
	stack = deque([[node]])
	J = dict()
	C = drawGraph(H, J, node, node)
	count = 0
	filename = 'output/graph' + str(count) + '.gv'
	C.render(filename)
	while nEdges > 0:
		path = stack.pop()
		while H[path[-1]] == []:
			stack.appendleft(path)
			path = stack.pop()
		node = path[-1] 
		while H[node] != []: # node has unused edges
			dest = H[node].pop()
			J[node] = J.get(node, []) + [dest]
			nEdges -= 1
			# if we didn't use up all the edges of node, break the path so we know to recheck
			if H[node]:
				stack.append(path)
				path = [node]
			path.append(dest)
			node = dest
			if stack:
				start = stack[0][0]
			else:
				start = path[0]
			C = drawGraph(H, J, start, path[-1])
			count += 1
			filename = 'output/graph' + str(count) + '.gv'
			C.render(filename)
		# now we are stuck
		stack.appendleft(path)
	# Glue the segments together
	path = []
	for segment in stack:
		path += segment[:-1]
	path.append(segment[-1])
	return path
	
def eulerianPath(G, start, end): # takes a semibalanced graph as input - start and end are the unbalanced nodes
	G[end] += [start]
	path = eulerianCircuit(G)
	ix = path.index(end)
	while path[ix + 1] != start:
		ix = path[ix + 1:].index(start) + ix
	path = path[ix + 1:-1] + path[:ix + 1]
	return path
	
def assemble(path):
	string = ''
	for i in range(len(path)):
		string += path[i][0]
	string += path[-1][1:]
	return string
	
def process(string, k):
	# construct de bruijn graph
	N = len(string)
	G = {node:[] for node in [string[i:i + k - 1] for i in range(N - k + 2)]}
	for i in range(N - k + 1):
		kmer = string[i:i + k]
		G[kmer[:-1]].append(kmer[1:])
	EP = eulerianPath(G, string[:k - 1], string[N - k + 1:])
	return assemble(EP)
	
def randomString(N):
	bases = 'ACGT'
	string = ''
	for i in range(N):
		string += bases[random.randrange(4)]
	return string
	
def computeStats():
	nPasses = 0
	nFails = 0
	for i in range(100):
		N = 20
		string = randomString(N)
		k = 5
		A = process(string, k)
		if A == string:
			nPasses += 1
		else:
			nFails += 1
			print(string, A)
	print(f'Found {nPasses} passing cases and {nFails} failures out of {nPasses + nFails} attempts.')

string = 'TCCTCCAATTTAGCTCCCGT'
# string = randomString(20)
# string = 'AATAAACTCTCGTTCGATAA'
print(string)
print(process(string, 4))
































# computeStats()
