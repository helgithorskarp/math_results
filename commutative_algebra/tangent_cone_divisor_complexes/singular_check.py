#!/usr/bin/env python3
"""Independent presentation/resolution check. Requires Singular 4.3.1 or later.

Eliminate t from (x_i-t^n_i), compute a local standard basis and its initial
forms using tangentcone, then compute a minimal homogeneous free resolution.
No factorization-order data or simplicial boundary matrices are sent to Singular.
"""
import argparse
import hashlib
import json
import re
import subprocess

from betti import fine_betti, graded_betti
from verify import corpus


def program(g, p, case):
    e = len(g)
    xs = [f"x{i}" for i in range(e)]
    names = ",".join(xs)
    ideal = ",".join(f"{x}-t^{n}" for x, n in zip(xs, g))
    weights = ",".join(map(str, g))
    return f'''
ring E={p},(t,{names}),lp;
ideal J={ideal};
ideal T=eliminate(J,t);
ring R={p},({names}),dp;
ideal I=imap(E,T);
ideal C=tangentcone(I);
resolution F=mres(C,0);
intmat B=betti(F);
int r,c;
for(r=1;r<=nrows(B);r++) {{
  for(c=1;c<=ncols(B);c++) {{
    if(B[r,c]!=0) {{
      print("B {case} "+string(c-1)+" "+string(r+c-2)+" "+string(B[r,c]));
    }}
  }}
}}
intvec W={weights};
intvec oldS=0;
intvec oldJ=0;
intvec ns,nj;
int h,good,ss,jj;
poly pp;
print("F {case} 0 0 0");
for(h=1;h<=size(F);h++) {{
  module M=F[h]; matrix A=M; ns=0; nj=0;
  for(c=1;c<=ncols(A);c++) {{
    good=0;
    for(r=1;r<=nrows(A);r++) {{
      pp=A[r,c];
      while(pp!=0) {{
        ss=deg(lead(pp),W)+oldS[r]; jj=deg(lead(pp))+oldJ[r];
        if(good==0) {{ns[c]=ss;nj[c]=jj;good=1;}}
        else {{if(ns[c]!=ss or nj[c]!=jj) {{print("ERROR: nonhomogeneous resolution");}}}}
        pp=pp-lead(pp);
      }}
    }}
    if(good) {{print("F {case} "+string(h)+" "+string(ns[c])+" "+string(nj[c]));}}
  }}
  oldS=ns;oldJ=nj;kill M,A;
}}
print("DONE {case}");
kill E,R;
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--singular", default="Singular")
    args = parser.parse_args()
    cases = [(g, p) for g in corpus() for p in (0, 2, 3)]
    script = 'LIB "sing.lib";\n' + "\n".join(program(g, p, c) for c, (g, p) in enumerate(cases)) + "\nquit;\n"
    run = subprocess.run([args.singular, "-q"], input=script, text=True,
                         capture_output=True, check=True, timeout=600)
    if "?" in run.stdout or "ERROR" in run.stdout or "error" in run.stderr.lower():
        raise RuntimeError(run.stdout + run.stderr)
    seen = {i: {} for i in range(len(cases))}
    fine_seen = {i: {} for i in range(len(cases))}
    done = set()
    for line in run.stdout.splitlines():
        if m := re.fullmatch(r"B (\d+) (\d+) (\d+) (\d+)", line.strip()):
            case, i, j, value = map(int, m.groups())
            assert (i, j) not in seen[case]
            seen[case][i, j] = value
        if m := re.fullmatch(r"F (\d+) (\d+) (\d+) (\d+)", line.strip()):
            case, i, s, j = map(int, m.groups())
            key = (i, s, j)
            fine_seen[case][key] = fine_seen[case].get(key, 0) + 1
        if m := re.fullmatch(r"DONE (\d+)", line.strip()):
            case = int(m[1])
            assert case not in done
            done.add(case)
    assert done == set(seen), "missing Singular cases"
    records = []
    for i, (g, p) in enumerate(cases):
        expected_fine = fine_betti(g, p)
        expected = graded_betti(expected_fine)
        assert seen[i] == expected, (g, p, seen[i], expected)
        assert fine_seen[i] == expected_fine, (g, p, fine_seen[i], expected_fine)
        records.append([list(g), p, [[a, b, c, d] for (a, b, c), d in sorted(fine_seen[i].items())]])
    data = json.dumps(records, separators=(",", ":")).encode()
    print(json.dumps({"tables": len(cases), "fine_entrywise_matches": len(cases),
                      "tables_sha256": hashlib.sha256(data).hexdigest(),
                      "checks": "PASS"}, sort_keys=True))


if __name__ == "__main__":
    main()
