# Reflected common fibres for a Schur construction

This is an exploratory construction rule with complete small witnesses and
an independent verifier. **It gives no new bound for S(6).** The current
545-modulus target is unresolved. We make no historical-priority claim for
the elementary product construction or its set formulation.

The purpose is to remove an extra coordinate-reflection restriction from
the [earlier shared-fibre construction](../schur6_shared_fibre_projection/).
That earlier model had four identical common-colour fibres. Here two are
identical and the opposite two are their reflections. The complete colouring
still has global reflection symmetry. The 234-point fixture cannot be
represented by any uniform palette map for reflection in the long coordinate.

## Construction and exact criterion

Let A be a finite abelian group. Partition its nonzero elements into
symmetric sets E0,...,E5, and partition A into R,C2,C3,C4,C5, with 0 in R.
The second partition need not be symmetric. In A x Z5, colour all points
other than (0,0) by the following six classes:

    K0 = (E0 x {0}) union (R x {1}) union (-R x {4}),
    K1 = (E1 x {0}) union (R x {2}) union (-R x {3}),
    Ki = (Ei x {0}) union (Ci x {1,2}) union (-Ci x {3,4}),  i=2,...,5.

These classes partition the punctured group and are symmetric under global
negation. They are all sum-free, including equal summands, **if and only if**:

1. Every Ei is sum-free in A.
2. Every Bi = Ci union (-Ci), for i=2,...,5, is sum-free in A.
3. (E0 union E1) is disjoint from R-R.
4. Ei is disjoint from Ci-Ci for i=2,...,5.

Empty colour classes are permitted. For odd A=Z_a with gcd(a,5)=1, the CRT
identifies the construction with Z_(5a). Its full word on nonzero residues
then gives a classical six-colouring of [1,5a-1]. This is the case handled
by the search code. The defining equation includes x=y throughout.

### Proof

Triples with all second coordinates zero give condition 1. In K0, two
nonzero second coordinates can sum to another allowed second coordinate
only as 1+4=0 or 4+1=0. Their first coordinates give R-R. A zero-fibre point
plus a nonzero-fibre point gives the same exclusion. The other two sums,
1+1=2 and 4+4=3, leave the second-coordinate support of K0. This proves the
criterion for K0. Replacing {1,4} by {2,3} gives the identical argument for K1.

For a common colour, the sums 1+1=2 and 1+2=3 respectively require

    (Ci+Ci) intersect Ci = empty,
    (Ci+Ci) intersect (-Ci) = empty.

These two conditions are equivalent to sum-freeness of Ci union (-Ci):
every signed triple can be negated and rearranged into one of these two
forms. All pairs of nonzero second coordinates whose sum is nonzero give
one of these forms. Pairs with sum zero, namely 1+4 and 2+3, give Ci-Ci.
A pair with one zero second coordinate also gives the difference-set
exclusion Ei intersect (Ci-Ci) = empty. Together with condition 1, this
exhausts all pairs, proving necessity and sufficiency.

The supplied one-colour audit independently exhausts 1,536 set assignments
over Z7 x Z5, using literal group addition. It checks both special types
and the common type. The all-parameter argument is the proof above, not
the finite audit.

## What the complete fixtures show

The two full words in fixtures.json are valid on [1,34] and [1,234]. They
are calibration examples, not record Schur partitions. The standard-library
verifier checks every integer sum, every modular sum, coverage, the stated
fibre rule, global reflection, and the set criterion.

The 234-point fixture has class sizes

    38, 36, 34, 42, 30, 54,

with |R|=18 and common sizes 6,8,5,10. Thirteen signed axis pairs have
different first-fibre colours. At first-fibre coordinates 0 and 4, the
colour is 0; after reflecting the long coordinate, their colours are 0
and 2 respectively. Therefore no single palette function, and in particular
no palette involution, implements that coordinate reflection. This puts
the fixture outside the previous uniform fibre-involution models. This
property is preserved by global colour relabelling and cyclic unit scaling.

