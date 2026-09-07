"""Definition-level interface controls and complete representative CNF audits."""
from collections import Counter
from itertools import combinations, combinations_with_replacement, product
import argparse
import hashlib
import json
from math import comb
from pathlib import Path
import random
import tempfile
import model
import normalize
import verify_target
import decode


def span_dimension(xs):
    s={0}
    for x in xs:s|={v^x for v in s}
    return len(s).bit_length()-1


def base_definition(rows,cols,r,known=False):
    if cols!=sorted(cols) or span_dimension(cols)!=r:return False
    c=Counter(cols)
    if c[0]>2 or any(n>5 for x,n in c.items() if x) or (0 in rows and c[0]):return False
    blue=[sum((1-((a&b).bit_count()%2))<<j for j,b in enumerate(cols)) for a in rows]
    if span_dimension(blue)<r:return False
    if known and 0 not in cols and all(1<=c[x]<=2 for x in range(1,16)):return False
    return True


def direct_graph(rows,cols,bits):
    a=len(rows);n=a+len(cols);matrix=[[0]*n for _ in range(n)];t=0
    for i,j in combinations(range(n),2):
        if i<a<=j:value=(rows[i]&cols[j-a]).bit_count()%2
        else:value=(bits>>t)&1;t+=1
        matrix[i][j]=matrix[j][i]=value
    return matrix


def good(matrix):
    for q in combinations(range(len(matrix)),5):
        total=sum(matrix[u][v] for u,v in combinations(q,2))
        if total==0 or total==10:return False
    return True


def categories(table):
    groups={};counts=Counter()
    for row in table:
        code=row[0];rs=model.rows_from_code(code)
        if 0 in rs:name='zero_row'
        elif model.full_support_double(rs):name='known_profile_guard'
        elif any(all((x&a).bit_count()%2 for a in rs) for x in range(1,16)):name='affine_rows'
        else:name='ordinary'
        groups.setdefault(name,code);counts[name]+=1
    if set(groups)!={'zero_row','known_profile_guard','affine_rows','ordinary'}:raise ValueError('category coverage')
    return groups,dict(counts)


def fixture(code):
    rows=model.rows_from_code(code)
    cols=sorted(list(range(1,16))+list(range(1,9)))
    if model.full_support_double(rows):cols=sorted([0]+list(range(1,16))+list(range(1,8)))
    bits=int.from_bytes(hashlib.sha512(f'row-cover-fixture:{code}'.encode()).digest(),'big')%(2**443)
    return {'row_code':code,'columns':cols,'internal_hex':format(bits,'0111x')}


def controls():
    base_cases=0;physical_cases=0;sat_cases=0
    for a,b in [(3,3),(3,4)]:
        for rows in combinations_with_replacement(range(4),a):
            if span_dimension(rows)!=2:continue
            task=model.Task(rows,b,2,False)
            ramsey=list(task.ramsey_clauses())
            for cs in product(range(4),repeat=b):
                cols=list(cs);expected_base=base_definition(rows,cols,2)
                if task.base_holds(cols)!=expected_base:raise ValueError(('base equivalence',rows,cols))
                base_cases+=1
                if not expected_base:continue
                values=task.primary(cols,0)
                for bits in range(2**len(task.internal)):
                    for k,v in enumerate(task.internal.values()):values[v]=bool(bits>>k&1)
                    actual=all(any(values[abs(v)]==(v>0) for v in c) for c in ramsey)
                    expected=good(direct_graph(rows,cols,bits))
                    if actual!=expected:raise ValueError(('physical clauses',rows,cols,bits))
                    physical_cases+=1;sat_cases+=actual
    table=model.load_cover();codes,category_counts=categories(table)
    guard=model.target(codes['known_profile_guard']);guard_cases=0;gate_mutations=0
    base_cols=sorted(list(range(1,16))+list(range(1,9)))
    column_controls=[base_cols,sorted([0]+base_cols[1:]),sorted([1]+base_cols[1:-1]+[1]),list(reversed(base_cols))]
    for cols in column_controls:
        values=guard.primary(cols,0)
        actual=all(any(values[abs(v)]==(v>0) for v in c) for c in guard.base)
        if actual!=base_definition(guard.rows,cols,4,True):raise ValueError('known-profile guard')
        guard_cases+=1
        # Every gate is a full equivalence even if the final exclusion is false.
        for y,op,args in guard.gates:
            expected=any(values[abs(v)]==(v>0) for v in args) if op=='or' else all(values[abs(v)]==(v>0) for v in args)
            if values[y]!=expected:raise ValueError('gate semantics')
            touched=[c for c in guard.base if y in c or -y in c]
            values[y]=not values[y]
            if all(any(values[abs(v)]==(v>0) for v in c) for c in touched):raise ValueError('undetected gate mutation')
            values[y]=not values[y];gate_mutations+=1
    rng=random.Random(19041);transports=0;coordinates=0
    for index in range(16):
        code=table[(index*701)%len(table)][0];data=fixture(code);rows=model.rows_from_code(code);cols=data['columns']
        pa=list(range(20));pb=list(range(23));rng.shuffle(pa);rng.shuffle(pb)
        # Apply one invertible change to rows and its explicitly solved dual to columns.
        image=normalize.linear_maps()[(index*1187)%20160]
        dual=[next(z for z in range(16) if all(((image[1<<k]&z).bit_count()%2)==((b>>k)&1) for k in range(4))) for b in range(16)]
        old=direct_graph(rows,cols,int(data['internal_hex'],16));order=pa+[20+j for j in pb]
        remapped_bits=sum(old[order[i]][order[j]]<<k for k,(i,j) in enumerate(p for p in combinations(range(43),2) if (p[0]<20)==(p[1]<20)))
        raw={'rows':[image[rows[i]] for i in pa],'columns':[dual[cols[j]] for j in pb],'internal_hex':format(remapped_bits,'0111x')}
        normalized=normalize.normalize(raw)
        source=direct_graph(raw['rows'],raw['columns'],remapped_bits);target=verify_target.adjacency(normalized['graph'])
        for i,j in combinations(range(43),2):
            if target[i][j]!=source[normalized['new_to_old'][i]][normalized['new_to_old'][j]]:raise ValueError('physical normalization')
            coordinates+=1
        if normalized['parameters']['row_code']!=code:raise ValueError('canonical task changed')
        transports+=1
    positive=verify_target.count(json.loads(Path(__file__).with_name('control42.json').read_text()),False)
    if positive['red_fives'] or positive['blue_fives'] or positive['n']!=42:raise ValueError('positive graph control')
    negatives=0;data=fixture(codes['ordinary']);task=model.target(data['row_code']);values=task.primary(data['columns'],int(data['internal_hex'],16))
    fake='s SATISFIABLE\nv '+' '.join(str(v if x else -v) for v,x in sorted(values.items()))+' 0\n'
    for text in ['s UNKNOWN\n','s SATISFIABLE\nv 1 0\n',fake.replace('v 1 ','v -1 ',1),fake]:
        try:decode.decode(data['row_code'],text)
        except ValueError:negatives+=1
        else:raise ValueError('invalid SAT transcript accepted')
    for graph in [json.loads(Path(__file__).with_name('control42.json').read_text()),{'n':23,'red_hex':'0'*64},{'n':43,'red_hex':'f'*226}]:
        try:verify_target.adjacency(graph)
        except ValueError:negatives+=1
        else:raise ValueError('invalid target graph accepted')
    # All independently reconstructed internal coordinates must remain decisions.
    for code in codes.values():
        t=model.target(code);d=fixture(code);zero=t.graph(d['columns'],0);base=int(zero['red_hex'],16)
        for k,pair in enumerate(t.internal):
            changed=int(t.graph(d['columns'],1<<k)['red_hex'],16)^base
            if changed!=1<<t.pairs.index(pair):raise ValueError('internal coordinate')
    return {'status':'VERIFIED_COMPLETE_TASK_INTERFACE_CONTROLS','base_label_cases':base_cases,'physical_primary_cases':physical_cases,'satisfying_small_cases':sat_cases,
            'known_guard_cases':guard_cases,'gate_mutations':gate_mutations,'normalization_transports':transports,'transported_physical_coordinates':coordinates,
            'internal_coordinate_checks':443*len(codes),'negative_controls':negatives,'positive42':positive,'category_counts':category_counts,'representative_codes':codes}


