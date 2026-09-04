# Four complete minimum-degree cycle-only components at Cyclic(43) objective thirteen

The two noncycle families in the certified Cyclic(43) objective-thirteen
boundary close at modest exact-level sizes, but the remaining 1,381
cycle-only exits expand much more rapidly.  This directory isolates and
closes the exact finite frontier visible at the bottom of that expansion:
all cycle-only parent exits having only one or two objective-thirteen flips.

There are exactly four such exits.  They generate four complete components
of the global exact-`q=13` graph in the `C_43` rotation quotient: two
reflection-paired 2-state components and two reflection-paired 16-state
components.  A separately reproducible 10,000-source breadth-first prefix
also records why bulk closure of the remaining cycle-only family was not a
credible target for this pass.

## Setting and exhaustive seed selection

Use the lexicographic edge order on `K_43` and the fixed circulant seed whose
red cyclic lengths are

```text
{1,2,7,10,12,13,14,16,18,20,21}.
```

A state records toggles from this seed.  We quotient by cyclic rotation and
choose the least tuple of 15 little-endian 64-bit words.  Let `q(G)` count
monochromatic `K_5`s.

The parent boundary contains 1,381 cycle-only `q=13` orbits.  Scanning all
903 flips at every one gives the exact `q=13`-degree histogram

```text
1^2, 2^2, 3^34, 4^121, 5^188, 6^210,
7^214, 8^146, 9^200, 10^164, 11^86, 12^14.
```

Thus the rule “retain all cycle-only parent exits of `q=13` degree at most
two” selects exactly four states, with no discretionary choice.

## Four-component closure theorem

Exhausting every exact-level move from those four seeds produces exactly 36
free `C_43` orbits.  Every `q=13` neighbor remains cycle-only and is present
in the certificate.  The quotient graph has

```text
4 components
54 edges
cycle rank 22
component sizes 16^2, 2^2.
```

Each 16-state component has 26 edges and cycle rank 11; each 2-state
component is a single edge.  Reflection `v -> -v (mod 43)` pairs the two
components of each size and fixes no state or component.

Although only four parent exits satisfy the selection rule, the closure
contains eight parent exits in total.  Their original `q=13` degrees have
histogram

```text
1^2, 2^2, 3^2, 4^2.
```

The two selected degree-two seeds lie in the 16-state components; each such
component contains three parent seeds.  The selected degree-one seeds lie in
the two-state components, one parent seed apiece.

All `36*903 = 32,508` flips were checked.  Exactly 108 directed incidences
remain at objective thirteen and pair to the 54 quotient edges.  The complete
sublevel boundary consists of

```text
q=10: 6 distinct endpoints and 6 incidences
q=11: 22 distinct endpoints and 22 incidences
q=12: 74 distinct endpoints and 74 incidences.
```

The 102 endpoint representatives are stored entry-for-entry.  The minimum
neighbor-objective histogram over the 36 sources is

```text
10^6, 11^18, 12^12.
```

## Precise negative result for bulk cycle-only closure

The file `growth_10000.json` records a deterministic FIFO breadth-first
prefix starting from all 1,381 cycle-only parent exits in canonical order.
After processing the first 10,000 states, exact computation had reached

```text
26,651 distinct q=13 orbits,
16,651 states still in the queue,
72,335 directed q=13 incidences from processed states.
```

Every reached state was still cycle-only.  The queue was growing, not
contracting.  This proves the full seed closure has at least 26,651 orbits
and that the declared 10,000-source search did not close.  It does **not**
claim that the full component is infinite, estimate its final size, or prove
that later states can never leave the cycle-only support stratum.

The growth record includes all 40 checkpoints and SHA-256 commitments to the
10,000-state processing order, sorted reached set, and residual FIFO queue.
This makes the negative stopping evidence deterministic and reproducible
without presenting it as a completed closure theorem.

## Proof computation

For a flipped edge `e=uv`, let `R_e` count red triangles in
`N_R(u) intersect N_R(v)` and define `B_e` analogously.  The exact delta is

```text
q(G flip e) = q(G) - R_e + B_e,  if e is red,
q(G flip e) = q(G) + R_e - B_e,  if e is blue.
```

