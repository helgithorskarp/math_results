from functools import lru_cache
from itertools import combinations
from pathlib import Path
from collections import Counter
import hashlib,json,resource,sys,time
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
work=Path(sys.argv[1]);work.mkdir(exist_ok=True)
import literal,model
started=time.monotonic();deadline=started+25
native=literal.geometry();oldred=native[1][0]
edge_to_orbit={tuple(sorted(e)):i for i,orb in enumerate(oldred) for e in orb}
parents=json.loads((HERE/'PARENTS.json').read_text())
node_limit=250000;total_nodes=0

def all_clauses(rows,D):
    by_mask={};books=0
    for u,v in combinations(range(22),2):
        if v not in rows[u]:continue
        common=sorted(rows[u]&rows[v])
        for pages in combinations(common,4):
            books+=1
            edges=[(u,v)]+[tuple(sorted((endpoint,w))) for endpoint in (u,v) for w in pages]
            mask=0
            for edge in edges:
                orbit=edge_to_orbit.get(edge)
                if orbit is not None:
                    if orbit in D:raise ValueError('deleted original-red edge in surviving book')
                    mask|=1<<orbit
            by_mask.setdefault(mask,dict(spine=[u,v],pages=list(pages)))
    keep=[]
    for mask in sorted(by_mask,key=lambda x:(x.bit_count(),x)):
        if not any(c&mask==c for c in keep):keep.append(mask)
    return tuple(keep),by_mask,books

def exact_minimum(clauses):
    global total_nodes
    nodes=0
    @lru_cache(maxsize=None)
    def search(cs,budget):
        nonlocal nodes
        global total_nodes
        nodes+=1;total_nodes+=1
        if total_nodes>node_limit or time.monotonic()>deadline:raise TimeoutError('predeclared finite-cover node/time limit')
        if not cs:return 0
        if budget==0:return None
        forced=0
        for c in cs:
            if c.bit_count()==1:forced|=c
        if forced:
            if forced.bit_count()>budget:return None
            result=search(tuple(c for c in cs if not c&forced),budget-forced.bit_count())
            return None if result is None else forced|result
        packing=0;occupied=0
        for c in cs:
            if not occupied&c:
                occupied|=c;packing+=1
                if packing>budget:return None
        c=cs[0];choices=[]
        while c:
            bit=c&-c;c-=bit
            choices.append(bit)
        choices.sort(key=lambda bit:-sum(bool(d&bit) for d in cs))
        for bit in choices:
            result=search(tuple(c for c in cs if not c&bit),budget-1)
            if result is not None:return bit|result
        return None
    failed=[]
    for k in range(27):
        result=search(clauses,k)
        if result is not None:
            if result.bit_count()!=k:raise ValueError('minimum cover cardinality differs')
            return k,result,dict(nodes=nodes,cache=search.cache_info()._asdict(),failed_budgets=failed)
        failed.append(k)
    raise ValueError('finite feasible cover not found')

records=[];hist=Counter();weighted=Counter();status='COMPLETE_MINIMUM_MONOTONE_RED_REPAIR'
try:
    for parent in parents:
        rows=literal.rows(native,parent['J'],parent['P'],parent['D'])
        cs,all_masks,books=all_clauses(rows,parent['D'])
        if not cs:raise ValueError('unexpected red-valid boundary')
        record={k:parent[k] for k in ['index','J','P','D','weight']}
        record.update(initial_red_books=books,distinct_deletion_clauses=len(all_masks),
                      inclusion_minimal_clauses=list(cs))
        if 0 in all_masks:
            record.update(repair_impossible=True,unmodifiable_book=all_masks[0]);hist['impossible']+=1;weighted['impossible']+=parent['weight']
        else:
            minimum,mask,stats=exact_minimum(cs)
            deletions=[d for d in range(35) if mask>>d&1]
            if any(d in parent['D'] for d in deletions):raise ValueError('minimum repair overlaps previous deletion')
            repaired=literal.rows(native,parent['J'],parent['P'],parent['D']+deletions)
            if any(len(repaired[u]&repaired[v])>=4 for u,v in combinations(range(22),2) if v in repaired[u]):
                raise ValueError('literal minimum repair graph still red-invalid')
            record.update(repair_impossible=False,minimum_extra_deletions=minimum,
                          example_extra_deletions=deletions,cover_search=stats,
                          example_red_edges=sum(map(len,repaired))//2)
            hist[str(minimum)]+=1;weighted[str(minimum)]+=parent['weight']
        records.append(record)
except TimeoutError as exc:
    status='INCOMPLETE_OPERATIONAL_COVER_LIMIT';reason=str(exc)
out=work
body=json.dumps(records,sort_keys=True,separators=(',',':'))+'\n';(out/'cover-records.json').write_text(body)
report=dict(status=status,author='six-books-2',role='researcher',completed_representatives=len(records),
            total_representatives=len(parents),minimum_repair_hist=dict(hist),labeled_repair_hist=dict(weighted),
            cover_nodes=total_nodes,node_limit=node_limit,soft_seconds=25,
            seconds=time.monotonic()-started,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            records_bytes=len(body.encode()),records_sha256=hashlib.sha256(body.encode()).hexdigest(),
            scope='Exact red-only monotone deletion repair of declared p4/q9 blue-boundary parents. No old-blue unpromotion, root change or generic p5 coverage. Completeness is the book-hitting equivalence and complete cover branching, unformalized; same author.')
if status!='COMPLETE_MINIMUM_MONOTONE_RED_REPAIR':report['reason']=reason
(out/'cover-summary.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
if status!='COMPLETE_MINIMUM_MONOTONE_RED_REPAIR':raise SystemExit(75)

if status=='COMPLETE_MINIMUM_MONOTONE_RED_REPAIR':
    lines=[]
    for r in records:
        if r['repair_impossible']:raise ValueError('fixture declares finite repairs')
        values=[r['index'],r['weight']]+r['J']+r['P']+r['D']+[r['minimum_extra_deletions']]+r['example_extra_deletions']
        lines.append(' '.join(map(str,values)))
    (work/'parents.txt').write_text('\n'.join(lines)+'\n')
