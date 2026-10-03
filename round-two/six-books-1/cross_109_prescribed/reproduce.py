"""Complete necessary-prefix exclusion for the precise E=109,T2=C shell."""
import argparse,ast,hashlib,json,math,time
from itertools import combinations,product
from pathlib import Path
import forcing,literal as L,reference as R,roles

START=time.monotonic()
def require(t,m):
    if not t:raise ValueError(m)
def guard():
    if time.monotonic()-START>30:raise RuntimeError('30s guard; INCOMPLETE is not exclusion')
def canonical(x):return (json.dumps(x,sort_keys=True,separators=(',',':'))+'\n').encode()
def digest(x):return hashlib.sha256(canonical(x)).hexdigest()

def domains(case,r=0,swapped=False):
    rows=(L.H,L.K,L.C) if r==0 else (L.K,L.H,L.C);sy=(L.S,L.P) if swapped else (L.P,L.S)
    e=(0,0,case['t2rank']-3)
    red,d,q=L.build(r,rows,sy,e);bits,bd,bq=R.build(r,rows,sy,e)
    require(tuple(sum(1<<j for j in a) for a in red)==bits and d==bd and q==bq,'full terminal literal/coordinate core')
    require(L.allowances(red,d)==R.allowances(bits,d),'all120 terminal physical allowances')
    a=L.column_domains(red,d,q,case);b=R.columns(bits,d,q,case)
    require(a==b,'ENTIRE literal/direct-blue column sets agree')
    return red,d,q,a

