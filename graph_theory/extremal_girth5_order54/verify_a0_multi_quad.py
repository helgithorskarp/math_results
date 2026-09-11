"""Definition-level finite controls, independent orbit traversal, and slot witnesses."""
from collections import Counter
from itertools import combinations, product
from pathlib import Path
import copy, hashlib, json
from a0_inventory import profiles
from a0_independent import inventory
from a0_unit_check import unit_contradiction
from verify_a0_quad_orbits import audit

HERE = Path(__file__).resolve().parent

def require(condition, message):
    if not condition:
        raise ValueError(message)

def witness(record):
    """Check the selected incidence objects directly, without SAT variables."""
    index = record["index"]
    m, k, six, seven = list(profiles())[index]
    H = [(0,1),(2,3),(4,5),(6,7),(8,9)] if k == 0 else [(0,1),(0,2),(3,4),(5,6),(7,8)]
    vertices = {i:(d,set(B)) for i,d,B,j in record["selected_vertices"]}
    require(len(vertices) == 42, "42 distinct low vertices required")
    Q = {v:B for v,(d,B) in vertices.items() if len(B) == 4}
    require(len(Q) == six[4] and all(vertices[q][0] == 6 for q in Q), "quad degrees")
    neighbors = {t:set() for t in range(12)}
    for t,u in H:
        neighbors[t].add(u); neighbors[u].add(t)
    for d,counts in ((6,six),(7,seven)):
        require([sum(dd==d and len(B)==c for dd,B in vertices.values()) for c in range(len(counts))] == list(counts), "profile")
    for v,(d,B) in vertices.items():
        require(B <= set(range(12)), "high point range")
        for t,u in combinations(B,2):
            require(u not in neighbors[t] and not neighbors[t]&neighbors[u], "H-square independence")
    for (d,B),(dd,A) in combinations(vertices.values(),2):
        require(len(A&B)<=1, "high-set linearity")
    for t in range(12):
        h=len(neighbors[t])
        require(sum(d==6 and t in B for d,B in vertices.values())==3+h, "six point quota")
        require(sum(d==7 and t in B for d,B in vertices.values())==5-2*h, "seven point quota")
        for u in range(t+1,12):
            paths=int(u in neighbors[t])+len(neighbors[t]&neighbors[u])
            paths+=sum(t in B and u in B for d,B in vertices.values())
            require(paths==1, "unique high pair short path")
    N={q:set() for q in Q};F={q:set() for q in Q}
    for q,v in record["selected_near"]:
        require(q in Q and v in vertices and q!=v, "near endpoints")
        N[q].add(v)
    for u,v in record["selected_far"]:
        require(u in vertices and v in vertices and u!=v, "far endpoints")
        if u in Q:F[u].add(v)
        if v in Q:F[v].add(u)
    qe=0
    for q,B in Q.items():
        require(len(N[q])==2, "two low quad neighbors")
        forbidden=B|set().union(*(neighbors[t] for t in B))
        coverage=Counter(t for v in N[q] for t in vertices[v][1])
        require(coverage==Counter(set(range(12))-forbidden), "quad near partition")
        e=sum(vertices[v][0]==7 for v in N[q]);qe+=e
        require(len(F[q])==9-e, "quad far cardinality")
        require(not N[q]&F[q], "near/far overlap")
        require(all(not vertices[v][1]&B for v in F[q]), "far own-set avoidance")
        coverage=Counter(t for v in F[q] for t in vertices[v][1])
        require(coverage==Counter({t:2 for t in set(range(12))-B}), "quad far double cover")
        for r in Q:
            require((r in N[q])==(q in N[r]), "symmetric quad adjacency")
    bad=set();helpers=[];weight=0
    for v,fs in record["selected_covers"]:
        require(v not in bad and v in vertices, "distinct bad vertices")
        bad.add(v);d,B=vertices[v]
        require(d==7 and len(B) in (1,2), "bad type")
        require(len(fs)==3 and len(set(fs))==3 and v not in fs, "three distinct far vertices")
        require(all(u in vertices for u in fs), "selected far helper")
        coverage=Counter(B)
        for u in fs:coverage.update(vertices[u][1])
        require(coverage==Counter(range(12)), "bad partition")
        qnum=sum(u in Q for u in fs)
        require(qnum>=1 and (len(B)!=1 or qnum==2), "quad cover alternatives")
        for q in Q:
            require((v in F[q])==(q in fs), "prescribed far symmetry")
        if qnum==1:
            hs=[u for u in fs if u not in Q]
            require(all(len(vertices[u][1])==3 for u in hs), "single-quad triple helpers")
            helpers.extend(hs)
        weight+=3-len(B)
    require(len(helpers)==len(set(helpers)), "helper non-reuse")
    require(weight>=2+qe+2*six[1], "charge inequality")
    return {"index":index,"orbit":record["orbit"],"vertices":len(vertices),
            "bad_vertices":len(bad),"weight":weight,"quad_epsilon_sum":qe}

def unit_controls():
    clauses=[]
    for word in product((-1,0,1),repeat=2):
        clauses.append([sign*(i+1) for i,sign in enumerate(word) if sign])
    checked=up=unsat=0
    for mask in range(1<<len(clauses)):
        cnf=[c for i,c in enumerate(clauses) if mask>>i&1]
        satisfiable=any(all(any(bits[abs(x)-1]==(x>0) for x in c) for c in cnf)
                        for bits in product((False,True),repeat=2))
        got=unit_contradiction(cnf)
        require(not got or not satisfiable, "false unit contradiction")
        if satisfiable:require(not got, "SAT formula rejected")
        checked+=1;up+=got;unsat+=not satisfiable
    require(unit_contradiction([[1,1],[-1,-1]]), "duplicate literal units")
    require(not unit_contradiction([[1,-1],[2,2]]), "tautology handling")
    return {"formulas":checked,"unsatisfiable":unsat,"unit_refutations":up}

def main():
    census=list(profiles())
    require(sorted(census)==inventory(), "independent 403-profile census")
    rows=[(i,*r) for i,r in enumerate(census)
          if r[0]==5 and not any(r[2][5:]) and not any(r[3][5:]) and r[2][4]+r[3][4]>=2]
    require([r[0] for r in rows]==[372,373,377,378,386], "complete multi-quad profile cover")
    fixtures=json.loads((HERE/"a0_multi_quad_controls.json").read_text())
    positives=[witness(r) for r in fixtures]
    mutants=[]
    x=copy.deepcopy(fixtures[0]);x["selected_covers"][0][1].pop();mutants.append(x)
    x=copy.deepcopy(fixtures[0]);x["selected_vertices"][0][1]=7;mutants.append(x)
    for x in mutants:
        try:witness(x)
        except ValueError:pass
        else:raise ValueError("Malformed fixture accepted")
    previous=json.loads((HERE/"a0_one_quad_expected.json").read_text())["finite_controls"]
    remainder=[r for r in previous["remaining_profiles"] if r[1]<5]
    forests=[r for r in previous["remaining_high_forests"] if r["m"]<5]
    require(len(remainder)==48 and len(forests)==8, "campaign remainder")
    output={"profiles":rows,"orbits":[audit(k,r) for k,r in ((0,2),(0,3),(1,2))],
            "positive_relaxation_controls":positives,"rejected_mutants":len(mutants),
            "unit_controls":unit_controls(),"remaining_profiles":remainder,
            "remaining_high_forests":forests}
    print(json.dumps(output,sort_keys=True,indent=2))

if __name__=="__main__":
    main()
