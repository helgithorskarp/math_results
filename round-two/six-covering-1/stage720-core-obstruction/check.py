"""Exact CRT-core regeneration and first-stage completion obstruction."""
from collections import Counter
import copy
import hashlib
import itertools
import json
from pathlib import Path
import time

ROOT=Path(__file__).resolve().parent
CORE=(10,12,15,16,18,20)
PAIRS=((24,30),(36,40),(45,48),(60,72),(80,90),(120,144),(180,240),(360,720))
LEFT=(10,15,20);RIGHT=(12,16,18);CAPS=(34,34,34,34,27)

def need(ok,message):
    if not ok:raise ValueError(message)

def bits(xs):return sum(1<<x for x in xs)

class Data:
    def __init__(self):
        self.R=bits(x for x in range(720) if x%8!=5 and x%9!=6 and x%18!=3)
        self.S=bits(4*t for t in range(180) if t%9!=6)
        self.F=self.R&~self.S
        self.B=tuple(bits(4*t for t in range(180) if t%9!=6 and t%2!=p and t%3!=b) for p in range(2) for b in (1,2))+(bits(4*t for t in range(180) if t%9!=6 and t%3==0),)
        need((self.R.bit_count(),self.F.bit_count(),self.S.bit_count())==(530,370,160),'physical sets')
        self.phase={m:[bits(range(a,720,m))&self.R for a in range(m)]+[0] for m in CORE+tuple(m for g in PAIRS for m in g)}
        self.choices={m:sorted(Counter(v).items()) for m,v in self.phase.items()}
    def allowed(self,mask):return all((mask&b).bit_count()<=c for b,c in zip(self.B,CAPS))

def patterns(n):
    if not n:yield ();return
    def visit(prefix):
        if len(prefix)==n:yield tuple(prefix);return
        for a in range(max(prefix,default=-1)+2):yield from visit(prefix+[a])
    yield from visit([])

def multiplicity(p):
    v=1
    for k in range(max(p,default=-1)+1):v*=5-k
    return v

def crt(d,r,f):return r+d*(((f-r)*pow(d,-1,5))%5)

TRANS=[(1+12*k,36*(k%2)+72*e) for k in range(12) for e in range(2)]

