"""six-reviewer-1: fresh exact reconstruction; Python standard library only."""
from pathlib import Path
from collections import Counter
from itertools import product, combinations
import argparse, hashlib, json

BASE = Path(__file__).resolve().parent

def require(ok, message):
    if not ok:
        raise ValueError(message)

def ints(value, n):
    require(isinstance(value, list) and len(value) == n, "integer vector")
    require(all(type(x) is int for x in value), "literal integer")
    return tuple(value)

def unique_json(path):
    def pairs(rows):
        d = {}
        for k, v in rows:
            require(k not in d, "duplicate JSON key")
            d[k] = v
        return d
    return json.loads(Path(path).read_text(), object_pairs_hook=pairs)

def point(m, p):
    a, b, c, d = m
    x, y = p
    return a*x+b*y, c*x+d*y

def matrix(m):
    m = ints(m, 4)
    a, b, c, d = m
    require(a*a+c*c == b*b+d*d == 1 and a*b+c*d == 0, "D4 orthogonality")
    return m

def cell(m, t, p):
    """Transform the doubled center, not vertices or a normalized mask."""
    cx, cy = point(m, (2*p[0]+1, 2*p[1]+1))
    x, y = cx+2*t[0]-1, cy+2*t[1]-1
    require(x % 2 == y % 2 == 0, "integer image square")
    return x//2, y//2

def halo(cells):
    return {(x+i,y+j) for x,y in cells for i,j in product((-1,0,1),repeat=2)}

def orientations(q):
    records = []
    for swap in (False,True):
        for a,b in product((-1,1),repeat=2):
            m = (0,a,b,0) if swap else (a,0,0,b)
            raw = [cell(m,(0,0),p) for p in q]
            low = min(p[0] for p in raw), min(p[1] for p in raw)
            normalized = tuple(sorted((x-low[0],y-low[1]) for x,y in raw))
            records.append((normalized,m,low))
    require(len({r[0] for r in records}) == 8, "eight distinct literal orientations")
    return sorted(records)

def quotient(p):
    """L=< (260,0),(94,2) >, proved by the integral basis change."""
    x,y=p
    s=y%2
    return s,(x-47*(y-s))%260

def adjugate(p):
    x,y=p
    return (22*x+6*y)%520,(-6*x+22*y)%520

def canonical(clause):
    return tuple(sorted(set(clause), key=lambda x:(abs(x),x)))

def clean(clauses):
    return sorted({canonical(c) for c in clauses if not any(-x in c for x in c)},
                  key=lambda c:(len(c),c))

