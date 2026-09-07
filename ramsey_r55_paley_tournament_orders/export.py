#!/usr/bin/env python3
import itertools
import json
import sys
from extract import graph

with open(sys.argv[1],encoding='utf8') as f: matrix=graph(json.load(f))
edges=[(u,v) for u,v in itertools.combinations(range(43),2) if matrix[u][v]]
print(43,len(edges))
for u,v in edges: print(u,v)
