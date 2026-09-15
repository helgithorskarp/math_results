#!/usr/bin/env python3
"""Semantic controls for the exact conditional-core certificate."""
import copy,json
import verify as v

def main():
 c=json.loads((v.HERE/'certificate.json').read_text());valid=v.run(c);rejected=[]
 def reject(name,d):
  try:v.run(d)
  except ValueError:rejected.append(name)
  else:raise ValueError('accepted corruption: '+name)
 d=copy.deepcopy(c);d['proper4']='0'*241;reject('monochromatic whole word',d)
 d=copy.deepcopy(c);d['deletion_words']['10']=d['deletion_words']['10'].replace('-', '0');reject('missing omitted vertex marker',d)
 d=copy.deepcopy(c);d['without_private_contacts_word']='0'*241;reject('invalid inherited-contact extension',d)
 d=copy.deepcopy(c);d['source_ids'][10]=d['source_ids'][11];reject('duplicate physical vertex',d)
 d=copy.deepcopy(c);d['bad_word']=c['proper4'][:10];reject('changed input theorem',d)
 source,maps,_=v.geometry();ids=c['source_ids'];points=[source[i] for i in ids];edges=v.all_edges(points)
 left,right=set(maps[1]),set(maps[2]);inherited=[(a,b) for a,b in edges if {ids[a],ids[b]}<=left or {ids[a],ids[b]}<=right]
 found,nodes,_=v.decide_pinned(241,inherited,{i:int(ch) for i,ch in enumerate(v.BAD)})
 v.need(found is not None,'private-contact deletion must admit the bad input');v.proper(found,241,inherited)
 # A different direct fixed-order census checks the 95 complete Golomb inputs.
 adj=v.adjacency(10,v.all_edges(v.G));count=0;w=[0,1,2]+[-1]*7
 def enumerate_fixed(i):
  nonlocal count
  if i==10:count+=1;return
  for colour in range(4):
   if all(w[j]!=colour for j in adj[i] if j<i):w[i]=colour;enumerate_fixed(i+1)
  w[i]=-1
 enumerate_fixed(3);v.need(count==95,'independent Golomb census')
 print(json.dumps({'status':'CONTROLS_PASSED','valid_result':valid['status'],'semantic_corruptions_rejected':rejected,'contact_deleted_graph_sat':True,'contact_deleted_search_nodes':nodes,'independent_Golomb_count':count},indent=2,sort_keys=True))
if __name__=='__main__':main()
