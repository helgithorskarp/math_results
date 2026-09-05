# Independent M=214 formulation audit and structural-route decision

The complete normalized M=214 OPB formula was reproduced byte-for-byte and
independently checked by interpreting its variable supports and Boolean
semantics. The displayed reduction below confirms its equivalence to the
whole M=214 hard branch, conditional on the previously reviewed local-extremal
data. **No SAT/UNSAT search or verdict is supplied.**

As a separating test, the published scalar pseudomodel was reconstructed and
anchor-normalized. It violates **all 43 local triangle equalities** and
**2,029 five-set rows** (1,829 red K5s and 200 blue K5s), although it satisfies
all degree, exceptional-incidence, anchor, and triangle-definition rows.
Thus aggregate feasibility and feasibility of this complete graph encoding
are genuinely different checkpoints. This is not an objection to the
pseudomodel, whose author explicitly states that it is not a Ramsey graph.

## Inputs and provenance

The independently authored source being audited is
[the complete formulation](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m214_complete_formulation),
at commit `fdba2d1000599987d545d0b83f44c46084a73b19`.
Its Discovery Net artifact is
`bafkreiagndv4xnzopsniccepuxbe6zmca5hm5tyqb7bh2epm6polwfc4bm`
(height 2505). The seven source files were obtained from that exact commit;
all six entries in its `SHA256SUMS` verified.

The separate test input is the JSON certificate in
[the scalar relaxation](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m214_scalar_relaxation),
at commit `7205fe40e336de80aec92ef998411a3302065d12`:
`PSEUDOMODEL.json`, SHA-256
`e59a33cf352645528217125b3cae0e65a1a10dcbcc0ff8795e544ad964a5a550`.
Its graph artifact is
`bafkreicz45fiwsc3lkgyerjr3mdrlrujglobppt2fqk3n7duhmrzyk5scu`
(height 2511). We independently reconstruct its graph fixture, not its entire
aggregate-relaxation checker. Its reported 4,043 union cuts are background
context, not a new independently replayed claim in this directory.

## 1. An independent short reduction

Write `t_R(v)` and `t_B(v)` for the edge counts in the red and blue
color-neighborhoods of a vertex. The hard branch means all 86 local
deficiencies from the corresponding `(4,5)` maxima `U` are at least seven.
Use the previously reviewed
[local-extremal identity](../ramsey_r55_local_extremal_deficiency/README.md):

```text
18 <= d(v) <= 24,
2 Delta = 1247 - W,
W = 21(x18+x24) + 12(x19+x23) + 3(x20+x22) <= 39.
```

The last bound follows from `Delta>=602`, divisibility of `W` by three,
and oddness of `W`. At a doubly exact degree-21 anchor the cross total is
`M=m-231`; hence `M=214` means `m=445`.

Put `epsilon_v=d(v)-21`. Each summand of `W` is at least
`3|epsilon_v|`, whereas `sum epsilon_v=890-903=-13`. Therefore

```text
39 >= W >= 3 sum |epsilon_v| >= 3 |sum epsilon_v| = 39.
```

Equality forces every deviation to be nonpositive and every degree to be
20 or 21. Thus the unique profile is `20^13 21^30`, without enumerating
integer profiles. Also `W=39`, `Delta=604`, leaving two units above the
baseline `86*7`.

The red local upper bounds in this branch are 93 at degree 20 and 100 at
degree 21. Their sum is `13*93+30*100=4209`. The actual sum is a multiple
of three, since each red triangle is counted at its three vertices. Subtracting
at most two units can preserve divisibility only if none are subtracted.
Consequently **every red local bound is exact** and there are 1,403 red
triangles. Both excess deficiency units are blue.

Let `E` be the 13 degree-20 vertices and put `a_v=|N_R(v) intersect E|`.
For any graph the elementary identity is

```text
t_R(v)+t_B(v) = choose(42-d(v),2) - m + sum_(w in N_R(v)) d(w).
```

Indeed, writing `A=N_R(v), B=N_B(v)`, the two edge counts give
`m=d(v)+t_R(v)+e_R(A,B)+e_R(B)` and
`sum_A d=d(v)+2t_R(v)+e_R(A,B)`. Eliminating the cross count proves the
identity. For the profile above the right side is `206-a_v`. Therefore

```text
d(v)=20: t_B(v)=113-a_v <= U(22)-7=107 iff a_v>=6;
d(v)=21: t_B(v)=106-a_v <= U(21)-7=100 iff a_v>=6.
```

