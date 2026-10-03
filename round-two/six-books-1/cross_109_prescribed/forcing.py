"""Corroborate the written VARIABLE-rank reduction, not a B-four-regular input."""
from itertools import product
import literal as L
import reference as R

def run(require,guard,digest):
    def core(rows,sy,e=(0,0,0),r=0):
        red,d,q=L.build(r,rows,sy,e); bits,bd,bq=R.build(r,rows,sy,e)
        require(tuple(sum(1<<j for j in a) for a in red)==bits and d==bd and q==bq,
                'whole old-label/coordinate variable-degree core')
        caps=L.allowances(red,d)
        require(caps==R.allowances(bits,bd),'all120 physical variable-degree allowances')
        return red,d,q,caps
    covers=[w for w in range(64) if all(w>>i&1 or w>>j&1 for i,j in L.CYCLE)]
    missing=[w for w in range(64) if all(not (w>>i&1 and w>>j&1) for i,j in L.CYCLE)]
    require(len(covers)==len(missing)==18 and sorted(63^w for w in missing)==covers,'whole C6 domain')
    eps=[e for e in product(range(3),repeat=3) if sum(e)<=2]
    require(len(eps)==10,'whole T excess domain after SY excesses are zero')
    red,d,q,b=core((L.H,L.K,L.C),(L.P,L.S))
    inside=sum(len(red[i]&set(range(1,11))) for i in range(1,11))//2
    require(inside==13 and sum(d[1:11])==99,'cut equality literal inputs')
    cycle_records=[]
    for i,j in L.CYCLE:
        records=[]
        for di,dj in product(range(32),repeat=2):
            if bool(di&16)!=(i<2) or bool(dj&16)!=(j<2):continue
            if di.bit_count()>(4 if i<2 else 3) or dj.bit_count()>(4 if j<2 else 3):continue
            qi=(7 if i<2 else 6)-di.bit_count();qj=(7 if j<2 else 6)-dj.bit_count()
            words=[(1<<i if di>>k&1 else 0)|(1<<j if dj>>k&1 else 0) for k in range(4)]
            sets,_,lq=L.build(0,(*words[2:],L.C),tuple(words[:2]))
            known=1+(di&dj).bit_count()
            require(known==len(sets[i+3]&sets[j+3]) and (qi,qj)==(lq[i+3],lq[j+3]),'cycle literal counts')
            possible=known+max(0,qi+qj-6)<=3
            require(possible==((di|dj)==(31 if i<2 or j<2 else 15)),'complete cycle union equivalence')
            if possible:require(known+qi+qj-6==3,'tight cycle Q union')
            records.append([di,dj,qi,qj,known,possible])
        cycle_records.append([i,j,len(records),sum(a[-1] for a in records),digest(records)])
    A=[w for w in covers if all(not (w>>i&1 and w>>j&1) for i,j in R.PATH_A)]
    D=[w for w in covers if all(not (w>>i&1 and w>>j&1) for i,j in R.PATH_D)]
    pairs=[[a,b] for a,b in product(A,D) if a|b==63]
    require(A==[L.P,L.H,L.S] and D==[L.P,L.K,L.S] and pairs==[[L.P,L.S],[L.H,L.K],[L.S,L.P]],'whole T path-cover domain')
    path_records=[]
    for endpoint,paths in ((13,R.PATH_A),(14,R.PATH_D)):
        records=[]
        for w in covers:
            for i,j in paths:
                if not (w>>i&1 and w>>j&1):continue
                for u,v in product(covers,repeat=2):
                    rows=(w,L.K,L.C) if endpoint==13 else (L.H,w,L.C)
                    red,_,_=L.build(0,rows,(u,v))
                    count=len(red[endpoint]&red[i+3])+len(red[endpoint]&red[j+3])
                    require(count>=(4 if endpoint==13 else 5),'doubled-edge bound independent of T rank')
                    records.append([w,i,j,u,v,count])
                guard()
        path_records.append([endpoint,len(records),min(a[-1] for a in records),digest(records)])
    t_records=[]
    for a,b in ((L.P,L.S),(L.S,L.P)):
        for u,v,e in product(covers,covers,eps):
            _,_,q,cap=core((a,b,L.C),(u,v),e)
            if e[0]:require(q[10]+q[13]-6>cap[10,13],'extra T0 already impossible on red SX1-T0')
            else:
                x=5 if a==L.P else 7
                require(q[10]+q[13]-6==cap[10,13],'tight SX1/T0 union')
                require(q[x]>cap[x,10]+cap[x,13],'own-X union contradiction')
            t_records.append([a,b,u,v,e])
            guard()
    us=[w for w in covers if (w&L.K).bit_count()<=2]
    vs=[w for w in us if (w&L.H).bit_count()<=2]
    require(us==[13,43,45,50,58,60] and vs==[13,50,60],'six/three SY covers')
    sy_records=[]
    for u,v,e in product(us,vs,eps):
        _,_,q,cap=core((L.H,L.K,L.C),(u,v),e)
        require(cap[11,14]==0 and cap[14,15]==e[1]+e[2],'variable T1/T2 overlap allowance')
        require(q[14]+q[15]-cap[14,15]==5 and q[11]==2,'union at least5 still forces SY0/T2 overlap')
        if u==L.H:require(cap[11,15]==0,'H contradiction unchanged')
        sy_records.append([u,v,e,q[14],q[15],cap[14,15]])
    pages=[]
    for w in missing:
        a=next(i for i in (2,5) if not (w>>i&1)); b=next(i for i in (3,4) if not (w>>i&1))
        red,_,_=L.build(0,(L.H,L.K,L.C),(L.L,L.P))
        witness=[1,15,3+a,3+b]
        require(len(set(witness))==4 and all(i in red[11] for i in witness),'L four distinct red pages')
        pages.append([w,witness])
    sy_pairs=[[u,v] for u,v in product((13,45,50,58),vs) if (u|v).bit_count()>=5]
    require(sy_pairs==[[13,50],[13,60],[45,50],[45,60],[50,13],[50,60],[58,13],[58,60]],'whole eight SY cases')
    joint=[]
    for u,v,e in product((13,45),(50,60),eps):
        if u==13 and v==50:continue
        _,_,q,cap=core((L.H,L.K,L.C),(u,v),e)
        if u==13:
            if e[0]:require(q[13]+q[8]-6>cap[13,8],'extra T0 impossible at X5')
            else:require(q[13]+q[8]-6==cap[13,8] and q[12]>cap[12,13]+cap[12,8],'P/L joint budget')
        else:require(q[3]+q[8]-6==cap[3,8] and q[5]>cap[5,3]+cap[5,8],'45/S,L joint budget')
        joint.append([u,v,e])
    # SY Q overlap is impossible using only missing independence and T cover.
    overlaps=[]
    for w,t in product(missing,product((0,1),repeat=3)):
        if sum(t)<1:continue
        mp=(w&L.P).bit_count();ms=(w&L.S).bit_count()
        require(not (mp>=1+t[1]+t[2] and ms>=1+t[0]+t[1]),'common SY point contradicts C6 independence')
        overlaps.append([w,t,mp,ms])
    ranks=[];transports=[]
    for e in eps:
        _,_,q,cap=core((L.H,L.K,L.C),(L.P,L.S),e)
        require(cap[13,8]==1 and q[8]==4,'T0 rank at most3')
        require(cap[11,14]==cap[12,14]==0,'T1 avoids both disjoint SY rows')
        require(cap[9,15]==cap[10,15]==2 and q[9]==q[10]==4,'T2 rank at most4')
        ranks.append([e,q[13:16]])
        for u,v,which in product(covers,covers,('phi','psi')):
            # Full arbitrary SY-cover transport, including variable T2 degree.
            p=R.permutation(which); rows=tuple(R.transport(w,p) for w in (L.H,L.K,L.C));sy=tuple(R.transport(w,p) for w in (u,v))
            a,d,q=L.build(0,(L.H,L.K,L.C),(u,v),e)
            b,nd,nq=L.build(int(which=='psi'),rows,sy,e)
            require(all(b[p[i]]=={p[j] for j in a[i]} and nd[p[i]]==d[i] and nq[p[i]]==q[i] for i in range(16)),'full free-completion core transport')
            transports.append([e,u,v,which]);guard()
    return {'complete':True,'Nu_edges':inside,'Nu_degree_sum':99,'cut':63,'E_minus_B_edges':86,
        'covers':covers,'independent_missing':missing,'T_excess_regimes':eps,'cycle_records':cycle_records,
        'path_bounds':path_records,'three_T_pairs':pairs,'nonterminal_T_records':[len(t_records),digest(t_records)],
        'variable_SY_records':[len(sy_records),digest(sy_records)],'L_four_pages':pages,'SY_pairs':sy_pairs,
        'joint_records':[len(joint),digest(joint)],'SY_overlap_records':[len(overlaps),digest(overlaps)],
        'forced_T_rank_records':ranks,'whole_transports':[len(transports),digest(transports)]}
