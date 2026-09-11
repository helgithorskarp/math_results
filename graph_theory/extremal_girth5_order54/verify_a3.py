#!/usr/bin/env python3
"""Exact A3 certificate and coverage checker; standard library only."""
import argparse,copy,hashlib,json
from collections import Counter
from fractions import Fraction
from itertools import combinations,combinations_with_replacement,product
from pathlib import Path
from a3_models import PROFILES,cases,model
from verify import graph,require,hoffman_singleton_edges
from verify_z12_distant_incidence import reconstructed_model,set_checks
from forest_constraints import model as degree_model


def check_certificate(rec,case):
    name,(types,edges,eq,eb,ub,bb),objective=case
    require(rec['name']==name,'certificate case name')
    require(rec['dimensions']==[len(types),len(edges),len(eq),len(ub)],'dimensions')
    D=rec['denominator'];require(type(D) is int and D>0,'denominator')
    require(rec['variable_budget']==428,'variable budget')
    n=len(types)+len(edges);cols=[0]*n;rhs=0
    def twice(x):
        y=2*Fraction(x)
        require(y.denominator==1,'non-half-integral model coefficient')
        return y.numerator
    for key,rows,bs in [('equality_multipliers',eq,eb),('inequality_multipliers',ub,bb)]:
        seen=set()
        for row,mul in rec[key]:
            require(type(row) is int and 0<=row<len(rows) and row not in seen,'row index')
            require(type(mul) is int and (key=='equality_multipliers' or mul<=0),'multiplier sign')
            seen.add(row);rhs+=mul*twice(bs[row])
            for i,a in rows[row].items():cols[i]+=mul*twice(a)
    excess=max([0]+[cols[i]-D*twice(objective[i]) for i in range(n)])
    raw=Fraction(rhs,2*D);error=Fraction(excess,2*D);bound=raw-428*error
    require(raw==Fraction(rec['uncorrected_bound']),'raw bound mismatch')
    require(error==Fraction(rec['coefficient_excess']),'coefficient excess mismatch')
    require(bound==Fraction(rec['corrected_bound']),'corrected bound mismatch')
    require(bound>(1 if name=='m_at_A3' else 0),'no strict certificate')
    return {'name':name,'dimensions':rec['dimensions'],'raw_bound':str(raw),
            'coefficient_excess':str(error),'exact_bound':str(bound),
            'certificate_sha256':hashlib.sha256(json.dumps(rec,sort_keys=True,separators=(',',':')).encode()).hexdigest()}