def run():
    f=forcing.run(require,guard,digest)
    profiles=roles.raw_profiles();require(len(profiles)==66 and len(set(profiles))==66 and all(sum(p)==2 for p in profiles),'whole raw induced-B excess profiles')
    reduced=[p for p in profiles if p[:4]==(0,0,0,0) and p[4]<=1]
    require(len(reduced)==27,'complete coarse excess reduction')
    raw=roles.generate();cases=roles.catalog()
    require(len(raw)==34 and len(cases)==9 and {roles.orbit(c) for c in raw}=={roles.orbit(c) for c in cases},'whole labelled-role coverage by nine free-label orbits')
    summaries=[];baselines={};survivors=[]
    for c in cases:
        guard();red,d,q,a=domains(c);baselines[c['name']]=a
        count=math.prod(len(x) for x in a);xmatched=0;balanced=[];rejected=[]
        require(sum(c['h'])==14-(c['t2rank']-3)*2 and sum(c['epsilon'])==5-c['t2rank'],'complete B edge/excess accounting')
        for choice in product(*a):
            if tuple(sum(bool(col[0]>>i&1) for col in choice) for i in range(6))!=(3,3,2,2,2,2):continue
            xmatched+=1
            if tuple(sum(col[1+i] for col in choice) for i in range(2))!=(4,4):continue
            graph=L.prefix(red,c,choice)
            require(tuple(len(graph[i]) for i in range(16))==d,'all actual marked degrees from complete prefix')
            require(all(len(graph[16+i])+c['h'][i]==choice[i][3] for i in range(6)),'variable actual Q degrees')
            require(sum(d)+sum(col[3] for col in choice)==218,'actual E=109 degree sum')
            records,bad=L.known_spines(graph)
            bits=tuple(sum(1<<j for j in row) for row in graph)
            for i,j,edge,pages in records:
                count2=(bits[i]&bits[j]).bit_count() if edge else (((1<<22)-1)&~(bits[i]|bits[j]|(1<<i)|(1<<j))).bit_count()
                require(count2==len(pages),'all120 direct coloured pages agree')
                if not edge:require(count2==22-2-d[i]-d[j]+(bits[i]&bits[j]).bit_count(),'blue/red-codegree identity with actual degrees')
            balanced.append(list(choice))
            if not bad:survivors.append([c['name'],list(choice)])
            else:
                require(bad[0][:3]==[3,5,0] and len(bad[0][3])==7,'four prefixes have seven BLUE X0-X2 pages')
                rejected.append({'prefix':list(choice),'first_bad_spine':bad[0],'all120_record_sha256':digest(records)})
        summaries.append(c|{'column_domains':a,'cartesian':count,'X_rank_matched':xmatched,'X_SX_rank_matched':len(balanced),'rejected_balanced_prefixes':rejected})
    require(not survivors and sum(a['X_SX_rank_matched'] for a in summaries)==4,'complete109 terminal prefix exclusion')
    transports=[]
    for c in cases:
        base=baselines[c['name']]
        for r,swapped in product((0,1),(False,True)):
            _,_,_,a=domains(c,r,swapped)
            p=R.permutation('psi') if r else tuple(range(16))
            if swapped:
                phi=R.permutation('phi');p=tuple(phi[p[i]] for i in range(16))
            image=[sorted([[R.transport(w,p),p1,p0,D] if r else [R.transport(w,p),p0,p1,D] for w,p0,p1,D in row]) for row in base]
            require(image==a,'whole actual-r/SY incidence-column transport')
            transports.append([c['name'],r,swapped,digest(a)])
    free=[]
    for c in raw:
        matches=[(cat,p) for cat,p in product(cases,roles.PERMUTATIONS) if roles.key(roles.transport(cat,p))==roles.key(c)]
        require(bool(matches),'each labelled role has explicit free-point relabeling')
        cat,p=matches[0];_,_,_,a=domains(c)
        require(all(a[p[i]]==baselines[cat['name']][i] for i in range(6)),'whole34 labelled-role column sets')
        free.append([roles.key(c),cat['name'],p,digest(a)]);guard()
    # Positive known Ramsey witness; direct red AND blue page checker accepts it.
    fixture=Path('primary21.txt').read_bytes();matrix=ast.literal_eval(fixture.decode().split('\n\nsearch_',1)[0])
    require(len(matrix)==21 and all(len(row)==21 for row in matrix),'primary21 matrix order')
    maxpages=[0,0];edges=[0,0]
    for i,j in combinations(range(21),2):
        value=matrix[i][j];require(value in (0,1) and value==matrix[j][i] and matrix[i][i]==0,'primary simple graph')
        # The primary authors encode the B4 color as ZERO, off the diagonal.
        edge=value==0
        color=0 if edge else 1;pages=sum(matrix[i][k]==value and matrix[j][k]==value for k in range(21) if k not in (i,j))
        require(pages<=(3 if edge else 6),'known positive primary witness')
        maxpages[color]=max(maxpages[color],pages);edges[color]+=1
    require(edges==[93,117] and maxpages==[3,6],'primary baseline counts')
    # Damages expose real dependence on labels, full coverage and ACTUAL degrees.
    old=list(L.OLD_MAP);old[4],old[5]=old[5],old[4]
    try:L.build(0,(L.H,L.K,L.C),(L.P,L.S),old_map=old)
    except ValueError:map_rejected=True
    else:map_rejected=False
    require(map_rejected and {roles.orbit(c) for c in raw}!={roles.orbit(c) for c in cases[:-1]},'damaged labels and missing role detected')
    require([L.P,1,1,11] in baselines['I-U'][4],'positive variable-degree local column')
    red,d,q,_=domains(cases[0]);n={1,9,10,13,14}|{3+i for i in (1,4,5)}
    require(len(red[12]&n)==6 and d[12]+11-14==6 and d[12]+10-14==5,'omitting Q excess falsely rejects the positive column')
    _,d,_,_=domains(cases[2]);require(d[15]==10 and d[14]+d[15]-14==6,'extra T2 degree must be retained')
    require(d[14]+9-14==5,'old T2 degree loses one blue allowance')
    guard()
    return {'agent':'six-books-1','role':'researcher','complete':True,
        'status':'exact computer-assisted conditional109-edge exclusion; ordinary reduction unformalized; independent review pending',
        'forcing':f,'raw66_excess_profiles_sha256':digest(profiles),'coarse27_profiles_sha256':digest(reduced),
        'whole34_role_records_sha256':digest(raw),'nine_role_cases':summaries,'remaining_Q_to_Q_search_needed':False,
        'all36_actual_core_column_transports':[len(transports),digest(transports)],
        'all34_free_point_label_transports':[len(free),digest(free)],
        'primary21':{'bytes':len(fixture),'sha256':hashlib.sha256(fixture).hexdigest(),'red_blue_edges':edges,'maximum_red_blue_pages':maxpages,'spines':210},
        'semantic_controls':{'wrong_old_label_map_rejected':True,'missing_role_detected':True,'extra_Q_degree_changes_real_blue_spine':True,'extra_T2_degree_changes_real_blue_allowance':True,'positive_Q_column_accepted':True},
        'solver_used':False,'floating_point_mathematics':False,'external_census_input':False,'formalized':False}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);p.add_argument('--check',type=Path);a=p.parse_args()
    raw=canonical(run())
    if a.check:require(raw==a.check.read_bytes(),'entire canonical record mismatch')
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_bytes(raw)
    print(json.dumps({'complete':True,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'wall_seconds':time.monotonic()-START,'guard_seconds':30}))
if __name__=='__main__':main()
