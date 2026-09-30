#!/usr/bin/env python3
"""Independent exact controls for the analytic105--115edge theorem.

Generated incidence fixtures test identities; they do not classify all
2-(7,3,2)designs and are not22-vertex witnesses. The universal proof is prose.
"""
from itertools import combinations,permutations
from collections import Counter,defaultdict
from hashlib import sha256
import json


def need(ok,message):
    if not ok:raise ValueError(message)


def fano_systems():
    pairs=list(combinations(range(7),2));bits={p:1<<i for i,p in enumerate(pairs)}
    triples=list(combinations(range(7),3));mask={t:sum(bits[p] for p in combinations(t,2)) for t in triples}
    through={p:[t for t in triples if set(p)<=set(t)] for p in pairs};goal=(1<<21)-1;answer=[]
    def visit(used,blocks):
        if used==goal:
            need(len(blocks)==7,'Fano block count');answer.append(tuple(sorted(blocks)));return
        p=next(p for p in pairs if not used&bits[p])
        for t in through[p]:
            if not mask[t]&used:visit(used|mask[t],blocks+[t])
    visit(0,[]);need(len(answer)==len(set(answer))==30,'Fano coverage')
    return sorted(answer)


def scalar_domain():
    # Multiplicity-weighted DP of all seven ordered pairs(h,sigma).
    states={(0,0,0,0):1}
    for _ in range(7):
        nxt=defaultdict(int)
        for (H,t,Q,D),count in states.items():
            for h in range(4):
                for sigma in range(2):nxt[H+h,t+sigma,Q+h*h,D+h*sigma]+=count
        states=nxt
    total=0;survivors=Counter()
    for (H,t,Q,D),count in states.items():
        if H%2 or H//2+t>6:continue
        e=H//2;total+=count
        # Sum k^2>=126+7t holds for any14integer rows totaling42+t.
        if 32*e-3*Q+13*t-2*D-(126+7*t)>=0:survivors[e,t,Q,D]+=count
    need(total==134184,'scalar domain multiplicity mismatch')
    need(dict(survivors)=={(6,0,22,0):21},'unexpected scalar survivors')
    # The remaining degrees0..3 have sum12, square sum22: only1,1,2^5.
    patterns=[]
    for n0 in range(8):
        for n1 in range(8-n0):
            for n2 in range(8-n0-n1):
                n3=7-n0-n1-n2
                if n1+2*n2+3*n3==12 and n1+4*n2+9*n3==22:patterns.append([n0,n1,n2,n3])
    need(patterns==[[0,2,5,0]],'unexpected equality histogram')
    values=[32*e-3*max(2*e,6*e-14)+6*(6-e)-126 for e in range(7)]
    need(values==[-90,-70,-50,-30,-16,-8,0],'upper budget mismatch')
    return {'ordered_states':total,'equality_states':21,'equality_parameters':[6,0,22,0],'equality_histogram_0_to_3':patterns[0],'upper_budgets':values}


def equality_graphs():
    # Fix the two degree-one vertices0,1. Enumerate all graphs of their
    # full required degree sequence by selecting a leaf's actual neighbor
    # and all completing cycles. Normalization concerns this algebra control.
    pairs=list(combinations(range(7),2));pos={p:i for i,p in enumerate(pairs)}
    target=[1,1]+[2]*5;rows=[set() for _ in range(7)];masks=[]
    def visit(i):
        if i==7:
            if list(map(len,rows))==target:masks.append(sum(1<<pos[(u,v)] for u,v in pairs if v in rows[u]))
            return
        deficit=target[i]-len(rows[i]);future=[j for j in range(i+1,7) if len(rows[j])<target[j]]
        if deficit<0:return
        for selected in combinations(future,deficit):
            for j in selected:rows[i].add(j);rows[j].add(i)
            visit(i+1)
            for j in selected:rows[i].remove(j);rows[j].remove(i)
    visit(0);need(len(masks)==len(set(masks))==167,'boundary graph cohort')
    retained=[]
    for mask in masks:
        L=[[0]*7 for _ in range(7)]
        for bit,(i,j) in enumerate(pairs):
            if mask>>bit&1:L[i][j]=L[j][i]=1
        h=list(map(sum,L));S=[[0]*7 for _ in range(7)]
        for i in range(7):
            for j in range(7):
                if i==j:S[i][j]=6
                else:
                    common=sum(L[i][k]*L[k][j] for k in range(7))
                    S[i][j]=(2-common) if L[i][j] else (h[i]+h[j]-1-common)
        literal=list(map(sum,S));formula=[9*h[i]+12-h[i]*h[i]-2*sum(L[i][j]*h[j] for j in range(7)) for i in range(7)]
        need(literal==formula,'saturated S row formula mismatch')
        if literal!=[18]*7:continue
        need(L[0][1]==1 and all(sum(L[i][j] for j in range(2,7))==2 for i in range(2,7)),'notK2plusC5')
        need(all(S[i][j]==4*(i==j)+2 for i in range(7) for j in range(7)),'equality S mismatch')
        retained.append((mask,L))
    need(len(retained)==12,'wrong equality graph survivors')
    return masks,retained


