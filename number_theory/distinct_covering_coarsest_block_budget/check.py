"""Exact source checks; no solver, graph, orbit code or private state required."""
from hashlib import sha256
from itertools import product
from math import gcd, prod
from pathlib import Path
import argparse
import json

from budget import coarsest_budget, decode_boxes, matrix, parameters, period_capacities

HERE = Path(__file__).resolve().parent


def require(value, message):
    if not value:
        raise ValueError(message)


def data_hash(value):
    return sha256(json.dumps(value,separators=(",",":")).encode()).hexdigest()


def literal_decode(Q,axes,boxes):
    """Scan every ordinary residue; no CRT arithmetic is used to decode."""
    result = []
    for x in range(Q):
        matches = [box[-1] for box in boxes
                   if all(mask>>(x%axis)&1 for mask,axis in zip(box,axes))]
        require(len(matches)<=1,"Literal overlapping box")
        result.append(matches[0] if matches else 0)
    return result


def literal_capacities(vector,resources):
    """All ordinary physical phases, using the full finite-period vector."""
    capacities, populations = {}, {}
    for n in resources:
        sums = [0]*n
        for x,w in enumerate(vector):
            sums[x%n] += w
        capacities[n] = max(sums)
        populations[n] = sums
    return capacities,populations


def physical_G(B,C,b,capacities,populations):
    """Restricted ordinary Bd-phases, independently of the W implementation."""
    H = {d:[max(populations[B*d][t::b]) for t in range(b)]
         for d in range(2,C+1) if C%d==0}
    M = {d:capacities[B*d] for d in H}
    totals = [sum(max(M[d],2*H[d][t]) for d in H) for t in range(b)]
    return max(totals),totals,H,M


def partitions(n):
    if n==0:
        yield ()
        return
    for earlier in partitions(n-1):
        for i in range(len(earlier)):
            yield earlier[:i]+(earlier[i]+(n-1,),)+earlier[i+1:]
        yield earlier+((n-1,),)


def literal_partition_budget(W,C):
    """Complete finite F_C definition for the small declared matrices only."""
    divisors = tuple(d for d in range(1,C+1) if C%d==0)
    choices = tuple(partitions(len(divisors)))
    best = 0
    tuples = 0
    for residues in product(*(range(d) for d in divisors)):
        for pi in choices:
            total = 0
            for group in pi:
                counts = [sum(z%divisors[i]==residues[i] for i in group) for z in range(C)]
                total += max(sum(k*W[z][t] for z,k in enumerate(counts) if k>=2)
                             for t in range(len(W[0])))
            best = max(best,total)
            tuples += 1
    return best,tuples


