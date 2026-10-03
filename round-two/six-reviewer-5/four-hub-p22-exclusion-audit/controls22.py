"""Independent literal-witness and fixed-N polynomial checks; semantic damages.
Valid local/necessary images never assert existence of a71-word packing.
"""
import collections,itertools as it,json,time
from independent import P,PAIRS,TRIPLES,F,local,enc,need
from columns22 import physical,option_tables,column,carriers

def reconstruct(stars,types,si,role):
    words=[sum(1<<a for a in w) for w in stars[si]]
    incidence=[[w for w in words if w>>a&1] for a in range(17)]
    delta=[5-len(v) for v in incidence];high=[a for a,d in enumerate(delta) if d];H=set(role)
    # Literal mask ownership, independent of the physical producer's leave sets.
    uncovered=lambda a,b:not any(w>>b&1 for w in incidence[a])
    edges=[(a,b) for a,b in it.combinations(high,2) if uncovered(a,b)]
    hubs=H&set(high);e=5-len(high);k=len(hubs)
    q=sum(a in hubs or b in hubs for a,b in edges)
    eligible=any(not any(a in p for p in edges) for a in hubs)
    g1=sum(delta[a]==1 for a in high if a not in H)
    sigma=sum(delta[a]-1 for a in high if a not in H)
    psi=g1 if e==0 and eligible else (-g1 if e>0 and not eligible else 0)
    typ=types.index((e,k,q,eligible,len(high),g1,sigma,psi,psi-3*(k-e-q)))
    d=tuple(delta[a] for a in role)
    hh=sum(int(uncovered(role[a],role[b]))<<j for j,(a,b) in enumerate(PAIRS))
    hhh=sum(int(any(all(w>>role[a]&1 for a in t) for w in words))<<j for j,t in enumerate(TRIPLES))
    wc=tuple(sum(sum(w>>a&1 for a in H)==j for w in words) for j in range(5))
    iso=sum(int(a in high and not any(a in p for p in edges))<<j for j,a in enumerate(role))
    L=tuple(sum(delta[t]==0 and t not in H and uncovered(a,t) for t in range(17) if t!=a) if delta[a] else 0 for a in role)
    return [typ,list(d),hh,hhh,list(wc),iso,list(L)]

def fixed_N(counts,options,D,N):
    # Ordinary coefficient support in z^deficit y^positive over parity Z/2.
    # Fix N BEFORE multiplying, rather than retaining a max friend requirement.
    state={(0,0,0)}
    for i,n in enumerate(counts):
        if not n:continue
        factor={(d,int(d>0),p) for d,r,p in options.get(i,[]) if r<=N}
        if not factor:return False
        for _ in range(n):
            state={(a+d,b+k,c^p) for a,b,c in state for d,k,p in factor if a+d<=D and b+k<=N}
            if not state:return False
    return (D,N,0) in state

def verify_row(item,stars,types):
    si,role=item['witness'];actual=reconstruct(stars,types,si,role)
    need(actual==item['signature'],'actual literal quadruple signature mismatch')

def main():
    start=time.monotonic();stars,raw,types,hist=local();data=json.loads((P/'physical22.json').read_text())
    records=data['physical_rows'];physical_rows=physical();tables=option_tables(physical_rows)
    checked=[];Cs=[]
    for ordinal,item in enumerate(records):
        verify_row(item,stars,types);s=item['signature']
        if s[0]==18:
            a=next(a for a,d in enumerate(s[1]) if d)
            need(s[1][a]==2 and s[6][a]>=4 and s[5]>>a&1,'literal C5 seven-neighbor mechanism')
            Cs.append(dict(row=ordinal,role=a,friends=s[6][a]))
        checked.append(ordinal)
    chosen={};summary=collections.Counter();labelled,canonical=carriers()
    for f in sorted((P/'column-phases').glob('*.json')):
        x=json.loads(f.read_text());summary.update(x['summary'])
        for pop in x['records']:
            for c in pop['carriers']:
                if not c['complete_choices']:continue
                D=canonical[c['carrier']][1]
                for a in range(4):
                    key=(tuple(pop['counts']),a==0,D[a]);chosen[key]=c['coordinate_support_sets'][a]
    polynomial=[]
    for (counts,heavy,D),expected in sorted(chosen.items()):
        role=0 if heavy else 1
        actual=[N for N in range(D+1) if fixed_N(counts,tables[role],D,N)]
        need(actual==expected,'whole retained-column fixed-N polynomial support differs from minmax-DP')
        polynomial.append(dict(counts=counts,heavy=heavy,D=D,all_N=actual))
        if time.monotonic()-start>45:raise RuntimeError('INCOMPLETE fixed45-second literal/coefficient control guard')
    need(len(Cs)==88,'all actual C signature witnesses, not just one representative')
    first=next(item for item in records if item['signature'][0]==18)
    damages=[]
    for name,path in [('wrong_delta',(1,0)),('wrong_HH_leave',(2,None)),('wrong_HHH',(3,None)),
                      ('wrong_hub_word_count',(4,0)),('wrong_isolation',(5,None)),('wrong_friend_count',(6,0))]:
        damaged=json.loads(json.dumps(first));j,k=path
        if k is None:damaged['signature'][j]^=1
        else:damaged['signature'][j][k]+=1
        try:verify_row(damaged,stars,types)
        except ValueError as e:damages.append(dict(name=name,rejected_for=str(e)))
        else:raise ValueError('semantic literal damage accepted:'+name)
    # Small exact column-polynomial models: zero deficits, a positive odd
    # friend total, and its two-vertex simple-edge counterpart. These are
    # algebraic factor controls, not literal stars or global packings.
    opts={0:[(0,0,0)],1:[(1,1,0)],2:[(1,2,1)]}
    images=[]
    for counts,D,N,expected in [([3,0,0],0,0,True),([0,2,0],2,2,True),
                                ([0,1,1],2,2,False),([0,0,2],2,2,True)]:
        actual=N in column(counts,opts,D)
        need(actual==fixed_N(counts,opts,D,N)==expected,'polynomial/parity boundary control')
        images.append(dict(counts=counts,D=D,N=N,accepted=actual))
    result=dict(all_literal_witness_rows=checked,complete_C_witnesses=Cs,
                complete_positive_carrier_column_coefficient_checks=polynomial,
                semantic_literal_rejections=damages,valid_or_parity_obstructed_column_images=images,
                complete_exclusion_summary=summary)
    (P/'controls22.json').write_bytes(enc(result))
    print(json.dumps(dict(witnesses=len(checked),C_witnesses=len(Cs),whole_fixedN_support_checks=len(polynomial),
                         semantic_rejections=len(damages),column_images=len(images),seconds=time.monotonic()-start)),flush=True)

if __name__=='__main__':main()