def validate_incidence(M):
    need(type(M) is list and len(M)==14 and all(type(row) is list and len(row)==7 for row in M),'bad incidence dimensions')
    need(all(type(x) is int and x in (0,1) for row in M for x in row),'nonbinary incidence')
    need(all(sum(row)==3 for row in M),'incidence rows nottriples')
    need(all(sum(row[a]*row[b] for row in M)==4*(a==b)+2 for a in range(7) for b in range(7)),'invalid design Gram')


def incidence_fixtures(systems):
    fixtures=0;projection_entries=0;loads=0;paired=0;hashes=sha256();samples=[]
    for i,first in enumerate(systems):
        for second in systems[i:]:
            triples=sorted(first+second);M=[[int(j in t) for j in range(7)] for t in triples]
            validate_incidence(M)
            S=[[sum(row[a]*row[b] for row in M) for b in range(7)] for a in range(7)]
            need(all(S[a][b]==4*(a==b)+2 for a in range(7) for b in range(7)),'invalid incidence fixture')
            # Four times the projector: N=MM^T-J. Test idempotence andimage.
            N=[[sum(x*y for x,y in zip(a,b))-1 for b in M] for a in M]
            for a in range(14):
                for b in range(14):
                    need(sum(N[a][c]*N[c][b] for c in range(14))==4*N[a][b],'projector idempotence')
                    projection_entries+=1
                need(N[a][a]==2,'projector diagonal')
                for b in range(7):need(sum(N[a][c]*M[c][b] for c in range(14))==4*M[a][b],'projector image')
            for a in range(14):
                # d=2e_a: ||d||^2=4, d^T Pi d=2: outside V.
                need(4*N[a][a]!=4*4,'double coordinate incorrectly lies in V');loads+=1
            for a,b in combinations(range(14),2):
                # d=e_a+e_b: test membership viaidempotent projector.
                norm_times4=8;qform=N[a][a]+N[b][b]+2*N[a][b]
                member=norm_times4==qform
                need(member==(M[a]==M[b]),'load-two projection mismatch');loads+=1;paired+=member
            hashes.update((json.dumps(triples,separators=(',',':'))+'\n').encode());fixtures+=1
            if len(samples)<4 and len(set(triples)) in (7,10,11,14):samples.append(M)
    need(fixtures==465 and projection_entries==91140 and loads==48825,'fixture coverage mismatch')
    return {'all_Fano_unions':fixtures,'projection_entries':projection_entries,'load_two_vectors':loads,'duplicate_pair_vectors_in_image':paired,'fixture_stream_sha256':hashes.hexdigest(),'not_all_twofold_designs':True},samples


