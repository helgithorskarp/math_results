# Degree-support limits for recursive sampling at Albertson `r=27`

This note determines exactly what the currently proved high-degree support
can add to the recursive convex-sampling bound in the sole surviving
`(n,m)=(53,713)` row.  It also tests a current 5-planar crossing line and
identifies a concrete order-25 extremal band whose improvement would close
the row.  It does **not** prove Albertson's conjecture for chromatic number 27.

## Result

Let `F_s(q)` be the recursive convex induced-sampling lower bound obtained
from the universal lines

```text
0,
q-3(s-2),
7q/3-25(s-2)/3,
37q/9-155(s-2)/9,
5q-203(s-2)/9,
6q-266(s-2)/9,
```

with integer rounding at every local graph.  The first five inputs are those
of the preceding recursive certificate.  The last follows from the current
simple 5-planar density bound `7(s-2)` by deleting an edge with at least six
crossings above that density and using the slope-5 line at the threshold.
Exact closure through order 53 still gives

```text
F_53(713)=6071, F_53(714)=6100, F_53(715)=6130.
```

Thus the newer slope-6 line does not improve the surviving row.

Now let `G` be a 27-critical graph with 53 vertices and 713 edges.  Put

```text
x_v=d_G(v)-26,   h=|{v:x_v>0}|.
```

Criticality and the handshake lemma give `0<=x_v<=26` and
`sum_v x_v=48`.  Deleting every vertex from a crossing-minimal good drawing
and applying the order-52 table gives

```text
49 cr(G) >= sum_v F_52(713-d_G(v))
          = sum_v F_52(687-x_v).                  (1)
```

An exact dynamic program over every integral excess multiset gives:

| `h` | minimum sum in (1) | a minimizing excess multiset | conclusion |
|---:|---:|---|---:|
| 10 | 297484 | `0^43,3^6,7^3,9` | `cr(G)>=6072` |
| 11 | 297482 | `0^42,3^8,7^2,10` | `cr(G)>=6072` |
| 12 | 297479 = `49*6071` | `0^41,3^9,7^3` | `cr(G)>=6071` |

The committed structural frontier now proves `h>=10`.  Therefore the method
does give a one-crossing conditional gain in the cases `h=10,11`, but the
proved support statistic alone cannot yield a universal gain: the displayed
`h=12` multiset is feasible in the degree-only relaxation and makes its
objective exactly 6071.  This is a limitation of the relaxation, not an
existence claim for a critical graph with that degree sequence.

## Order-25 sensitivity

The verifier also recomputes the entire closure under three explicit
hypothetical local improvements.

1. The present value is `F_25(152)=242`.  If the single local theorem
   `cr(25,152)>=243` were proved, recursive propagation would give only
   `cr(G)>=6077`.
2. The Pach--Radoicic--Tardos--Toth sparse-line conjecture at the endpoint
   `(25,138)` predicts `cr(25,138)>=173`.  Together with the simple
   4-planar density bound, edge deletion gives `cr(25,q)>=5q-517` for
   `q>=138`.  This improves the present order-25 table by one exactly for
   `q=138,...,152`, but the resulting order-53 floor is still only 6079.
3. A one-unit improvement over the present `F_25(q)` at every
   `q=138,...,163` gives `F_53(713)=6100`, which exceeds
   `Z(27)=6084` and would close the remaining row.

Consequently, neither the current 5-planar line, the high-degree support
count by itself, nor the single classical `(25,138)` endpoint is sufficient.
A successful analytic refinement must use richer incidence/dispersion data
or strengthen a longer part of the active order-25 extremal band.

## Proof of (1)

Every crossing of a good drawing has four distinct endpoints, so it survives
in exactly 49 of the 53 one-vertex deletions.  The inherited drawing of
`G-v` has at least `F_52(713-d_G(v))` crossings.  Summing these 53 inequalities
proves (1).  The dynamic program is an exhaustive finite minimization over
53 integers in `[0,26]`, their sum 48, and their positive support size.

The recursive step is the standard induced-sampling double count followed by
the greatest convex minorant and Jensen's inequality.  The verifier constructs
the closure with exact rational arithmetic; no floating-point comparison is
used.

## Reproduction and trust boundary

Run with CPython 3.9 or later; there are no third-party dependencies:

```sh
python3 verify.py
```

Expected first line:

```text
PASS Albertson r=27 degree-support limitation audit
```

SHA-256 of `verify.py`:
`1fd16f9fb1460752619438ed9e8cac8f70b4168a277ae4b24ed2cebc3eaad55f`.
The enhanced recursive-table digest printed by the verifier is
`55da0a3d413620951dba0ac52618fa24f09d59de43a0c7e8a0f3927283036f43`;
its equality with the preceding certificate's digest independently confirms
that the slope-6 line changes no table entry through order 53.

The executable trust boundary is CPython arbitrary-precision integers,
`fractions.Fraction`, and binomial coefficients.  The code uses no solver,
randomness, external data, floating point, or project import.  It proves the
finite arithmetic and optimization statements, not the imported topological
crossing inequalities.

The mathematical trust boundary consists of good-drawing normalization; the
universal linear crossing bounds; the 5-planar density theorem; the standard
4-planar density theorem; the September 2026 order-53 frontier; and the
committed `h>=10` structural reduction.

## Sources and novelty scope

- A. Büngener and M. Kaufmann, [*Improving the Crossing Lemma by
  Characterizing Dense 2-Planar and 3-Planar
  Graphs*](https://arxiv.org/abs/2409.01733v2), Theorem 6.
- A. Büngener, J. Franz, M. Kaufmann, and M. Pfister, [*A First View on the
  Density of 5-Planar Graphs*](https://arxiv.org/abs/2505.24364v3),
  Theorem 4 and its displayed slope-6 consequence.
- J. Pach, R. Radoicic, G. Tardos, and G. Toth, [*Improving the Crossing
  Lemma by Finding More Crossings in Sparse
  Graphs*](https://doi.org/10.1007/s00454-006-1264-9), especially
  Conjecture 5.7.
- A. Sadhu, [*Albertson's Conjecture Holds for `r` at Most
  26*](https://arxiv.org/abs/2609.01682v1), for the two-order frontier.
- The preceding [recursive convex-sampling
  certificate](../albertson_r27_recursive_convex_sampling/README.md) and
  [`h>=10` closure](../albertson_r27_order53_h9_closure/README.md).

Targeted primary-literature and committed-graph searches found no prior
statement of this degree-support optimization, the slope-6 non-improvement,
or the order-25 sensitivity thresholds.  This is a search-relative novelty
assessment, not a claim of historical priority.