The special axis classes of this fixture can be merged. Nevertheless,
the old five-colour projection, which uses merged E labels at even points
and Q labels at odd points modulo 2a, has 19 modular defects. Its first
ordinary defect is 1+7=8. Thus that projection operation does not transfer
to the reflected-fibre model. **This is not a counterexample to the
numerical cap 394:** the fixture has endpoint 234, and existence above 394
in the mergeable reflected family has not been established.

## Search encoding and honest target status

search.py uses one six-valued state for each signed nonzero E orbit and one
for each individual nonzero Q coordinate. State 1 is forbidden in Q; state
0 means R. Every literal nonzero modular sum is encoded, including repeated
summands. Two fixed short-axis states enforce colours 0 and 1 at second
coordinates +/-1 and +/-2. Decoding produces every entry of the full word.

Only common labels 2,...,5 are interchangeable. The free model orders their
first occurrences. A frozen labelled axis disables that ordering. The
optional asymmetric flag requires at least one Q(x) != Q(-x).

For prime a>45, the optional normalization E(1)=0 preserves the free family.
The axis requires at least five colours because S(4)=44. It therefore uses
one of the two special colours. Exchanging E0 and E1 alone preserves the
criterion, and multiplication by a unit puts one such element at 1. This
uses the known S(4) theorem, not a new computation here. The normalization
must not be added to a frozen labelled axis.

The search environments used CPython 3.12.14, python-sat 1.9.dev15 and
CaDiCaL 1.9.5. Recorded observations:

| Instance | Result | Conflicts |
|---|---|---:|
| a=47, normalized, asymmetric | SAT; full 234-point fixture | 304 |
| a=83, normalized, asymmetric, mergeable special axis | UNKNOWN | 100,003 |
| a=109, normalized, asymmetric | UNKNOWN | 1,000,002 |

The last instance has 164 states and 112,614 clauses. Neither UNKNOWN
result is an exclusion. No complete target word, family-wide UNSAT proof,
or numerical improvement follows. A fixed five-colour 109-axis also failed
five tested roles in local exploratory solves; those narrow UNSAT observations
are not independently certified and are not used as a mathematical result.

## Reproduction

The independent verification needs only Python 3.11 or later:

    python3 -B verify.py
    sha256sum -c SHA256SUMS

It prints the complete expected.json report: PASS, endpoints 34 and 234,
the two coordinate-reflection obstructions, projection-defect counts 5 and
19, and all 1,536 one-colour checks. It imports no search code or SAT package.

To audit the encoding or reproduce a search, create a local environment
and install requirements.txt. Then run, from this directory:

    python audit_encoding.py --output /tmp/reflected-audit.json
    python search.py --axis-factor 47 --budget 100000 --normalize-axis --require-asymmetric --output /tmp/reflected235.json
    python search.py --axis-factor 109 --budget 1000000 --normalize-axis --require-asymmetric --output /tmp/reflected545.json

The encoding audit checks 99,648 local truth assignments and the 1,536
one-colour cases. Positive witnesses are accepted only after the complete
independent word check. The source is small; no raw CNF dump, bulky search
log, private state or UNSAT proof claim is included.

## Next constructive test and literature context

The 234-point fixture suggests a more structured search. With
I={16,...,31} in Z47, the symmetric supports B2, B3 and B5 lie in 11I, 13I
and 8I respectively. B4 lies in no unit dilation of I. This is checked
directly by verify.py. Thus a test with three middle-third supports and one
unrestricted support has a positive control. Requiring all four supports
to be interval dilates would discard this control. Such a support restriction
would be a proposed construction subfamily, not a completeness theorem for
the reflected model.

The classical frontier remains S(6)>=536 from
[Fredricksen--Sweet (2000)](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v7i1r32),
also used in the [July 2026 shifted-template paper](https://arxiv.org/abs/2607.15034).
[Heule's Schur Number Five paper](https://arxiv.org/html/1711.08076v1) supplies
S(5)=160 and records S(4)=44. Rowley's
[template construction paper](https://arxiv.org/abs/2107.03560) and the 2026
paper concern interval/template recurrences; this note instead records a
specific punctured-group criterion and its checked finite instances.
The targeted literature search does not establish historical novelty.