def independent_colored_model(p,profile,m,k):
    """Multiset type enumeration and rowwise neighbor incidence reconstruction.

    This does not call the production composition generator or column filler.
    """
    sizes=[13+p,26-p,9,3,3-p]+([p] if p else [])
    ds=[6,7,8,8,6]+([7] if p else [])
    nc=len(sizes);types=[]
    for cl,d in enumerate(ds):
        rows=[]
        for word in combinations_with_replacement(range(nc),d):
            count=Counter(word);ns=tuple(count[a] for a in range(nc))
            if any(ns[a]>sizes[a]-(cl==a) for a in range(nc)):continue
            total=sum(ds[a]*ns[a] for a in range(nc));h=ns[2]+ns[3];nx=sum(ns[4:])
            if total>53 or (d==8 and h>2):continue
            if cl==2:
                good=total==53 and nx==0 and ns[3]<=1
            elif cl==3:
                good=total==52 and nx==2 and ns[3]==0
            elif cl>=4:
                good=ns[3]==2 and ns[2]==0 and nx==0
            else:
                good=ns[3]<=1 and nx<=1
            if not good:continue
            if cl not in (2,3):
                if not any(dd==d and c==h for dd,c,num in profile):continue
                if d==7 and h==2 and total-6*d-7==2:continue
            rows.append(ns)
        types += [(cl,ns) for ns in sorted(rows)]
    nt=len(types)
    edges=[(i,j) for i in range(nt) for j in range(i,nt)
           if types[i][1][types[j][0]]>0 and types[j][1][types[i][0]]>0]
    neighbors=[[] for _ in types]
    for col,(i,j) in enumerate(edges,nt):
        neighbors[i].append((col,j))
        if i!=j:neighbors[j].append((col,i))
    eq=[];eb=[];ub=[];bb=[]
    def add(rows,rhs,row,b):rows.append({i:v for i,v in row.items() if v});rhs.append(b)
    for a in range(nc):add(eq,eb,{i:int(cl==a) for i,(cl,ns) in enumerate(types)},sizes[a])
    for a,b in combinations(range(nc),2):add(eq,eb,{i:(cl==a)*ns[b]-(cl==b)*ns[a] for i,(cl,ns) in enumerate(types)},0)
    for a in range(nc):add(ub,bb,{i:ns[a]*(ns[a]-1)+(cl==a)*ns[a] for i,(cl,ns) in enumerate(types)},sizes[a]*(sizes[a]-1))
    for a,b in combinations(range(nc),2):add(ub,bb,{i:ns[a]*ns[b]+(cl==a)*ns[b] for i,(cl,ns) in enumerate(types)},sizes[a]*sizes[b])
    for i,(cl,ns) in enumerate(types):
        for a in range(nc):
            row={i:-ns[a]}
            for col,j in neighbors[i]:
                if types[j][0]==a:row[col]=1
            add(eq,eb,row,0)
            missed=int(cl>=4 and a==3)
            row={i:ns[a]-sizes[a]+missed-(ds[cl]-1)*(cl==a)}
            for col,j in neighbors[i]:row[col]=types[j][1][a]
            exact=(a in (2,3)) or (cl==3 and a<4) or cl==2
            add(eq if exact else ub,eb if exact else bb,row,0)
    for d,c,num in profile:add(eq,eb,{i:1 for i,(cl,ns) in enumerate(types) if ds[cl]==d and ns[2]+ns[3]==c},num)
    count4=next(num for d,c,num in profile if (d,c)==(6,4))
    add(ub,bb,{i:1 for i,(cl,ns) in enumerate(types) if ds[cl]==7 and ns[2]+ns[3]==1 and sum(ns[a]*(ds[a]-6) for a in range(nc))==8},0 if count4==2 else 3)
    add(eq,eb,{i:Fraction(ns[2]+ns[3],2) for i,(cl,ns) in enumerate(types) if cl in (2,3)},m)
    add(eq,eb,{i:1 for i,(cl,ns) in enumerate(types) if cl in (2,3) and ns[2]+ns[3]==2},k)
    return sizes,ds,types,edges,eq,eb,ub,bb


def normalized(data):
    return [{i:v for i,v in x.items() if v} if isinstance(x,dict) else x for x in data]


def model_audit():
    for a,b in zip(degree_model((16,26,12),False),reconstructed_model()):
        require(normalized(a)==normalized(b),'base model independent reconstruction')
    count=columns=0
    for p in (0,1):
        for m,k,name,prof in PROFILES:
            a=model(p,prof,m,k);b=independent_colored_model(p,prof,m,k)
            for left,right in zip(a,b):
                require(normalized(left)==normalized(right),'colored model reconstruction '+name)
            count+=1;columns+=len(a[2])+len(a[3])
    return {'colored_models':count,'colored_columns':columns,'base_columns':1710,
            'type_enumeration':'neighbor multisets versus recursive compositions',
            'row_reconstruction':'rowwise incident neighbors versus production column filling'}


def profile_audit():
    found=[]
    # Exactly 2 or3 c4 six-vertices; all other positive charges are the
    # single-unit types (6,1),(7,0),(7,3). Counts of zero-charge types then
    # follow from the two high/low handshakes.
    for m,k in ((2,0),(2,1),(3,0)):
        B=5-m-k
        for n4 in range(2,4):
            for six1,seven0,seven3 in product(range(2),repeat=3):
                if n4+six1+seven0+seven3!=B:continue
                left6=16-n4-six1
                n63=(36+3+2*m)-4*n4-six1-2*left6
                n62=left6-n63
                left7=26-seven0-seven3
                n72=(60-3-4*m)-3*seven3-left7
                n71=left7-n72
                if min(n62,n63,n71,n72)<0:continue
                prof=[(6,1,six1),(6,2,n62),(6,3,n63),(6,4,n4),
                      (7,0,seven0),(7,1,n71),(7,2,n72),(7,3,seven3)]
                found.append((m,k,tuple((d,c,n) for d,c,n in prof if n)))
    expected=[(m,k,tuple(prof)) for m,k,name,prof in PROFILES]
    require(set(found)==set(expected) and len(found)==6,'complete profile cover')
    return {'profiles':len(found),'records':[{'m':m,'k':k,'name':name,'profile':prof} for m,k,name,prof in PROFILES]}