def build(input_path=None, tiling_path=None, row_order="hnf"):
    data=unique_json(input_path or BASE/"input.json")
    require(data.get("depth")==2 and data.get("margin")==1, "literal depth/margin")
    q=tuple(ints(x,2) for x in data["cells"])
    require(len(q)==65 and len(set(q))==65 and tuple(sorted(q))==q, "literal 65-cell source")
    u=tuple(sorted(halo(q))); variables={p:i+1 for i,p in enumerate(u)}
    require(len(u)==123, "123-site ground set")
    oo=orientations(q); levels=data["levels"]
    require([len(x) for x in levels]==[1,6,12], "19-map level partition")
    maps=[]; cuts=[0]
    for level in levels:
        for pose in level:
            o,x,y=ints(pose,3);require(0<=o<8,"orientation index")
            _,m,low=oo[o];maps.append((m,(x-low[0],y-low[1])))
        cuts.append(len(maps))
    require(maps[0]==((1,0,0,1),(0,0)), "identity physical root")
    images=[{p:cell(m,t,p) for p in u} for m,t in maps]
    inverse=[{v:p for p,v in im.items()} for im in images]
    require(all(len(im)==len(u) for im in inverse), "injective cell maps")
    packing=[]; packing_tags=[]
    for i,j in combinations(range(len(maps)),2):
        for v in sorted(set(inverse[i]) & set(inverse[j])):
            a,b=variables[inverse[i][v]],variables[inverse[j][v]]
            packing.append((-a,-b));packing_tags.append((i,j,v))
    stages=[]; stage_tags=[]
    for k in (0,1):
        suppliers={}
        for j in range(cuts[k+2]):
            for p,v in images[j].items():
                suppliers.setdefault(v,set()).add(variables[p])
        rows=[]; tags=[]
        for j in range(cuts[k+1]):
            for p,v in images[j].items():
                x,y=v
                for dx,dy in product((-1,0,1),repeat=2):
                    w=x+dx,y+dy
                    rows.append((-variables[p],*sorted(suppliers.get(w,set()))))
                    tags.append((k,j,p,w))
        stages.append(rows);stage_tags.append(tags)
    tt=unique_json(tiling_path or BASE/"tiling.json")
    require([ints(p,2) for p in tt["periods"]]==[(22,6),(-6,22)], "literal lattice")
    periods=((22,6),(-6,22))
    # h1=11u-3v; h2=4u-v; inversely u=-h1+3h2,v=-4h1+11h2.
    u0,v0=periods
    require(tuple(11*u0[i]-3*v0[i] for i in (0,1))==(260,0), "basis h1")
    require(tuple(4*u0[i]-v0[i] for i in (0,1))==(94,2), "basis h2")
    require(u0[0]*v0[1]-u0[1]*v0[0]==520, "lattice index")
    reps=[(matrix(r["matrix"]),ints(r["translation"],2)) for r in tt["representatives"]]
    require(len(reps)==8, "eight representatives")
    keys=tuple((s,r) for s in range(2) for r in range(260))
    row_coefficients={k:Counter() for k in keys}
    for m,t in reps:
        for p in u:row_coefficients[quotient(cell(m,t,p))][variables[p]]+=1
    # A bijective alternate row naming for public trace compatibility.
    naming={k:adjugate((k[1],k[0])) for k in keys}
    require(len(set(naming.values()))==520, "complete quotient naming")
    order=keys if row_order=="hnf" else tuple(sorted(keys,key=naming.__getitem__))
    bad=[];bad_tags=[]
    for n,k in enumerate(order):
        z=len(u)+1+n;row=row_coefficients[k]
        for x,multiplicity in sorted(row.items()):
            if multiplicity==1:
                bad.append((-z,-x,*sorted(y for y in row if y!=x)))
                bad_tags.append((k,x))
    failed=tuple(range(len(u)+1,len(u)+521))
    nonempty=tuple(range(1,len(u)+1))
    groups={"packing":clean(packing),"halo0":clean(stages[0]),"halo1":clean(stages[1]),
            "nonempty":[nonempty],"failure":clean(bad+[failed])}
    formula=clean([c for cs in groups.values() for c in cs])
    require(all(abs(x)<=643 for c in formula for x in c), "variable universe")
    return {"q":q,"u":u,"maps":maps,"images":images,"cuts":cuts,"reps":reps,
            "coefficients":row_coefficients,"order":order,"naming":naming,"groups":groups,
            "formula":formula,"nonempty":nonempty,"failed":failed,
            "raw_obligations":{"packing":len(packing),"halo0":len(stages[0]),"halo1":len(stages[1])}}

def evaluate(formula, assignment):
    return all(any(assignment[abs(x)]==(x>0) for x in c) for c in formula)

def assignment(model, chosen, failed=False):
    vv={p:i+1 for i,p in enumerate(model["u"])}
    out={vv[p]:(p in chosen) for p in vv}
    for i,k in enumerate(model["order"]):
        count=sum(n*out[x] for x,n in model["coefficients"][k].items())
        out[len(vv)+1+i]=failed and count!=1
    return out

def physical(model, chosen, depth=2):
    footprints=[{cell(m,t,p) for p in chosen} for m,t in model["maps"][:model["cuts"][depth+1]]]
    require(all(not (a&b) for a,b in combinations(footprints,2)), "physical disjointness")
    unions=[set().union(*footprints[:n]) for n in model["cuts"][1:depth+2]]
    for a,b in zip(unions,unions[1:]):require(halo(a)<=b,"physical halo")
    return footprints,unions

