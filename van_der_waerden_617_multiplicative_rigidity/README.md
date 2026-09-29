# Multiplicative rigidity of the 617-residue construction

**Claim (exact computer-assisted lemma).** Let
`c : F_617^* -> {0,1}` contain no monochromatic progression
`a, a+d, ..., a+6d`, where `d != 0` and all seven terms are nonzero in
`F_617`. Suppose `c(h*x)=c(x)` for every `h` in a multiplicative subgroup
`H <= F_617^*` with `|H| >= 14`. Then `c` is the quadratic-residue coloring,
up to a global exchange of the two colors.

Equivalently, any different nonzero pattern avoiding these progressions
has a multiplicative stabilizer of order at most 11. This does not assert
existence at stabilizer order 11, classify arbitrary colorings, or improve
the known lower bound for the two-color/seven-term van der Waerden number.
It tells a coset-based construction search exactly which symmetries at
the incumbent modulus must be relaxed.

Author and role: **six-vdw-1, researcher**, 2026-09-29. The primary approach
is construction/counterexample. SAT was used to explore the family; the
claim below is certified independently by exhaustive Python computation
without a SAT library or solver trust assumption. It has not been
independently peer reviewed.

## Reduction and proof

The number 617 is prime, `617-1=616=2^3*7*11`, and 3 is a primitive root.
For `m | 616`, put `H_m=<3^m>`. An `H_m`-invariant coloring is specified
by a binary cyclic word `y[0],...,y[m-1]`, with
`c(3^e)=y[e mod m]`.

For every pair `(a,d)` with `a in F_617` and `d != 0`, form the set of
coset indices met by `a+j*d`, `j=0,...,6`. Retain the pair only when every
term is nonzero. Its constraint is that the colors on that index set
are not all equal. Repeated indices are handled by sets, not discarded.
`certify.py` enumerates **all 617*616 pairs directly**, constructs the
cosets by multiplication, and exhaustively checks these constraints.

The independent scaling construction in `validate.py` instead forms the
index sets of the spacing-one progressions and takes all their cyclic
coset shifts. Multiplying a progression by a nonzero scalar preserves
nonvanishing and shifts every discrete-log index by the scalar's index.
Consequently these are exactly the same constraints; validation compares
the entire edge sets, not just their sizes.

The three indices `m=8,28,44` suffice. Every divisor of 616 at most 44 is
in `{1,2,4,7,8,11,14,22,28,44}` and divides at least one of these three.
If `m | M`, an `H_m`-invariant coloring is also `H_M`-invariant. Thus
classifying the three refinements covers every subgroup of order at
least 14. If the original index is odd, the alternating word cannot be
periodic with that index, so that case has no coloring.

For each of the three cases, complement symmetry fixes `y[0]=0`.
Every nonalternating assignment has a unique first deviation `j>=1`
from `y[v]=v mod 2`. The checker covers all `m-1` possibilities for `j`,
then branches exhaustively on every remaining undetermined variable,
with sound propagation of a not-all-equal constraint's final variable.
Every case reaches a contradiction. A node budget causes an explicit
`INCOMPLETE` error; it never produces a nonexistence conclusion. The
alternating word itself satisfies every retained constraint.

| Index m | Subgroup order | Full edge sets | Nonzero edge sets | Exhaustive nodes |
| --- | --- | --- | --- | --- |
| 8 | 77 | 196 | 184 | 7 |
| 28 | 22 | 8036 | 7924 | 211 |
| 44 | 14 | 13112 | 12936 | 1895 |

The classification also implies that an `H`-invariant coloring of all of
`F_617` under this hypothesis has the quadratic-residue pattern at its
nonzero positions. Both choices for the color of zero work; this is
checked against every nonzero-spacing progression in the field. There
are therefore exactly four such full-field colorings, counting the two
global color orientations and the two choices at zero.

## Reproduce

Python 3.11.2 was used. Only the standard library is required. From the
repository root:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
python3 van_der_waerden_617_multiplicative_rigidity/certify.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
python3 van_der_waerden_617_multiplicative_rigidity/validate.py
```

The first command returns `RIGIDITY_CERTIFIED` for exactly the three
indices, with the edge counts and node counts in the table. Compact
expected output, including every first-deviation case and hashes of the
direct edge sets, is in `expected.json`. The first full run took 15.9
seconds and 18,848 KiB peak resident memory in the shared one-CPU scope;
runtime is environment dependent. No parallel solver or worker is used.

Validation checks the exhaustive Boolean search against brute force on
192 deterministic small instances; compares the two different edge
constructions entry by entry; brute-forces all 256 index-eight colorings
(only masks 85 and 170 survive); checks 760,144 cyclic progressions for
the two colors of zero; and reconstructs the classical length-3703
interval coloring, checking all 1,140,833 seven-term progressions.
Its canonical bit string has SHA256
`a27ec1e5f03030b2e88f0e5d7b493a8cd18976bbdbce94a0043f95b2823da83f`.

The trust boundary is the supplied exact-arithmetic Python program and
interpreter, together with the elementary finite-group reduction above.
There is no imported large certificate, solver trace, floating-point
calculation, or assumption that an incomplete search is exhaustive.

## Literature and scope

The incumbent comes from the power-residue construction at prime 617.
[Monroe, JCMCC 128, Tables 1–3](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/)
still lists `>3703` for two colors/seven terms and uses the notation
`W(length, colors)`. Here `W(2,7)` always means two colors/seven terms.
[Herwig, Heule, van Lambalgen and van Maaren](https://www.cs.utexas.edu/~marijn/publications/waerden.pdf)
also give the 617 construction without zipping.

The multiplicative pre-partition method is established prior work;
[Heule, *Avoiding triples in arithmetic progression*, Section 4.3](https://www.cs.utexas.edu/~marijn/publications/JOC_08_03_A01.pdf)
describes assigning colors to multiplicative orbit classes. The claim
here is the specific finite rigidity threshold at 617, rather than
novelty of that method. This threshold was not found in the checked
primary papers or their source repositories; no priority claim is made.

The first next construction frontier is index 56 (subgroup order 11),
or a template that breaks multiplicative invariance. Transient search
logs and dependencies remain outside this public directory.
