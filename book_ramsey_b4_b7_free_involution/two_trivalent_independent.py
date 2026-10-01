"""Independent all-one-trivalent Book quotient census; six-books-2 researcher.
No other generator imports. Binary decisions and literal 22-point spines.
Binary propagation helper adapted from own trivalent_independent.py485cb22.
"""
from collections import Counter
from itertools import combinations, combinations_with_replacement, product
from hashlib import sha256
from pathlib import Path
import argparse
import json

PAIRS=tuple(combinations(range(11),2));INDEX={e:k for k,e in enumerate(PAIRS)}
UNIVERSE=(1<<55)-1;ALL22=(1<<22)-1
INCIDENT=[sum(1<<k for k,e in enumerate(PAIRS) if i in e) for i in range(11)]
P=Path(__file__).resolve().parent
def pair_mask(edges):return sum(1<<INDEX[tuple(sorted(e))] for e in edges)

def enumerate_binary(wanted,included,excluded,clauses):
    def visit(yes,no):
        while True:
            previous=yes,no
            if yes&no:return
            for i in range(11):
                if yes&no:return
                need=wanted[i]-(yes&INCIDENT[i]).bit_count()
                choices=(UNIVERSE^(yes|no))&INCIDENT[i];count=choices.bit_count()
                if need<0 or need>count:return
                if need==0:no|=choices
                elif need==count:yes|=choices
            for clause in clauses:
                if yes&clause:continue
                choices=clause&~no
                if not choices:return
                if choices.bit_count()==1:yes|=choices
            if (yes,no)==previous:break
        if yes&no:return
        if all((yes&INCIDENT[i]).bit_count()==wanted[i] for i in range(11)):
            yield yes;return
        undecided=UNIVERSE^(yes|no)
        active=[i for i in range(11) if (yes&INCIDENT[i]).bit_count()<wanted[i]]
        vertex=min(active,key=lambda i:(undecided&INCIDENT[i]).bit_count())
        choice=undecided&INCIDENT[vertex];bit=choice&-choice
        yield from visit(yes|bit,no)
        yield from visit(yes,no|bit)
    yield from visit(included,excluded)

def geometry():
    # At most one separate cycle fits. Independent integer-equation inventory.
    for arms in combinations_with_replacement(range(1,11),3):
        for cycle in (0,5,6,7):
            if sum(arms)+cycle!=10:continue
            components=[];v=1
            for length in arms:components.append([0]+list(range(v,v+length)));v+=length
            edges={tuple(sorted((a,b))) for arm in components for a,b in zip(arm,arm[1:])}
            if cycle:
                verts=list(range(v,v+cycle));edges|={tuple(sorted((a,b))) for a,b in zip(verts,verts[1:]+verts[:1])}
            yield 'Y:'+','.join(map(str,arms))+('+'+'C'+str(cycle) if cycle else ''),edges
    for k,t,p in product(range(5,11),range(1,7),range(3,6)):
        if p==5 or k+t+p!=11:continue
        cycle=list(range(k));tail=[0]+list(range(k,k+t));path=list(range(k+t,11))
        edges={tuple(sorted((a,b))) for a,b in zip(cycle,cycle[1:]+cycle[:1])}
        edges|={tuple(sorted((a,b))) for arm in (tail,path) for a,b in zip(arm,arm[1:])}
        yield f'L10:{k},{t},{p}',edges
    for k,t,c in product(range(5,11),range(1,7),(0,5)):
        if k+t+c!=11:continue
        cycle=list(range(k));tail=[0]+list(range(k,k+t))
        edges={tuple(sorted((a,b))) for a,b in zip(cycle,cycle[1:]+cycle[:1])}
        edges|={tuple(sorted((a,b))) for a,b in zip(tail,tail[1:])}
        if c:
            verts=list(range(k+t,11));edges|={tuple(sorted((a,b))) for a,b in zip(verts,verts[1:]+verts[:1])}
        yield f'L11:{k},{t}'+('+C5' if c else ''),edges

def graph_rows(red,blue,inside,sign_word=0):
    rows=[0]*22
    for i in range(11):
        if (inside>>i)&1:rows[2*i]|=1<<(2*i+1);rows[2*i+1]|=1<<(2*i)
    matching=0
    for k,(i,j) in enumerate(PAIRS):
        if (red>>k)&1:
            for a in (0,1):rows[2*i+a]|=3<<(2*j);rows[2*j+a]|=3<<(2*i)
        elif not (blue>>k)&1:
            parity=(sign_word>>matching)&1;matching+=1
            for a in (0,1):
                b=a^parity;rows[2*i+a]|=1<<(2*j+b);rows[2*j+b]|=1<<(2*i+a)
    if any(row.bit_count()!=10 for row in rows):raise RuntimeError('literal regular degree')
    return rows

def page_table(red,blue,inside,sign_word=0):
    rows=graph_rows(red,blue,inside,sign_word);comp=[ALL22^(1<<i)^r for i,r in enumerate(rows)]
    result=[];matching=0
    for k,(i,j) in enumerate(PAIRS):
        if (red>>k)&1:
            count=(rows[2*i]&rows[2*j]).bit_count()+(rows[2*i]&rows[2*j+1]).bit_count();label='R'
        elif (blue>>k)&1:
            count=(comp[2*i]&comp[2*j]).bit_count()+(comp[2*i]&comp[2*j+1]).bit_count();label='D'
        else:
            p=(sign_word>>matching)&1;matching+=1
            count=(rows[2*i]&rows[2*j+p]).bit_count()+(comp[2*i]&comp[2*j+(1-p)]).bit_count();label='M'
        result.append([label,i,j,count])
    return result

