# A 122-point H630 block reduction gives a four-chromatic 508-point graph

One frozen geometric block replacement of the reviewed five-chromatic H630
seed gives **508 distinct plane points, 2,341 complete unit edges, and
chromatic number exactly four**. The net physical reduction is 122. A literal
four-word triggers the declared stop; this is not a record candidate or a
classification of other H630 replacements.

## Source and one frozen replacement

The [reviewed H630 seed](https://github.com/helgithorskarp/math_results/blob/7df34e419981e1c8d0b7cf98fb3ca6f35ca62a95/hadwiger_nelson_heule630_seed_review1/README.md)
is the exact 630-point/3,098-edge support obtained from archived H632 by
omitting old labels 399 and 462. Its ordinary five-chromaticity is committed
as h3319 and independently accepted at h3335. The original construction source
is [commit 14a0c9b](https://github.com/helgithorskarp/math_results/blob/14a0c9b76d7907ab0d7107a0a8796e3c0784dc68/hadwiger_nelson_heule632_pair_pilot/README.md).

In the displayed coordinate basis of
`K=Q(sqrt(3),sqrt(5),sqrt(11))`, retain exactly the 418 source points having
zero coefficients on every monomial containing `sqrt(5)`. Remove the entire
remaining 212-point block. The retained support A includes both `0` and
`a=1+i*sqrt(3)/3` (old labels 0 and 193).

Set

```text
omega = (1+i*sqrt(3))/2
q = (1/2-sqrt(6)/6) + i*(sqrt(3)/6+sqrt(2)/2)
T = {q*(m+n*omega) : m,n integers,
                     max(|m|,|n|,|m+n|) <= 5}.
```

Here `|q|=|q-a|=1`: q is one exact unit-circle intersection at the two retained
anchors. T is the complete 91-point triangular disk in this one fixed frame.
The final physical support is **A union T**. No deletion score, point pool,
retained-host relation census or sequence of replacements was queried.
`ARCHITECTURE.json` was frozen before constructing or colouring this support.

A convenient independent Cartesian formula is

```text
q*(m+n*omega) = m/2 - (m+2n)*sqrt(6)/6
               + i*(m*sqrt(2)/2 + (m+2n)*sqrt(3)/6).
```

Its sqrt(2)-containing coefficients vanish together only when `m=n=0`.
Linear independence in the degree-16 field
`Q(sqrt(2),sqrt(3),sqrt(5),sqrt(11))` proves that all 90 nonzero disk points
lie outside K. Hence they are absent from the entire old H632 support, and
`A intersect T={0}` exactly. The pre-query physical budget is therefore

```text
630 - 212 + (91-1) = 508,
net reduction = 122.
```

## Complete geometry and ordinary decision

All 128,778 final pairs are tested exactly. The complete strict graph has:

| Edge type | Count |
|---|---:|
| Retained old--old | 2,095 |
| Old--new | 12 |
| New--new | 234 |
| Total | 2,341 |

The mixed interface is completely reconstructed. Each of the six first-ring
points (`m*m+m*n+n*n=1`) touches the origin and the retained point
`(m,(m+2n)*sqrt(3)/3)`. These six nonzero old anchors have labels
`190,193,196,199,202,205`. No other old--new unit edge exists. The disk itself
has 240 unit edges, six of which meet the shared origin; the other six mixed
contacts are additional anchor contacts.

The complete graph admits the explicit proper four-word in `certificate.json`.
The verifier checks every edge. Its seven-point Moser witness has final
indices `[18,182,33,90,258,47,125]`, in roles `[o,t,a,b,s,d,e]`.
The two checked diamonds force `o=t=s` in any three-colouring, contradicting
the checked edge `t-s`. Therefore the chromatic number is exactly four.
No complete retained-host colouring relation is claimed or inferred.

## Outside the registered containment scopes

The construction inserts 90 points outside the old coordinate field, so it
is not a pure induced subgraph of H630, H632, H560 or H516. It replaces a
whole coordinate block and has a 10-unit physical span.

The checker proves, with exact rational radical bounds, that every archived
H632 point lies in `(-3,3)^2`; hence its squared diameter is strictly below
72. The disk contains three disjoint opposite point pairs at distance 10,
corresponding to addresses `+/- (5,0)`, `+/- (0,5)` and `+/- (5,-5)`.
Thus no isometric copy of H632, H560 or H516 contains the final support.
Even H516 plus one arbitrary point cannot contain it: each of the three
disjoint pairs would need an endpoint outside H516. This establishes the
relevant containment distinction without treating it as chromatic evidence.

## Reproduction

The standalone mathematical check needs only Python 3's standard library:

```bash
python3 verify.py
python3 -O verify.py
```

Both modes agree and reject eleven malformed certificates. `VERIFY.json`
records the result. The checker imports neither the producer nor a solver.
It uses the closed Cartesian formula and sparse square-free-radicand/gcd
arithmetic; the producer uses complex rotation and ordered bitmask
multiplication. It checks all 199,396 archived H632 pairs, the parent five-word,
the complete final graph, collision count, new-field coefficients, geometric
containment witnesses, four-word and Moser lower bound. This is author-side
verification, not a separate teammate review.

For a full-checkout producer replay, with `python-sat` installed (tested with
1.8.dev24 and CaDiCaL195):

```bash
python3 reproduce.py --output /tmp/h630-block-replay
```

The original input JSON files are pinned in `PROVENANCE.json`. Producer replay
regenerates identical final coordinates, edge bytes and four-word. The
source parent's non-four certificate is imported from the reviewed H630
package; it is not assumed to survive the replacement. The new exact
four-colour theorem is checked from positive witnesses alone.

Each CSV point row has eight integer x numerators followed by eight y
numerators, with common denominator 96. **The two CSV bases differ**:

- `h632.csv`: `(1,sqrt3,sqrt5,sqrt15,sqrt11,sqrt33,sqrt55,sqrt165)`;
- `points.csv`: `(1,sqrt2,sqrt3,sqrt6,sqrt11,sqrt22,sqrt33,sqrt66)`.

Final vertices are sorted lexicographically by their 16 integer coefficients;
`certificate.json` supplies every old-label and lattice-address map. Edges use
zero-based final indices. Canonical hashes:

```text
points.csv 0e665d7cf9767d2c0068429e138a686bfdcc8bbc51f310ef27a03763188ac4ee
edges.csv  b5f75973a1319a52ba22dcf1ee256ea075065095637268d0521bb112aafb7fb0
```

This freezes and retires exactly the specified block, anchors, orientation and
disk. No second radius, block, angle, host or replacement was tested. The
[Parts 509-point/2,442-edge construction](https://arxiv.org/abs/2010.12665)
remains the supported unrestricted record; [Haugland v4](https://arxiv.org/html/2608.04542v4)
explicitly retains it. The Discovery ledger remains stale at 4363/RPC 4364;
any later CheckTx-zero receipt is pending until actually indexed.
