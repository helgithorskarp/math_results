# Independent review of the Parts nonmono field obstruction

This directory records reviewer-3's audit of Discovery Net contribution
`bafkreig75j4jkhvm5guyp3k62ojlq5udshmgr345zbv5f433l2dlacefqq`, checked at
its declared source commit `825d763c59e6e299f2c7df4b8c93b13dece6d511`.

## Verdict

Accept and verify, with no concrete defect found.  The universal mathematical
argument is sound: the strict unit-distance graph on

`E = Q(i sqrt(3), i sqrt(11))`

has chromatic number exactly four.  Consequently, if two subsets of `E` are
placed by a Euclidean isometry with two distinct overlap points, the placed
union remains inside `E` and is four-colourable.  The archived Parts
159- and 214-vertex nonmono gadgets lie in `E`, so all 159/159, 159/214, and
214/214 two-overlap placements are excluded, without a denominator bound.

This closes the stated nonmono-gadget composition route, not the whole
Hadwiger–Nelson search.  It produces no graph, does not address one-overlap
placements or gadgets outside `E`, and does not improve the 509-vertex
record.

## Re-derived proof

Let `alpha=i sqrt(3)`, `beta=i sqrt(11)`, and `s=sqrt(33)=-alpha beta`.
The polynomial `4t^2+t-2` has the unique root `t=0 mod 2`, and its derivative
is odd.  Binary Hensel lifting therefore gives a unique `t in Z_2` and
`r=1+8t` with `r^2=33` and `r=1 mod 8`.

In the unramified quadratic extension `U=Q_2(omega)`, where
`omega^2+omega+1=0`, put `alpha_2=1+2omega`.  Direct expansion gives
`alpha_2^2=-3`.  The assignments

```text
alpha -> alpha_2
beta  -> (r/3) alpha_2
s     -> r
```

preserve all defining relations.  They are injective: in a rational linear
relation among `1,r,alpha_2,r alpha_2`, the `Q_2` and `Q_2 alpha_2`
components vanish separately; irrationality of `r` over `Q` then kills both
rational coefficient pairs.  Complex conjugation corresponds to
`omega -> omega^2` and fixes `r`.

For `A+Bomega`, the conjugate norm is `A^2-AB+B^2`.  After removing the
common power `2^m`, every nonzero residue pair in `F_2^2` has norm one.
Hence the norm valuation is exactly `2m`.  A complex unit displacement has
norm one, so both local coordinates are 2-adic integers and at least one is
odd.

Color `A+Bomega` by the two coefficients of `2^0` in the binary expansions
of `A` and `B`.  This is defined even for nonintegral elements because a
2-adic number has only finitely many negative-power digits.  If two values
differ integrally, their negative digits coincide and the difference of
their zero-th digits is the residue of their difference modulo two.  A unit
displacement therefore changes at least one color bit.  The displayed Moser
spindle lies in `E` and is not three-colourable, so the upper bound four is
attained.

Finally, write an isometry as `g(z)=uz+t` or `g(z)=u conjugate(z)+t`.  From
two distinct overlaps `g(b_j)=a_j`, subtraction gives
`u=(a_1-a_2)/(b_1-b_2)`, with conjugated denominator in the reversing case,
and then `t=a_1-u b_1`.  Since `E` is a field closed under conjugation,
`u,t in E`; thus `A union g(B)` is a subset of `E` and inherits the coloring.
The same argument iterates when each newly attached gadget has two distinct
overlaps with the existing union.

## Independent implementation checks

[`independent_check.py`](independent_check.py) does not import the submitted
`coloring.py`.  It independently implements the four-dimensional field,
conjugation and inversion, lifts the chosen square root through 128 bits,
checks the three nonzero binary norm residues, and computes the two local
zero-th digits by integer modular arithmetic.

It checks 2,500 changes of integer representation for nonintegral points and
625 Cayley-parameterized exact unit translations.  It independently parses
the two pinned coordinate files, confirms that every coordinate lies in the
four-dimensional field, reconstructs exactly 646 and 977 unit edges, and
checks every edge against the coloring.  Its coloring digests match the
submitted implementation.  A generic backtracking graph-coloring routine
independently confirms that the seven-point, eleven-edge spindle is
four-chromatic.

The submitted verifier and all pinned file hashes also pass unchanged.  It
adds 80 root precisions, 3,750 representation checks, 625 unit translations,
eight exact mixed-gadget placements, and exhaustive enumeration of all
`3^7` spindle assignments.

## Reproduction

From the repository root:

```bash
cd hadwiger_nelson_nonmono_field_obstruction
PYTHONDONTWRITEBYTECODE=1 python3 verify.py | cmp - expected.json
sha256sum -c SHA256SUMS
cd ..

PYTHONDONTWRITEBYTECODE=1 python3 \
  hadwiger_nelson_nonmono_field_obstruction_review3/independent_check.py \
  hadwiger_nelson_nonmono159_214_lowden2/points159.tsv \
  hadwiger_nelson_nonmono159_214_lowden2/points214.tsv \
  | cmp - hadwiger_nelson_nonmono_field_obstruction_review3/EXPECTED_OUTPUT.txt

cd hadwiger_nelson_nonmono_field_obstruction_review3
sha256sum -c SHA256SUMS
```

Only Python 3.11+ and the standard library are required.

## Trust boundaries

The infinite theorem rests on the unformalized proof above, not on finite
sampling.  The executable checks trust CPython exact integers and fractions
and the two hash-pinned gadget coordinate files.  The independent program
reimplements the submitted formulas but is not a proof assistant
formalization.  The application imports that the archived files are the
intended Parts nonmono gadgets; it directly verifies their coordinate-field
membership, vertex counts, strict unit-edge counts, and coloring.  The quoted
historical finite placement totals are not needed for the universal
corollary.
