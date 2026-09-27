"""Definition-level certificate checks and exact universal-budget controls."""
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
from copy import deepcopy
import argparse
import json
from guard import finite_guard, nonpositive_direction

ROOT = Path(__file__).resolve().parent


def need(value, why):
    if not value:
        raise ValueError(why)


def scalar(x, y):
    return sum((a*b for a, b in zip(x, y)), F(0))


def distance2(x, y):
    return sum((a-b)**2 for a, b in zip(x, y))


def determinant(a):
    return (a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1])
            -a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0])
            +a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0]))


def rank(rows):
    a = [[F(v) for v in row] for row in rows]
    pivot = 0
    for j in range(len(a[0])):
        p = next((i for i in range(pivot, len(a)) if a[i][j]), None)
        if p is None:
            continue
        a[pivot], a[p] = a[p], a[pivot]
        scale = a[pivot][j]
        a[pivot] = [v/scale for v in a[pivot]]
        for i in range(len(a)):
            if i != pivot:
                factor = a[i][j]
                a[i] = [u-factor*v for u, v in zip(a[i], a[pivot])]
        pivot += 1
        if pivot == len(a):
            break
    return pivot


def encoded(x, y, p, s=1):
    return {"sources": [[str(v) for v in point] for point in x],
            "targets": [[str(v) for v in point] for point in y],
            "weights": list(map(str, p)), "variance": str(s)}


def fixtures():
    v = [(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)]
    eps = F(1, 2**60)
    x = [tuple(F(a, 10) for a in z) for z in v]
    y = [tuple(F(63, 64)*F(a, 10) for a in z) for z in v]
    for i, j in product(range(4), repeat=2):
        if i != j:
            x.append(tuple(F(v[j][k]-2*v[i][k], 10) for k in range(3)))
            y.append(tuple(F(63, 640)*(v[j][k]+2*v[i][k]) for k in range(3)))
    y = [(a,b,eps*c) for a,b,c in y]
    target = encoded(x,y,[F(1,16)]*16)
    grid = list(product([-2,-1,1,2], repeat=2))
    x = [(F(a,8),F(b,8),eps*F(a*b,8)) for a,b in grid]
    y = [(abs(a)/4,abs(b)/4,abs(a+b)/4) for a,b,_ in x]
    source = encoded(x,y,[F(1,16)]*16)
    alpha = F(1, 2**100)
    x = [(F(a,8),F(b,8),F(0)) for a,b in grid]+[(F(0),F(0),F(1,4))]
    y = [(abs(a)/4,abs(b)/4,abs(a+b)/4) for a,b,_ in x]
    rare = encoded(x,y,[(1-alpha)/16]*16+[alpha])
    x = [tuple(F(a,8) for a in z) for z in v]
    y = [tuple(a/2 for a in z) for z in x]
    unresolved = encoded(x,y,[F(1,4)]*4)
    identity = encoded(x,x,[F(1,4)]*4)
    return {"target_thin":target,"source_thin":source,"rare_source":rare,
            "unresolved":unresolved,"isometry":identity}