`generate_closure.py` first rescans all 1,381 candidate seeds, then performs
complete breadth-first closure from the four selected states and writes all
36 sources, all 102 sublevel endpoints, every component profile, and the full
flip-objective histogram.

`verify_closure.py` imports no generator code.  It uses the independently
written standard-library color/rotation engine and the edge/common-neighbor
triangle identity from the preceding medium-family verifier.  It separately
rescans the 1,381 seed degrees, proves the selection rule identifies exactly
the stored four states, and then regenerates the entire closure and boundary
entry-for-entry.  `measure_growth.py` is a deterministic implementation of
the explicitly capped full-family prefix.  All programs use exact integer
arithmetic and no randomness, floating point, solver, native extension, or
network input during execution.

## Reproduction

Python 3.11 or later is sufficient.  From this directory:

```bash
python3 generate_closure.py \
  ../ramsey_r55_cyclic43_q13_boundary_certificate/boundary_certificate.json \
  closure_certificate.regenerated.json

cmp closure_certificate.json closure_certificate.regenerated.json

python3 verify_closure.py \
  ../ramsey_r55_cyclic43_q13_boundary_certificate/boundary_certificate.json \
  closure_certificate.json

python3 measure_growth.py \
  ../ramsey_r55_cyclic43_q13_boundary_certificate/boundary_certificate.json \
  growth_10000.regenerated.json

cmp growth_10000.json growth_10000.regenerated.json

python3 -m unittest -v test_closure.py
```

Expected closure headline output is

```text
parent_seeds=1381 selected=4 states=36 components=4
edges=54 cycle_rank=22 component_sizes={'16': 2, '2': 2}
sublevel_targets={'10': 6, '11': 22, '12': 74}
```

Expected growth headline output is

```text
PASS processed=10000 reached=26651 queue=16651 closed=False directed=72335
```

On the research host with CPython 3.11.2, generation took 33 seconds, the
independent closure verification took 50 seconds, the 10,000-source prefix
took 418 seconds, and the five focused tests took 0.3 seconds.

Pinned and generated evidence hashes are

```text
af8b6892049ace5610e2d7cea4c8642f39f53634287474127990aca0abbe2b85  parent boundary_certificate.json
66ddc8576a84165926b51c589206a9276baf3e0a2ef27dc06db0fe96a6e5cf7b  closure_certificate.json
74549ccee598de6cc00285e7bf706d612325db2c344a99d6a17d445309486725  growth_10000.json
0bde95c58a6a8dea8c173457d88fe6c4f08734f391e22d549e2d0987a0c3c976  generate_closure.py
9151e0f6d121097c060dee92939f78d013b9268603d635f4948d095aebdd60b5  verify_closure.py
c240b5a98fe02cd477cfb808a19e2ee588e73dfe76d80548129927f54d6ed334  measure_growth.py
d888bb3144e308d09c8b599e90aa3c9477efacca2c238f69c4a004f142478f4b  test_closure.py
```

## Scope and significance

The theorem is conditional on the parent 1,381-state cycle-only exit set,
whose completeness is inherited from the public independently reproduced
boundary certificate.  It closes exactly the components meeting all parent
seeds of `q=13` degree one or two.  It does not classify components meeting
the other 1,373 parent seeds, close the full primary sublevel-thirteen basin,
classify disconnected low-objective colorings, construct a `K_5`-free
coloring of `K_43`, or alter the bounds on `R(5,5)`.

This is the first exact component result inside the remaining cycle-only
family.  It turns a failed bulk-closure attempt into a rigorous frontier:
four components are now complete, the minimum-degree tail is exhausted, and
the quantified expansion shows that future work should proceed component by
component or with a more scalable cycle-subcube method.

Ge, Jayasooriya, Qiu, Sun, and Yuan's
[*Study of Exoo's Lower Bound for Ramsey number R(5,5)*](https://arxiv.org/abs/2212.12630)
studies nearby changes to the same Cyclic(43) coloring but not this quotient
component census.  Angeltveit and McKay's
[*R(5,5) <= 46*](https://arxiv.org/abs/2409.15709) addresses a different
global census.  Novelty is claimed relative to the searched public sources
and refreshed Discovery Net, not as a historical-priority claim.
