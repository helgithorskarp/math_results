#!/usr/bin/env python3
"""A fixed four-colouring extends after any at-most-two plane points are added."""
from pathlib import Path
from collections import Counter
from math import comb
import argparse,json
import geometry as G
HERE=Path(__file__).resolve().parent

def colour_lists(edges,neighbors,cedges,color=None):
 raw=(HERE/'host_colors.txt').read_text().splitlines()
 if len(raw)!=1:raise ValueError('expected one fixed host colouring')
 c=tuple(map(int,raw[0])) if color is None else tuple(color)
 if len(c)!=506 or not set(c)<=set(range(4)) or any(c[i]==c[j] for i,j in edges):raise ValueError('invalid host colouring')
 available=[]
 for nn in neighbors:
  used=0
  for v in nn:used|=1<<c[v]
  available.append(15^used)
 if not all(available):raise ValueError('single-point obstruction')
 bad=[(i,j) for i,j in cedges if available[i]==available[j] and available[i].bit_count()==1]
 if bad:raise ValueError('adjacent equal-singleton obstruction')
 return available

def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--work',type=Path,required=True);args=parser.parse_args();args.work.mkdir(parents=True,exist_ok=False)
 P=G.host();ds,adj,edges=G.distances(P);points,neighbors,positive,screen=G.candidates(P,ds,adj)
 cedges,pairs=G.graph(P,points,neighbors);available=colour_lists(edges,neighbors,cedges)
 data={'points':points,'neighbors':neighbors,'positive_triples':positive,'candidate_edges':cedges,'available_masks':available}
 (args.work/'candidates.json').write_text(json.dumps(data,separators=(',',':'))+'\n')
 result={'host_vertices':len(P),'host_edges':len(edges),'host_edge_sha256':G.digest(edges),'triples':comb(len(P),3),'screen':screen,'candidate_points':len(points),'positive_triples':len(positive),'positive_triple_sha256':G.digest(positive),'candidate_point_sha256':G.digest(points),'neighbor_sha256':G.digest(neighbors),'degree_histogram':dict(sorted(Counter(map(len,neighbors)).items())),'host_candidate_edges':sum(map(len,neighbors)),'candidate_edges':len(cedges),'candidate_edge_sha256':G.digest(cedges),'adjacency_checks':pairs,'fixed_host_colourings':1,'available_list_size_histogram':dict(sorted(Counter(m.bit_count() for m in available).items())),'available_mask_sha256':G.digest(available),'adjacent_singleton_pairs':sum(available[i].bit_count()==available[j].bit_count()==1 for i,j in cedges),'adjacent_equal_singleton_pairs':0,'single_point_cases':len(points),'two_point_cases':comb(len(points),2),'uncovered':0}
 (args.work/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