def boundary(cells):
    """Planar square-complex boundary; one simple positive cycle, all edges."""
    edges=set()
    for x,y in cells:
        edges.update([((x,y),(x+1,y)),((x+1,y),(x+1,y+1)),
                      ((x+1,y+1),(x,y+1)),((x,y+1),(x,y))])
    exposed={e for e in edges if (e[1],e[0]) not in edges}
    outgoing={};incoming=Counter()
    for a,b in exposed:
        require(a not in outgoing,"pinched/multiple boundary exits")
        outgoing[a]=b;incoming[b]+=1
    require(all(incoming[v]==1 for v in outgoing) and set(incoming)==set(outgoing),"simple boundary")
    require(bool(outgoing),"nonempty boundary")
    start=min(outgoing);v=start;seen=set();twice_area=0
    while v not in seen:
        seen.add(v);w=outgoing[v];twice_area+=v[0]*w[1]-w[0]*v[1];v=w
    require(v==start and len(seen)==len(exposed),"one whole boundary cycle")
    require(twice_area==2*len(cells),"positive boundary area")
    return len(exposed)

def read_rup(path,nvars):
    """Strict addition-only textual RUP; no deletions/RAT or ignored trailing fields."""
    clauses=[]
    for line in Path(path).read_text().splitlines():
        if not line.strip() or line.startswith("c"):continue
        tokens=line.split()
        require(all(t.lstrip("-").isdigit() for t in tokens),"RUP integer syntax")
        row=[int(t) for t in tokens]
        require(bool(row) and row[-1]==0 and 0 not in row[:-1],"one final RUP zero")
        require(all(0<abs(x)<=nvars for x in row[:-1]),"RUP literal domain")
        c=canonical(row[:-1]);require(len(c)==len(row)-1,"duplicate RUP literal")
        clauses.append(c)
    require(bool(clauses) and clauses[-1]==(),"final empty RUP clause")
    require(() not in clauses[:-1],"premature empty RUP clause")
    return clauses

def propagate(database,assumptions):
    """Independent full scanning closure, with explicit original-premise dependencies."""
    values={};reasons={};used=set();assignments=0;passes=0
    for lit in assumptions:
        x=abs(lit);v=lit>0
        if x in values and values[x]!=v:return True,set(),assignments,passes
        values[x]=v;reasons[x]=set()
    while True:
        changed=False;passes+=1
        for c,dependency in database:
            if any(abs(x) in values and values[abs(x)]==(x>0) for x in c):continue
            free=[x for x in c if abs(x) not in values]
            if len(free)>1:continue
            dep=set(dependency)
            for x in c:
                if abs(x) in values:dep.update(reasons[abs(x)])
            if not free:return True,dep,assignments,passes
            x=abs(free[0]);values[x]=free[0]>0;reasons[x]=dep
            assignments+=1;changed=True
        if not changed:return False,set(),assignments,passes

def verify_rup(formula,proof):
    database=[(c,{i}) for i,c in enumerate(formula)]
    records=[]
    for i,c in enumerate(proof):
        ok,deps,units,passes=propagate(database,[-x for x in c])
        require(ok,f"non-RUP addition {i}")
        database.append((c,deps));records.append({"index":i,"clause":list(c),"units":units,
                                                "passes":passes,"original_dependencies":sorted(deps)})
    return records

def local_controls():
    rows=0
    for coefficients in [(1,),(2,),(1,1),(1,2),(2,2),(1,1,1),(1,2,3),()]:
        for bits in product((False,True),repeat=len(coefficients)):
            actual=sum(n*x for n,x in zip(coefficients,bits))!=1
            permit=all(not bits[i] or any(bits[j] for j in range(len(bits)) if j!=i)
                       for i,n in enumerate(coefficients) if n==1)
            require(actual==permit,"full bad-row predicate truth table");rows+=1
    # Cell-center and four-corner images agree for ALL D4/negative coordinates.
    for swap in (False,True):
        for a,b in product((-1,1),repeat=2):
            m=(0,a,b,0) if swap else (a,0,0,b)
            for p in product(range(-2,3),repeat=2):
                t=(-3,4);cs=[point(m,(p[0]+i,p[1]+j)) for i,j in product((0,1),repeat=2)]
                expected=min(x for x,y in cs)+t[0],min(y for x,y in cs)+t[1]
                require(cell(m,t,p)==expected,"cell-center physical bridge");rows+=1
    # Negative coordinates and a full quotient fundamental rectangle.
    for x,y in product(range(-15,16),repeat=2):
        for dx,dy in ((22,6),(-6,22),(260,0),(94,2)):
            require(quotient((x+dx,y+dy))==quotient((x,y)),"quotient translation");rows+=1
    # Small RUP soundness controls plus finite independent semantic exhaustion.
    tiny=[(1,2),(-1,2),(1,-2),(-1,-2)]
    rec=verify_rup(clean(tiny),[(1,),()])
    require(len(rec)==2,"tiny RUP refutation")
    for bits in product((False,True),repeat=2):
        require(not evaluate(tiny,{1:bits[0],2:bits[1]}),"tiny exhaustive UNSAT");rows+=1
    for f,p in [([(1,2)],[(1,),()]), ([(1,)], [()])]:
        try:verify_rup(f,p)
        except ValueError:rows+=1
        else:raise ValueError("unsound RUP control accepted")
    for bad in [set(),{(0,0),(2,0)}, {(0,0),(1,1)},halo({(0,0)})-{(0,0)}]:
        try:boundary(bad)
        except ValueError:rows+=1
        else:raise ValueError("bad polygon accepted")
    require(boundary({(0,0),(1,0)})==6,"disc positive boundary")
    return rows