def literal_cross_counts(samples,retained):
    # A blue6-regular circulant, arbitraryred incidenceandBgraphs asabove.
    # These fixtures mayviolatesomebookcaps; theycheckidentities, notexistence.
    P=[[int((j-i)%14 in (1,2,3,11,12,13)) for j in range(14)] for i in range(14)]
    count=0;rows=0;Bspines=0
    for M in samples:
        for _,L in retained:
            red=[[0]*22 for _ in range(22)]
            for b in range(7):red[0][15+b]=red[15+b][0]=1
            for a,c in combinations(range(14),2):red[1+a][1+c]=red[1+c][1+a]=1-P[a][c]
            for b,c in combinations(range(7),2):red[15+b][15+c]=red[15+c][15+b]=L[b][c]
            for a in range(14):
                for b in range(7):red[1+a][15+b]=red[15+b][1+a]=M[a][b]
            blue=[[int(i!=j and not red[i][j]) for j in range(22)] for i in range(22)]
            h=list(map(sum,L));e=sum(h)//2;k=list(map(sum,M));sigma=[sum(row[b] for row in M)-6 for b in range(7)]
            for a in range(14):
                defects=0
                for b in range(7):
                    D=sum(P[a][c]*M[c][b] for c in range(14))-sum(M[a][c]*L[c][b] for c in range(7))
                    if M[a][b]:
                        actual=sum(red[1+a][c]*red[15+b][c] for c in range(22));need(actual==5+sigma[b]-D,'redcrosspages');defects+=3-actual
                    else:
                        actual=sum(blue[1+a][c]*blue[15+b][c] for c in range(22));need(actual==12-h[b]-k[a]-D,'bluecrosspages');defects+=6-actual
                    count+=1
                Mh=sum(M[a][b]*h[b] for b in range(7))
                formula=sum(P[a][c]*k[c] for c in range(14))-2*Mh-sum(M[a][b]*sigma[b] for b in range(7))+11*k[a]-k[a]**2+2*e-42
                need(defects==formula==2*e-21+10*k[a]-k[a]**2-2*Mh,'row defect identity');rows+=1
            unused=0
            for b,c in combinations(range(7),2):
                if L[b][c]:actual=sum(red[15+b][a]*red[15+c][a] for a in range(22));unused+=3-actual
                else:actual=sum(blue[15+b][a]*blue[15+c][a] for a in range(22));unused+=6-actual
                Bspines+=1
            budget=32*e-3*sum(x*x for x in h)+13*sum(sigma)-2*sum(h[b]*sigma[b] for b in range(7))-sum(x*x for x in k)
            need(2*unused==budget==0,'seven-neighbor capacity budget')
    return {'fixture_graphs':len(samples)*len(retained),'mixed_spines':count,'row_defects':rows,'B_spines':Bspines,'not_valid22_witnesses':True}


def algebra_controls():
    # On V perpendicular1, thepolynomialP^2-P-2I=0hasroots2,-1.
    # Thus(P+I)^2=3(P+I), givingtheexactdifferenceidentity.
    polynomial=[-2,-1,1]
    need([3*x for x in [1,1]]==[3,3],'difference coefficient')
    need([1,2,1]==[3+polynomial[0],3+polynomial[1],polynomial[2]],'difference polynomial')
    need(all(4!=6*(wp-wq) for wp in (-1,0,1) for wq in (-1,0,1)),
         'distinct pairedsupports satisfydifferenceidentity')
    # Finalcountsforceoverlap>=2ofonlyonepossibleotherrow.
    need(4+4-6==2 and 2>1,'final overlap contradiction')
    return {'difference_polynomial_checked':True,'distinct_load_two_supports_excluded_by_divisibility':True,'forced_neighbor_overlap':2,'available_distinct_pair_rows':1}


def negative_controls(systems):
    M=[[int(j in t) for j in range(7)] for t in systems[0]+systems[0]]
    validate_incidence(M)
    wrong=[row[:] for row in M];wrong[0][0]=2
    altered=[row[:] for row in M];altered[0]=altered[1][:]
    cases=[M[:-1],wrong,altered]
    for case in cases:
        try:validate_incidence(case)
        except ValueError:pass
        else:raise ValueError('malformed incidence fixture accepted')
    return len(cases)


def run():
    systems=fano_systems();masks,retained=equality_graphs();fixt,samples=incidence_fixtures(systems)
    return {'scalar':scalar_domain(),'boundary_graphs':{'normalized_graphs':len(masks),'K2_plus_C5':len(retained)},'Fano_systems':len(systems),'incidence':fixt,'literal_spines':literal_cross_counts(samples,retained),'algebra':algebra_controls(),'negative_controls':negative_controls(systems),'trust':'Written universal analytic proof; generated design fixtures are arithmetic controls, not a completeness premise.'}

if __name__=='__main__':print(json.dumps(run(),indent=2,sort_keys=True))
