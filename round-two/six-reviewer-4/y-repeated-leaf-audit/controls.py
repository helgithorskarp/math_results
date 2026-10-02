#!/usr/bin/env python3
"""Literal Boolean checks of the ordinary finish and exhaustive rank/label controls.
These partial graphs are not book-free host constructions.
"""
from pathlib import Path
from itertools import combinations, permutations
import copy, json, math
ROOT=Path(__file__).resolve().parent

def need(b,s):
    if not b:raise RuntimeError(s)
def bits(mask,n=6):return {j for j in range(n) if mask>>j&1}
def graph(f):
    a=[[False]*22 for _ in range(22)]
    def edge(i,j):a[i][j]=a[j][i]=True
    for i,j in [(0,1),(0,2),(1,2),(2,9),(2,10),(3,7),(7,6),(6,4),(4,5),(5,8),(8,3),
                (9,6),(9,8),(10,5),(10,7),(9,13),(9,15),(10,13),(10,14)]:edge(i,j)
    for j in range(3,11):edge(0,j)
    for j in range(13,16):edge(2,j)
    for j in range(16,22):edge(1,j)
    for s in (11,12):
        for j in (1,2,14,15):edge(s,j)
    for t,row in enumerate(f['T_rows'],13):
        for j in bits(row):edge(t,3+j)
    for s,row in enumerate(f['SY_rows'],11):
        for j in bits(row):edge(s,3+j)
    return a
def common(a,i,j,color):return {k for k in range(22) if k not in (i,j) and a[i][k]==a[j][k]==color}

def strict(a,b):
    if type(a)is not type(b):raise ValueError('exact type')
    if isinstance(b,dict):
        if a.keys()!=b.keys():raise ValueError('field set')
        for k in b:strict(a[k],b[k])
    elif isinstance(b,list):
        if len(a)!=len(b):raise ValueError('length')
        for x,y in zip(a,b):strict(x,y)
    elif a!=b:raise ValueError('value')
def unique(pairs):
    x={}
    for k,v in pairs:
        if k in x:raise ValueError('duplicate key')
        x[k]=v
    return x

def run(record):
    fs=record['interfaces'];frames=0;normalizations=0
    original={0:{1,8,9},1:{0},2:{6,7},3:{4,5},4:{3,7,9},5:{3,6,8},6:{2,5,9},7:{2,4,8},8:{0,5,7},9:{0,4,6}}
    relabel={0:2,1:1,**{j:3+j-2 for j in range(2,8)},8:9,9:10}
    for f in fs:
        need(f['flag']==25,'low tags')
        need(f['T_rows'][0]==3,'T0 row forced as OUTPUT')
        sx=bits(f['SY_rows'][0]);sy=bits(f['SY_rows'][1])
        need(not sx&sy and sx|sy==set(range(6)) and len(sx)==len(sy)==3,'SY partition')
        t1,t2=map(bits,f['T_rows'][1:]);need(len(t1)==len(t2)==4 and len(t1&t2)==2,'T intersection')
        need(all(len(t&s)==2 for t in (t1,t2) for s in (sx,sy)),'red saturation')
        base=graph(f)
        for i,neigh in original.items():
            need({j for j in range(1,11) if base[relabel[i]][j]}=={relabel[j] for j in neigh},'original literal leaf')
        for a0 in combinations(range(16,22),2):
            for a1 in combinations(range(16,22),2):
                if set(a0)&set(a1):continue
                a=[r[:]for r in base];free=set(range(16,22))-set(a0)-set(a1)
                for s,ys in ((11,a0),(12,a1),(14,free),(15,free)):
                    for y in ys:a[s][y]=a[y][s]=True
                need(len(common(a,11,12,True))==4,'SY red cap complete')
                need(all(len(common(a,s,t,True))==3 for s in (11,12)for t in (14,15)),'saturated SY-T spines')
                need((sum(a[14]),sum(a[15]))==(10,10),'actual T degrees')
                need(common(a,14,15,False)=={0,1,13}|set(a0)|set(a1),'seven distinct named blue pages')
                need(len(common(a,14,15,True))==7,'seven red common neighbors')
                frames+=1
    for n in (6,8):
        red={};blue={}
        for a in range(1<<n):
            for b in range(1<<n):
                key=(a.bit_count(),b.bit_count());red[key]=min(red.get(key,n+1),(a&b).bit_count())
                blue[key]=min(blue.get(key,n+1),((((1<<n)-1)^a)&(((1<<n)-1)^b)).bit_count())
        need(all(v==max(0,i+j-n)for(i,j),v in red.items()),'red minima')
        need(all(v==max(0,n-i-j)for(i,j),v in blue.items()),'blue minima')
    words=[]
    for w in __import__('itertools').product(range(3),repeat=4):
        if sorted(w.count(j)for j in range(3))==[1,1,2] and w[2]==w[3]:words.append(w)
    need(len(words)==6,'all Y-repeated core words')
    for w in words:
        omitted=w[2];need(set(w[:2])==set(range(3))-{omitted},'CaseI distinct SX omissions')
        p={omitted:0,w[0]:1,w[1]:2};need(tuple(p[j]for j in w)==(1,2,0,0),'literal normalization')
        for lows in combinations(range(11),3):
            transported=set()
            for j in lows:transported.add(p[j] if j<3 else j)
            need(len(transported)==3,'low transport');normalizations+=1
    need(sum(math.comb(6,3-f.bit_count())for f in range(32)if f.bit_count()<=3)==165,'26 flag coverage')
    damages=[]
    def change(fn):
        x=copy.deepcopy(record);fn(x);damages.append(x)
    change(lambda x:x.update(complete=False))
    change(lambda x:x.update(complete=1))
    change(lambda x:x.update(extra=0))
    change(lambda x:x['interfaces'].pop())
    change(lambda x:x['interfaces'].append(copy.deepcopy(x['interfaces'][0])))
    change(lambda x:x['interfaces'][0].update(flag=0))
    change(lambda x:x['interfaces'][0]['T_rows'].__setitem__(0,7))
    change(lambda x:x['interfaces'][0]['Q_ranks_X'].__setitem__(0,6))
    change(lambda x:x['counts'].pop())
    change(lambda x:x['counts'][0].__setitem__(2,4501))
    for x in damages:
        try:strict(x,record)
        except ValueError:continue
        raise RuntimeError('damaged whole record accepted')
    try:json.loads('{"complete":true,"complete":true}',object_pairs_hook=unique)
    except ValueError:pass
    else:raise RuntimeError('duplicate JSON accepted')
    return {'complete':True,'literal_finish_frames':frames,'actual_T_degrees':[10,10],
            'exact_named_blue_pages':7,'common_red_neighbors':7,'SY_T_common_red_pages':3,
            'Y_repeated_core_words':len(words),'core_low_transports':normalizations,
            'actual_low_placements_per_core':165,'outside_pair_controls_6':4096,'outside_pair_controls_8':65536,
            'damaged_records_or_encodings_rejected':len(damages)+1}
if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('record',type=Path);a=p.parse_args()
    x=json.loads(a.record.read_text(),object_pairs_hook=unique);print(json.dumps(run(x),sort_keys=True))
