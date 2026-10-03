# Exact balanced private-triangle repair line on every old cube

Actual author **six-downset-1**, role **researcher**, 2026-10-03.
Complete ordinary author argument, unformalized and independently unreviewed.

Fix the precise seed of [2252bca, original all-cube cap](https://github.com/helgithorskarp/math_results/blob/2252bcaacf4798c6b13d75b4918792fd7c8bbe9c/round-two/six-downset-1/balanced-triangle-all-cubes/PROOF.md),
actually committed10111/0. For every integer n>=3,h>=2 take the old n-point
cube, two distinct marks, h mutually private triangles at EACH mark and
all2h private pairs disjoint and outside the cube. q=2^(n-1),N=2q+12h,s=q+3h.
The fixed repair increases the three free entries between the FIRST x-private
triple and the LAST y-private full row by the SAME real delta. Empty is retained.

Let u=sum_(first triple)e_i-3e_empty,v=e_last-e_empty and K0=NP-Q0 on1-perp.
The [complete ordinary proof](PROOF.md) gives exact rational energies
A=u'K0^-1u,B=v'K0^-1v,C=u'K0^-1v, AB>C^2, and kappa=2/nu+4/beta>0.
The exact lower and cap intervals on THIS real one-parameter line are

    lower PSD iff 0<=delta<=6/kappa,
    cap PSD iff 1/(C-sqrt(AB))<=delta<=1/(C+sqrt(AB)).

Greatest lower rankN-2, cap rankN-1 and simple unit hold simultaneously iff

    0<delta<min(6/kappa,1/(C+sqrt(AB))).

The lower has rankN-3 at0 and6/kappa. The cap has rankN-2 at either of its
endpoints. Whole original support, rows, empty/loop and both centered maximum
stars survive for ALL real delta. Each exclusion is on this specific fixed
seed/repair line. No absence of other H matrices, arbitrary downsets, general
H/I, n2,h1,unequal counts, other seeds or optimal cap gap is claimed.
Ordering the two positive endpoints uniformly is a separate unsolved
obligation here; finite comparisons are not used to order them for all n,h.

Two right sides of ONE positive4-by4 standard solve, ONE positive2-by2 trace
solve and one scalar compute all three energies, independently of N. The
full Woodbury identity retains the original physical-range complement;
original Schur and whole rank-two congruences prove necessity and endpoint
ranks. Old full-space seed positivity/completeness is a cited premise,
unformalized and independently unreviewed for n>=4. [PRIOR-ART.md](PRIOR-ART.md)
credits the ordinary rank, seed, Schur and norm-based sufficient interval.

## Reproduce from compact source

CPython3.12.14, standard library only. From this directory:

```sh
python3 -I -B verify.py
python3 -I -B -O verify.py
```

Every mathematical child is fully waited before the next starts. The five
serial phases regenerate ALL47,974 bytes of [INVERSE.json](INVERSE.json), run
the separate inverse checker, check whole original n4/h2 andn4/h3 matrices,
and reject eight semantic damages. Every7,894 mathematical result byte is
compared with [RESULTS.json](RESULTS.json), SHA256
`8b475f843984ff98e6f6128bf0fb30a885e725faebcfc3a6a73423d82be8d3fa`.
The normal/O streams agree entirely; generated work/ is ignored.

All10 compact inverse equations and8 energy identities have separately
propagated conservative bidegree bound(146,56). ALL8,379 complete Cartesian
nodes yield150,822 identities; all7 positive denominator polynomials/27
factor occurrences are checked. Clearing denominators and the polynomial
root bound prove rational identities on the entire auxiliary quadrant.
This is degree-complete identity checking, not finite case extrapolation.
The checker imports no producer, recipe, sector module or polynomial engine.

The literal controls have N40 andN52. Every original row/support/empty/star
condition, all72/96 physical projection coordinates,80/104 original inverse
equations and80/104 whole Woodbury entries are checked. Exact lower endpoint
ranks and original negative witnesses outside both lower ends are retained.
Both algebraic cap endpoints have every80/104 original null equation checked
in QQ[e]/(e^2-AB), without floats. Rational brackets also provide a full cap
PSD/rank immediately inside and an explicit original negative witness outside.
The cap endpoint rank is supplied by the written whole rank-two proof; no
unperformed algebraic PSD elimination is represented as computation.
The eight damages include an energy agreeing on both h2 andq4 boundary lines.

Unchanged60s child guards,512 polynomial terms,32MiB packing, literal
h<=10,n<=6,N<=80,native threads1/serial mathematical child1/1CPU2GiB.
No resource escalation, external solver, generated private proof corpus,
network or private data is needed for the mathematical replay. A timeout,
UNKNOWN, killed process or incomplete run is never a proof or rejection.
These are same-author separate arithmetic checks, not independent review.

[SOURCES.json](SOURCES.json) records all15 programs and9 unchanged seed
utility copies (one renamed decoder module). [VALIDATION.json](VALIDATION.json)
records sealed normal/O checks; [SHA256SUMS](SHA256SUMS) binds packet files.
The [primary definition](https://arxiv.org/html/2609.28404v1#S4) still proposes
H/I at the liveOct3 check. Its known classical/projection-packing proofs do
not supply the tight H/I matrices considered here.
