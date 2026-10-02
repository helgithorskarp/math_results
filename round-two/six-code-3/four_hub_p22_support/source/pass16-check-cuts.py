"""PRIVATE independent cut replay: no author mathematical imports.

Closure uses direct crossing-pair checks; monotone propagation fixes one
edge then restarts; radius maximizes over literal neighbor subsets; unit
cross demands use augmenting-path flows rather than the author's Hall
subset tests. Finite unit graphs use integer adjacency masks.
"""
from collections import Counter,deque
import hashlib
import itertools
import json
from pathlib import Path
import time

R=Path('round-two/six-code-3/scratch')

def need(c,m):
    if not c:raise ValueError(m)

def categories(v):
    U={i for i,r in enumerate(v) if r['e']==0}
    A={i for i in U if not v[i]['eligible']}
    C={i for i,r in enumerate(v) if r['e'] and not r['eligible']}
    B={i for i,r in enumerate(v) if r['e'] and r['eligible']}
    D=sum(sum(v[i]['ss_hist']) for i in U)
    I=sum(min(sum(v[i]['ss_hist']),len(A)-1) for i in A)
    C1=sum(v[i]['ss_hist'][0] for i in C)
    return U,A,C,B,D,I,C1

def domains(v):
    U,A,C,B,D,I,C1=categories(v)
    m=[[0]*len(v) for _ in v]
    for i,j in itertools.combinations(range(len(v)),2):
        if (i in U and v[j]['eligible']) or (j in U and v[i]['eligible']):continue
        labels=sum(1<<c for c in range(5) if v[i]['ss_hist'][c] and v[j]['ss_hist'][c])
        if D==I+C1 and i not in U and j not in U and (i in C or j in C):labels &= ~1
        m[i][j]=m[j][i]=labels
    return m

def propagate(v):
    m=domains(v);assigned={}
    while True:
        action=None
        for i,row in enumerate(v):
            for c,degree in enumerate(row['ss_hist']):
                done=sum(i in pair and colour==c for pair,colour in assigned.items())
                pairs=[tuple(sorted((i,j))) for j in range(len(v)) if m[i][j]>>c&1 and tuple(sorted((i,j))) not in assigned]
                debt=degree-done
                if debt<0 or debt>len(pairs):return m,assigned,True
                if debt==0 and pairs:action=('remove',pairs,c);break
                if debt and debt==len(pairs):action=('force',pairs[:1],c);break
            if action:break
        if not action:break
        kind,pairs,c=action
        for i,j in pairs:
            if kind=='remove':m[i][j]&=~(1<<c);m[j][i]=m[i][j]
            else:assigned[(i,j)]=c;m[i][j]=m[j][i]=1<<c
    return m,assigned,False

def base_record(v,record):
    U,A,C,B,D,I,C1=categories(v);kind=record['kind']
    if kind=='unit_capacity':need(D>I+C1,'unit inequality not violated')
    elif kind=='closed_partition':
        m=domains(v);inside=set(record['inside']);outside=set(record['outside'])
        need(inside|outside==set(range(len(v))) and not inside&outside and outside,'partition')
        need(record['root'] in inside and v[record['root']]['k']==0,'physical root')
        need(all(not m[i][j] for i in inside for j in outside),'permitted crossing color')
        need(record['capacity_equality']==(D==I+C1),'capacity equality predicate')
    elif kind=='radius_crossing_capacity':
        roots=sum(v[i]['k']==0 for i in U)
        total=sum(sum(v[i]['ss_hist']) for i in C)
        need(roots and B and total<max(roots,D-I)+len(B),'crossing inequality not violated')
        need(record['crossing_lower']==max(roots,D-I)+len(B),'crossing quantified bound')
    elif kind=='UNRESOLVED':return
    else:raise ValueError('unhandled base certificate')
    if kind in ('unit_capacity','closed_partition'):
        need([record[k] for k in ('unit_demand','internal_upper','external_upper')]==[D,I,C1],'wrong endpoint scalars')

def color_assignment(v,root,chosen,m,assigned):
    fixed={j if i==root else i:c for (i,j),c in assigned.items() if root in (i,j)}
    if not fixed.keys()<=set(chosen):return False
    remaining=list(v[root]['ss_hist'])
    for c in fixed.values():remaining[c]-=1
    candidates=[p for p in chosen if p not in fixed]
    def walk(at):
        if at==len(candidates):return not any(remaining)
        p=candidates[at]
        for c in range(5):
            if remaining[c]>0 and m[root][p]>>c&1:
                remaining[c]-=1
                good=walk(at+1)
                remaining[c]+=1
                if good:return True
        return False
    return min(remaining)>=0 and walk(0)

