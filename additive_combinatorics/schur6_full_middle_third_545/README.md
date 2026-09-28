# A full-middle-third obstruction for reflected Schur fibres modulo 545

**Certified finite exclusion.** In the reflected-fibre construction below
over A = Z109, there is no valid six-colouring for which some common fibre
Ci is a unit dilation of I = {37,...,72} and the corresponding axis class
Ei is empty. The axis and all other fibres are otherwise free within the
stated construction. A 666-variable, 20,574-clause CNF is UNSAT; an
independent DRAT-trim check verified the generated proof.

This gives **no new bound for S(6)**. It does not exclude all reflected
constructions, all interval-supported common fibres, or all colourings of
[1,537]. In particular, Ci = kI is a stronger condition than Ci contained
in kI, and stronger than Ci union (-Ci) = kI. The criterion used here has
an [independent review](../../schur_s6_reflected_fibres_review1/REVIEW.md);
this new finite exclusion has not yet received a separate peer review.

## Exact family

Let symmetric E0,...,E5 partition A minus {0}, and let R,C2,...,C5 partition
A, with 0 in R. Empty classes are allowed. The common fibres and R need
not be symmetric. On the punctured product A x Z5, define

    K0 = (E0 x {0}) union (R x {1}) union (-R x {4}),
    K1 = (E1 x {0}) union (R x {2}) union (-R x {3}),
    Ki = (Ei x {0}) union (Ci x {1,2}) union (-Ci x {3,4}), i=2,...,5.

All monochromatic equations x+y=z, including x=y, are forbidden. The
[reflected-fibre criterion](../schur6_reflected_fibres/README.md) says this
holds exactly when each Ei and each Bi = Ci union (-Ci) is sum-free,
(E0 union E1) avoids R-R, and Ei avoids Ci-Ci for i=2,...,5.
CRT identifies this product with Z545. A valid full modular word would
therefore give a classical word through 544.

The restriction tested here is E2 empty and C2 = I. Relabelling the four
common colours and multiplying the long coordinate by a unit show that
the exclusion covers every common index and every unit dilation of I.
There is no normalization E(1)=0 and no condition requiring asymmetry.

## Reduced encoding and completeness

The generator handles odd a >= 7 with gcd(a,15)=1. Write
m = floor((a-1)/3), I = {x: a < 3x < 2a}. Its complement is
{0} union +/-[1,m]. Since C2 is fixed to I, the remaining first-fibre
states are R,3,4,5 on these nonzero complement points, with 0 fixed in R.
The axis uses states 0,1,3,4,5 on the (a-1)/2 signed orbits.

For c=3,4,5 let Pc contain u in [1,m] when either u or -u belongs to Cc.
Thus Bc = +/-Pc. Because 3m<a, Bc is modular sum-free exactly when Pc
contains no ordinary x+y=z. Indeed, any signed modular equation has
absolute integer discrepancy at most 3m<a, so it is an integer equation;
rearranging its signs gives a positive sum equation. Conversely every
positive sum equation is a modular one. The fixed set I is symmetric and
modular sum-free.

The CNF contains:

1. One-hot axis and first-fibre states.
2. Every modular axis Schur edge, including repeated summands.
3. Auxiliary definitions P(u,c) iff Q(u,c) or Q(-u,c), and ordinary Schur
   constraints on each Pc.
4. Difference compatibility: two R coordinates forbid both special axis
   colours at their difference; two Cc coordinates forbid axis colour c.
   The zero coordinate is included in R. Zero differences need no clause
   because the zero point is not on the axis.

The model has two sound palette normalizations. Common labels 3,4,5 appear
in order of first occurrence, scanning Q(u), Q(-u), E(u), then moving to
the next u; Q entries are skipped for u>m. Any finite assignment can be
relabeled this way. Also, the first axis occurrence of either special
colour is 0. Swapping E0 and E1 alone preserves every criterion condition,
so this loses no construction. These operations commute. No use of a
known Schur-number upper bound is needed for either normalization.

The variables for a=109 are 270 axis indicators, 288 first-fibre
indicators, and 108 support indicators, for 666 in total. Including the
palette clauses, the generator emits exactly 20,574 clauses.

## Independent checks and complete controls

