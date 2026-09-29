# Construction and optimality within the fixed-seed extension family

Write a congruence as `(a,m)`, meaning `x ≡ a (mod m)`, with `0 ≤ a < m`.
A distinct covering has pairwise distinct moduli and covers every integer.
`L_min(8)` minimizes the LCM over coverings whose smallest modulus is exactly
eight.

## Prime-digit refinement

Let `S` be a distinct covering with LCM `pM`, where `p` is prime and
`gcd(p,M)=1`. Suppose `(c,p)` occurs in `S`. Keep every congruence except
`(c,p)`. For each original congruence `(a,pd)` with `d | M`, add a congruence
`(b,p²d)` specified uniquely by

\[
b\equiv c+p(a\bmod p)\pmod {p^2},\qquad
b\equiv a\pmod d.                                      \tag{1}
\]

The moduli in the new collection are distinct: retained moduli have
`p`-adic valuation zero or one, while added moduli have valuation two; the
values of `d` were distinct in the original collection.

To prove coverage, consider an integer `x` not covered by the retained
congruences. Since `S` covers, `x ≡ c (mod p)`. Set `y=(x-c)/p` and choose
`z` by the Chinese remainder theorem with

\[
z\equiv x\pmod M,\qquad z\equiv y\pmod p.
\]

Some congruence of `S` covers `z`. Its modulus cannot be coprime to `p`,
because such a modulus divides `M` and would then cover `x` as well.
Consequently `z ≡ a (mod pd)` for some original `(a,pd)`. We have
`y ≡ a (mod p)` and `x ≡ a (mod d)`. Hence `x` satisfies (1) and is covered
by the corresponding added congruence.

The resulting LCM is exactly `p²M`. All other prime-power factors of the
original LCM remain after deleting `(c,p)`, and the added class corresponding
to `(c,p)` has modulus `p²`.

For the seed in `seed_m7.json`, `p=7`, `c=6`, and `M=1440`. Its 66 moduli
are every divisor of 10080 at least seven. Exactly 36 are divisible by seven.
The refinement retains 65 classes and adds 36, giving 101 classes with LCM

\[
7^2\cdot1440=70560.
\]

The retained class `(7,8)` is present. Every retained modulus is at least
eight and every added modulus is at least 49. The minimum is therefore
exactly eight. This proves `L_min(8) ≤ 70560` without relying on any
nonexistence result about minimum-seven coverings. In fact the 101 moduli
are all divisors of 70560 at least eight.

The JSON witness contains the uniquely determined residues in (1). For
example, `(6,7)` gives `(48,49)`, `(8,14)` gives `(62,98)`, and `(4,21)`
gives `(34,147)`. The verifier also checks every residue directly.

## Exact capacity of an added congruence

Let a fixed partial congruence collection have LCM `B` and uncovered set
`H ⊆ {0,…,B−1}`. At a prospective LCM `L=tB`, the holes are

\[
H_L=\{h+kB:h\in H,\ 0\leq k<t\}.
\]

For a candidate added modulus `d | L`, put `g=gcd(B,d)` and

\[
w(g)=\max_{0\leq r<g}|\{h\in H:h\equiv r\pmod g\}|.
\]

Then the exact maximum number of holes an arbitrary one congruence modulo
`d` can cover is

\[
C_L(d)=\frac{tg}{d}\,w(g).                              \tag{2}
\]

Indeed, `d/g | t`. As `k` ranges from zero to `t−1`, `h+kB` visits every
residue modulo `d` congruent to `h` modulo `g` exactly `tg/d` times. For
each residue `a (mod d)`, its hole count is therefore `tg/d` times the
number of original holes congruent to `a (mod g)`. Taking the maximum proves
(2). All arithmetic is integral.

If moduli in a fixed collection must remain with their fixed residues,
distinctness permits at most one added congruence for each unused divisor
of `L` at least eight. The union bound thus gives the necessary condition

\[
|H_L|\leq \sum_{\substack{d\mid L,\ d\geq8\\
d\text{ unused}}} C_L(d).                              \tag{3}
\]

No disjointness assumption is made. Violating (3) excludes every extension
at that LCM, even if only a subset of the available new moduli is used.

## Least LCM with all 65 retained seed classes fixed

The retained classes have LCM `B=10080`, and direct evaluation gives
`|H|=252`. All divisors of 10080 at least eight are already used. An extension
containing those 65 classes has LCM a multiple of 10080. Any LCM below
70560 is thus `t·10080` with `1 ≤ t ≤ 6`.

For `t=1` there are no available new moduli. For `2 ≤ t ≤ 6`, complete
divisor enumeration and formula (2) give:

| `t` | Proposed LCM | New moduli | Holes | Sum of exact individual capacities |
|---:|---:|---:|---:|---:|
| 1 | 10080 | 0 | 252 | 0 |
| 2 | 20160 | 12 | 504 | 94 |
| 3 | 30240 | 24 | 756 | 452 |
| 4 | 40320 | 24 | 1008 | 282 |
| 5 | 50400 | 36 | 1260 | 1066 |
| 6 | 60480 | 40 | 1512 | 1198 |

Every row violates (3). `capacity_manifest.json` lists every new modulus
and the exact integers in (2); `verify.py` independently computes each
capacity by lifting the holes explicitly and comparing residue counts.
The enumeration is complete because any congruence modulus divides the
actual LCM, previously used moduli cannot recur in a distinct system, and
all unused divisors at least eight are included.

The refinement above is an extension at 70560 containing all 65 classes.
Therefore **70560 is the exact least LCM within this fixed-seed extension
family**. This local optimality statement says nothing about smaller LCMs
after changing the retained congruences or starting from a different seed.
