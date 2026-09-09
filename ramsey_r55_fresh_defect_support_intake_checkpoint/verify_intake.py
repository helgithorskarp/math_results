"""Literal all-five-set census and all single-flip derivatives; no producer import."""
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json
import time

def need(x,why):
    if not x:raise ValueError(why)

def census(row):
    n=row['n'];h=row['red_hex']
    need(n==43 and len(h)==226 and all(c in '0123456789abcdef' for c in h),'graph format')
    word=int(h,16);need(word<2**903,'padding')
    colors=[[0]*n for _ in range(n)];index=[[0]*n for _ in range(n)]
    for p,(u,v) in enumerate(combinations(range(n),2)):
        colors[u][v]=colors[v][u]=(word>>p)&1
        index[u][v]=index[v][u]=p
    bad=[0,0];gradient=[0]*903;sets=0
    for a,b,c,d,e in combinations(range(n),5):
        bits=(colors[a][b],colors[a][c],colors[a][d],colors[a][e],colors[b][c],
              colors[b][d],colors[b][e],colors[c][d],colors[c][e],colors[d][e])
        red=sum(bits);sets+=1
        if red not in (0,1,9,10):continue
        indices=(index[a][b],index[a][c],index[a][d],index[a][e],index[b][c],
                 index[b][d],index[b][e],index[c][d],index[c][e],index[d][e])
        if red in (0,10):
            bad[red//10]+=1
            for p in indices:gradient[p]-=1
        else:
            minority=1 if red==1 else 0
            gradient[indices[bits.index(minority)]]+=1
    need(sets==962598,'all-five-set count')
    score=sum(bad)
    need(score==row['score'],'literal objective mismatch')
    need(min(gradient)>=0,'strict descent not finished')
    return {'seed_index':row['seed_index'],'score':score,'red_K5':bad[1],'blue_K5':bad[0],
            'minimum_flip_delta':min(gradient),'zero_delta_moves':gradient.count(0),
            'gradient_sha256':hashlib.sha256(json.dumps(gradient,separators=(',',':')).encode()).hexdigest(),
            'graph_sha256':hashlib.sha256(h.encode()).hexdigest(),'five_sets_examined':sets}

def verify(path,out):
    rows=[json.loads(s) for s in Path(path).read_text().splitlines()]
    need(len(rows)==32 or (rows and rows[-1]['score']==0),'incomplete fixed intake')
    results=[];started=time.monotonic()
    for i,row in enumerate(rows):
        need(row['seed_index']==i and row['seed']==202609090000+i,'seed registry')
        need(row['proposals']==524288 or row['score']==0,'proposal schedule')
        need(row['energy_checks']=='PASS','incremental control')
        results.append(census(row))
    scores=[r['score'] for r in results]
    distinct={r['red_hex'] for r in rows if r['score']<=16}
    result={'status':'LITERAL_INTAKE_VERIFIED','starts':len(rows),'qualifying_distinct_centers':len(distinct),
            'required_centers':8,'quality_ceiling':16,'gate_pass':len(distinct)>=8 or 0 in scores,
            'minimum_score':min(scores),'maximum_score':max(scores),'total_proposals':sum(r['proposals'] for r in rows),
            'literal_five_sets_examined':sum(r['five_sets_examined'] for r in results),
            'literal_single_flip_derivatives':903*len(rows),'results':results,
            'target_found':0 in scores,'seconds':time.monotonic()-started}
    Path(out).write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='results'},sort_keys=True))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('registry');parser.add_argument('output');a=parser.parse_args();verify(a.registry,a.output)