def forced_record(v,branch,record):
    m,a,failed=propagate(v);kind=record['kind']
    if kind=='forced_color_degree_failure':need(failed,'independent forced propagation is consistent');return
    need(not failed,'prior propagation should have failed')
    if kind=='closed_color_parity':
        J=set(record['component']);c=record['colour']
        need(not any(m[i][j]>>c&1 for i in J for j in set(range(len(v)))-J),'not a closed layer component')
        need(sum(v[i]['ss_hist'][c] for i in J)==record['degree'] and record['degree']%2,'not odd')
    elif kind in ('forced_uncovered_triangle','forced_radius_losses'):
        root=record['root'];N={j if i==root else i for i,j in a if root in (i,j)}
        triangles=sum(tuple(sorted((p,q))) in a for p,q in itertools.combinations(N,2))
        need(triangles==record['forced_triangles'],'wrong forced triangle count')
        degree=sum(v[root]['ss_hist'])
        if kind=='forced_uncovered_triangle':
            leave=v[root]['h']-1-v[root]['q']
            need(branch[3]==0 and triangles>degree*(degree-1)//2-leave,'tau-zero local leave is feasible')
            need(record['SS_high_leave']==leave and record['saturated_degree']==degree,'wrong leave/degree')
        else:
            need(v[root]['k']==0,'radius root is not hub-complete')
            pool=[i for i in range(len(v)) if m[root][i]]
            best=max((sum(sum(v[i]['ss_hist']) for i in J)
                      for J in itertools.combinations(pool,degree) if color_assignment(v,root,J,m,a)),default=-1)
            sure_out=set(range(len(v)))-{root}-set(pool)
            collision=sum(max(0,sum(tuple(sorted((w,p))) in a for p in N)-1) for w in sure_out)
            need(best==record['neighbor_degree_upper'] and collision==record['forced_collision'],'wrong walk maxima/losses')
            need(best-2*triangles-collision<13,'physical radius bound not violated')
    elif kind=='UNRESOLVED':
        need(record['forced_edges']==[[list(pair),c] for pair,c in sorted(a.items())],'entire forced closure differs')
    else:raise ValueError('unhandled forced certificate')

def flow(debt,caps,pairs):
    nu,nc=len(debt),len(caps);n=nu+nc+2;source=n-2;sink=n-1
    cap=[[0]*n for _ in range(n)]
    for u,d in enumerate(debt):cap[source][u]=d
    for c,d in enumerate(caps):cap[nu+c][sink]=d
    for u,c in pairs:cap[u][nu+c]=1
    result=0
    while True:
        parent=[-1]*n;parent[source]=source;todo=deque([source])
        while todo and parent[sink]<0:
            i=todo.popleft()
            for j in range(n):
                if cap[i][j]>0 and parent[j]<0:parent[j]=i;todo.append(j)
        if parent[sink]<0:break
        j=sink;amount=sum(debt)
        while j!=source:amount=min(amount,cap[parent[j]][j]);j=parent[j]
        j=sink
        while j!=source:i=parent[j];cap[i][j]-=amount;cap[j][i]+=amount;j=i
        result+=amount
    return result==sum(debt)

def unit_record(v,branch,record):
    m,a,failed=propagate(v);need(not failed,'unit-record input is inconsistent')
    U,A,C,B,D,I,C1=categories(v);units=sorted(U);external=sorted(C)
    edges=list(itertools.combinations(units,2));edges=[p for p in edges if m[p[0]][p[1]]&1]
    need(len(edges)<=15,'finite guard exceeds authorized carrier')
    need(record['units']==units and record['potential_internal_edges']==[list(e) for e in edges],'entire unit edge domain')
    required={p for p,c in a.items() if c==0 and set(p)<=U}
    fixed={(u,c) for u in units for c in external if a.get(tuple(sorted((u,c))))==0}
    pool={(u,c) for u in units for c in external if m[u][c]&1 and tuple(sorted((u,c))) not in a}
    cap=[v[c]['ss_hist'][0]-sum(c in p for p,k in a.items() if k==0 and not set(p)&U)-sum(y==c for x,y in fixed) for c in external]
    expected=[];start=time.monotonic()
    # Independent cardinality-ordered subsets rather than numeric full-mask order.
    tested=0
    for length in range(len(edges)+1):
        for indices in itertools.combinations(range(len(edges)),length):
            tested+=1;need(time.monotonic()-start<10,'INCOMPLETE fixed independent unit guard')
            chosen={edges[i] for i in indices}
            if not required<=chosen:continue
            adjacency={u:0 for u in units}
            for u,w in chosen:adjacency[u]|=1<<w;adjacency[w]|=1<<u
            debt=[sum(v[u]['ss_hist'])-adjacency[u].bit_count()-sum(x==u for x,y in fixed) for u in units]
            if min(debt,default=0)<0 or sum(debt)>sum(cap):continue
            if any(debt[j]>sum(x==u for x,y in pool) for j,u in enumerate(units)):continue
            if branch[3]==0:
                bad=False
                for u in units:
                    neighbors=[w for w in units if adjacency[u]>>w&1]
                    triangles=sum((adjacency[w]&adjacency[u]).bit_count() for w in neighbors)//2
                    degree=sum(v[u]['ss_hist']);leave=4-v[u]['q']
                    if triangles>degree*(degree-1)//2-leave:bad=True;break
                if bad:continue
            translated={(units.index(u),external.index(c)) for u,c in pool}
            if not flow(debt,cap,translated):continue
            expected.append(sum(1<<i for i in indices))
    need(tested==1<<len(edges),'complete finite subset coverage')
    need(sorted(expected)==record['accepted_internal_masks'],'every internal candidate differs')
    need((not expected)==(record['kind']=='unit_graph_INCOMPATIBLE'),'wrong exclusion kind')
    return tested

def main():
    start=time.monotonic()
    inventory=json.loads((R/'pass16-p21-producer.json').read_text())['inventory']
    make=lambda p:[inventory['types'][i] for i,n in p for _ in range(n)]
    base=json.loads((R/'pass16-p21-cuts.json').read_text())
    necessary=[dict(branch=[b[k] for k in ('Q','T','X','tau')],population=t['population'])
               for b in inventory['branches'] for t in b['templates'] if not t['failures']]
    need([(r['branch'],r['population']) for r in base['records']]==[(r['branch'],r['population']) for r in necessary],'all494 necessary populations')
    for record in base['records']:base_record(make(record['population']),record)
    structural=json.loads((R/'pass16-p21-forced.json').read_text())
    need([(r['branch'],r['population']) for r in structural['records']]==[(r['branch'],r['population']) for r in base['survivors']],'all28 forced populations')
    for record in structural['records']:forced_record(make(record['population']),record['branch'],record)
    units=json.loads((R/'pass16-p21-unit-graphs.json').read_text())
    need([(r['branch'],r['population']) for r in units['records']]==[(r['branch'],r['population']) for r in structural['survivors']],'all14 finite unit populations')
    tested=sum(unit_record(make(r['population']),r['branch'],r) for r in units['records'])
    # Certificate-damage controls run through semantic predicates, no hashes.
    damages=0
    for record in structural['records']:
        if record['kind']=='forced_radius_losses':
            changed=dict(record);changed['forced_triangles']+=1
            try:forced_record(make(changed['population']),changed['branch'],changed)
            except ValueError:damages+=1
            else:raise ValueError('lost triangle damage accepted')
            break
    for record in structural['records']:
        if record['kind']=='forced_uncovered_triangle':
            changed=dict(record);changed['SS_high_leave']-=1
            try:forced_record(make(changed['population']),changed['branch'],changed)
            except ValueError:damages+=1
            else:raise ValueError('leave demand damage accepted')
            break
    for record in units['records']:
        if record['kind']=='unit_graph_INCOMPATIBLE':
            changed=dict(record);changed['accepted_internal_masks']=[0]
            try:unit_record(make(changed['population']),changed['branch'],changed)
            except ValueError:damages+=1
            else:raise ValueError('false unit realization accepted')
            break
    for record in base['records']:
        if record['kind']=='radius_crossing_capacity':
            changed=dict(record);changed['crossing_lower']+=1
            try:base_record(make(changed['population']),changed)
            except ValueError:damages+=1
            else:raise ValueError('crossing bound damage accepted')
            break
    need(damages==4,'four independent semantic damages')
    summary=dict(agent='six-code-3',role='researcher',status='PRIVATE_COMPLETE_INDEPENDENT_ALGORITHM_CUT_REPLAY',
                 necessary_populations=494,base_survivors=28,forced_survivors=14,final_necessary_survivors=len(units['survivors']),
                 finite_unit_masks_tested=tested,all_accepted_internal_mask_sets_match=True,
                 checked_certificate_damages=damages,elapsed_seconds=time.monotonic()-start,
                 independent_peer_review=False,ordinary_bridges_formalized=False,new_pair_total_claim=None)
    out=R/'pass16-independent-cuts.json';need(not out.exists(),'fresh independent result')
    out.write_text(json.dumps(summary,sort_keys=True,indent=2)+'\n')
    print(json.dumps(summary,sort_keys=True))

if __name__=='__main__':main()