def certificate_check():
    certificate = json.loads((HERE/"certificate.json").read_text())
    B,C,b,N,Q = (certificate[k] for k in ("B","C","b","N","weight_period"))
    require(parameters(B,C,b)==N and N%Q==0 and (b*C)%Q==0,"Period hypotheses")
    require(certificate["anchors"]==[[8,0],[9,0],[10,5],[12,9],[15,10]],"Wrong declared prefix")
    require(len({n for n,a in certificate["anchors"]})==5,"Repeated prescribed modulus")
    base = decode_boxes(Q,certificate["axes"],certificate["boxes"])
    require(base==literal_decode(Q,certificate["axes"],certificate["boxes"]),"Decoder mismatch")
    require(data_hash(base)==certificate["base_weight_sha256"],"Wrong weight digest")
    actual = base*(N//Q)
    require(all(not w or all(x%n!=a for n,a in certificate["anchors"])
                for x,w in enumerate(actual)),"Weight on a prescribed class")
    placed = {n for n,a in certificate["anchors"]}
    resources = tuple(n for n in range(8,N+1) if N%n==0 and n not in placed)
    top = {B*d for d in range(1,C+1) if C%d==0}
    require(top<=set(resources),"A top resource has been prescribed or is ineligible")
    reduced = period_capacities(N,base,resources)
    literal,populations = literal_capacities(actual,resources)
    require(reduced==literal,"Actual phase maximum or CRT lift differs")
    inverse = pow(b,-1,C)
    W = [[base[(t+b*((z-t)*inverse%C))%Q] for t in range(b)] for z in range(C)]
    formula = coarsest_budget(W,C)
    G,totals,H,M = physical_G(B,C,b,literal,populations)
    require((formula["G"],formula["label_totals"],formula["H"],formula["M"])==
            (G,totals,H,M),"Full physical G maximum differs")
    outside = sum(literal[n] for n in resources if n not in top)
    demand = sum(actual)
    total = outside+G
    require((demand,outside,G,total,demand-total)==
            tuple(certificate[k] for k in ("expected_physical_demand","expected_outside_capacity",
                                          "expected_G","expected_total","expected_gap")),
            "Wrong exact certificate totals")
    require(total<demand,"Strict covering obstruction fails")
    ordinary = sum(literal.values())
    old_fibre = ordinary-literal[1728]+literal[8640]+literal[N]
    require(old_fibre==certificate["comparison_old_fibre_capacity"],"Old same-vector comparison differs")
    return {"N":N,"B":B,"C":C,"b":b,"Q":Q,"anchors":certificate["anchors"],
            "resource_count":len(resources),"top_count":len(top),
            "outside_resource_count":len(resources)-len(top),"boxes":len(certificate["boxes"]),
            "base_demand":sum(base),"physical_demand":demand,"outside_capacity":outside,
            "G":G,"total_capacity":total,"strict_gap":demand-total,
            "G_label_totals":totals,"G_maximizing_label":formula["maximizing_label"],
            "top_cofactor_maxima":M,"actual_phase_maxima_sha256":data_hash(literal),
            "ordinary_capacity":ordinary,"old_fibre_capacity_same_vector":old_fibre,
            "base_weight_sha256":data_hash(base),"full_root_exclusion":False}


def partition_controls():
    rows = []
    scans = 0
    for C in (4,6,8,9):
        for b in (1,2,3):
            for seed in range(2):
                W = [[(7*z+3*t+5*seed)%6 for t in range(b)] for z in range(C)]
                F,tuples = literal_partition_budget(W,C)
                answer = coarsest_budget(W,C)
                require(F<=answer["G"]<=answer["doubled_independent_sum"],"Coarsest upper inequalities")
                scans += tuples
                rows.append({"C":C,"b":b,"seed":seed,"F":F,"G":answer["G"]})
    fixture = [[2,0,0],[0,3,0],[2,0,0],[0,0,0]]
    require(parameters(9,4,3)==36,"Fixture physical parameters")
    F,_ = literal_partition_budget(fixture,4)
    answer = coarsest_budget(fixture,4)
    require((F,answer["G"],answer["doubled_independent_sum"])==(10,12,14),"Strict relaxation fixture")
    return {"fixed_matrices":len(rows),"complete_partition_phase_tuples":scans,
            "rows_sha256":data_hash(rows),"strict_fixture":{"N":36,"F":F,"G":12,"doubled_sum":14}}


def positive_controls():
    B,C,b = 4,3,2
    N = parameters(B,C,b)
    cover = ((2,0),(3,0),(4,1),(6,1),(12,11))
    require(len({n for n,a in cover})==len(cover) and
            all(any(x%n==a for n,a in cover) for x in range(N)),"Genuine positive cover")
    counts = {"unprescribed_weights":0,"prescribed_two_weights":0}
    for prescribed in (False,True):
        for data in product(range(3),repeat=3 if prescribed else 6):
            W = ([[0,w] for w in data] if prescribed else [list(data[2*z:2*z+2]) for z in range(C)])
            actual = [W[x%C][x%b] for x in range(N)]
            resources = [n for n,a in cover if not(prescribed and n==2)]
            capacities,populations = literal_capacities(actual,resources)
            G = coarsest_budget(W,C)["G"]
            physical,_,_,_ = physical_G(B,C,b,capacities,populations)
            require(G==physical,"Positive control physical G mismatch")
            require(sum(actual)<=sum(v for n,v in capacities.items() if n not in (4,12))+G,
                    "False exclusion of a genuine covering")
            if prescribed:
                require(all(actual[x]==0 for x in range(0,N,2)),"Prescribed support control")
            counts["prescribed_two_weights" if prescribed else "unprescribed_weights"] += 1
    return {"cover_moduli":[n for n,a in cover],"N":N,**counts,
            "scope":"Small genuine cover has minimum2, used only to test the general inequality"}


def rejection_controls():
    cases = (lambda:coarsest_budget([[1]],2),
             lambda:coarsest_budget([[1],[-1]],2),
             lambda:coarsest_budget([[True],[0]],2),
             lambda:coarsest_budget([[1],[0,1]],2),
             lambda:parameters(4,2,2),lambda:parameters(9,4,2),
             lambda:decode_boxes(6,[2,3,2],[[1,1,1,1]]),
             lambda:period_capacities(12,[1,0,0],[4,4]))
    for case in cases:
        try:
            case()
        except ValueError:
            continue
        raise ValueError("Malformed hypothesis was accepted")
    require(coarsest_budget([[0],[0]],2)["G"]==0,"Zero component boundary")
    return len(cases)


def evidence():
    return {"actual_author":"six-covering-3","role":"researcher",
            "scope":"Written general lemma; exact fixed-prefix43200 cut; no full root or new global bound",
            "certificate":certificate_check(),"partition_controls":partition_controls(),
            "positive_controls":positive_controls(),"rejected_invalid_inputs":rejection_controls(),
            "independent_reviewer":False}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-expected",action="store_true")
    args = parser.parse_args()
    result = evidence()
    rendered = json.dumps(result,indent=2)+"\n"
    if args.write_expected:
        (HERE/"expected.json").write_text(rendered)
    else:
        expected = json.loads((HERE/"expected.json").read_text())
        require(json.loads(rendered)==expected,"Expected evidence mismatch")
    print(rendered,end="")


if __name__=="__main__":
    main()