def four_sets_audit():
    U=set(range(4));universe=set(range(12));configs=templates=0
    for V in (set(range(4,8)),{0,4,5,6}):
        for wt in combinations(range(12),4):
            W=set(wt)
            if len(U&W)>1 or len(V&W)>1:continue
            blocks=[U,V,W];options=[];configs+=1
            for i,j in combinations(range(3),2):
                if blocks[i]&blocks[j]:continue
                rem=universe-blocks[i]-blocks[j];other=3-i-j
                for p in rem:
                    Z=rem-{p}
                    if len(Z&blocks[other])<=1:options.append((p,Z))
            union=U|V|W
            if len(union)==11:options.append((next(iter(universe-union)),None))
            templates+=len(options)
            for (p,Z),(q,L) in combinations(options,2):
                if p!=q:
                    require(Z is not None and L is not None and len(Z&L)>=2,
                            'distinct A1 singleton templates could coexist')
    require(max(min(2+a,5-a) for a in range(4))==3,'common-singleton capacity')
    return {'three_four_configurations':configs,'A1_templates':templates,
            'two_four_checks':set_checks()}


def restricted_growth(n):
    def rec(a):
        if len(a)==n:yield tuple(a);return
        for k in range(max(a,default=-1)+2):yield from rec(a+[k])
    yield from rec([])


