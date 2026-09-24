# Square saturation of the hypercube: upper constant seven

**Complete proof attempt; independent external review pending.**

An explicit construction gives

$$
\limsup_{n\to\infty}\frac{\operatorname{sat}(Q_n,Q_2)}{2^n}\le7,
\qquad
\liminf_{n\to\infty}\frac{\operatorname{sat}(Q_n,Q_2)}{2^n}\le\frac{11}{2}.
$$

Here square saturation means that no four-cycle is present and adding any
missing cube edge creates one. The proof is in [proof.md](proof.md).
It supplies a deterministic construction for every dimension at least six
and the explicit estimate

$$\operatorname{sat}(Q_n,Q_2)<\left(7+\frac{48}{n+2}\right)2^n.$$

The mechanism is a syndrome graph on $q=2^t$ points with $2q-4$ edges.
It has two disjoint independent dominating sets of sizes one and two, and
every missing edge incident to their union has an affine-square witness.
Hamming lifts of this finite template feed a parity construction in two
coordinate blocks. Only $9\cdot2^n/(pq)$ exceptional vertices require
greedy completion. Choosing unequal block lengths removes the worst
loss between consecutive powers of two.

For any powers of two $p,q\ge4$ with $p+q-2\le n$, the precise coefficient
proved here is

$$F(n;p,q)=\frac52+\frac{3n-13}{4}\left(\frac1p+\frac1q\right)+\frac{9n}{pq}.$$

No exact value of $\operatorname{sat}(Q_7,Q_2)$ or asymptotic optimality is
claimed. The small expanded instances below validate the construction;
they are not claimed as improved finite upper bounds.

## Reproduce

Python 3.11 or later, standard library only. From this directory:

```bash
python3 verify_template.py > /tmp/upper7-template.json
diff -u EXPECTED_TEMPLATE.json /tmp/upper7-template.json
python3 verify.py > /tmp/upper7-verification.json
diff -u EXPECTED_OUTPUT.json /tmp/upper7-verification.json
sha256sum -c SHA256SUMS
```

Generate and check a single expanded witness, or obtain a bound without
expanding an exponentially large graph:

```bash
python3 construct.py --dimension 10 > /tmp/upper7-q10.json
python3 verify.py /tmp/upper7-q10.json
python3 construct.py --dimension 1000000 --bound
```

The last command returns blocks `[524287,262143,213570]` and coefficient
`14584809809/2147483648`. The generator caps expansion at dimension 16;
the mathematical construction has no such restriction. Keep generated
edge lists outside the repository.

## Validation and trust boundary

The template audit checks all affine square cycles for
$q=4,8,16,32,64,128$, both independent dominating sets, all missing edges
incident to their union, and exact rational endpoint formulas through
dyadic exponent 60.

The expanded-construction suite contains nine instances. Its edge counts are:

| Block lengths `(a,b,r)` | Dimension | Selected edges |
|---|---:|---:|
| `(3,3,0)` | 6 | 115 |
| `(3,3,1)` | 7 | 259 |
| `(3,3,2)` | 8 | 571 |
| `(3,3,3)` | 9 | 1252 |
| `(3,7,0)` | 10 | 2726 |
| `(7,3,0)` | 10 | 2592 |
| `(7,3,1)` | 11 | 5701 |
| `(3,7,2)` | 12 | 12423 |
| `(7,7,0)` | 14 | 50723 |

The constructor uses square-face incidence to complete and check each graph.
The independent checker imports none of that code: it reads the resulting
edge list, builds vertex adjacency, rejects four-cycles, and checks a
three-edge path for every missing cube edge. It checks 76,362 selected edges
and 88,374 missing edges across the suite. Duplicate-edge, empty-graph, and
full-cube negative controls are rejected. Edge-list hashes and all expected
outputs are in [EXPECTED_OUTPUT.json](EXPECTED_OUTPUT.json) and
[EXPECTED_TEMPLATE.json](EXPECTED_TEMPLATE.json).

The full suite reproduced under Python 3.11.2 in 2.62 seconds,
with 156,640 KiB peak child RSS on the recorded host.

The universal statement rests on the written proof, not on sampling finitely
many dimensions. Its unformalized bridges are the syndrome lifting argument,
the parity case analysis, and the counting argument. The finite checker is
independent of the construction implementation, but this is not an external
peer review. No solver or floating-point result is a proof assumption.

## Prior work and graph context

[Johnson and Pinto, *Saturated Subgraphs of the Hypercube*](https://arxiv.org/abs/1406.1766),
Section 4.2, state the upper bound $10\cdot2^n$ and a bound $6\cdot2^n$ on
a Hamming-length subsequence. Their two-block parity method is the starting
point for this construction. The changes here are the two-coset second
dominating set, the explicit boundary-witness property, and unequal Hamming
block lengths. The complete argument is provided locally.

[Morrison, Noel and Scott](https://arxiv.org/abs/1408.5488) establish the
$\Theta(2^n)$ scale for every fixed forbidden subcube.
Primary-source and exact-phrase searches refreshed on 2026-09-24 found no
earlier statement of the constants seven or $11/2$ from this construction.
This supports an apparently new result in the searched sources, not a
priority claim.

Graph source: `bafkreigkl27efnd3pt7fkz3igzslgxevezlbxkp7qorifc4cekw6ol3kgm`.
The existing [208-edge Q7 construction](../hypercube_square_saturation_q7/README.md)
and [432-edge Q8 product lift](../hypercube_square_saturation_lift_q8/README.md)
motivated this investigation. Neither their optimality certificates nor
their classifications are assumptions of the proof above.
