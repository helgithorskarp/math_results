"""Ordinary edge-free rank floors/caps and original-label correspondence.

Every box is a local necessary projection, not a census of actual hosts.
The written proof, rather than a matched hash, supplies the global bridge.
"""
from itertools import product
import literal as L
import reference as R

def run(require,guard,digest):
    def core(r,rows,sy,e=(0,0,0)):
        red,d,q=L.build(r,rows,sy,e);bits,bd,bq=R.build(r,rows,sy,e)
        require(tuple(sum(1<<j for j in a) for a in red)==bits and d==bd and q==bq,
                'full literal/coordinate core correspondence')
        c=L.allowances(red,d)
        require(c==R.allowances(bits,bd),'all120 physical pair allowances')
        return red,d,q,c
    B={11,12,13,14,15,16,17,18,19,20,21}
    Nu=set(range(1,11));Nv={0,2,11,12,*range(16,22)}
    floors=[]
    for b in sorted(B):
        if b in (11,12):
            fixed={14,15} if b==11 else {13,14};free=list(range(16,22))
        elif b in (13,14,15):
            fixed={12} if b==13 else {11,12} if b==14 else {11};free=list(range(16,22))
        else:fixed=set();free=sorted(B-{b})
        for w in range(1<<len(free)):
            nb=fixed|{x for i,x in enumerate(free) if w>>i&1}
            D=len(nb);physical=[x for x in range(22) if x not in (0,b) and x not in Nu and x not in nb]
            require(len(physical)==10-D,'blue u-b floor on original22 labels')
            if b in (11,12):
                red_pages=1+(nb&set(range(16,22))).__len__()
                require((D>=4 and red_pages<=3)==((nb&set(range(16,22))).__len__()==2),
                        'SY Q rank exactly2, no E bound')
            elif b>=16:
                nb.add(1);s=len(nb&{11,12});t=len(nb&{13,14,15});h=len(nb&set(range(16,22)))
                require(len(Nv&nb)==s+h and D==s+t+h,'literal red v-q and B-degree')
                if D>=4 and s+h<=3:require(t>=1+(D-4),'pointwise T incidence lower bound')
            floors.append([b,w,D,len(physical)])
        guard()
    require(len(floors)==6464,'whole original B floor projections')

    caps=[]
    for r,k,w in product((0,1),range(3),range(64)):
        rows=[L.H,L.K,L.C] if r==0 else [L.K,L.H,L.C];rows[k]=w
        partner=((10,9,9) if r==0 else (9,10,9))[k]
        owner=R.OWN[partner-9]
        for rank in range((3,2,3)[k],7):
            e=[0,0,0];e[k]=rank-(3,2,3)[k]
            red,d,q,c=core(r,tuple(rows),(L.P,L.S),tuple(e))
            known=len(red[partner]&red[13+k]);lower=max(0,4+rank-6)
            require(q[partner]==4 and q[13+k]==rank and known==1+(w&owner).bit_count(),
                    'generic SX/T red page and Q-rank identity')
            possible=lower<=c[partner,13+k]
            if rank>4:require(not possible,'original red SX/T spine excludes every rank>4')
            caps.append([r,k,w,rank,known,lower,possible])
        guard()
    require(len(caps)==1664,'entire generic rank-page domain')
    raw=list(product(range(3,7),range(2,7),range(3,7)))
    retained=[a for a in raw if all(x<=4 for x in a)]
    require(len(raw)==80 and len(retained)==12,'ordinary rank pruning80 to12')

    vpages=[]
    for r,i,D in product((0,1),range(6),range(32)):
        if bool(D&16)!=(i<2) or D.bit_count()>(4 if i<2 else 3):continue
        words=[(1<<i if D>>j&1 else 0) for j in range(4)]
        red,d,q,c=core(r,(*words[2:],L.C),tuple(words[:2]))
        s=(D&3).bit_count();t=(D>>2).bit_count();qi=(7 if i<2 else 6)-D.bit_count()
        require(q[1]==6 and q[3+i]==qi and c[1,3+i]==5-s,'blue v-X Q allowance')
        nv=red[1]|set(range(16,22));nx=red[3+i]|set(range(16,16+qi))
        blue=[a for a in range(22) if a not in (1,3+i) and a not in nv and a not in nx]
        require(len(nv)==len(nx)==10 and len(blue)==1+s+qi,'literal original blue v-X pages')
        ok=qi<=c[1,3+i]
        require(ok==(t>=(2 if i<2 else 1)) and ok==(len(blue)<=6),
                'v-X forces T0/T1 union all X when T2=C')
        vpages.append([r,i,D,s,t,qi,len(blue),ok])
    require(len(vpages)==180,'whole v-X local endpoint domain')
    guard()
    return {'complete':True,'claim_scope':'Ordinary local floors/caps; no E or outside global-degree input',
            'B_floor_records':[len(floors),digest(floors)],
            'all1664_SX_T_rank_cells':[len(caps),digest(caps)],
            'initial_rank_triples':raw,'necessary_rank_triples':retained,
            'all180_v_X_endpoint_cells':[len(vpages),digest(vpages)]}