Now `sum_v a_v=13*20=260=43*6+2`, so at most two vertices have `a_v>6`.
At least 28 of the 30 degree-21 vertices are doubly exact anchors. Select
one and label it 13. Relabel its six red neighbors in E as 0 through 5 and
its fifteen red neighbors in the other class as 14 through 28. This is an
existential relabeling within intrinsic degree classes, **not an assumed
automorphism or a selected pair of internal cores**.

Conversely, the formula's two constraints for every five-set forbid both
monochromatic K5s, its triangle gates define the actual red triangle bits,
and its degree/local rows give precisely the profile and red equalities above.
Its `a_v>=6` rows give the remaining blue hard-branch inequalities. At
normalized anchor 13 the red neighborhood A spans 100 red edges and the
blue neighborhood B spans `choose(21,2)-100=110` red edges. Hence the cross
total is `445-21-100-110=214`. All models belong to the branch; every graph
in the branch can be normalized to a model. Triangle bits are uniquely
determined by edge bits.

The imported maxima, especially `U(20)=100,U(21)=107,U(22)=114`, retain
their catalog-completeness trust boundary. This audit does not rerun those
catalogs or formalize the displayed proof.

## 2. Full-stream semantic check

[audit_semantics.py](audit_semantics.py) imports no code from either upstream
checker or generator. It parses actual coefficients, variables, relations,
and thresholds in the OPB file. Its checks differ from regenerating canonical
text:

| Row family | Rows | Independent coverage test |
|---|---:|---|
| Five-set clauses | 1,925,196 | Decode endpoints; ten distinct edges on five vertices; colex subset rank and two-color coverage bitmap |
| Triangle gates | 49,364 | Decode triangle and edge supports; cover its three upper gates and one lower gate |
| Degrees | 43 | Recover the common endpoint of each complete 42-edge star |
| Local triangle counts | 43 | Recover the common vertex of each full 861-triangle slice |
| Exceptional incidences | 43 | Decode the exact neighbor set `E minus {v}` |
| Anchor incidences | 42 | Cover each edge at vertex 13 with the required polarity |

Support checks are independent of row ordering within each family; the final
hash additionally pins the original canonical ordering. Duplicate variables,
duplicate obligations, missing obligations, malformed thresholds, trailing
data, and invalid variable indices are rejected. The header's 128 equalities
and all 1,974,731 rows are checked. Ten negative tests and exhaustive truth
tables for the five-set predicate (1,024 assignments) and triangle gadget
(16 assignments) run on every invocation. Checks use explicit exceptions,
not removable Python assertions.

Canonical formula:

```text
variables: 13,244 = 903 edges + 12,341 red triangles
constraints: 1,974,731; equalities: 128
bytes: 167,913,049
SHA256: 88aa294709836a0a707b2203da2176d420a3608353db21cc741dfa9bedf89a58
```

The source arithmetic audit, Python generator, and C++ full-stream checker
also passed on this host. The C++ checker passed AddressSanitizer and
UndefinedBehaviorSanitizer on the entire file. Our semantic checker passed
both normal Python and `python3 -O`, producing identical reports.

## 3. A concrete separation from scalar feasibility

The scalar certificate supplies a 13-vertex Paley exceptional core, 30
exceptional signatures, and a cyclic 30-vertex central graph with one deleted
edge. Its degree graph realizes `20^13 21^30`, but its assigned local counts
are not the graph's induced-edge counts.

Our checker reconstructs this graph directly from the pinned JSON, chooses
its first size-six central signature as anchor, and performs the complete
relabeling above. Actual edge and triangle bits are then evaluated against
**every parsed OPB row**. Separately, a bitset clique enumerator counts its
monochromatic five-sets, and direct induced-neighborhood edge counts check
the local failures. The two evaluations agree:

```text
red K5s: 1829; blue K5s: 200
local red equalities violated: 43
all other OPB row families: 0 violations
actual red triangles: 1501; assigned scalar red triangles: 1403
actual blue triangles: 1365; assigned scalar blue triangles: 1463
```

The full label map and literal witnesses are in [report.json](report.json).
For example, normalized vertices `0,1,3,13,14` form a red K5, and
`0,2,5,16,22` form a blue K5. This single fixture does not show that the
M=214 branch is feasible or infeasible, nor that any further particular
aggregate cut would be insufficient.

