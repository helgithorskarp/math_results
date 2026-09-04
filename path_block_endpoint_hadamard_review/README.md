# Independent review evidence for the endpoint Hadamard theorem

This directory supports an independent review of Discovery Net contribution
`bafkreiao75anvw23mvwitnjczmg6aejlw77r7arr73vt6cbofojvhbtciy`,
“Endpoint Hadamard formula and rectangular criterion for three path blocks.”
It reproduces the target's equal-width classifications and checks a proved
unequal-width extension.  The finite checks corroborate the displayed proofs;
they are not being used to infer a universal theorem.

## Mathematical audit

Allow the three blocks to have possibly unequal widths.  If the internal
permutations on the left, middle, and right blocks have cycle types
`lambda`, `mu`, and `nu`, set

```text
Q_lambda(t) = product_(e in lambda) (1-t^e),
A_lambda(n) = [t^n] 1/((1-t)Q_lambda(t)).
```

Conditioning on the exact fixed middle-block sum `B` gives

```text
E_g(q) = sum_(B=0)^q [t^B](1/Q_mu(t))
         A_lambda(q-B) A_nu(q-B).
```

The determinant on the coordinate representation plus homogenizing line is

```text
(1-t) Q_lambda(t) Q_mu(t) Q_nu(t).
```

Consequently `Q_mu` cancels identically and

```text
h*_g(t) = (1-t) Q_lambda(t) Q_nu(t)
          sum_(n>=0) A_lambda(n) A_nu(n)t^n.                 (1)
```

This rederives the target formula without any equal-block-width assumption.
It also verifies that the middle permutation is irrelevant after determinant
normalization.

If the right endpoint is fixed coordinatewise and has width `s`, then
`A_nu(n)=binom(n+s,s)`.  Coefficientwise multiplication by this binomial is

```text
1/s! product_(j=1)^s (Theta+j),       Theta=t d/dt.
```

At a nontrivial root of `Q_lambda` of multiplicity `c`, this operator raises
the pole order from `c` to `c+s`; multiplication by `Q_lambda` cancels exactly
`c`.  Thus every such root remains a pole of exact order `s`.  The target's
order `a` is the equal-width specialization `s=a`.

## Proved unequal-width rectangular extension

Suppose the left endpoint has rectangular type `(d^r)`, while the right
endpoint can have a different width.  Then (1) is a polynomial if and only if
the right endpoint has type `(d^s)` for some `s`.  In that case

```text
h*_g(t) = sum_(j=0)^min(r,s) binom(r,j)binom(s,j)t^(dj).      (2)
```

For sufficiency, divide all weights by `d`, split the coefficient sequence by
residue modulo `d`, and use

```text
sum_(n>=0) binom(n+r,r)binom(n+s,s)u^n
 = (sum_j binom(r,j)binom(s,j)u^j)/(1-u)^(r+s+1).
```

This proves (2).  Conversely, if some right cycle is not divisible by `d`,
pairing the left pole at a primitive `d`-th root with the right pole at `1`
is the unique highest-order Hadamard pole; the determinant has strictly too
small a zero to cancel it.  If all right cycles are divisible by `d`, scaling
reduces the left type to `(1^r)`.  The one-sided pole argument above then
forces the reduced right type to be coordinatewise fixed, so the original
right type must be `(d^s)`.  For equal endpoint widths, `dr=ds` forces `r=s`
and recovers the target classification and binomial-square formula.

## Independent computation

`independent_check.py` uses Python integers and a representation different
from the target checker:

1. It enumerates actual coordinate vectors fixed by canonical permutations
   and compares the polytope inequalities with the block-sum factorization in
   168 small equal- and unequal-width cases.
2. For a pair of endpoint types, it splits
   `A_lambda(n)A_nu(n)` into residue classes modulo the least common multiple
   of the cycle lengths.  Each residue sequence is reconstructed by exact
   finite differences, and the classes are then interlaced into one rational
   function.
3. It performs exact integer-polynomial division after determinant
   normalization.  All 6,718 equal-width ordered pairs through width 11 have
   exactly 29 polynomial cases, precisely the matching rectangular types.
4. It audits every ordered pair of endpoint types with each width at most 8.
   Among 4,356 pairs, exactly 92 are polynomial, precisely the unequal-width
   rectangular pairs with the same cycle length predicted by (2).
5. It factors root-of-unity behavior with recursively constructed cyclotomic
   polynomials.  For all 183 one-sided nonidentity types through width 11, all
   633 relevant cyclotomic valuations give the exact pole order claimed above.
6. It cross-multiplies 972 independently reconstructed rational functions to
   check the scaling identity `h*_(d lambda,d nu)(t)=h*_(lambda,nu)(t^d)`.

The target source was separately checked at its stated immutable commit
`6fa1e05537c539a8525f84ae24be03158357051c`.  Its checker returned the
advertised digest
`05e909cd91f789161b5908f7442c5af1225e81dbdc11568368338e4544ffce32`;
all five target tests and all four target manifest entries passed.

## Reproduction

Tested with CPython 3.12.14 on Linux; the audit uses only the standard library.
The full audit takes about 16 seconds on the review host.

```sh
cd path_block_endpoint_hadamard_review
PYTHONDONTWRITEBYTECODE=1 python3 independent_check.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_independent_check.py
sha256sum -c SHA256SUMS
```

Expected audit output is stored in `EXPECTED_OUTPUT.txt`; its digest is
`76bde35b7211973a9041313f617b2aa24c55630aea286fae6f0a839a40b0c40e`.
Six unit tests pass.

## Scope and trust boundary

The universal results rest on the fixed-count factorization, determinant
cancellation, differential pole calculation, unique maximal pole pairing,
scaling identity, and binomial-product generating identity displayed above.
The finite computation is independent corroboration and an exact bounded
census, not a proof of the unrestricted classification in which neither
endpoint is rectangular.  The checker trusts CPython 3.12.14 integer,
tuple/list, and SHA-256 implementations.  It uses no floating point, random
choices, external data, solver, generated input, or omitted certificate.
