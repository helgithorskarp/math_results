from collections import Counter
from itertools import combinations
from pathlib import Path
import hashlib,json,math,resource,sys,time
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
work=Path(sys.argv[1])
import model,literal
started=time.monotonic();deadline=started+25
g=model.geometry();native=literal.geometry()
parents=json.loads((work/'cover-records.json').read_text())
stream=(work/'optimal.txt').read_text();direct=set()
for line in stream.splitlines():
 fields=line.split()
 if len(fields)!=2:raise ValueError('optimal stream row encoding')
 ordinal,mask=map(int,fields)
 if not 0<=ordinal<len(parents) or mask<0 or mask>>35:raise ValueError('optimal row domain')
 if (ordinal,mask) in direct:raise ValueError('duplicate native optimum')
 direct.add((ordinal,mask))
independent=set();checked=0
for ordinal,parent in enumerate(parents):
 available=[d for d in range(35) if d not in parent['D']]
 k=parent['minimum_extra_deletions'];clauses=parent['inclusion_minimal_clauses']
 for values in combinations(available,k):
  checked+=1;mask=sum(1<<d for d in values)
  if all(mask&c for c in clauses):independent.add((ordinal,mask))
 if time.monotonic()>deadline:raise TimeoutError('predeclared25-second phase budget')
if independent!=direct or checked!=825240 or len(direct)!=1642:
 raise ValueError('complete graph vs book-cover optimum inventory differs')

def red_free(rows):
 return all((rows[u]&rows[v]).bit_count()<4 for u,v in model.PAIRS if rows[u]>>v&1)

blue_orbits=g[3]
records=[];pool_hist=Counter();unresolved=[];merged={}
for ordinal,mask in sorted(direct):
 parent=parents[ordinal]
 additions=[d for d in range(35) if mask>>d&1]
 if len(additions)!=parent['minimum_extra_deletions'] or set(additions)&set(parent['D']):raise ValueError('actual optimum recipe')
 D=sorted(parent['D']+additions);key=(tuple(parent['J']),tuple(parent['P']),tuple(D))
 merged.setdefault(key,[]).append([ordinal,additions])
for number,(key,origins) in enumerate(sorted(merged.items())):
 J,P,D=map(list,key);rows=model.graph(g,J,P,D)
 native_rows=literal.rows(native,J,P,D)
 if rows!=[sum(1<<v for v in row) for row in native_rows] or not red_free(rows):raise ValueError('literal optimum reconstruction/red cap')
 eligible=[]
 for p in range(35):
  if p in P:continue
  child=rows[:];model.toggle(child,blue_orbits[p])
  if red_free(child):eligible.append(p)
 pool_hist[len(eligible)]+=1
 maximal=rows[:]
 for p in eligible:model.toggle(maximal,blue_orbits[p])
 witness=model.blue_bad(maximal)
 record=dict(J=J,P=P,D=D,origins=origins,eligible_promotions=eligible,
             original_red_edges=sum(r.bit_count() for r in rows)//2)
 if witness is None:
  record['full_eligible_pool_blue_valid']=True;unresolved.append(record)
 else:
  u,v,pages=witness;record['permanent_blue_book']=dict(spine=[u,v],pages=pages[:7])
  if len(pages)<7 or maximal[u]>>v&1 or any(maximal[u]>>w&1 or maximal[v]>>w&1 for w in pages[:7]):
   raise ValueError('literal full-pool blue book certificate')
 records.append(record)
 if time.monotonic()>deadline:raise TimeoutError('predeclared25-second phase budget')
out=work
body=json.dumps(records,sort_keys=True,separators=(',',':'))+'\n';(out/'pool-records.json').write_text(body)
report=dict(status='COMPLETE_INDIVIDUAL_RED_PROMOTION_OVERAPPROXIMATION',author='six-books-2',role='researcher',
            complete_optimum_subset_tests=checked,optimal_parent_repair_choices=len(direct),
            unique_red_repaired_recipes=len(merged),eligible_promotion_pool_hist=dict(sorted(pool_hist.items())),
            blue_obstructed_even_after_full_eligible_pool=len(records)-len(unresolved),
            remaining_after_blue_overapproximation=len(unresolved),
            records_bytes=len(body.encode()),records_sha256=hashlib.sha256(body.encode()).hexdigest(),
            optimal_native_stream_sha256=hashlib.sha256(stream.encode()).hexdigest(),
            seconds=time.monotonic()-started,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            soft_seconds=25,
            scope='Every optimum fixed-parent old-red deletion set, merged by final J/P/D recipe. Every red-valid promotion-only descendant is a subset of the individually red-valid pool. A blue B7 in its full pool is permanent. No further red deletions, unpromotions or genericp5/22-host coverage.')
(out/'pool-summary.json').write_text(json.dumps(report,indent=2)+'\n');(out/'unresolved.json').write_text(json.dumps(unresolved,indent=2)+'\n')
print(json.dumps(report,indent=2))

native_rows=[tuple(map(int,line.split())) for line in (work/'pools.txt').read_text().splitlines()]
python_rows=set()
for r in records:
    b=r.get('permanent_blue_book');u,v=b['spine'] if b else (-1,-1)
    pages=sum(1<<x for x in b['pages']) if b else 0
    python_rows.add(tuple([sum(1<<x for x in r[key]) for key in ['J','P','D']]+[r['original_red_edges'],sum(1<<x for x in r['eligible_promotions']),u,v,pages]))
if len(native_rows)!=len(set(native_rows)) or set(native_rows)!=python_rows:
    raise ValueError('complete native vs Python pool/blue-witness records differ')
