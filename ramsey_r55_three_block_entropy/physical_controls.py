"""Complete primitive truth table and indexed physical controls in own q9 fixtures."""
from collections import Counter
from itertools import combinations,product
from pathlib import Path
import argparse,hashlib,json,time
import physical
HERE=Path(__file__).resolve().parent

def need(ok,why):
    if not ok:raise ValueError(why)
def literal_five(a,s):
    values={a[u][v] for u,v in combinations(s,2)}
    return next(iter(values)) if len(values)==1 else None

def pair_ok(a,i,j):
    return all(literal_five(a,s) is None for s in combinations(list(range(4*i,4*i+4))+list(range(4*j,4*j+4)),5))
def independent_oracle(a):
    tested=0
    for s in combinations(range(4,36),5):
        sizes=Counter(v//4 for v in s)
        if sorted(sizes.values())!=[1,1,3]:continue
        tested+=1
        if literal_five(a,s) is not None:return False,tested
    return True,tested

def truth_table():
    cases=0
    for colour in (0,1):
        for x,y,edge in product(range(15) if colour else range(1,16),range(15) if colour else range(1,16),range(2)):
            a=[[0]*6 for _ in range(6)]
            for u,v in combinations(range(4),2):a[u][v]=a[v][u]=colour
            for u in range(4):a[u][4]=a[4][u]=(x>>u)&1;a[u][5]=a[5][u]=(y>>u)&1
            a[4][5]=a[5][4]=edge
            bad=any(literal_five(a,list(s)+[4,5]) is not None for s in combinations(range(4),3))
            mx=x if colour else 15^x;my=y if colour else 15^y
            by_types=bool(set(physical.column_types(mx))&set(physical.column_types(my))) and edge==colour
            need(bad==by_types,'complete primitive truth table');cases+=1
    return cases

def run(out):
    out=Path(out);out.mkdir();start=time.monotonic();truth=truth_table();cases=Counter();stream=hashlib.sha256();fixtures=[];positive_fives=0;pair_checks=0;rejections=0
    with (out/'MUTATIONS.jsonl').open('w') as dump:
        for number in range(3):
            original=json.loads((HERE.parent/'ramsey_r55_q9_core_contact_domains'/f'FIXTURE{number}.json').read_text());task=original['task'];r=int(task.split('-')[2][1:]);base=physical.matrix(original['graph'])
            allowed=set()
            for i,j in combinations(range(1,9),2):
                for u,v in product(range(4),repeat=2):
                    base[4*i+u][4*j+v]=base[4*j+v][4*i+u]=int(u//2==v//2);allowed.add((4*i+u,4*j+v))
                need(pair_ok(base,i,j),'balanced pair palette');pair_checks+=1
            old=physical.matrix(original['graph'])
            need(all(base[u][v]==old[u][v] for u,v in physical.PAIRS if (u,v) not in allowed),'only ordinary non-root coordinates changed')
            ok,n=independent_oracle(base);need(ok and physical.witness(base,9,r) is None,'positive full physical oracle');positive_fives+=n
            item=dict(task=task,graph=physical.graph(base),passes_filter=True,parent_fixture=f'FIXTURE{number}.json')
            fixtures.append(item);(out/f'positive{number}.json').write_text(json.dumps(item,sort_keys=True,indent=2)+'\n')
            saved_colours=set()
            for centre in range(1,9):
                colour=int(centre<r)
                for left,right in combinations([i for i in range(1,9) if i!=centre],2):
                    for omitted in range(4):
                        group=(1-omitted//2) if colour else omitted//2
                        for s,t in product(range(2),repeat=2):
                            v=4*left+2*group+s;w=4*right+2*group+t;a=[row[:] for row in base]
                            central=[4*centre+u for u in range(4) if u!=omitted]
                            for u in central:
                                a[u][v]=a[v][u]=a[u][w]=a[w][u]=colour
                            a[v][w]=a[w][v]=colour
                            need(literal_five(a,central+[v,w])==colour,'planted literal obstruction')
                            for i,j in combinations(sorted((centre,left,right)),2):need(pair_ok(a,i,j),'mutation leaves prior pair palette');pair_checks+=1
                            found=physical.witness(a,9,r);need(found is not None,'missed physical obstruction');physical.verify_witness(a,9,found)
                            # A red five-set on the eight first non-root vertices certifies every test is bad.
                            bad=next((list(s) for s in combinations(range(4,36,4),5) if literal_five(a,s)==1),None);need(bad is not None,'unexpected candidate fixture')
                            entry=dict(task=task,centre=centre,others=[left,right],omitted=omitted,external=[v,w],colour=colour,graph=physical.graph(a),witness=found,global_red_five=bad)
                            raw=json.dumps(entry,sort_keys=True,separators=(',',':'))+'\n';dump.write(raw);stream.update(raw.encode());cases[colour]+=1
                            if colour not in saved_colours:
                                saved_colours.add(colour);fixtures.append(dict(task=task,graph=entry['graph'],passes_filter=False,expected_colour=colour,witness=found,parent_fixture=f'FIXTURE{number}.json'))
            print(json.dumps(dict(completed_parent_fixture=number,seconds=time.monotonic()-start)),flush=True)
    # Malformed graph and witness controls must fail without relying on asserts.
    def reject(fn):
        nonlocal rejections
        try:fn()
        except (ValueError,KeyError,TypeError):rejections+=1
        else:raise ValueError('accepted corrupt physical input')
    reject(lambda:physical.matrix(dict(n=43,red_hex='0')))
    reject(lambda:physical.matrix(dict(n=43,red_hex=format(1<<903,'0226x'))))
    reject(lambda:physical.matrix(dict(n=True,red_hex='0'*226)))
    reject(lambda:physical.witness(base,9,10));reject(lambda:physical.witness(base,True,5))
    wrong=dict(fixtures[-1]['witness']);wrong['vertices']=[0]+wrong['vertices'][1:];reject(lambda:physical.verify_witness(physical.matrix(fixtures[-1]['graph']),9,wrong))
    (out/'FIXTURES.json').write_text(json.dumps(fixtures,sort_keys=True,indent=2)+'\n')
    result=dict(status='VERIFIED_LITERAL_THREE_BLOCK_PHYSICAL_CONTROLS',primitive_truth_cases=truth,indexed_mutations=sum(cases.values()),
        red_mutations=cases[1],blue_mutations=cases[0],positive_fixtures=3,positive_literal_three_block_fives=positive_fives,
        complete_two_block_palette_checks=pair_checks,physical_corruptions_rejected=rejections,
        mutation_stream_sha256=stream.hexdigest(),fixtures_sha256=hashlib.sha256((out/'FIXTURES.json').read_bytes()).hexdigest(),
        q10_child_inputs_inspected=0,target_found=False)
    (out/'PHYSICAL.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('out');a=p.parse_args();print(json.dumps(run(a.out),sort_keys=True))