def norm(p):
    seen={};out=list(p)
    for m in LEFT:
        i=CORE.index(m);a=p[i]
        if a is None:continue
        f=a%5;seen.setdefault(f,len(seen));out[i]=crt(m//5,a%(m//5),seen[f])
    return tuple(out)

def transform(p,u,v):
    return norm(tuple(None if a is None else (u*a+v)%m if m%5 else crt(m//5,(u*a+v)%(m//5),a%5) for m,a in zip(CORE,p)))

def key(p):return tuple(-1 if a is None else a for a in p)

def census(d):
    left=[];right=[]
    for active in itertools.product((False,True),repeat=3):
        ids=[i for i,a in enumerate(active) if a]
        for pattern in patterns(len(ids)):
            fs=dict(zip(ids,pattern))
            domains=[range(m//5) if active[i] else [None] for i,m in enumerate(LEFT)]
            for rs in itertools.product(*domains):
                p=tuple(crt(m//5,r,fs[i]) if r is not None else None for i,(m,r) in enumerate(zip(LEFT,rs)))
                mask=0
                for m,a in zip(LEFT,p):mask|=d.phase[m][m if a is None else a]
                left.append((p,mask,multiplicity(pattern)))
    for phases in itertools.product(range(1,12),range(17),range(19)):
        mask=0
        for m,a in zip(RIGHT,phases):mask|=d.phase[m][a]
        right.append((tuple(None if a==m else a for m,a in zip(RIGHT,phases)),mask))
    need(len(left)==182 and sum(w for p,m,w in left)==3696 and len(right)==3553,'CRT phase omission inventory')
    rows={};normalized=set();raw=0
    for (lp,lm,w),(rp,rm) in itertools.product(left,right):
        mask=lm|rm
        if (mask&d.F).bit_count()<204 or not d.allowed(mask):continue
        by_m=dict(zip(LEFT,lp));by_m.update(zip(RIGHT,rp));p=tuple(by_m[m] for m in CORE)
        need(all(a is not None for a in p),'admissible core omitted resource')
        orbit={transform(p,u,v) for u,v in TRANS};rep=min(orbit,key=key)
        normalized.add(p);raw+=w
        row=rows.setdefault(rep,{'original_phases':list(rep),'raw_count':0,'normalized_count':0,'affine_normalized_orbit_size':len(orbit),'Fgain':(mask&d.F).bit_count(),'Sgain':(mask&d.S).bit_count()})
        row['raw_count']+=w;row['normalized_count']+=1
    for rep,row in rows.items():
        orbit={transform(rep,u,v) for u,v in TRANS}
        need(orbit<=normalized and len(orbit)==row['normalized_count'],'affine orbit coverage')
        seen={};pattern=[]
        for m in LEFT:
            f=rep[CORE.index(m)]%5;seen.setdefault(f,len(seen));pattern.append(seen[f])
        row['fibre_pattern']=pattern
        need(row['raw_count']==len(orbit)*multiplicity(pattern),'S5 multiplicity')
    need(raw==2560 and len(normalized)==48 and len(rows)==14,'complete core totals')
    return [rows[p] for p in sorted(rows,key=key)]

def complete_rows(d):
    rows=census(d)
    for row in rows:
        cmask=0
        for m,a in zip(CORE,row['original_phases']):cmask|=d.phase[m][a]
        target=d.F&~cmask;row['pairs']=[]
        for group in PAIRS:
            best=-1;best_masks=None;accepted=0;rejected=0
            for a,wa in d.choices[group[0]]:
                if not d.allowed(cmask|a):rejected+=wa*(group[1]+1);continue
                for b,wb in d.choices[group[1]]:
                    union=a|b
                    if not d.allowed(cmask|union):rejected+=wa*wb;continue
                    accepted+=wa*wb;gain=(union&target).bit_count()
                    if gain>best:best=gain;best_masks=(a,b)
            need(accepted+rejected==(group[0]+1)*(group[1]+1),'original pair omission accounting')
            phases=[]
            for m,mask in zip(group,best_masks):
                a=d.phase[m].index(mask);phases.append(None if a==m else a)
            literal=[x for x in range(720) if target&(1<<x) and any(a is not None and x%m==a for m,a in zip(group,phases))]
            need(len(literal)==best,'literal maximizing witness')
            row['pairs'].append({'moduli':list(group),'capacity':best,'maximizing_original_phases':phases,'accepted_raw':accepted,'rejected_raw':rejected})
        row['remaining_demand']=target.bit_count();row['completion_capacity']=sum(p['capacity'] for p in row['pairs'])
        row['strict_gap']=row['remaining_demand']-row['completion_capacity']
        need(row['strict_gap']>0,'canonical core not excluded')
    return rows

def validate(cert,rows):
    need(cert['period']==720 and cert['fixed']==[[5,8],[6,9]] and cert['holes_confined_to']==[[3,18],[0,4]],'scope damaged')
    need(cert['F_size']==370 and cert['S_size']==160 and cert['core_min_F_gain']==204 and cert['original12_present_nonzero'] is True,'core premise damaged')
    need(cert['target_caps']==list(CAPS) and cert['blocks']==[list(CORE)]+[list(g) for g in PAIRS],'caps or ORIGINAL partition damaged')
    need(cert['raw_core_product']==13131888 and cert['raw_core_accepted']==2560 and cert['normalized_core_accepted']==48 and cert['canonical_core_count']==14,'core inventory damaged')
    need(cert['affine_map_count']==24 and cert['full_symmetry_maps']==2880,'symmetry inventory damaged')
    need(cert['cores']==rows,'complete regenerated core and every pair maximum/count differs')

def damages(cert,rows):
    mutations=[lambda c:c.__setitem__('core_min_F_gain',203),lambda c:c.__setitem__('original12_present_nonzero',False),
               lambda c:c['target_caps'].__setitem__(4,28),lambda c:c['fixed'][0].__setitem__(0,4),
               lambda c:c.__setitem__('raw_core_accepted',2561),lambda c:c['cores'].pop(),
               lambda c:c['cores'][0]['original_phases'].__setitem__(1,0),lambda c:c['cores'][0].__setitem__('raw_count',361),
               lambda c:c['cores'][0]['pairs'][0].__setitem__('capacity',999),lambda c:c['cores'][0]['pairs'][0].__setitem__('accepted_raw',0)]
    for mutation in mutations:
        bad=copy.deepcopy(cert);mutation(bad)
        try:validate(bad,rows)
        except ValueError:pass
        else:raise ValueError('semantic damage accepted')
    return len(mutations)

def main():
    start=time.monotonic();cert=json.loads((ROOT/'certificate.json').read_text());rows=complete_rows(Data());validate(cert,rows)
    out={'status':'COMPLETE_CRT_CORE_AND_FIXED_PAIR_REPLAY_PASSED','canonical_cores':14,'raw_core_product':13131888,
         'raw_core_accepted':2560,'normalized_cores':48,'pair_maxima_compared':112,'all_six_core_resources_present':True,
         'strict_gaps':[r['strict_gap'] for r in rows],'semantic_damages_rejected':damages(cert,rows),
         'certificate_sha256':hashlib.sha256((ROOT/'certificate.json').read_bytes()).hexdigest()}
    expected=json.loads((ROOT/'expected.json').read_text());need(out==expected,'expected output differs')
    out['seconds']=time.monotonic()-start;print(json.dumps(out))

if __name__=='__main__':main()