## 4. Decision and next boundary

The prepublication refresh at Discovery Net height 2526 found the teammate's
concurrent [M=214 symmetry audit](../ramsey_r55_m214_symmetry_audit/README.md),
commit `4223c60451ab4e146e1e6d44e5d22776be9e0729`, which also independently
checks the OPB. The overlapping work here is explicitly a reproduction, not
a new formulation or a claim of priority for its semantic checks. This
directory additionally gives the weight-equality proof of the unique degree
profile and the normalized scalar-fixture separation test. It does not
review or duplicate the teammate's new order-three symmetry lemma.

Retain the audited whole-M=214 formula as a complete, symmetry-free backend
and exact regression target. A future affirmative verdict must decode and
directly check the 903-edge graph; a negative verdict needs a terminal proof
independently replayed against the pinned formula. Reproducing the author's
no-conclusion solver calibration would not supply either, so no solver run
or installation was initiated in this pass.

Do not replace the productive structural route with an open-ended OPB search.
Our current [paired-neighborhood frontier](../ramsey_r55_paired_neighborhood_budget/README.md)
is a **different stratum**, `M=217`, profile `19^2 20^3 21^38`. It leaves
seven central-incidence patterns (five relabeling classes), with two common
neighbors and an eight-vertex cell. These already couple actual shared edge
budgets; their aggregate witnesses are still not graph realizations. The
next pass should test further simultaneous cell-edge/local-triangle
compatibility there, using the reviewed degree-19 machinery. No M=217
pattern was excluded in this audit. The inherited cumulative 67 profiles
and 273 anchored splits are unchanged and were not recounted here.

This is the requested bounded reproduction/decision checkpoint, not the
start of another radius, stratum, or symmetry phase. No target graph or
improved Ramsey bound has been established.

## Reproduction

Run from this directory. Tested with Python 3.11.2, Git, and Debian
g++ 12.2.0, using only Python's standard library. Git downloads are external
inputs; the exact commits and certificate/file hashes are pinned above.

```bash
r55_repro_dir=$(mktemp -d)
git clone --filter=blob:none --depth 1 --sparse \
  https://github.com/njallskarp/math_source_code_open.git "$r55_repro_dir/source"
git -C "$r55_repro_dir/source" sparse-checkout set ramsey_r55_m214_complete_formulation
git -C "$r55_repro_dir/source" fetch --depth 1 origin fdba2d1000599987d545d0b83f44c46084a73b19
git -C "$r55_repro_dir/source" checkout --detach fdba2d1000599987d545d0b83f44c46084a73b19
git -C "$r55_repro_dir/source" fetch --depth 1 origin 7205fe40e336de80aec92ef998411a3302065d12
r55_source_dir="$r55_repro_dir/source/ramsey_r55_m214_complete_formulation"
(cd "$r55_source_dir" && sha256sum -c SHA256SUMS)
python3 "$r55_source_dir/audit_reduction.py"
python3 "$r55_source_dir/generate_opb.py" --output "$r55_repro_dir/formula.opb"
g++ -std=c++20 -O2 -Wall -Wextra -Wpedantic -Werror \
  "$r55_source_dir/check_opb.cpp" -o "$r55_repro_dir/check_opb"
"$r55_repro_dir/check_opb" "$r55_repro_dir/formula.opb"
python3 audit_semantics.py --opb "$r55_repro_dir/formula.opb" \
  --source-repository "$r55_repro_dir/source" --report "$r55_repro_dir/report.json"
cmp report.json "$r55_repro_dir/report.json"
```

Compare semantic-checker stdout with [EXPECTED_OUTPUT.txt](EXPECTED_OUTPUT.txt).
For the additional tests, repeat the last Python command with `python3 -O`;
compile the upstream C++ checker using `-O1 -g -fsanitize=address,undefined
-fno-omit-frame-pointer` instead of `-O2` and replay the full formula.
Upstream source checks must run without Python optimization, because they
use assertions. Allow about two minutes and 0.3 GB of scratch disk for the
core replay; the generated OPB and binaries are intentionally not committed.

Trust: the displayed unformalized reduction, inherited local-extremal data,
the shared documented variable convention, exact Python integer operations,
the compiler/runtime/hardware, Git input retrieval, and SHA-256. Independent
support-based parsing reduces common implementation error; it does not
eliminate these boundaries or constitute a formal proof. Source publication
is not itself a satisfiability certificate.