`audit.py` does not import the axis-edge generator or the model's short
Schur-edge construction as an oracle. It uses the model's variable maps
as a numbering scheme, checks all auxiliary OR definitions, eliminates
those auxiliary variables by distributive expansion, and compares the
result with clauses projected independently from every literal modular
equation in the full word. Both directions of implication are checked
by explicit clause subsumption. The palette clauses are omitted from
this comparison; their completeness follows from the relabellings above.

At a=109 this checks all 147,968 nonzero modular pairs, including
doublings. There are 26,640 distinct projected clauses and 26,532 expanded
reduced clauses. The 108 extra projected clauses each contain an already
present smaller clause. No unproved equivalence transformation is used.
The same audit runs at a=7 and a=47. At a=7 a separate complete test checks
all 32,000 assignments against literal sums: 2,988 are valid, and every
valid assignment has a representative satisfying the palette clauses.

`controls.json` gives two complete words through 234. `verify.py` imports
no generator or SAT solver and checks every integer and modular equation,
the CRT fibre rule, reflection, the set criterion, and the claimed support
properties. The first word belongs to the excluded-at-109 family:
C2={16,...,31}, E2 empty, class sizes 24,24,64,36,42,44. It shows that the
family is nonempty at a smaller factor.

The second word is a possible direction beyond the excluded family:
E5 is empty, while C5 is contained in no unit dilation of the middle third.
The other common supports lie in I,4I,23I. It has class sizes
24,34,40,50,42,44. Its target analogue at a=109 remains unresolved; no
exclusion or existence assertion for that target follows here.

## Reproduce

The generator, audits and full-word verifier need only Python 3.11 or
later and its standard library. From this directory:

    sha256sum -c SHA256SUMS
    python3 -B verify.py
    python3 -B audit.py
    python3 -B model.py /tmp/schur-middle545.cnf

The word verifier and encoding audit print PASS with the complete reports
in expected.json.
The generated CNF has 388,678 bytes and SHA-256

    0b2b8adecfdd9f5f6e9144fcad75449ea9355e3afb6454beb873c3a8c6d55886

For the UNSAT certificate, build these external tools at the recorded
source commits using their own build instructions:

| Tool | Source | Commit |
|---|---|---|
| CaDiCaL 1.9.5 | https://github.com/arminbiere/cadical | 146207318796f094dcded87349a64f0c6927309e |
| DRAT-trim | https://github.com/marijnheule/drat-trim | 2e3b2dc0ecf938addbd779d42877b6ed69d9a985 |

Then run:

    python3 -B prove.py --cadical /path/to/cadical --drat-trim /path/to/drat-trim

This generates the exact CNF, runs CaDiCaL to completion, and invokes
DRAT-trim on the completed proof. It requires solver exit 20 with UNSAT
and checker exit 0 with VERIFIED. The reference binary proof has
52,312,176 bytes and SHA-256

    622c570d13299c138f8131877ef1445d564239fbb080fe76c3ff733ed8b8e4f5

The reference run took about 62 seconds to generate and 68 seconds to
check. Times vary. The checker found zero RAT lemmas in the proof core.
The script reports whether the regenerated proof matches this hash;
another correctly verified proof of the same CNF is also valid.

The bulky proof is retained in the research workspace and omitted from
GitHub; reproduction regenerates it. The script uses a temporary directory
and removes its generated files afterward. To retain a proof, run
`model.py`, then `cadical -q instance.cnf proof.drat`, then
`drat-trim instance.cnf proof.drat -i -t 600` directly. An earlier local
attempt to capture the solver's still-buffered output was truncated and
failed verification. It is not the proof reported here.

The trust boundary is the mathematical reduction, the checked palette
normalizations, the literal encoding audit, and the external proof checker.
A solver's UNSAT answer or a matching hash alone is not the verification.
The certificate establishes this finite family exclusion only.

## Literature and scope

The classical endpoint convention is used: S(6)>=536 means [1,536] is
colourable. The construction of
[Fredricksen and Sweet (2000)](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v7i1r32)
and the [July 2026 shifted-template paper](https://arxiv.org/abs/2607.15034)
provide the current reference point. This computation does not improve it.
We make no historical-priority claim for the elementary product criterion.
