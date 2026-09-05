# Sharp signature bound reduces the eleven-cycle branch to two cores

The eleven-cycle three-versus-eight branch now has **two remaining minority
cores**, with red offset words on pairs 01,02,12 equal to `100,110,110` or
`110,110,101` (classes 11 and 13). The former third core `100,100,100`
(class 8) has a full refutation replayed twice. The remaining two extensions
returned UNKNOWN at 60 seconds. Four-versus-seven remains open, and the
minimum moving count remains eleven. **No target graph or lower-bound gain
is claimed.**

The structural input is a solver-free lemma: for any three disjoint red
triangles in a graph with no monochromatic K5, at most nine outside vertices
uniformly attached to each triangle have nonempty red signatures. Equality
forces two copies of each singleton and one copy of each pair signature.
This abstract lemma uses no degree estimate or automorphism. It has sharp
19-vertex witnesses for all three inherited cores.

The [proof](PROOF.md) establishes the lemma, equality case, complete
normalization and formula bridge. The [preceding three-core cover](../ramsey_r55_order3_eleven_minority_core)
is an inherited computer-assisted dependency and still awaits independent
review. Its [parent eleven-cycle formula](../ramsey_r55_order3_eleven_cycle_obstruction)
has an [accepted independent review](../ramsey_r55_order3_eleven_cycle_obstruction_review1).
The new core-8 exclusion and the combined two-core conclusion have internal
validation and await independent review.

## Mathematical and computational evidence

For a chosen red triangle, its uniform red neighbors form a blue clique,
so number at most four. Each singleton signature occurs at most twice:
three such vertices and a blue edge between the other two triangles would
form a blue K5. Write X,Y,Z for the numbers of singleton, pair and triple
signatures, and I for total incidence. Then

```text
I = X+2Y+3Z <= 12,   X <= 6,
2(X+Y+Z) = I+X-Z <= 18.
```

Equality fixes the stated multiplicities. Also each oriented singleton/pair
sum `x_i+y_ij<=3`. Among ten fixed vertices at least one is therefore blue
to all nine minority vertices. Existing lexicographic ordering puts such
a vertex first, giving three necessary primary units.

There are 19448 ten-vertex signature count vectors. Exactly 928 satisfy the
basic inequalities and 778 also satisfy the singleton/pair cuts. These are
arithmetic profiles, not graph-realization counts. Independent composition
and sorted-signature enumeration agree. The compact [edge lists](core8.edges),
[core11.edges](core11.edges), and [core13.edges](core13.edges) attain the
nine-nonempty bound. Each has nineteen vertices; all five-sets, fixed
incidences, core orbit bits and all 171 action pairs are checked literally.
The fixed-to-fixed red edges are exactly the pairs of disjoint signatures.

The full formulas retain every parent clause and nine core units, then add
1623 primary consequences: three forced units, 360 singleton-triplet cuts
and 1260 four-vertex cuts. Each formula has 34268 variables and 617204
clauses. Full parent generation and independent C++ reconstruction precede
literal primary-orbit and complete-tail audits. Truth-table controls check
1536 singleton-cut and 24576 four-vertex-cut assignments.

| core | outcome | solve seconds | successful proof bytes |
|---:|---|---:|---:|
| 8 | excluded | 46.335606 | 49868240 |
| 11 | UNKNOWN, open | 60.243524 | — |
| 13 | UNKNOWN, open | 60.251670 | — |

The initial three-case run took 147.457911 seconds with two workers and
largest child peak RSS259516 KiB. The successful proof uses 821 RAT core
lemmas, so a RUP-only checker is insufficient. Fresh reconstruction of all
three complete formulas and a fresh full replay took 78.574414 seconds.
Four malformed formulas and three malformed fixtures were rejected. Normal
and optimized-Python controls match. Exact hashes and audits are in
[result.json](result.json), [verification_result.json](verification_result.json),
[controls_result.json](controls_result.json), and [fixture_report.json](fixture_report.json).

## Reproduction

Use Python 3.11.2 standard library, GCC 12.2.0, Kissat 4.0.4 and drat-trim.
The inherited C++ auditor builds with
`-std=c++17 -O2 -Wall -Wextra -Wpedantic -Werror`.
Kissat source: `8af8e56f174b778aef3aa45af9f739b2a5f492c2`.
DRAT source: `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`.
Source and binary hashes are pinned in `result.json`.

From this directory, choose fresh work directories outside Git:

```sh
python3 controls.py --work /scratch/r55-k11-signatures/controls
python3 -O controls.py --work /scratch/r55-k11-signatures/controls_O
cmp /scratch/r55-k11-signatures/controls/controls.json /scratch/r55-k11-signatures/controls_O/controls.json
python3 inspect_fixtures.py --fixtures . --report /scratch/r55-k11-signatures/fixtures.json
python3 run.py --work /scratch/r55-k11-signatures/full \
  --kissat /path/to/kissat --drat-trim /path/to/drat-trim \
  --solve-seconds 60 --replay-seconds 300
python3 verify.py --source-work /scratch/r55-k11-signatures/full \
  --work /scratch/r55-k11-signatures/verification \
  --drat-trim /path/to/drat-trim --replay-seconds 300
sha256sum -c SHA256SUMS
```

Expected output is summarized in [EXPECTED_OUTPUT](EXPECTED_OUTPUT).
Sharpness and arithmetic checks need no solver or omitted data. Full
exclusion reproduction regenerates the omitted trace. A changed proof
must pass replay against the exact audited formula; host-dependent timeout
changes do not establish an exclusion.

`run.py` saves atomic per-case checkpoints. A STOP file prevents further
cases starting while active cases finish. Resume requires an identical
contract and retains OPEN cases at their original bounds. Verification
always uses a fresh work directory. UNKNOWN traces are not resumable SAT
states. No equality-branch subdivision or new four-versus-seven search is
part of this milestone.

## Scope and trust

The nine-uniform-neighbor bound and equality case have the self-contained
counting proof. The full core-8 exclusion additionally uses the inherited
Ramsey formula, its justified relabeling/counter bridge and the degree
window from [R(4,5)=25](https://users.cecs.anu.edu.au/~bdm/papers/r45.pdf).
Reducing the entire branch to two cores also imports the preceding
fourteen-class cover and eleven exclusions. The lemma and its application
must not be assigned the same dependency boundary.

Large CNFs, the 49868240-byte successful DRAT trace, partial traces and logs
stay outside Git. Source regenerates them; reports and hashes alone are not
refutations. The proof is not formalized in a proof assistant. Runtime,
compiler/hardware, exact source and the external DRAT checker remain trust
boundaries. Internal validation does not constitute independent review.
