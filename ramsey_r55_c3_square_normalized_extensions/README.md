# No C3-square automorphism subgroup on a Ramsey (5,5;43) graph

The two residual `C_3 x C_3` actions are excluded by complete normalized
Ramsey formulas and replayed DRAT certificates. Together with the sixteen
exclusions in [the action sweep](../ramsey_r55_c3_square_action_sweep), this
excludes every elementary abelian subgroup of order nine. The independently
reviewed [order-nine element exclusion](../ramsey_r55_order9_automorphism_obstruction)
then implies

> **9 does not divide the automorphism-group order of a Ramsey (5,5;43) graph.**

With the earlier prime-divisor exclusions, `|Aut(G)| = 2^a 3^b`, where
`b` is zero or one. Thus every nontrivial 3-subgroup is cyclic of order three.
This is a global restriction, with no hard-branch or degree-profile assumption.
It supersedes the earlier order-27 global bound and M=214-only order-nine bound.
It supplies neither a 43-vertex target graph nor an improved Ramsey lower bound.

## Exact scope and dependencies

The parent action sweep uses the minimum-eleven moving-cycle theorem for
order-three elements to enumerate 117 ordered multiplicity patterns, or
18 action classes after the projective `S_4` action. Sixteen were already
excluded with checked proofs. This package addresses exactly its two open
classes, without recomputing that census or those sixteen proofs:

| parent index | fixed points | quotient 3-orbits | regular 9-orbits | edge-orbit variables |
|---:|---:|---|---:|---:|
| 9 | 1 | two with the same stabilizer line | 4 | 105 |
| 10 | 1 | two with different stabilizer lines | 4 | 103 |

The complete ten-cycle exclusion, including the older four-versus-six split,
now has an [accepted independent review](../ramsey_r55_order3_ten_cycle_signature_propagation_review1).
Its review source is `13d5b8135635669d4f223b7635613a87f0278840`.
The parent C3-square classification and this new closure still await independent
peer review. Internal independent reconstruction is not a peer-review verdict.

## Centralizer normalization lemma

Write `H = F_3^2` additively. Vertex 0 is fixed. Quotient copies `Q_0` and
`Q_1` occupy vertices 1..3 and 4..6, and regular copies `R_0,..,R_3`
occupy 7..15, 16..24, 25..33, 34..42. Within each regular copy, `(u,v)`
has index `3u+v`. Translation `(x,y)` adds `(x,y)` on every regular copy.
On the quotient copies it adds the values of linear forms: both are `x+2y`
in case 9, and the forms are respectively `x+y` and `x+2y` in case 10.
All arithmetic here is modulo three. These are group orbits of size nine;
individual nonidentity group elements have order three.

Color red by 1. Global complementation first makes the orbit of edge `(0,1)`
red; this is the parent's unit `x_1`. Complementation preserves the Ramsey
property and H-invariance. We subsequently use only the following
permutations, which centralize H.

1. Permute the four regular copies, carrying their coordinates identically.
   Sort the five-bit profiles consisting of the edge to vertex 0 followed
   by the internal direction colors `(0,1),(1,0),(1,1),(1,2)`, in that order.
   These four directions represent every nonzero vector modulo sign, so they
   determine the internal undirected Cayley graph. Sort ascending with `0<1`.
2. Keep the origin of the newly first regular copy as anchor (vertex 7).
   Independently translate each of the other three regular copies to make
   its nine-bit cross word from that anchor lexicographically minimal under
   the nine translations of `F_3^2`.
3. Independently rotate each quotient copy to make its three-bit cross word
   from the same anchor lexicographically minimal under its three translations.

Sorting is possible because all regular copies are isomorphic H-sets.
Translations commute with H and preserve both the internal direction colors
and the uniform edge to vertex 0, so they preserve the sorted profiles.
Each later translation changes only its own anchor word; previously minimized
words stay minimized. Quotient rotations also commute with H. They preserve
`x_1` because the fixed vertex has one uniform color to all of `Q_0`.
Regular permutations and translations leave that edge orbit untouched.
Thus every complement-normalized H-invariant graph has a representative
satisfying all three conditions. No independent linear basis change on
individual copies, quotient-copy swap, or extra color assumption is used.
This proves completeness of the normalization needed for the UNSAT implication.

## Exact CNF layer and proof evidence

The parent has one Boolean variable per unordered-pair orbit. Each of the
962,598 five-sets contributes the positive and negative clauses on its distinct
pair-orbit variables. Clauses are deduplicated, and `x_1` is set red. The new
formula preserves the entire canonical parent body byte for byte, then appends
2,840 normalization clauses on the same primary variables, with no auxiliaries:

- 1,488 profile-order clauses: each adjacent pair forbids the `32*31/2 = 496`
  assignments with the left five-bit profile greater than the right.
- 1,344 regular translation clauses: each nine-bit word has 64 translation
  classes, so `512-64 = 448` nonminimal words are forbidden, on three copies.
- 8 quotient rotation clauses: each three-bit word has four classes, so four
  nonminimal words are forbidden, on two copies.

For an assignment word, its blocking clause negates each assigned bit.
All variables within each compared word are distinct. Parent clauses are
ordered by length then signed tuple; the appended layer uses that same order
within the tail. Duplicate clauses between parent and tail, if any, are harmless.
Burnside's lemma independently gives `(512+8*8)/9 = 64` binary regular
translation classes, because every nonidentity translation has three 3-cycles;
it gives `(8+2*2)/3 = 4` quotient classes.

