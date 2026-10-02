"""Late source correspondence; target code visible here, not blind evidence."""
import argparse,hashlib,importlib,itertools,json,sys
from pathlib import Path
from model import *

PINS={'literal.py':'edfb8daaeb6d70c2d647e493d962ea0a083accbd1760456540d8b315fff9cbb4',
      'formulas.py':'44b0a6c6cb885b7fe404931c7fc9576b2b761d985a7478a9c1f91a72e2f5ec52',
      'RESULTS.json':'157735924b9a9f264972371dc453abdbd669db3e805e2993c446ce7da722db76'}

def bits(s):return sum(1<<i for i in s)
def row(s):return frozenset(int(i) for i in s)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--native',type=Path,required=True);ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args()
    for n,pin in PINS.items():need(hashlib.sha256((args.native/n).read_bytes()).hexdigest()==pin,'native input source pin '+n)
    sys.path.insert(0,str(args.native.resolve()))
    literal=importlib.import_module('literal');formula=importlib.import_module('formulas')
    native=json.loads((args.native/'RESULTS.json').read_text());owned=json.loads((Path(__file__).parent/'RESULTS.json').read_text())
    cv=covers();decks=owned['endpoint_decks'];decks[0]=[z for z in decks[0] if z!='0145']
    valid=[];frames=0;fields=0
    for rr in itertools.product(*decks):
        rows=dict(zip(SY+T,[row(z) for z in rr]+[row('023')]))
        for r in (0,1):
            g,rk,d=frame(rows,r)
            gg,dd,qq=literal.build(r,tuple(bits(rows[z])for z in T),tuple(bits(rows[z])for z in SY))
            bw,bd,bq=formula.build(r,tuple(bits(rows[z])for z in T),tuple(bits(rows[z])for z in SY))
            for i,z in enumerate(OLD):
                need({OLD[j]for j in gg[i]}==g[z] and bits(gg[i])==bw[i], 'all adjacency entries')
                need(dd[i]==bd[i]==d[z] and qq[i]==bq[i]==rk[z], 'all degrees/ranks')
                fields+=3
            frames+=1
            ok=all(bounds(g,rk,d,a,b)[0]<=bounds(g,rk,d,a,b)[1]for a,b in itertools.combinations(OLD,2))
            need(ok==(not literal.pair_failures(gg,dd,qq))==formula.valid(bw,bd,bq),'whole pair feasibility')
            if r==0 and ok:valid.append([bits(rows[z])for z in T[:2]+SY])
    # Compare full nine native records as sets because iteration orders differ.
    need(sorted(valid)==sorted(native['endpoint_cases']['whole_literal_formula_necessary_records']),'whole nine entry-level outcomes')
    for own_key,native_key in [('cover_rows','covers'),('missing_rows','missing'),('initial_T2','T2_masks'),('final_T2','T2_rows_after_union_budget')]:
        need(sorted(bits(row(z))for z in owned[own_key])==native['cut_cycle'][native_key],'complete '+own_key)
    grouped={}
    for mask,s0,edge,counts in owned['union_budget_records']:
        k=bits(row(mask));grouped.setdefault(k,[]).append([bits(row(s0)),edge,6-sum(counts)])
    for rec in native['cut_cycle']['T2_union_rejections']:
        ours=grouped[rec['T2_row']]
        need(len(ours)==rec['SY0_covers_checked'] and all(z[1]==rec['witness_edge'] for z in ours) and
             max(z[2]for z in ours)==rec['largest_union_allowance'],'all 200 union witnesses')
    def native_shape(rr):return [bits(row(rr[i]))for i in (2,3,0,1)]
    need(sorted(native_shape(rr)for rr in owned['scalar_shapes'])==native['endpoint_cases']['elementary_cover_records'],'all scalar shapes')
    need(sorted(native_shape(rr)for rr in owned['physical_shapes'])==native['endpoint_cases']['remaining_records'],'all final shapes')
    forced={U:frozenset(),V:Q,A:frozenset(),X[1]:row('0145'),X[2]:row('023'),X[3]:row('123'),
            SX[0]:row('0345'),SX[1]:row('1345'),T[2]:row('012')}
    need({str(OLD.index(z)):bits(q)for z,q in forced.items()}==native['forced_pattern']['named_complete_Q_rows'],'all named forced rows')
    domain_checks=[]
    for rec in owned['physical_shapes']:
        rows=dict(zip(SY+T,[row(z)for z in rec]+[row('023')]))
        g,rk,d=frame(rows)
        gg,dd,qq=literal.build(0,tuple(bits(rows[z])for z in T),tuple(bits(rows[z])for z in SY))
        forced2=forced|{X[4]:row('0245'),SY[1]:row('01')}
        unknown=(X[0],X[5],SY[0],T[0],T[1]);domains=[]
        for z in unknown:
            independent=[bits(q)for q in subsets(Q,rk[z]) if all(row_pair_ok(g,rk,d,z,q,b,qb)for b,qb in forced.items())]
            independent.sort()
            need(independent==literal.row_options(gg,dd,qq,OLD.index(z)),'every row-domain word')
            domains.append(independent)
        prefixes=[]
        for rs in itertools.product(*domains):
            qr=forced2|{z:frozenset(i for i in range(6)if w>>i&1)for z,w in zip(unknown,rs)}
            if all(row_pair_ok(g,rk,d,a,qr[a],b,qr[b])for a,b in itertools.combinations(OLD,2)):
                prefixes.append({z:sorted(qr[z])for z in OLD})
        need(not prefixes,'native forced-SY1 scan independently empty')
        nat=next(x for x in native['terminal_cases']['records']if x['R_SY0']==bits(rows[SY[0]]))
        need([len(d)for d in domains]==nat['unknown_row_domain_counts'] and
             len(list(itertools.product(*domains)))==nat['complete_row_tuples'] and not nat['whole_accepted_prefixes'],'full domain-prefix census')
        domain_checks.append({'SY0':rec[0],'domains':domains,'prefixes':prefixes})
    # Independently reproduce exact complement/cap control on the native fixture.
    rows=dict(zip(SY+T,[row(z)for z in owned['physical_shapes'][1]]+[row('023')]))
    g,rk,d=frame(rows); words=(0,63,0,11,51,13,14,53,52,57,58,36,3,56,24,7)
    full={z:set(g[z])for z in OLD};full.update({q:set()for q in range(6)})
    for z,w in zip(OLD,words):
        for q in range(6):
            if w>>q&1:full[z].add(q);full[q].add(z)
    for q in range(6):
        for b in ((q-1)%6,(q+1)%6):full[q].add(b)
    universe=set(full);fail=[]
    for a,b in itertools.combinations(OLD+tuple(range(6)),2):
        pages=(full[a]&full[b])if b in full[a]else((universe-full[a]-{a})&(universe-full[b]-{b}))
        cap=3 if b in full[a] else 6
        if len(pages)>cap:fail.append([a,b,len(pages),cap])
    need(fail and len(full[X[5]]&full[T[0]])==4,'native invalid22 fixture ordinary audit')
    out={'actual_agent':'six-reviewer-4','role':'independent mathematical reviewer','late_target_visible':True,
         'source_pins':PINS,'whole_frames_compared':frames,'adjacency_degree_rank_fields':fields,
         'whole_nine_records':valid,'all200_union_witnesses_checked':True,'terminal_domains':domain_checks,
         'all_two_scalar_shape_sets_match':True,'invalid22_fixture_degree_and_edge_preserved':all(len(full[z])==d[z]for z in OLD)and sum(map(len,full.values()))==216,
         'invalid22_B_four_regular':all(len(full[z]&set(SY+T+tuple(range(6))))==4 for z in SY+T+tuple(range(6))),
         'invalid22_first_failure':fail[0],'status':'PASS'}
    args.output.write_text(canonical(out));print(json.dumps({'status':'PASS','frames':frames,'all_fields':fields,'bytes':args.output.stat().st_size,'sha256':hashlib.sha256(args.output.read_bytes()).hexdigest()}))
if __name__=='__main__':main()
