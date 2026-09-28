# A complete reflected product family is impossible modulo 553

**Certified finite exclusion.** The six-colour construction below has no
valid instance over Z79 x Z7, for any of its eight choices of short-coordinate
orientations. All axis classes and all first-coordinate component sets are
free within the model. A 663-variable, 24,765-clause CNF is UNSAT, with an
independently verified DRAT proof. No axis coordinate is normalized and no
asymmetry, middle-third support, or empty-axis condition is imposed.

This excludes the entire stated product family at modulus 553. It does not
exclude arbitrary reflected colourings, arbitrary symmetric colourings of
[1,552], or arbitrary six-colourings of [1,537]. **No numerical bound for
S(6) changes.** A valid full word here would have given S(6)>=552; the
supplied small words are calibration examples only.

## The family and its exact criterion

Let A=Z79. Partition A minus {0} into symmetric sets E0,...,E5, and
partition A into R,C3,C4,C5 with 0 in R. Empty classes are allowed.
R and the common fibres Ci need not be symmetric.

Choose j0 from {1,6}, j1 from {2,5}, and j2 from {3,4} in Z7, and put
T={j0,j1,j2}. Thus T and -T partition the six nonzero short coordinates.
For s=0,1,2 and i=3,4,5 define

    Ks = Es x {0} union R x {js} union (-R) x {-js},
    Ki = Ei x {0} union Ci x T union (-Ci) x (-T).

These classes partition (A x Z7) minus {(0,0)}, with global negation
symmetry. They are all sum-free, including x=y, exactly when

1. Every Ei is sum-free in A.
2. Each Bi=Ci union (-Ci), i=3,4,5, is sum-free in A.
3. (E0 union E1 union E2) is disjoint from R-R.
4. Ei is disjoint from Ci-Ci for i=3,4,5.

This criterion holds for every finite abelian A. The implementation uses
odd cyclic A; the target CRT identification is Z79 x Z7 = Z553.
The earlier [factor-five criterion](../schur6_reflected_fibres/README.md)
and its [review](../../schur_s6_reflected_fibres_review1/REVIEW.md) motivated
this change of short factor. The criterion here has three special and
three common classes, and is proved directly below.

### Proof of the criterion, including all eight orientations

Each pair {js,-js} is sum-free in Z7. For a special colour, two nonzero
short coordinates return to its support only by js+(-js)=0. These pairs
give the R-R condition. One zero and one nonzero short coordinate gives
the same difference condition. Two zero coordinates give sum-freeness
of Es. This proves necessity and sufficiency for each special class.

For a common colour, a zero short coordinate gives sum-freeness of Ei or
the Ci-Ci exclusion. Two nonzero short coordinates summing to zero also
give that exclusion. Every other pair gives a signed equation in Ci,
which is forbidden by sum-freeness of Bi.

For necessity of the full Bi condition, each of the eight sets T contains
a pair x,y with x+y in T, and a pair u,v with u+v in -T. These force
(Ci+Ci) to avoid both Ci and -Ci. Their conjunction is equivalent to
sum-freeness of Ci union (-Ci), by changing signs and rearranging a
signed equation. The eight finite short-coordinate checks, with explicit
witness pairs, appear in expected.json and are independently enumerated
by audit.py. For T={1,2,3}, the witnesses are 1+1=2 and 3+3=6.
All cases include repeated summands. Thus the same criterion applies to
every orientation; a single UNSAT instance for its variables covers all
eight construction families.

## Exact encoding and certificate

There are six one-hot axis colours on each of the 39 signed nonzero
orbits. Each of the 78 individual nonzero fibre coordinates has one of
four states: R,3,4,5. Zero is fixed in R. For each common colour and
signed orbit, a support variable is defined as the OR of the two fibre
membership variables. The counts are 234 axis, 312 fibre and 117 support
variables, totalling 663.

The CNF contains all symmetric modular Schur edges for each axis class
and each common support. For every two distinct R coordinates, including
zero, their difference is forbidden in each special axis class. For two
coordinates in one common Ci, their difference is forbidden in Ei.
Zero differences are absent from the axis. No other set restrictions
are added.

The common names 3,4,5 are ordered by first occurrence across
Q(u),Q(-u),E(u). The special axis names 0,1,2 are independently ordered
by first occurrence on the axis. Any common palette permutation preserves
the criterion, as does any permutation of E0,E1,E2 alone: only their
union occurs in the compatibility condition. These commuting palette
operations prove completeness of the normalization. In particular there
is **no** unit clause E(1)=0 and no imported numerical Schur theorem in
the proof.

CaDiCaL 1.9.5 generated a 57,810,991-byte binary DRAT proof; DRAT-trim
returned `s VERIFIED`. Its backward core uses 9,499 input clauses and
615,704 lemmas, with zero RAT lemmas in the core. Generation and checking
took about 91 and 89 seconds respectively; times vary.

## Independent checks and complete controls

The literal clause auditor uses the variable maps as a numbering scheme,
checks every support OR definition, eliminates those auxiliaries by
distributive expansion, and compares the remaining clauses with every
literal full-word modular equation by explicit mutual clause subsumption.
It does not use the model's axis-edge generator to derive the expected
clauses. At modulus 553 it checks all 152,352 unordered nonzero modular
pairs, including all 552 doubling pairs. There are 34,788 distinct
projected clauses and 34,554 expanded reduced clauses; the extra 234
projected clauses are explicitly subsumed. Palette completeness rests on
the relabelling argument above.

The audit also runs at factors 5 and 13. At a=5 it exhausts all 9,216
complete assignments, finds 1,344 valid words, and checks that every valid
assignment has a representative satisfying the palette clauses.

The independent standard-library verifier checks the full supplied words
through 34 and 90 against every integer and modular sum, reconstructs all
fibres, and checks the criterion. A second 34-point control has asymmetric
fibres. The verifier rebuilds and checks all eight short orientations for
each of these three controls. The endpoint-90 control has class sizes
6,6,6,24,24,24. None is a record Schur partition.

## Reproduce and trust boundary

Use Python 3.11 or later with its standard library. From this directory:

    sha256sum -c SHA256SUMS
    python3 -B verify.py
    python3 -B audit.py
    python3 -B model.py /tmp/schur-factor7.cnf

The verifiers print PASS with the full expected.json reports. The CNF
has 451,030 bytes and SHA-256

    c18a9e6d9ffaeb5fb32158a360bd147fea35bb4328b7a5c15a8689a6447dd9c6

Build [CaDiCaL](https://github.com/arminbiere/cadical) 1.9.5 at commit
`146207318796f094dcded87349a64f0c6927309e` and
[DRAT-trim](https://github.com/marijnheule/drat-trim) at commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`, then run

    python3 -B prove.py --cadical /path/to/cadical --drat-trim /path/to/drat-trim

The runner requires solver exit 20 with UNSAT and checker exit 0 with
VERIFIED. The reference proof SHA-256 is

    e3ade4fa9022aebf7fe50fdb8929a21fcda987f75816a492afe319eca4197659

A regenerated proof may have another hash and still be valid if it verifies
against the same audited CNF. The bulky proof is retained in the research
workspace and regenerated by the source, not uploaded. The runner removes
its temporary outputs after verification. The trust boundary is the exact
criterion, palette completeness, literal clause audit, and external proof
checker; a solver status or matching hash alone is insufficient.

This finite exclusion has not yet received a separate peer review. No
historical-priority claim is made for the elementary product criterion.
The [July 2026 primary reference](https://arxiv.org/abs/2607.15034) still
uses the classical lower bound S(6)>=536. The present result does not
change that bound or the largest-colourable-endpoint convention.
