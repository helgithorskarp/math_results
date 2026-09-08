"""Independent certificate check using inverse quotient fibres, not graph census.
Standard Python only. Does not import producer, C++, SAT or graph packages.
"""
import argparse,hashlib,itertools,json,pathlib
D=pathlib.Path(__file__).resolve().parent

def need(ok,why):
    if not ok:raise ValueError(why)

def verify(source,cert):
    labels=source['labels'];edges={frozenset(e) for e in source['edges']};vertices=set(labels)
    need(len(vertices)==516 and len(edges)==2538,'source size')
    neighbors={u:set() for u in vertices}
    for e in edges:
        need(len(e)==2 and e<=vertices,'source simple edge')
        u,v=e;neighbors[u].add(v);neighbors[v].add(u)
    centres=sorted(u for u in vertices if len(neighbors[u])==4)
    need(centres==cert['centres'],'complete degree-four list')
    witnesses=cert['witnesses']
    need(len(witnesses)>0 and len({tuple(w) for w in witnesses})==len(witnesses),'witness uniqueness')
    for w in witnesses:need(len(w)==5 and len(set(w))==5 and set(w)<=vertices,'distinct witness vertices')
    counts=[0]*len(witnesses);quads=0;cases=0;digest=hashlib.sha256()
    for centres4 in itertools.combinations(centres,4):
        stars=[neighbors[c]|{c} for c in centres4]
        if len(set.union(*stars))!=20:continue
        quads+=1
        # Enumerate unordered allowed pairs directly from the four-neighbour sets.
        choices=[]
        for c in centres4:
            choices.append([(u,v) for u in sorted(neighbors[c]) for v in sorted(neighbors[c]) if u<v and frozenset((u,v)) not in edges])
        for pairs in itertools.product(*choices):
            # All stars are disjoint, so these are all nontrivial quotient fibres.
            fibres={u:(u,v) for u,v in pairs}
            removed=set(centres4)|{v for u,v in pairs}
            need(len(removed)==8,'exact target order')
            for wi,w in enumerate(witnesses):
                if removed.intersection(w):continue
                left=w[:2];right=w[2:]
                if all(any(frozenset((a,b)) in edges for a in fibres.get(u,(u,)) for b in fibres.get(v,(v,))) for u in left for v in right):
                    counts[wi]+=1;digest.update(wi.to_bytes(2,'little'));break
            else:raise ValueError(f'uncovered final quotient: {centres4}, {pairs}')
            cases+=1
    need(cases==cert['cases'] and quads==cert['quadruples'],'complete family count')
    return {'verified':True,'source_vertices':516,'source_edges':2538,'centres':len(centres),'compatible_quadruples':quads,'labelled_cases':cases,'vertices_per_case':508,'K23_witnesses':len(witnesses),'covered_cases':sum(counts),'survivors':0,'chosen_witness_counts':counts,'chosen_witness_sha256':digest.hexdigest(),'new_solver_calls':0,'method':'Independent inverse-fibre edge membership on every final quotient'}

def geometry(source):
    labels=source['labels'];points=source['coordinates'];rad=(1,3,5,15,11,33,55,165)
    need(labels==sorted(set(labels)) and len(labels)==516,'source labels')
    need(len(points)==516 and all(len(p)==2 and all(len(z)==8 and all(type(a) is int for a in z) for z in p) for p in points),'coordinate format')
    need(len({tuple(x+y) for x,y in points})==516,'distinct coordinates')
    actual=[];pairs=0
    for u,v in itertools.combinations(range(516),2):
        norm=[0]*8;pairs+=1
        for axis in range(2):
            d=[a-b for a,b in zip(points[u][axis],points[v][axis])]
            for i in range(8):
                norm[0]+=d[i]*d[i]*rad[i]
                for j in range(i+1,8):norm[i^j]+=2*d[i]*d[j]*rad[i&j]
        if norm==[96*96]+[0]*7:actual.append([labels[u],labels[v]])
    need(actual==source['edges'] and len(actual)==2538,'all strict unit edges')
    return {'all_pairs_checked':pairs,'strict_edges':len(actual),'distinct_points':516,'coordinate_denominator':96,'radicands':list(rad)}

def main():
    import copy
    ap=argparse.ArgumentParser();ap.add_argument('--work',type=pathlib.Path,required=True);a=ap.parse_args();a.work.mkdir(parents=True,exist_ok=True)
    raw=(D/'SOURCE.json').read_bytes();s=json.loads(raw);c=json.loads((D/'certificate.json').read_text())
    need(hashlib.sha256(raw).hexdigest()==c['source_sha256'],'source hash')
    r=verify(s,c);r['source_geometry']=geometry(s)
    controls={}
    for name,mutate in [
        ('empty_cover',lambda x:x.update(witnesses=[])),
        ('one_witness_only',lambda x:x.update(witnesses=x['witnesses'][:1])),
        ('repeated_witness_vertex',lambda x:x['witnesses'][0].__setitem__(1,x['witnesses'][0][0])),
        ('missing_centre',lambda x:x.update(centres=x['centres'][:-1]))]:
        bad=copy.deepcopy(c);mutate(bad)
        try:verify(s,bad)
        except ValueError:controls[name]=True
        else:raise ValueError('bad certificate accepted: '+name)
    r['negative_controls']=controls
    want=json.loads((D/'expected.json').read_text())['cover_verification']
    need(r==want,'expected exact receipt')
    (a.work/'verification.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,sort_keys=True))
if __name__=='__main__':main()
