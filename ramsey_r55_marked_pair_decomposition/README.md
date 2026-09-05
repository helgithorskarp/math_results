# Five maximal attachments and an exact 100-case marked-core decomposition

For the specific O22 graph from
[the opposite-neighborhood realization](../ramsey_r55_opposite22_realization),
the largest induced red-K4-free set has **14 vertices**, and there are exactly
five such 14-sets. Thus every vertex added to O in any Ramsey(5,5) supergraph
has at most 14 red neighbors in O. This excludes all gluings of the fixed
H20/O22 pair in which the marked H20 vertex of internal red degree 5 has
total red degree at least 21: its degree is at most `5+1+14=20`.

For the selected marked-degree/coverage scope, the 44 cross-incidences of
the two marked H vertices have exactly **100 possible assignments**. This
package provides the complete, disjoint case list and a checked selector
encoding, not merely a survivor count. Each case fixes those 44 incidences
and leaves the other **396 cross-edges** for the full gluing problem.

No full gluing was tested here. The 100 cases are actual valid **25-vertex
local graphs**, not 43-vertex solutions or proven extendible cases. No global
profile exclusion, general H20/O22 incompatibility, or Ramsey-number bound
improvement is claimed. No further monolithic solve was run.

## Input and scope

The fixed O has 22 vertices, 124 red / 107 blue edges, no red K5 and no blue
K4. Its source is `ramsey_r55_opposite22_realization/GRAPH.json` at commit
`2396381c98135e7819becd092627006262891d67`, Discovery Net height 3026,
`bafkreichit22jd3pb3olz2n6dgyjcn6wbbzaexgjbysuoehijgad4makva`.
Both programs pin its SHA-256:
`e7f6086e6f99edcf47f5f931106bdfc294703e9a74aa8eb1caad60978917f355`.
They recheck its clique conditions; no external refutation or numerical
Ramsey theorem is imported. Only the selected O is analyzed, not the other
15 successful deletions in its parent construction.

Adjoin a red triangle `r,a,b`, with r blue to all O. Write S0 and S1 for
the red neighborhoods of a and b inside O. The marked subproblem imposes

```
|S0| = 12,  |S1| = 14,  S0 union S1 = O.
```

The union condition is an **explicit hypothesis of this selected scope**,
not a consequence asserted for arbitrary Ramsey graphs. It implies
`|S0 intersection S1|=4`, hence only-first / only-second / both classes of
sizes 8 / 10 / 4. No partition of the labeled O graph is arbitrarily fixed.

In the existing marked
[H20 realization](../ramsey_r55_root20_anchor_realization), source
`3e20c2a890f21b5224fb55effbb9964a9ac33f4b`, a and b are local H0,H1, of
internal red degrees 7 and 5. Root r is red to all H. Consequently total red
degrees 20 at a,b require cross-degrees 12,14. That H graph and its affine
handoff have an [accepted independent review](../ramsey_r55_root20_anchor_realization_review1),
source `c5b252742f3157bc5adb9a9c278a7816dce03b20`. The five-maximizer theorem
uses only O; the degree-20 consequence additionally uses these H incidences.

## Exact local criterion and finite proof

The graph on `r,a,b,O` is Ramsey(5,5) if and only if

1. O[S0] and O[S1] contain no red K4;
2. O[S0 intersection S1] contains no red triangle.

A red K5 using one of a,b needs four O vertices in its red neighborhood;
one using both needs three in their common red neighborhood. A blue K5
using one is impossible because O has no blue K4, and one using both is
impossible because ab is red. Root-containing mixed five-sets have opposite
root incidences; r plus four O is safe by O's blue-K4-free condition. The
remaining five-sets lie in O. This proves both directions, even before
the sizes and union condition are imposed.

The producer computes the red clique number w(S) for all 2^22 subsets by

```
w(empty)=0,
w(S)=max(w(S minus {v}), 1+w((S minus {v}) intersection N_red(v))),
```

where v is the least element of S. Subsets with w(S)<=3 are precisely the
red-K4-free sets. There are 6,212 of size 12, five of size 14, and none of
size 15 or larger. The five maximizers are shown below. Masks are hexadecimal,
with bit v indicating local O vertex v; leading zeroes are significant only
for the six-digit serialization, not for the represented subset.

| S1 mask | Locally valid marked pairs using S1 |
|---|---:|
| `1276fe` | 0 |
| `127ede` | 20 |
| `29bb79` | 30 |
| `39ab79` | 35 |
| `3e363e` | 15 |

The degree/coverage hypotheses initially allow
`C(22,4) C(18,8)=320,089,770` ordered pairs. Joining the two exact red-K4-free
domains leaves 103 cover pairs. Three fail the common-neighborhood condition:
S1 is `39ab79`, and S0 is `165cce`, `1674ce` or `3654ce`. In each, the common
set contains the literal red triangle `{3,6,20}`. Thus exactly 100 remain.
No isomorphism quotient is taken.

[cases.json](cases.json) lists all 100 assignments, ordered by numeric S1,
then numeric S0. Its SHA-256 is
`c5dfb2f121e8b85fb4078f622257d4a6d924a3f81e055ded9f214d5ed9c89ef9`.
The selected local witness [LOCAL_GRAPH.json](LOCAL_GRAPH.json) is case 0,
`S0=2d81bb, S1=127ede`, and uses local labels `r=0,a=1,b=2,O=3..24`.
It has 25 vertices and 153 red edges. **These local O labels differ from
the 43-vertex embedding below.** Every other local graph is regenerated
from its case and the fixed O, and all 100 are checked.

## Exact decomposition of the conditional full problem

