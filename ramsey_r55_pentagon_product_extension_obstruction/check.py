"""Independent literal checker for the factored extension certificate."""
from collections import Counter
from itertools import combinations, product
from pathlib import Path
import argparse
import json


def require(condition, message):
    if not condition:
        raise ValueError(message)


def make_cycle():
    edges = {frozenset((i,(i+1)%5)) for i in range(5)}
    return edges


def make_core():
    cycle = make_cycle()
    edges = set()
    for u,v in combinations(range(25),2):
        bu,bv = u//5,v//5
        is_red = (frozenset((u%5,v%5)) in cycle) if bu==bv else (frozenset((bu,bv)) in cycle)
        if is_red:
            edges.add(frozenset((u,v)))
    return edges


def is_path(vertices, edges):
    degrees = {v:sum(frozenset((u,v)) in edges for u in vertices if u != v) for v in vertices}
    if sorted(degrees.values()) != [1,1,2,2,2]:
        return False
    seen = {vertices[0]}
    while True:
        more = {v for v in vertices if any(frozenset((u,v)) in edges for u in seen)}
        if more <= seen:
            break
        seen |= more
    return len(seen) == 5


def validate(certificate):
    require(certificate['format']=='pentagon-product-extension-v1','format')
    cycle = make_cycle()
    all_pairs = {frozenset(e) for e in combinations(range(5),2)}
    group = {1:[],2:[],3:[]}
    rows = certificate['inner']
    require(len(rows)==32 and [r['word'] for r in rows]==list(range(32)),'inner coverage')
    for row in rows:
        word=row['word'];red={i for i in range(5) if word & (1 << i)};blue=set(range(5))-red
        rp=[sorted(e) for e in cycle if e <= red]
        bp=[sorted(e) for e in all_pairs-cycle if e <= blue]
        rp.sort();bp.sort()
        tag=int(bool(rp))+2*int(bool(bp))
        require(tag != 0 and row['tag']==tag,'inner covering tag')
        require(row['red_pair']==(rp[0] if rp else None),'red pair')
        require(row['blue_pair']==(bp[0] if bp else None),'blue pair')
        group[tag].append(word)
    weights={str(k):len(v) for k,v in group.items()}
    require(weights=={'1':11,'2':11,'3':10} and certificate['tag_counts']==weights,'tag weights')
    outer=certificate['outer']
    require(len(outer)==243 and [tuple(r['tags']) for r in outer]==list(product((1,2,3),repeat=5)), 'outer coverage')
    core=make_core();coverage=0;physical_checks=0;color_counts=Counter()
    literal=json.loads(Path(__file__).with_name('CORE.json').read_text())
    core_word=sum(1 << i for i,e in enumerate(combinations(range(25),2)) if frozenset(e) in core)
    require(literal['n']==25 and literal['red_hex']==format(core_word,'075x') and literal['red_edges']==len(core),'literal core file')
    for row in outer:
        tags=row['tags'];color=row['color'];pair=row['blocks']
        require(color in ('red','blue') and len(pair)==2 and pair==sorted(set(pair)) and all(type(i) is int and 0<=i<5 for i in pair),'outer certificate shape')
        i,j=pair;red=color=='red';flag=1 if red else 2
        require(tags[i]&flag and tags[j]&flag,'outer marked blocks')
        require((frozenset(pair) in cycle)==red,'outer color')
        count=1
        for tag in tags:count*=len(group[tag])
        require(row['attachment_count']==count,'class weight')
        coverage+=count;color_counts[color]+=count
        # Exhaust every attachment on the two selected blocks. The other
        # three blocks do not meet the five-set, so their choices are free.
        for wi,wj in product(group[tags[i]],group[tags[j]]):
            pi=rows[wi][color+'_pair'];pj=rows[wj][color+'_pair']
            vertices=[25]+[5*i+a for a in pi]+[5*j+a for a in pj]
            require(len(set(vertices))==5,'literal five distinct')
            for u,v in combinations(vertices,2):
                if u==25 or v==25:
                    z=v if u==25 else u
                    attachment=wi if z//5==i else wj
                    edge=bool(attachment & (1 << (z%5)))
                else:
                    edge=frozenset((u,v)) in core
                require(edge==red,'literal monochromatic K5')
            physical_checks+=1
    require(coverage==1 << 25 and certificate['attachment_count']==coverage,'all attachments covered')
    require(certificate['free_43_edges']==603 and certificate['fixed_ordered_core_family_count']==1 << 603,'global family size')
    require(certificate['status']=='COMPLETE_CORE_EXTENSION_FAMILY_EXCLUDED','status')
    # Independently check that the fixed core is itself a good25 in h3931's
    # hereditary class; the equality classification remains imported.
    five_sets=0
    all_core_pairs={frozenset(e) for e in combinations(range(25),2)}
    comp=all_core_pairs-core
    for vertices in combinations(range(25),5):
        pairs={frozenset(e) for e in combinations(vertices,2)}
        require(not pairs<=core and not pairs<=comp,'core Ramsey property')
        require(not is_path(vertices,core) and not is_path(vertices,comp),'core P5/coP5 property')
        five_sets+=1
    return dict(status='CHECKED_COMPLETE_PENTAGON_PRODUCT_EXTENSION_EXCLUSION',
                inner_words=32,outer_tag_classes=243,all_attachment_words_covered=coverage,
                literal_selected_two_block_attachment_checks=physical_checks,
                selected_certificate_color_counts=dict(sorted(color_counts.items())),
                core_order=25,core_red_edges=len(core),core_five_sets_checked=five_sets,
                free_edges_fixed_core43=603,full_fixed_core43_family_count=1 << 603,
                target_solver_calls=0,target_found=False)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('certificate',type=Path);a=p.parse_args()
    print(json.dumps(validate(json.loads(a.certificate.read_text())),indent=2,sort_keys=True))