def build_record(model):
    q=set(model["q"]);_,unions=physical(model,q)
    assignment_q=assignment(model,q)
    no_fail=clean([c for c in model["formula"] if c!=model["failed"]])
    require(evaluate(no_fail,assignment_q),"Q65 positive full original formula without failure")
    require(not evaluate(model["formula"],assignment_q),"Q65 cannot license a bad row")
    empty=assignment(model,set(),True)
    no_empty=clean([c for c in model["formula"] if c!=model["nonempty"]])
    require(evaluate(no_empty,empty),"empty source actual nonempty-removed control")
    counts={k:sum(n*assignment_q[x] for x,n in r.items()) for k,r in model["coefficients"].items()}
    require(set(counts.values())=={1},"literal Q65 full periodic cover")
    serial=lambda x:hashlib.sha256(json.dumps(x,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    return {"role":"independent mathematical reviewer","agent":"six-reviewer-1",
            "sites":len(model["u"]),"copy_maps":[[list(m),list(t)] for m,t in model["maps"]],
            "all_quotient_rows":[{"key":list(k),"coefficients":sorted(r.items())} for k,r in sorted(model["coefficients"].items())],
            "variables":643,"clauses":len(model["formula"]),
            "formula_sha256":serial(model["formula"]),
            "group_clauses":{g:len(c) for g,c in model["groups"].items()},
            "raw_obligations":model["raw_obligations"],
            "prefix_areas":[len(x) for x in unions],"prefix_boundaries":[boundary(x) for x in unions],
            "multiplicities":dict(sorted(Counter(n for r in model["coefficients"].values() for n in r.values()).items())),
            "local_exact_control_rows":local_controls()}

def main():
    p=argparse.ArgumentParser();p.add_argument("--proof",type=Path);p.add_argument("--wire",action="store_true")
    p.add_argument("--counterexample",type=Path);p.add_argument("--output",type=Path)
    a=p.parse_args();model=build(row_order="adjugate" if a.wire else "hnf")
    result=build_record(model)
    if a.proof:
        proof=read_rup(a.proof,643);rec=verify_rup(model["formula"],proof)
        result["proof_records"]=rec;result["proof_additions"]=len(proof)
        support=rec[-1]["original_dependencies"]
        small=[model["formula"][i] for i in support]
        # Retain only additions whose transitive original support is contained.
        # Every used earlier lemma remains available; final empty is retained.
        retained=[c for c,r in zip(proof,rec) if set(r["original_dependencies"])<=set(support)]
        verify_rup(small,retained)
        result["sufficient_original_support"]={"clauses":[list(c) for c in small],"size":len(small),
                                              "retained_proof":[list(c) for c in retained],
                                              "groups":{g:len(set(cs)&set(small)) for g,cs in model["groups"].items()}}
    if a.counterexample:
        fixture=unique_json(a.counterexample)
        # The data bridge is deliberately supplied by a separate late adapter.
        raise ValueError("Use the separately documented late data-only adapter")
    text=json.dumps(result,sort_keys=True,indent=2)+"\n"
    if a.output:a.output.write_text(text)
    else:print(text,end="")

if __name__=="__main__":
    main()