def literal_failure(red,blue,inside):
    pages=page_table(red,blue,inside)
    for label,cap in [('R',6),('D',12),('M',9)]:
        for row in pages:
            if row[0]==label and row[3]>cap:return row
    return None

def degree_controls():
    inventory={};pairs=tuple(combinations(range(5),2))
    for word in range(1024):
        edges={e for k,e in enumerate(pairs) if (word>>k)&1}
        degree=tuple(sum(v in e for e in edges) for v in range(5))
        if max(degree)<=3:inventory.setdefault(degree,set()).add(pair_mask(edges))
    targets=0
    for d in product(range(4),repeat=5):
        expected=inventory.get(d,set());actual=set(enumerate_binary(list(d)+[0]*6,0,0,[]))
        if actual!=expected:raise RuntimeError('independent degree-three positive/control domain')
        targets+=1
    wanted=(2,)*5;clause=pair_mask({(0,2),(1,3),(2,4)});yes=pair_mask({(0,1)});no=pair_mask({(0,3)})
    expected={m for m in inventory[wanted] if m&clause and m&yes and not m&no}
    actual=set(enumerate_binary(list(wanted)+[0]*6,yes,no,[clause]))
    if not actual or actual!=expected:raise RuntimeError('positive three-edge clause/forced/excluded control')
    if list(enumerate_binary(list(wanted)+[0]*6,yes,yes,[])):raise RuntimeError('inconsistent include/exclude accepted')
    return {'five_vertex_binary_graphs':1024,'degree_vectors_0_to_3':targets,'three_edge_clause_positive_graphs':len(actual),'inconsistent_include_exclude_rejected':True}

def run(record_path):
    expected={}
    for line in record_path.read_text().splitlines():
        row=json.loads(line)
        if type(row)!=list or len(row)!=3 or type(row[0])!=str or type(row[1])!=int or (row[0],row[1]) in expected:raise RuntimeError('invalid main comparison data')
        expected[row[0],row[1]]=row[2]
    records=[];summaries=[];geometry_count=0;flagwords=0;sign_checks=0;flagcases=0
    for label,edges in geometry():
        geometry_count+=1;nr=[set() for _ in range(11)]
        for i,j in edges:nr[i].add(j);nr[j].add(i)
        rd=[len(v) for v in nr];red=pair_mask(edges)
        if rd.count(3)!=1 or min(rd)!=1 or max(rd)!=3 or sum(rd) not in (20,22):raise RuntimeError('independent geometry/profile')
        for inside in range(2048):
            flagwords+=1
            if inside.bit_count()%2:continue
            if any((inside>>i)&1 and (rd[i]!=1 or rd[next(iter(nr[i]))]!=3) for i in range(11)):continue
            flagcases+=1;wanted=[rd[i]+((inside>>i)&1) for i in range(11)];no=red;yes=0
            for k,(i,j) in enumerate(PAIRS):
                if rd[i]==1 and j not in nr[next(iter(nr[i]))]-{i}:no|=1<<k
                if rd[j]==1 and i not in nr[next(iter(nr[j]))]-{j}:no|=1<<k
                if rd[i]==rd[j]==1 and nr[i]==nr[j]:yes|=1<<k
            clauses=[]
            for i,j in edges:
                choices=set()
                for e in PAIRS:
                    a,b=e
                    if ((a==i and b in nr[j]) or (b==i and a in nr[j]) or
                        (a==j and b in nr[i]) or (b==j and a in nr[i])):
                        choices.add(e)
                clauses.append(pair_mask(choices)&~no)
            case=label+':F'+str(inside);seen=set();counts=Counter();control_done=False
            for blue in enumerate_binary(wanted,yes,no,clauses):
                if blue in seen:raise RuntimeError('duplicate independent completion')
                seen.add(blue);fail=literal_failure(red,blue,inside)
                key=(case,blue)
                if key not in expected or expected.pop(key)!=fail:raise RuntimeError('domain/literal page disagreement '+case)
                if fail is None:raise RuntimeError('independent necessary survivor')
                counts[fail[0]]+=1;records.append([case,blue,fail])
                if not control_done:
                    m=55-(red|blue).bit_count();words=[0,(1<<m)-1]+[1<<v for v in range(m)]
                    words.append(sum(1<<v for v in range(m) if v%2))
                    reference=page_table(red,blue,inside)
                    for word in words:
                        if page_table(red,blue,inside,word)!=reference:raise RuntimeError('summed page signing control')
                        sign_checks+=1
                    control_done=True
            summaries.append({'case':case,'D_completions':len(seen),'first_failure_counts':dict(counts)})
    if expected:raise RuntimeError('unmatched main comparison records')
    records.sort(key=lambda x:(x[0],x[1]));encoded=''.join(json.dumps(x,separators=(',',':'))+'\n' for x in records)
    return {'agent':'six-books-2','role':'researcher','complete':True,'profiles':summaries,'geometric_R_forms':geometry_count,'inside_words_tested':flagwords,'eligible_R_inside_cases':flagcases,'D_completions':len(records),'survivors':0,'canonical_records_sha256':sha256(encoded.encode()).hexdigest(),'all_records_match_entrywise':True,'binary_degree_controls':degree_controls(),'literal_signing_control_words':sign_checks,'signing_controls_are_validation_not_universal_sign_proof':True,'threads':1,'local_jobs':1,'author_algorithmic_independence_not_peer_review':True}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--main-records',type=Path,required=True)
    parser.add_argument('--emit',action='store_true')
    parser.add_argument('--expected',type=Path,default=Path(__file__).with_name('two_trivalent_expected.json'))
    args=parser.parse_args();result=run(args.main_records)
    if not args.emit and result!=json.loads(args.expected.read_text())['independent']:
        raise RuntimeError('independent fixture mismatch')
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':main()
