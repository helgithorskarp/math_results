#!/usr/bin/env python3
"""Literal good23 check and exhaustive side-word proof of no good24 extension."""
import hashlib,json
from itertools import combinations
from pathlib import Path

def need(ok,message):
    if not ok:raise ValueError(message)

def verify(data):
    need(data['n']==23 and data['component_orders']==[10,13],'fixture shape')
    text=data['red_hex'];need(isinstance(text,str) and len(text)==64 and all(c in '0123456789abcdef' for c in text),'core word')
    word=int(text,16);need(word<1<<253,'core padding')
    a=[[False]*23 for _ in range(23)]
    for i,(u,v) in enumerate(combinations(range(23),2)):a[u][v]=a[v][u]=bool(word>>i&1)
    checks=0
    for q in combinations(range(23),5):
        values=[a[u][v] for u,v in combinations(q,2)]
        need(any(values) and not all(values),'core contains a monochromatic five')
        checks+=1
    need(all(not a[u][v] for u in range(10) for v in range(10,23)),'core is not anticomplete across its two parts')
    rows=[]
    for vertices in (list(range(10)),list(range(10,23))):
        red4=[q for q in combinations(vertices,4) if all(a[u][v] for u,v in combinations(q,2))]
        blue2=[q for q in combinations(vertices,2) if not a[q[0]][q[1]]]
        counts={'red_four':0,'blue_pair':0};digest=hashlib.sha256()
        for word in range(1<<len(vertices)):
            red={v for i,v in enumerate(vertices) if word>>i&1};blue=set(vertices)-red
            q=next((t for t in red4 if set(t)<=red),None)
            kind='red_four'
            if q is None:
                q=next((t for t in blue2 if set(t)<=blue),None);kind='blue_pair'
            need(q is not None,'uncovered attachment word')
            # Directly verify the returned physical labels and the contact word.
            if kind=='red_four':need(len(q)==4 and set(q)<=red and all(a[u][v] for u,v in combinations(q,2)),'bad red-four witness')
            else:need(len(q)==2 and set(q)<=blue and not a[q[0]][q[1]],'bad blue-pair witness')
            counts[kind]+=1
            digest.update((json.dumps([word,kind,list(q)],separators=(',',':'))+'\n').encode())
        rows.append({'order':len(vertices),'attachment_words':1<<len(vertices),'counts':counts,'witness_sha256':digest.hexdigest()})
    return {'status':'VERIFIED_GOOD23_WITH_NO_GOOD24_EXTENSION','literal_five_sets_checked':checks,'side_certificates':rows,'joint_words_covered_by_product_implication':1<<23,'unrestricted_new_vertices_for_target43':20,'unrestricted_target_edge_variables':650,'good43_found':False,'catalog_completeness_required':False}

if __name__=='__main__':
    here=Path(__file__).resolve().parent
    print(json.dumps(verify(json.loads((here/'UNEXTENDABLE_CORE.json').read_text())),indent=2,sort_keys=True))
