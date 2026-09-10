# A global point-link bridge for `C(13,7,5)`

This directory gives an exact two-case reduction for the remaining frontier

\[
77 \le C(13,7,5) \le 78.
\]

Unlike the earlier fixed-link symmetry certificates, the reduction covers
every hypothetical 77-block design, including asymmetric designs and designs
whose optimal point link is not the archived 41-block example.  It reduces
existence to one canonical `e0` formula and twelve canonical `e1` formulas.
Those formulas remain open: this artifact is a structural reduction and
exhaustive case interface, not a nonexistence certificate.

The exact values and uniqueness input are from C. Krug, *The covering number
`C(12,6,4)` is 41*, [arXiv:2607.23766](https://arxiv.org/abs/2607.23766).
The representative 41-block link is the previously published
[`cover_41.txt`](../covering_c1375_fixed_link_symmetry/cover_41.txt), copied
from the public proof package
[dennisonbertram/covering-number-c12-6-4](https://github.com/dennisonbertram/covering-number-c12-6-4).

## First global restriction: optimal-link degree profiles

Let `L` be any 41-block `C(12,6,4)` cover.  Write its point degrees as

\[
d_L(i)=20+a_i.
\]

The value `C(11,5,3)=20` gives `a_i >= 0`, and incidence counting gives
`sum(a_i)=41*6-12*20=6`.  Write pair degrees as

\[
d_L(ij)=9+q_{ij}.
\]

Here `q_ij >= 0` because `C(10,4,2)=9`.  A second incidence count gives

\[
\sum_{i<j}q_{ij}=41\binom{6}{2}-66\cdot9=21
\]

and, at every point,

\[
\sum_{j\ne i}q_{ij}=5(20+a_i)-11\cdot9=1+5a_i.
\]

The left side is the incident weight at `i` in a nonnegative weighted graph
of total edge weight 21, so it is at most 21.  Therefore `a_i <= 4` for every
point.  In particular the degree-excess profiles `6` and `5+1` are impossible
for every optimal link; only nine integer partitions of six remain.

## The nested point-pair bridge

Suppose a 77-block `C(13,7,5)` cover `D` exists.  Every point has degree at
least 41, while

\[
\sum_x(d_D(x)-41)=77\cdot7-13\cdot41=6.
\]

Choose a degree-41 point `0`.  Its link is an optimal 41-block
`C(12,6,4)` cover.  At least six points of this link have degree exactly 20,
because its link-degree excess also sums to six.

There are two exhaustive cases.

### Case `e0`

Some pair of degree-41 points occurs in exactly 20 blocks.  Label the pair
`{0,1}`.  The 20 blocks through both points, with the pair deleted, form an
optimal 20-block `C(11,5,3)` cover.  Krug's certified uniqueness theorem lets
us fix this second link to one canonical representative without loss of
generality.

The other blocks split into

| category | contains | exact count |
| --- | --- | ---: |
| `A` | both `0,1` | 20, fixed |
| `B` | `0` but not `1` | 21 |
| `C` | `1` but not `0` | 21 |
| `D` | neither | 15 |

### Case `e1`

No pair of degree-41 points occurs in exactly 20 blocks.  Fix any degree-41
point `0`.  Every link-degree-20 neighbour of `0` then has positive full
degree excess.  There are at least six such neighbours but only six excess
units in total.  Consequently there are exactly six, all have full degree 42,
and the remaining six neighbours have link excess one and full degree 41.
Thus the full point-degree sequence is

\[
41^7,42^6.
\]

For a degree-41 point, the total incident pair excess above 20 is
`6*41-12*20=6`.  Since it has six other degree-41 neighbours and no such pair
has multiplicity 20, those six pairs all have multiplicity 21 and every
cross-pair has multiplicity 20.

Choose `1` among the six degree-42 neighbours of `0`.  Again `d_D(01)=20`, so
the same unique second link can be fixed.  The category counts are now

| category | exact count |
| --- | ---: |
| `A` | 20, fixed |
| `B` | 21 |
| `C` | 22 |
| `D` | 14 |

The six degree-41 points other than `0` form a six-subset of the remaining
eleven points.  The canonical second link has automorphism group 240.
Exhaustive standard-library backtracking first enumerates a
pair-multiplicity-preserving supergroup and then checks every candidate on the
full 20-block family.  Its action partitions all 462 six-subsets into exactly
12 orbits; the representatives and orbit sizes are in
[`EXPECTED_SECOND_LINK_ORBITS.txt`](EXPECTED_SECOND_LINK_ORBITS.txt).

Hence one `e0` formula and the twelve `e1` orbit formulas cover every possible
77-block design.

## Exact encoding

The 20 `A` blocks are fixed.  The primary variables are

- 462 category-`B` blocks `{0}` plus a six-subset of points `2,...,12`;
- 462 category-`C` blocks `{1}` plus such a six-subset; and
- 330 category-`D` seven-subsets of points `2,...,12`.

For every five-subset not already covered by `A`, the generator adds the
complete clause of primary blocks containing it.  It then adds the exact
category counts.  These conditions alone are necessary and sufficient for a
77-block completion of the fixed second link.

The `e1` formulas additionally impose the proved full point and pair
multiplicities.  Optional shadow constraints impose, for every subset `S` of
size at most four,

\[
d_D(S)\ge 41,20,9,3
\]

respectively.  These follow from the covering numbers of the corresponding
links and do not change the solution set.

`GLOBAL_BRIDGE_MANIFEST.tsv` records exact hashes and dimensions for an `e0`
instance with point shadows and the twelve hard-`e1` instances.  Generated
CNFs are 5–28 MB each and are intentionally omitted from GitHub.  Every status
in the manifest is `OPEN`; bounded CaDiCaL/Kissat experiments produced no
verdict, and no timeout is treated as mathematical evidence.

## Reproduction

The recorded run used Python 3.11.2 and `python-sat` 1.9.dev15 with `pypblib`
0.0.4.

```sh
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -r requirements.txt

LINK=../covering_c1375_fixed_link_symmetry/cover_41.txt
python3 global_point_link_bridge.py self-test "$LINK"
python3 global_point_link_bridge.py orbits "$LINK" \
  | diff -u EXPECTED_SECOND_LINK_ORBITS.txt -

python3 global_point_link_bridge.py generate "$LINK" build/e0.cnf \
  --case e0 --max-shadow 1
python3 global_point_link_bridge.py generate "$LINK" build/e1-orbit0.cnf \
  --case e1 --high-set 2 3 4 5 6 7
```

Repeat the final command with the other eleven representatives in the orbit
table.  The outputs must match `GLOBAL_BRIDGE_MANIFEST.tsv` byte for byte.
A future satisfying model can be checked directly against the covering
definition and the applicable hard-case degrees using `check-model`.

## Trust boundary and next step

The counting reduction is ordinary mathematics.  Fixing the second link uses
Krug's certified uniqueness theorem for optimal `C(11,5,3)` covers.  The group
and orbit enumeration uses exact Python integers and exhaustive backtracking.
CNF generation additionally trusts PySAT/pypblib's PB translation; the script
truth-table checks the encodings on all assignments for small instances.
There is currently no UNSAT certificate and no claim that either global case
is impossible.

The next completion-aware milestone is to enumerate the 21-block category-`B`
extensions of the canonical second link modulo its order-240 automorphism
group, immediately testing each canonical optimal link against the coupled
`C,D` completion constraints.  This attacks admissible optimal links
exhaustively and uses the earlier fixed-link symmetry certificates only as
validation fixtures.