def full_instance(code,path):
    task=model.target(code);record=task.write(path);data=fixture(code);bits=int(data['internal_hex'],16)
    values=task.primary(data['columns'],bits);matrix=direct_graph(task.rows,data['columns'],bits)
    def physical_id(i,j):
        if i<20<=j:
            label=task.rows[i]
            return -1 if label==0 else 2+443+23*16+(label-1)*23+(j-20)
        if i<20:a,b,n,offset=i,j,20,0
        else:a,b,n,offset=i-20,j-20,23,190
        return 2+offset+a*n-a*(a+1)//2+(b-a-1)
    checked=0;red=0;blue=0
    with Path(path).open() as f:
        header=f.readline().split()
        if header!=['p','cnf',str(task.variables),str(record['clauses'])]:raise ValueError('header')
        for original in task.base:
            line=tuple(map(int,f.readline().split()))
            if line!=tuple(original)+(0,):raise ValueError('base prefix')
        for q in combinations(range(43),5):
            pairs=list(combinations(q,2));colors=[matrix[u][v] for u,v in pairs]
            red+=all(colors);blue+=not any(colors)
            for sign in (-1,1):
                literal_set={sign*physical_id(u,v) for u,v in pairs}
                if 1 in literal_set:continue
                literal_set.discard(-1)
                expected=tuple(sorted(literal_set,key=lambda x:(abs(x),x)))
                actual=tuple(map(int,f.readline().split()))
                if actual!=expected+(0,):raise ValueError(('physical clause content',code,q,sign))
                holds=any(values[abs(v)]==(v>0) for v in expected)
                wanted=not all(colors) if sign==-1 else any(colors)
                if holds!=wanted:raise ValueError('physical clause semantics')
                checked+=1
        if f.read():raise ValueError('extra DIMACS content')
    expected_ramsey=2*comb(43,5)-(comb(42,4)-comb(19,4) if 0 in task.rows else 0)
    if checked!=record['ramsey_clauses'] or checked!=expected_ramsey:raise ValueError('five-set clause census')
    if not red+blue:raise ValueError('fixture unexpectedly target')
    return {'row_code':code,**record,'physical_clauses_checked':checked,'fixture_red_fives':red,'fixture_blue_fives':blue}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--work',required=True);p.add_argument('--output',required=True);p.add_argument('--controls-only',action='store_true');p.add_argument('--existing-controls')
    args=p.parse_args();work=Path(args.work);work.mkdir(exist_ok=True)
    result=json.loads(Path(args.existing_controls).read_text()) if args.existing_controls else controls()
    if not args.controls_only:
        instances=[]
        for category,code in sorted(result['representative_codes'].items()):
            print(f'Checking full43 category {category}',flush=True)
            path=work/f'{category}.cnf';r=full_instance(code,path);r['category']=category;instances.append(r)
        result={'controls':result,'instances':instances,'status':'VERIFIED_ALL_PATTERN_RANK4_TASK_HANDOFF'}
    Path(args.output).write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(result['status'],flush=True)