def independent_check(data, record):
    need(all(type(v) in (int,str) for row in data["sources"]+data["targets"] for v in row)
         and all(type(v) in (int,str) for v in data["weights"])
         and type(data.get("variance",1)) in (int,str),"exact rational input")
    x = [list(map(F,z)) for z in data["sources"]]
    y = [list(map(F,z)) for z in data["targets"]]
    p = list(map(F,data["weights"]));s=F(data.get("variance",1))
    need(len(x)==len(y)==len(p)>0 and all(len(z)==3 for z in x+y),"input dimensions")
    need(s>0 and all(w>=0 for w in p) and sum(p)==1,"input probability and variance")
    keep=[i for i in range(len(p)) if p[i]]
    x,y,p=[[z[i] for i in keep] for z in (x,y,p)]
    need(record["schema"]=="covariance-collapse-v1" and record["active_sites"]==len(p),"schema and count")
    need(record["status"] in ("SIGNED_MIDDLE","ISOMETRIC_ZERO","UNRESOLVED"),"status")
    losses=[[distance2(x[i],x[j])-distance2(y[i],y[j])
             for j in range(len(p))] for i in range(len(p))]
    need(all(v>=0 for row in losses for v in row),"pair geometry")
    d=sum(p[i]*p[j]*losses[i][j] for i in range(len(p)) for j in range(len(p)))/s
    need(F(record["D"])==d,"mean loss")
    if record["status"]=="SIGNED_MIDDLE":
        need(d>0 and record["side"] in ("source","target"),"signed side and loss")
        need(record["margin_interval"]=="[1/64,1/2]"
             and record["signed_thresholds"]=="[1/64,infinity)","threshold intervals")
        need(len(record["direction"])==3
             and all(type(v) is int for v in record["direction"]),"integer direction")
        direction=list(map(F,record["direction"]))
        need(scalar(direction,direction)>0,"nonzero witness")
        cloud=x if record["side"]=="source" else y
        q=sum(p[i]*p[j]*(scalar(direction,cloud[i])-scalar(direction,cloud[j]))**2
              for i in range(len(p)) for j in range(len(p)))/(2*s*scalar(direction,direction))
        need(q==F(record["directional_variance"]),"directional variance")
        need(q<=d*d/F(2**86),"covariance guard")
        need(F(record["variance_cutoff"])==d*d/F(2**86),"claimed cutoff")
        need(F(record["middle_margin"])==d/F(2**42),"claimed margin")
        # Distance to the mean expressed solely through pair distances.
        pair_source=sum(p[i]*p[j]*distance2(x[i],x[j])
                        for i in range(len(p)) for j in range(len(p)))
        r2=max(sum(p[j]*distance2(x[i],x[j]) for j in range(len(p)))
               -pair_source/2 for i in range(len(p)))/s
        need(r2<=F(1,4) and F(record["source_radius_squared"])==r2,"radius")
    if record["status"]=="ISOMETRIC_ZERO":
        need(d==0,"isometry branch")
    Q=sum(p[i]*p[j]*(losses[i][j]/s)**2 for i in range(len(p)) for j in range(len(p)))
    affine_rank=rank([[1]+a+b for a,b in zip(x,y)])-1
    return {"D":str(d),"Q_over_D":str(Q/d) if d else None,
            "paired_affine_rank":affine_rank,"ordered_pairs":len(p)**2}