| case | variables / clauses | solver seconds | proof bytes | RAT lemmas in core |
|---:|---|---:|---:|---:|
| 9 | 105 / 214,163 | 6.509183 | 4,359,167 | 138 |
| 10 | 103 / 213,747 | 10.723448 | 5,517,636 | 88 |

Formula SHA256 values are
`e58d139ede296b86b44cb5d452c2cc80d374e0805e936dadfed5deb94cd7162f` and
`3f583630b73b13026e24415838526984f376315aae9e0f5cc33a5f24e48c3420`.
Full proof SHA256 values are
`9e10d8805ebb22704c6b17c408632ebc53a4d0b8f6f8b4a74fc5bbc2b7c57ac1` and
`58894c980c186d3811b33daef72a930b381f2dd80a101cc3c29fb2f53319800e`.
Both solver exits were 20 and both proofs replayed with exit zero and
`s VERIFIED`. General DRAT, including RAT, is required. No timeout is an exclusion.
The two-worker sweep took 38.922123 seconds; largest child peak RSS was
180,872 KiB. Search limits were 180 seconds per case, replay limits 300 seconds.

`audit.py` imports no generator. It independently reconstructs pair orbits by
closure under the two literal vertex generators, uses integer truth tables
and actual vertex translations to reconstruct every tail clause, and checks
byte preservation of every parent clause. The parent's separately compiled
C++ checker uses pair DSU and all literal five-sets to check every base clause.
`verify.py` freshly regenerates both formulas, repeats their full audits and
replays both saved proofs against the fresh formulas. Five malformed formula
mutations per case are rejected: omitted tail clause, reversed literal,
wrong orbit variable, unsupported empty axiom, and changed parent complement
unit. Both cases also pass address/undefined-behavior sanitizer reconstruction
of the full parent. There are no new C++ sources in this package.

The constructive normalization is checked on 258 deterministic arbitrary
colorings per action (all-zero, all-one, and 256 pseudorandom orbit assignments).
Each check validates the relabeling permutation, commutation with both H
generators, all 903 literal edges, every normalization clause, and `x_1`.
All 512 and eight local words are exhausted, with Burnside counts checked.
Normal Python and `python -O` give identical control reports. These controls
support the unformalized coverage proof; sampling does not replace that proof.

## Group-order corollary

If nine divides the automorphism-group order, a Sylow 3-subgroup contains a
subgroup of order nine. Every group of order nine is `C_9` or `C_3 x C_3`.
The previously reviewed cyclic order-nine exclusion rules out the first;
the sixteen parent cases and these two complete extensions rule out the
second. Thus nine does not divide the group order. Together with absence
of prime-order elements at least five and Cauchy's theorem, this proves the
stated form `2^a 3^b` with `b <= 1`. No assertion of asymmetry follows:
involutions and order-three elements with eleven through fourteen moving
cycles remain possible under the current restrictions.

## Reproduce

Python 3.11.2 and GCC 12.2.0 were used, with C++17, `-O2 -Wall -Wextra
-Wpedantic -Werror` for the inherited base checker. Only the Python standard
library is needed. Parent source hashes are enforced by `generate.py`.
Kissat 4.0.4 source: `8af8e56f174b778aef3aa45af9f739b2a5f492c2`.
drat-trim source: `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`.
Binary digests and frozen run-source hashes are in `result.json`.

From this directory, using an empty work directory outside the repository:

```sh
python3 run.py --work /scratch/r55-c3-square-normalized/full \
  --kissat /path/to/kissat/build/kissat --drat-trim /path/to/drat-trim \
  --workers 2 --solve-seconds 180 --replay-seconds 300
python3 verify.py --source-work /scratch/r55-c3-square-normalized/full \
  --work /scratch/r55-c3-square-normalized/verification \
  --drat-trim /path/to/drat-trim --replay-seconds 300
python3 -O audit.py --report /scratch/r55-c3-square-normalized/controls_optimized.json
sha256sum -c SHA256SUMS
```

Expected: excluded indices `[9,10]`, open indices `[]`, two full audits and
proof replays, ten rejected mutations, and translation-class counts 64 and 4.
Timing and memory fields are host-dependent; formula hashes and local control
results are deterministic. Solver traces can depend on the build. A different
trace is acceptable only after successful replay against the audited formula.
`--resume` requires an unchanged contract, reconstructs formulas, and replays
saved exclusions. It retains an OPEN case without extending its time budget.
A `STOP` file prevents a case from starting; active bounded cases finish.
Atomic case checkpoints and the final manifest preserve progress.

Large generated formulas and 9,876,803 proof bytes remain outside Git.
They can be regenerated from this package; manifests and hashes alone are
not standalone refutations. The research-host evidence is under
`/scratch/team-r55-1-c3-square-normalized`, with original evidence in `full/`
and fresh reconstruction/replay in `verification/`. All jobs completed.

## Trust boundary and handoff

The two explicit action exclusions require the elementary action and
normalization proofs, correct source, exact Python/C++ execution, compiler,
hardware, and drat-trim. Global completeness additionally imports the parent
18-type classification, its sixteen exclusions, and the reviewed
minimum-eleven order-three chain. The group-order corollary also imports
the reviewed order-nine element exclusion and elementary finite-group facts.
There is no floating-point mathematical step. No solver verdict alone is
accepted as proof. This package and the preceding C3-square classification
have not received independent peer review at publication.

The bounded two-case milestone is complete. The next symmetry frontier is
single order-three actions, beginning with eleven moving cycles, or a justified
restriction on residual 2-subgroups. No such next phase was started here.
The teammate's non-symmetric graph-realization lane is separate.
