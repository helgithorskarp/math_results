# Independent review evidence for the Cyclic(43) small-support q=13 closure

This directory contains a clean-room exact checker for the Discovery Net lemma
“Six complete small-support components of the Cyclic(43) objective-thirteen
layer” (`bafkreifhmlyw57avqmyjbom4r2jeds3iu5y3un5mxfada3huq2y4hnsqzy`).

The checker verifies the complete public certificate entry-by-entry. It uses a
different computation from both programs in the reviewed contribution: it
enumerates all \(\binom{43}{5}=962,598\) vertex five-sets, records each set's
ten edges, and updates red-edge counts from the cyclic seed. For every listed
state it derives all 903 flip objectives directly from these five-set color
counts. It then independently reconstructs canonical rotation orbits, the
six connected components, reflection pairs, support and objective histograms,
all internal incidences, and the full 274-entry sublevel payload.

For a five-set with \(r\) red edges, flipping an edge destroys a monochromatic
\(K_5\) exactly when \(r\in\{0,10\}\). It creates one exactly when
\(r\in\{1,9\}\) and the minority edge is flipped. Summing this definition-level
identity over all five-sets gives every one-edge objective without the common-
neighborhood triangle formula used by the reviewed source.

## Reproduce

CPython 3.11 or later is sufficient; there are no third-party dependencies.
From this directory, run one process:

```bash
python3 independent_check.py \
  ../ramsey_r55_cyclic43_q13_small_support_closure/closure_certificate.json \
  ../ramsey_r55_cyclic43_q13_boundary_certificate/boundary_certificate.json \
  /path/to/objective-six-component-representatives.json \
  /path/to/objective-eight-component-fast.json
```

Obtain the last two inputs from the immutable upstream directory:

https://github.com/njallskarp/math_source_code_open/tree/02a959f499aa8e3b749a7f7fb3d3fc5f255c3b14/ramsey_r55_cyclic43

Expected hashes:

```text
85e271af8ebbd55c8bf8e6ad033122911f750a13dc95f638d74681f8c03e4d1e  closure_certificate.json
af8b6892049ace5610e2d7cea4c8642f39f53634287474127990aca0abbe2b85  boundary_certificate.json
aea99967a1a3cc41c640c73c471a73b015259186619495ffa5223968cb48d320  objective-six-component-representatives.json
740c10a6cc72d148ce949749aa8d8f132aa70f9bb0b797ee3e2fbe5ba84fdc1a  objective-eight-component-fast.json
```

Expected headline:

```text
PASS clean-room five-subset verification of small-support q=13 closure
python=3.11.2 five_sets=962598 cpu_processes=1
states=150 components=6 edges=228 cycle_rank=84
component_sizes={'10': 2, '59': 2, '6': 2}
sublevel_targets={'6': 8, '8': 16, '10': 20, '11': 52, '12': 178}
closure_sha256=85e271af8ebbd55c8bf8e6ad033122911f750a13dc95f638d74681f8c03e4d1e
```

The run is deterministic and exact. On the review host, pinned to one CPU
core, the complete checker used CPython 3.11.2, took 23.360 seconds internally
(23.52 seconds wall time), and reached 103,120 KiB peak resident-set size.
Checker SHA-256:

```text
7c4a87748a4adf6bbeb3863382b3433312d711676875a93908457560943cceab  independent_check.py
```

## Scope and trust boundary

This checker establishes that the 150 published states are precisely the
union of the exact-\(q=13\) components reached from the 18 selected parent
seeds and verifies every claimed component, incidence, reflection, and
sublevel-boundary datum. It also verifies the claimed \(q=6\) and \(q=8\)
membership indices against the hash-pinned arrays.

The completeness of the 18-state seed family is conditional on the public
1,785-target parent-boundary certificate. Membership in the previously known
primary \(q=6\) and \(q=8\) layers is conditional on the two external arrays;
this checker does not regenerate those layers. The result is an intermediate
local classification. It does not close the full sublevel-13 component,
construct a Ramsey(5,5,43) graph, prove \(R(5,5)\ge 44\), or change any global
Ramsey bound.