def checks():
    inputs=json.loads((ROOT/"INPUTS.json").read_text())
    for item in inputs:
        need(sha256((ROOT/item["relative_path"]).read_bytes()).hexdigest()==item["sha256"],
             "source pin "+item["relative_path"])
    k=F(1,2**40);eta=k/8
    core=F(4,45)*F(3,10)**4/F(3**18)
    need(core>k,"core rational margin")
    need(F(8,3)>F(64,25),"gradient enclosure")
    need(7*F(7,10)<F(128,25),"outer Gaussian sphere")
    need(F(441,25)<18,"product exponent")
    need(1-4*eta-eta*eta>=F(1,2),"projection loss budget")
    need(k/2-2*eta==F(1,2**42),"source sign margin")
    need(k-eta>=F(1,2**42),"target sign margin")
    need(F(5,4)>F(7,10),"high-noise overlap")
    need(sum(F(7,10)**j/F([1,1,2,6][j]) for j in range(4))>2,"log 2 bound")

    spectral=0;positive=0
    for diag in product([-1,0,1,2],repeat=3):
        for off in product([-1,0,1],repeat=3):
            M=[[diag[0],off[0],off[1]],[off[0],diag[1],off[2]],[off[1],off[2],diag[2]]]
            spd=(M[0][0]>0 and M[0][0]*M[1][1]-M[0][1]**2>0 and determinant(M)>0)
            v=nonpositive_direction(M)
            need((v is None)==spd,"Sylvester comparison")
            if v is not None:
                need(scalar(v,[scalar(row,v) for row in M])<=0 and any(v),"spectral witness")
            spectral+=1;positive+=spd
    # A positive semidefinite zero pivot after elimination, not a coordinate zero.
    v=nonpositive_direction([[1,1,0],[1,1,0],[0,0,1]])
    need(v==[1,-1,0],"singular rational witness")

    cases=fixtures();records={};stats={}
    for name,data in cases.items():
        rec=finite_guard(data);records[name]=rec
        stats[name]=independent_check(data,rec)
    for name,side in [("target_thin","target"),("source_thin","source"),("rare_source","source")]:
        need(records[name]["status"]=="SIGNED_MIDDLE" and records[name]["side"]==side,"signed branch")
        need(stats[name]["paired_affine_rank"]==6,"genuine paired rank six")
        need(F(stats[name]["D"])>F(1,2**360),"outside mean-loss guard")
        need(F(stats[name]["Q_over_D"])>F(1,2**48),"outside quartic guard")
    need(records["unresolved"]["status"]=="UNRESOLVED","honest failed guard")
    need(records["isometry"]["status"]=="ISOMETRIC_ZERO","exact equality")

    # A rational rotation makes the certificate direction non-coordinate.
    rotated=deepcopy(cases["target_thin"])
    for key in ["sources","targets"]:
        rotated[key]=[[str(F(3,5)*F(a)+F(4,5)*F(c)),str(F(b)),
                       str(-F(4,5)*F(a)+F(3,5)*F(c))] for a,b,c in rotated[key]]
    rec=finite_guard(rotated);independent_check(rotated,rec)
    need(rec["status"]=="SIGNED_MIDDLE" and sum(bool(v) for v in rec["direction"])>=2,"rotated witness")
    rotated_hash=sha256(json.dumps(rec,sort_keys=True).encode()).hexdigest()

    scaled=deepcopy(cases["source_thin"])
    for key in ["sources","targets"]:
        scaled[key]=[[str(4*F(v)+(7 if key=="sources" else -3)) for v in row] for row in scaled[key]]
    scaled["variance"]="16"
    need(finite_guard(scaled)==records["source_thin"],"scale and translation invariance")
    zero=deepcopy(cases["source_thin"])
    zero["sources"].append(["0","0","0"]);zero["targets"].append(["100","100","100"])
    zero["weights"].append("0")
    need(finite_guard(zero)==records["source_thin"],"zero mass handling")

    rejected=0
    broken_records=[]
    for key,value in [("direction",[1,0,0]),("direction",[0,0,0]),
                      ("middle_margin","1"),("directional_variance","0"),
                      ("side","unknown"),("signed_thresholds","[0,infinity)")]:
        rec=deepcopy(records["target_thin"]);rec[key]=value
        broken_records.append(rec)
    for rec in broken_records:
        try:independent_check(cases["target_thin"],rec)
        except ValueError:rejected+=1
        else:raise RuntimeError("corrupted certificate accepted")
    changes=[("variance",0),("weights",["-1"]+["1/16"]*15),
             ("weights",["1/16"]*15),("variance",1.0)]
    for key,value in changes:
        data=deepcopy(cases["target_thin"]);data[key]=value
        try:finite_guard(data)
        except ValueError:rejected+=1
        else:raise RuntimeError("invalid input accepted")
    expansion=encoded([[0,0,0],[0,0,0]],[[0,0,0],[1,0,0]],[F(1,2)]*2)
    try:finite_guard(expansion)
    except ValueError:rejected+=1
    else:raise RuntimeError("duplicate source expansion accepted")
    return {"status":"COVARIANCE_COLLAPSE_GUARD_PASS","pinned_sources":len(inputs),
            "core_rational_coefficient":str(core),"spectral_controls":spectral,
            "positive_definite_controls":positive,"rejected_inputs":rejected,
            "records":records,"definition_level_checks":stats,"rotated_record_sha256":rotated_hash}


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit",action="store_true")
    parser.add_argument("--write-fixtures",action="store_true")
    parser.add_argument("--input",help="rational finite input for a supplied certificate")
    parser.add_argument("--certificate",help="record to check by ordered-pair formulas")
    args=parser.parse_args()
    if args.input or args.certificate:
        if not(args.input and args.certificate) or args.emit or args.write_fixtures:
            parser.error("use --input and --certificate together, without other options")
        stats=independent_check(json.loads(Path(args.input).read_text()),
                                json.loads(Path(args.certificate).read_text()))
        print(json.dumps(dict(status="RECORD_CHECK_PASS",statistics=stats),sort_keys=True,indent=2))
    elif args.write_fixtures:
        print(json.dumps(fixtures(),sort_keys=True,indent=2))
    else:
        result=checks()
        if not args.emit:
            need(result==json.loads((ROOT/"EXPECTED.json").read_text()),"expected record")
        print(json.dumps(result,sort_keys=True,indent=2))
        if not args.emit:
            print("record_sha256",sha256(json.dumps(result,sort_keys=True,separators=(",",":")).encode()).hexdigest())
