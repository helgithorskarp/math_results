"""Exact centred 3+1+1 census via forbidden physical cross-edge masks."""
from collections import Counter
from itertools import combinations
from pathlib import Path
import argparse,hashlib,json,time
HERE=Path(__file__).resolve().parent
FULL=(1<<16)-1

def need(ok,why):
    if not ok:raise ValueError(why)
def rows(x):return [(x>>(4*i))&15 for i in range(4)]
def columns(x):return [sum(((x>>(4*i+j))&1)<<i for i in range(4)) for j in range(4)]
def domain(kind):
    out=[]
    for x in range(1<<16):
        r=rows(x);c=columns(x)
        if kind=='RR':
            if 15 in r or 15 in c:continue
            if any((r[i]&r[j]).bit_count()>=3 or (c[i]&c[j]).bit_count()>=3 for i,j in combinations(range(4),2)):continue
        elif kind=='RB':
            if 0 in r or 15 in c:continue
        else:raise ValueError('domain kind')
        out.append(x)
    return out

def pattern(x):
    # A nonzero type is the unique missing row of a three-neighbour column.
    return tuple((15^c).bit_length() if c.bit_count()==3 else 0 for c in columns(x))
def code(t):return sum(v*5**k for k,v in enumerate(t))
def forbidden(t,u):return sum(1<<(4*j+k) for j in range(4) for k in range(4) if t[j]!=0 and t[j]==u[k])
def zeta(values):
    table=[0]*(1<<16)
    for x in values:table[x]+=1
    for bit in range(16):
        step=1<<bit
        for start in range(0,1<<16,2*step):
            for x in range(start+step,start+2*step):table[x]+=table[x-step]
    return table

def calculate(out):
    out=Path(out);out.mkdir();start=time.monotonic()
    rr=domain('RR');rb=domain('RB');bb=sorted(FULL^x for x in rr)
    need((len(rr),len(rb),len(bb))==(37823,35714,37823),'accepted pair-domain counts')
    hrr=Counter(pattern(x) for x in rr);hrb=Counter(pattern(x) for x in rb)
    hist=[]
    for kind,h in (('RR',hrr),('RB',hrb)):
        for t,w in sorted(h.items(),key=lambda item:code(item[0])):hist.append([kind,code(t),w])
    histogram=''.join(f'{k}\t{c}\t{w}\n' for k,c,w in hist).encode();(out/'HISTOGRAM.tsv').write_bytes(histogram)
    result={};profiles=[]
    for kind,left,right,last in (('same',hrr,hrr,rr),('majority',hrr,hrb,rb),('minority',hrb,hrb,bb)):
        allowed=zeta(last);numerator=0;mask_hist=Counter()
        for t,wt in sorted(left.items(),key=lambda item:code(item[0])):
            subtotal=0
            for u,wu in right.items():
                mask=forbidden(t,u);mask_hist[mask]+=wt*wu;subtotal+=wu*allowed[FULL^mask]
            profiles.append([kind,code(t),wt,subtotal])
        for mask,w in mask_hist.items():numerator+=w*allowed[FULL^mask]
        denominator=sum(left.values())*sum(right.values())*len(last)
        need(0<numerator<denominator,'nontrivial centred probability')
        raw=''.join(f'{m}\t{w}\t{allowed[FULL^m]}\n' for m,w in sorted(mask_hist.items())).encode()
        (out/(kind+'-masks.tsv')).write_bytes(raw)
        result[kind]=dict(allowed=numerator,total=denominator,mask_classes=len(mask_hist),mask_sha256=hashlib.sha256(raw).hexdigest())
    profile=''.join(f'{k}\t{t}\t{w}\t{v}\n' for k,t,w,v in profiles).encode();(out/'PROFILE.tsv').write_bytes(profile)
    domains={k:dict(count=len(v),sha256=hashlib.sha256(b''.join(x.to_bytes(2,'little') for x in v)).hexdigest()) for k,v in (('RR',rr),('RB',rb),('BB',bb))}
    result=dict(status='COMPLETE_CENTRED_TRIPLE_CENSUS',probabilities=result,domains=domains,histogram_sha256=hashlib.sha256(histogram).hexdigest(),histogram_rows=len(hist),profile_rows=len(profiles),profile_sha256=hashlib.sha256(profile).hexdigest(),source_graph_orders=[12],total_matrix_space=sum(x['total'] for x in result.values()))
    (out/'LOCAL.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps(dict(seconds=time.monotonic()-start,probabilities=result['probabilities'],histogram_rows=len(hist))),flush=True)
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('out');a=p.parse_args();calculate(a.out)
