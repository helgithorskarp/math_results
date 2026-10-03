"""LATE full-entry correspondence only; imports author source explicitly."""
import argparse,importlib.util,sys
from independent import *
from reproduce import canonical_hash

def main():
    p=argparse.ArgumentParser();p.add_argument("native",type=Path);a=p.parse_args()
    # Optional validation, never imported by independent.py or reproduce.py.
    sys.path.insert(0,str(a.native.resolve()))
    spec=importlib.util.spec_from_file_location("native_reader",a.native/"check.py")
    native=importlib.util.module_from_spec(spec);spec.loader.exec_module(native)
    d=unique_json(a.native/"input.json");t=unique_json(a.native/"tiling.json")
    n=native.formula(d,t,2,1);m=build()
    require(n["universe"]==list(m["u"]),"all123 literal sites")
    require(clean(n["clauses"])==m["formula"],"entire2859 clause set")
    require(n["rows"]==[sorted(m["coefficients"][k].items())for k in m["order"]],"all520 integer rows")
    require([(matrix(list(v[1])),tuple(v[2]))for v in n["frames"]]==m["maps"],"all19 physical maps")
    dimacs=("p cnf 643 2859\n"+"".join(" ".join(map(str,c))+" 0\n"for c in sorted(tuple(sorted(c))for c in m["formula"]))).encode()
    require(hashlib.sha256(dimacs).hexdigest()==n["formula_sha256"],"complete native DIMACS serialization")
    result={"whole_123_site_list":True,"whole_2859_clause_set":True,"whole_520_integer_rows":True,
            "whole_19_physical_maps":True,"whole_native_DIMACS_sha256":n["formula_sha256"],
            "scope":"Late correspondence, not a second independent proof"}
    print(json.dumps(result,sort_keys=True))

if __name__=="__main__":main()