In the 43-vertex problem use labels `[r,H0,...,H19,O0,...,O21]`. Let
`x_(h,o)=1+22*h+o` denote a red H--O edge. These 440 primary variables have
no imposed symmetry order. The marked pair uses variables 1..44.

The generator emits `boundary.cnf` outside Git. For each case j=0..99,
introduce selector `z_j=441+j`. Add the clause containing all 100 selectors,
and for each case add 44 implications from its selector to its signed
cross-edge assignments. The resulting 540-variable, 4,401-clause formula B
has SHA-256
`31472122d30364511de642747e4215bf5a41e9f2f55eb56a122f7b974d8c9340`.
Variables 45..440 are genuinely unconstrained by B.

Existentially eliminating the selectors gives exactly the disjunction of
the 100 complete boundary assignments: some selector must be true, and a
true selector forces precisely its case. Conversely, a listed case satisfies
B by selecting it. Distinct cases disagree on a primary literal, so they
cannot both be selected. No additional at-most-one constraint is needed.

Let F be the complete fixed-H/O Ramsey gluing condition, possibly conjoined
with further degree or neighborhood-density conditions. Let D be the stated
marked sizes and union condition. F already implies the local criterion,
so

```
F AND D  iff  exists z: F AND B
        iff  the disjoint union over the 100 cases of F with 44 fixed units.
```

This is the material reduction: a complete relation on 44 boundary edges,
with a mechanically checked encoding, leaving 396 edges in each disjoint
case. It is **conditional on D**, not an equivalent replacement for the
unrestricted gluing problem without D. All additional constraints remain
in F; in particular, the other 18 H attachments, their degrees, and the two
marked vertices' neighborhood densities 92/107 are not silently discharged.

For integration, reserve variables 441..540 for these selectors and allocate
other auxiliaries above 540, or rename the selectors above the actual maximum
variable of F. Do not append this tail into an older 627-primary layout or
reuse IDs already occupied by counters. No such integration or solver call
is part of this pass. The prior unrestricted 440-primary gluing test remains
UNKNOWN and is not reinterpreted as an exclusion.

## Independent validation and controls

The verifier imports no producer. It lists all 111 literal red K4s of O,
then examines **646,646** 12-sets, **319,770** 14-sets and **170,544** 15-sets,
testing containment of those quadruples. Every accepted subset record is
compared, not just the totals. The absence of a 15-set proves the absence of
all larger red-K4-free sets by heredity, while the five 14-sets prove sharpness.

The pair checker uses a different enumeration: for each of the five S1,
the complement of S0 must be a ten-subset of S1. It examines all
`5*C(14,10)=5,005` possibilities, reconstructs the 103 cover pairs and the
three literal obstructions, and matches the complete 100-case list. It
constructs every 25-vertex graph and counts K5s in both colors by set-based
common-neighbor recursion. It also checks every selector clause, header
and EOF against the independently recovered cases.

Controls include 33,867 subset-clique-number checks over all labeled graphs
of orders 0..5; 16,640 literal small graphs testing both directions of the
local criterion; and 712 small selector case families with 22,424 primary
assignments and all 160,296 full selector assignments, including empty
families and an unused primary bit. Fourteen corrupted certificates/formulas
are rejected; five malformed graphs are rejected by both readers. Mutation
controls reuse one independently reconstructed subset universe; fresh full
verification separately rebuilds it. Normal and optimized Python agree on
all final generated files, case records, graphs, audits and controls.

This is author validation by different algorithms, not independent peer
review or proof-assistant formalization. Trust remains in the finite
reductions, exact source, interpreter/hardware, and hash identity. There
are no solver, floating-point or catalogue-completeness trust boundaries.
No general algorithmic or historical-priority claim is made.

## Reproduction and bounded handoff

Use CPython 3.11.2, standard library only, from the repository root. Choose
a fresh work directory; the producer refuses to overwrite one.

```bash
python3 -B ramsey_r55_marked_pair_decomposition/analyze.py --work /scratch/r55-marked-new
python3 -B ramsey_r55_marked_pair_decomposition/verify.py --work /scratch/r55-marked-new --report /scratch/r55-marked-new/verification.json
python3 -B ramsey_r55_marked_pair_decomposition/controls.py --work /scratch/r55-marked-new --report /scratch/r55-marked-new/controls.json
diff ramsey_r55_marked_pair_decomposition/result.json /scratch/r55-marked-new/result.json
diff ramsey_r55_marked_pair_decomposition/cases.json /scratch/r55-marked-new/cases.json
diff ramsey_r55_marked_pair_decomposition/LOCAL_GRAPH.json /scratch/r55-marked-new/LOCAL_GRAPH.json
diff ramsey_r55_marked_pair_decomposition/verification.json /scratch/r55-marked-new/verification.json
diff ramsey_r55_marked_pair_decomposition/controls.json /scratch/r55-marked-new/controls.json
(cd ramsey_r55_marked_pair_decomposition && sha256sum -c SHA256SUMS)
```

Repeat with `python3 -O -B` and a fresh work directory. Expected results are
maximum 14, five maximizers, 100 cases, verifier VERIFIED, controls PASS.
The final six normal-plus-optimized commands took 27.190960 seconds total
and peak child RSS 23,696 KiB on the production host; this is an observation,
not a performance guarantee. The generated subset streams (24,868 bytes
total) and boundary CNF (45,317 bytes) stay outside Git and are regenerated
and checked entry-by-entry. No omitted large certificate is required.

This exact structural milestone ends here. No job remains active. A future
phase can use these explicit cases for stronger residual compatibility or a
carefully scoped completion test. The symmetry teammate's full-extension
work remains separate. No certified 43-vertex Ramsey(5,5) graph has been found.