def frame_audit():
    counts=Counter();survivors=Counter();records=[]
    for deficit in ((3,),(2,1),(1,1,1)):
        r=len(deficit);owners=[i for i,a in enumerate(deficit) for _ in range(a)]
        for labels in restricted_growth(3):
            far=[{labels[j] for j,t in enumerate(owners) if t==i} for i in range(r)]
            if any(len(far[i])!=deficit[i] for i in range(r)):continue
            nx=max(labels)+1
            available=[(i,x) for i in range(r) for x in range(nx) if x not in far[i]]
            for bits in range(1<<len(available)):
                C=[set() for _ in range(nx)]
                for j,(i,x) in enumerate(available):
                    if (bits>>j)&1:C[x].add(i)
                if any(sum(i in C[x] for x in far[j])!=sum(j in C[x] for x in far[i])
                       for i,j in combinations(range(r),2)):continue
                if any(len(C[x]&C[y])>1 for x,y in combinations(range(nx),2)):continue
                counts['incidence_frames']+=1
                forbidden={(i,j) for i,j in combinations(range(r),2)
                           if any(i in c and j in c for c in C)
                           or any(j in C[x] for x in far[i])
                           or any(i in C[x] for x in far[j])}
                independent=len(forbidden)==r*(r-1)//2
                multiplicity=[sum(x in f for f in far) for x in range(nx)]
                for degrees in product((6,7),repeat=nx):
                    counts['degree_assignments']+=1
                    charge=sum((len(C[x])-3)*(len(C[x])-2)//2 if degrees[x]==6
                               else (len(C[x])-1)*(len(C[x])-2)//2 for x in range(nx))
                    p7=sum(multiplicity[x] for x in range(nx) if degrees[x]==7)
                    highgap=sum(a*(a+4) for a in deficit)
                    min_low=sum((2-len(C[x]))**2 for x in range(nx) if degrees[x]==6)
                    positive=sum((len(C[x])-3)*(len(C[x])-2) for x in range(nx) if degrees[x]==6)
                    for m,k in ((2,0),(2,1),(3,0)):
                        B=5-m-k
                        for fours in (2,3):
                            counts['bounded_cases']+=1
                            if charge+fours>B:continue
                            Q=28-highgap-4*p7
                            if Q<min_low:continue
                            Rbound=m if independent and deficit==(1,1,1) else 3+k
                            b1max=0 if fours==2 else 3
                            lower=21-2*m-Rbound+p7+positive
                            upper=7+Q+b1max
                            if lower>upper:continue
                            if deficit==(1,1,1) and nx==2 and sorted(map(len,C))==[1,2] and degrees==(6,6):
                                tag='shared_six_endpoint'
                                require(m==2 and k==0 and fours==2,'shared profile scope')
                            elif deficit==(1,1,1) and nx==3 and all(len(c)==2 for c in C):
                                tag='cycle_p'+str(p7)
                                require(p7 in (0,1) and independent,'cycle scope')
                            else:raise ValueError('uncovered frame '+str((deficit,labels,C,degrees,m,k,fours)))
                            survivors[tag]+=1
                            records.append([list(deficit),list(labels),[sorted(c) for c in C],list(degrees),m,k,fours,tag])
    require(set(survivors)=={'shared_six_endpoint','cycle_p0','cycle_p1'},'residual frame list')
    return {'counts':dict(counts),'remaining_labeled_cases':dict(survivors),
            'survivor_sha256':hashlib.sha256(json.dumps(records,separators=(',',':')).encode()).hexdigest()}


def colored_count_controls():
    """Definition-level class ball equalities on all small girth-five graphs."""
    graphs=rows=0
    instances=[]
    for n in range(1,6):
        pairs=list(combinations(range(n),2))
        for bits in range(1<<len(pairs)):
            adj=graph(n,[e for i,e in enumerate(pairs) if (bits>>i)&1])
            if any(len(adj[i]&adj[j])>1 or (j in adj[i] and adj[i]&adj[j]) for i,j in pairs):continue
            instances.append(adj)
    instances.append(graph(6,[(i,(i+1)%6) for i in range(6)]))
    instances.append(graph(50,sorted(hoffman_singleton_edges())))
    fixture=json.loads((Path(__file__).parent/'lower_bound_54_185.json').read_text())
    instances.append(graph(54,fixture['edges']))
    for adj in instances:
        n=len(adj);d=list(map(len,adj))
        labels=[(d[v],v%2) for v in range(n)];classes=sorted(set(labels));which=[classes.index(c) for c in labels]
        sizes=[which.count(a) for a in range(len(classes))]
        ns=[[sum(which[u]==a for u in adj[v]) for a in range(len(classes))] for v in range(n)]
        for v in range(n):
            near={v}|adj[v]
            for u in adj[v]:near |= adj[u]
            for a in range(len(classes)):
                far=sum(which[x]==a and x not in near for x in range(n))
                lhs=sum(ns[u][a] for u in adj[v])+ns[v][a]
                rhs=sizes[a]+(d[v]-1)*(which[v]==a)-far
                require(lhs==rhs,'colored ball correction')
                rows+=1
        for a in range(len(classes)):
            for b in range(a,len(classes)):
                if a==b:
                    lhs=sum(ns[v][a]*(ns[v][a]-1)+(which[v]==a)*ns[v][a] for v in range(n))
                    require(lhs<=sizes[a]*(sizes[a]-1),'colored diagonal pair capacity')
                else:
                    lhs=sum(ns[v][a]*ns[v][b]+(which[v]==a)*ns[v][b] for v in range(n))
                    require(lhs<=sizes[a]*sizes[b],'colored cross pair capacity')
        graphs+=1
    return {'graphs':graphs,'exact_colored_ball_rows':rows}


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--certificates',type=Path,required=True);args=parser.parse_args()
    data=json.loads(args.certificates.read_text());built=list(cases())
    require(len(data)==len(built)==14,'complete certificate count')
    certificates=[check_certificate(rec,case) for rec,case in zip(data,built)]
    bad=[]
    x=copy.deepcopy(data[1]);x['inequality_multipliers'][0][1]=1;bad.append((x,built[1]))
    x=copy.deepcopy(data[-1]);x['equality_multipliers'][0][1]+=10**8;bad.append((x,built[-1]))
    x=copy.deepcopy(data[0]);x['name']='m_at_A4';bad.append((x,built[0]))
    x=copy.deepcopy(data[2]);x['equality_multipliers'].append(x['equality_multipliers'][0]);bad.append((x,built[2]))
    for rec,case in bad:
        try:check_certificate(rec,case)
        except ValueError:pass
        else:raise ValueError('tampered certificate accepted')
    output={'claim':'z12 A3 impossible; combined with previous theorem A<=2',
            'certificates':certificates,'tampered_certificates_rejected':len(bad),
            'models':model_audit(),'profiles':profile_audit(),'four_sets':four_sets_audit(),
            'frames':frame_audit(),'colored_controls':colored_count_controls()}
    print(json.dumps(output,indent=2,sort_keys=True))

if __name__=='__main__':main()
