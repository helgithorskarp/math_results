"""Root-certificate rejections, complete-cover rejections, tiny truth tables."""
import copy
import itertools
import json
import sys
from pathlib import Path
import verify

HERE = Path(__file__).parent


def main():
    colors,K,_ = verify.premise()
    docs = [json.loads((HERE / f"roots/{v}.json").read_text()) for v in (1004,1327,1650,1973)]
    baseline = verify.check_all(documents=docs)
    original = docs[0]
    mutations = []
    def add(name,fn):
        d=copy.deepcopy(original);fn(d);mutations.append((name,d))
    add("missing_caps",lambda d:d.pop("caps"))
    add("larger_class_cap",lambda d:d.update(caps=[197,198]))
    add("boolean_cap",lambda d:d.update(caps=[True,197]))
    add("wrong_phase",lambda d:d.update(phase=184))
    add("boolean_root",lambda d:d.update(root=True))
    add("out_of_range_root",lambda d:d.update(root=3704))
    add("fixed_trial_root",lambda d:d.update(root=35))
    add("wrong_original_class_root",lambda d:d.update(root=next(x for x,c in enumerate(colors) if c==1)))
    add("wrong_low_load_dependency",lambda d:d.update(low_certificate_sha256="0"*64))
    add("hidden_initial_edit",lambda d:d.update(other_trial=1327))
    add("hidden_fixed_colors",lambda d:d.update(fixed_colors={"1":1}))
    add("zero_denominator",lambda d:d.update(denominator=0))
    add("boolean_denominator",lambda d:d.update(denominator=True))
    add("capacity_overflow",lambda d:d.update(denominator=1))
    add("no_strict_gap",lambda d:d.update(denominator=2_000_000))
    add("zero_AP_step",lambda d:d["AP_weights"][0].__setitem__(1,0))
    add("out_of_range_AP",lambda d:d["AP_weights"][0].__setitem__(0,3704))
    add("zero_AP_weight",lambda d:d["AP_weights"][0].__setitem__(2,0))
    add("boolean_AP_weight",lambda d:d["AP_weights"][0].__setitem__(2,True))
    add("negative_AP_weight",lambda d:d["AP_weights"][0].__setitem__(2,-1))
    add("duplicate_AP",lambda d:d["AP_weights"].append(d["AP_weights"][0][:]))
    add("unnecessary_AP",lambda d:d["AP_weights"].__setitem__(0,[0,1,1]))
    add("zero_triple_weight",lambda d:d["cover2_weights"][0].__setitem__(1,0))
    add("duplicate_triple",lambda d:d["cover2_weights"].append(copy.deepcopy(d["cover2_weights"][0])))
    add("repeated_triple_AP",lambda d:d["cover2_weights"][0][0].__setitem__(1,d["cover2_weights"][0][0][0][:]))
    add("surcharge_on_fixed_point",lambda d:d["surcharges"].append([next(iter(K[1])),1]))
    add("negative_surcharge",lambda d:d["surcharges"].append([next(x for x,c in enumerate(colors) if c==1 and x not in K[1]),-1]))
    add("no_positive_proof",lambda d:d.update(AP_weights=[],cover2_weights=[],surcharges=[]))
    # Change only the trial hypothesis: a weighted six-point row formerly
    # activated at1004 is then unjustified. The actual-AP checker must notice.
    add("wrong_trial_for_activated_APs",lambda d:d.update(root=1327))
    common = {}
    for a,s,w in original["AP_weights"]:
        points={a+j*s for j in range(7)}
        if not all(colors[x]==1 for x in points):continue
        for x in points-K[1]:common.setdefault(x,[]).append([a,s])
    triple = next(rows[:3] for rows in common.values() if len(rows)>=3)
    add("triple_with_permitted_common_point",lambda d:d["cover2_weights"][0].__setitem__(0,triple))
    rejected=[]
    for name,d in mutations:
        try:verify.check_root(d,colors,K)
        except (ValueError,KeyError,TypeError):rejected.append(name)
        else:raise ValueError("Accepted corrupted root: "+name)
    covers=[("missing_root",docs[:-1]),("duplicate_root",docs[:-1]+[docs[0]]),
            ("extra_root",docs+[docs[0]])]
    for name,changed in covers:
        try:verify.check_all(documents=changed)
        except (ValueError,KeyError,TypeError):rejected.append(name)
        else:raise ValueError("Accepted incomplete/extra anchor cover: "+name)
    # Tiny direct enumeration independently checks the two logical bridges.
    activated_cases=0
    for flips in itertools.product((0,1),repeat=6):
        resulting=[1]+[1-e for e in flips]
        avoids=not all(c==resulting[0] for c in resulting)
        verify.need(avoids == any(flips),"Activated six-term truth table")
        activated_cases+=1
    anchor_cases=0
    for flips in itertools.product((0,1),repeat=4):
        resulting=[0,0,0]+list(flips)
        avoids=not all(c==resulting[0] for c in resulting)
        verify.need(avoids == any(flips),"Four-root anchor truth table")
        anchor_cases+=1
    verify.need(verify.check_all(documents=docs)==baseline,"Controls mutated frozen documents")
    print(json.dumps({"agent":"six-vdw-3","role":"researcher","all_rejected":True,
                      "python_optimization":sys.flags.optimize,
                      "rejected_controls":len(rejected),"names":rejected,
                      "activated_truth_table_cases":activated_cases,"anchor_truth_table_cases":anchor_cases}))


if __name__=="__main__":main()
