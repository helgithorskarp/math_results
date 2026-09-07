# Every target-sized high-contact completion of T375 is four-colourable

Let `T` be the exact 375-vertex, 1,661-edge graph from
[`hadwiger_nelson_small_triangle_forcer375`](../hadwiger_nelson_small_triangle_forcer375/README.md).
Its points lie in the integer coordinate lattice

\[
\Lambda=\left\{\left(\frac{a\sqrt3+b\sqrt{11}}{36},
\frac{c+d\sqrt{33}}{36}\right):a,b,c,d\in\mathbb Z\right\}.
\]

Let `C` contain every point of `Lambda` outside `T` that is unit distance
from at least one point of `T`, and write `degree_T(q)` for its number of
unit neighbours in `T`. Define

```text
H = T union {q in C : degree_T(q) >= 6},
P = {q in C : degree_T(q) = 5}.
```

**Exact result.** The strict unit-distance graph on `H union X` is
four-colourable for every subset `X` of `P` with at most two elements.
There are 131 added points in `H`, so `H` has 506 vertices. The next band
`P` has 141 points. The theorem therefore decides

```text
1 + 141 + C(141,2) = 10,012
```

physical graphs of orders 506, 507 and 508, including all 9,870 choices at
the target order. Every graph includes every unit edge among its chosen
points. The 508-vertex members have between 2,687 and 2,695 edges.

No five-chromatic graph was found. This closes the one-step integral
high-contact family; it is not an assertion about arbitrary completion
points, lower-incidence selections, or other geometric wrappers around T.

## Complete geometric enumeration

For an integer difference row `[a,b,c,d]`, squared distance one is equivalent
to

```text
3a^2 + 11b^2 + c^2 + 33d^2 = 1296,
ab + cd = 0.
```

The first equation bounds every coefficient, so a finite nested integer loop
enumerates all possibilities. There are exactly 54 oriented unit directions.
Adding them to all 375 points of `T`, deduplicating, and removing `T` gives
exactly 12,184 completion points. Their incidence distribution is

| `degree_T` | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| points | 9,615 | 1,482 | 529 | 286 | 141 | 71 | 21 | 16 | 18 | 5 |

Thus all 131 points of degree at least six fit beside T at order 506. The
degree-five band is the first tied band that cannot be included in full under
the 508-vertex budget, which is why every two-element choice is tested.

The strict graph on the 506-point core has 2,677 edges. Across all 141
optional points there are 868 optional-to-core edges and 81 edges within the
optional band. The verifier reconstructs these counts and the complete edge
sets exactly.

## Eight-colouring certificate

The certificate contains eight proper colourings of the 506-vertex core. For
a core colouring `f` and an optional point `q`, put

\[
A_f(q)=\{0,1,2,3\}\setminus\{f(v):v\in H,\ |v-q|=1\}.
\]

A singleton extension exists exactly when `A_f(q)` is nonempty. A pair
`q,r` extends unless one of these sets is empty, or `q,r` are adjacent and
both available sets are the same singleton. This is a complete condition:
choose any available colours, choosing distinct ones only when the optional
pair is an edge.

In certificate order, the eight core colourings cover respectively

```text
9,179; 9,315; 9,452; 9,590; 9,729; 9,729; 9,452; 9,044
```

of the 9,870 pairs. Their new contributions to the running union are

```text
9,179; 136; 137; 138; 139; 139; 1; 1.
```

The union is every pair. It also gives a nonempty available set for every
single optional point, while any one core row colours the empty selection.
The SHA-256 of the first covering-row index for all pairs in lexicographic
order is

```text
acb69e6ee2b01076cec61cefde51506a2b3609e2ddf8326b1e75fbfaa572ead3
```

This positive witness proof uses no negative solver answer. The optional
producer uses CaDiCaL 1.9.5 through `python-sat` to obtain a colouring for the
first pair not covered by the current library. Every new row covers that
trigger pair, so the process must either enlarge the cover or expose a target
candidate. It terminated with the eight rows above.

## Independent verification

`verify.py` uses Python's standard library and imports no producer or sibling
implementation. It:

1. reconstructs the 627-point Exoo–Ismailescu orbit from the pinned appendix
   and selects the 375 T vertices;
2. recomputes all 1,661 T edges and their canonical hashes;
3. enumerates the 54 unit directions and all 12,184 completion points;
4. recomputes the incidence histogram and the 647-point degree-at-least-five
   support;
5. scans all 208,981 support pairs with the exact squared-distance equations;
6. checks every core colouring on all 2,677 core edges and verifies every
   singleton and pair extension; and
7. rejects seven malformed-certificate controls.

Normal and optimized Python runs produce exactly `expected.json`. The trust
boundary is the written finite reduction, faithful parent coordinate data,
Python integer arithmetic, complete finite loops, and direct colour checks.
No floating-point predicate, SAT soundness premise, proof trace, or large
generated artifact is required.

## Reproduction

From this directory, using Python 3.11 or later:

```sh
python3 verify.py
python3 -O verify.py
sha256sum -c SHA256SUMS
```

To regenerate the eight-row certificate, install the optional pinned search
dependency outside the repository and run:

```sh
python3 -m venv /scratch/t375-high-contact-venv
/scratch/t375-high-contact-venv/bin/pip install -r requirements.txt
/scratch/t375-high-contact-venv/bin/python build_certificate.py
```

The source construction is Exoo and Ismailescu,
[arXiv:1805.00157v1](https://arxiv.org/abs/1805.00157v1). The campaign's
509-vertex comparison is Parts,
[arXiv:2010.12665](https://arxiv.org/abs/2010.12665), also stated in Haugland's
current manuscript, [arXiv:2608.04542v4](https://arxiv.org/html/2608.04542v4).
No record or priority claim is made. The new HN-2 scope consolidation was
inspected for coordination and is not a premise of this construction.

## Files

- `certificate.json`: eight core colourings, exact counts, and canonical
  hashes.
- `verify.py`: independent exact geometry and colouring-cover checker.
- `build_certificate.py`: optional deterministic certificate producer.
- `expected.json`: canonical verification output.
- `provenance.json`: pinned inputs and source context.
- `validation.json`: recorded interpreter, solver-discovery, and checker scope.
- `requirements.txt`: optional producer dependency only.
