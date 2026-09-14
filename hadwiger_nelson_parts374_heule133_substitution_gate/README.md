# The native Parts374–Heule133 substitution is four-colourable

The exact support defined here has **507 distinct plane points and 2,436
complete unit edges**. An explicit proper four-colouring certifies that it
does not retain the five-chromatic obstruction of its positive parent.
This closes one specified construction gate, not a family of placements or
the global sub-509 problem.

## Construction and budget

Heule's [2018 primary paper](https://arxiv.org/abs/1805.12181) gives a
five-chromatic 553-point graph with a 420-point large part and a 134-point
small part, sharing the origin. The coordinate archive's `553.vtx` has this
partition. Replace its entire large part with the first 374 points of the
archived Parts construction, retaining all 133 noncentral small points.
Use the coordinates exactly as displayed in the two sources; apply no
additional rotation, reflection, translation or deletion. The resulting
budget is

```text
553 - 420 + 374 = 507.
```

Precisely, in `K=Q(sqrt(3),sqrt(5),sqrt(11))`, let `sigma` negate `sqrt(5)`
and fix the other two generators. Let `P553` be the native Heule coordinates
and `L374` the first 374 archived Parts points. The selected support is

```text
L374 union {p in P553 : sigma(p) != p},
```

with `sigma` applied to both Cartesian coordinates. The two sets have sizes
374 and 133 and are disjoint. [build.py](build.py) reconstructs the support
and compares every point with [points.json](points.json). The latter stores
sorted 16-integer tuples: eight coefficients for x followed by eight for y,
all divided by 288, in the squarefree-radical basis

```text
1, sqrt(3), sqrt(5), sqrt(15), sqrt(11), sqrt(33), sqrt(55), sqrt(165).
```

The complete edge partition is 1,860 within the large part, 547 within the
noncentral small part, and 29 between them. The support has 15 points outside
the native 711-point Heule catalogue host and 17 outside the 644-point Parts
quadratic-switching host. Those two existing host closures therefore do not
apply by direct containment in their frozen frames. These counts do not
classify containment after other isometries or in other hosts.

## Certificate and verification

[four_colour.txt](four_colour.txt) gives one colour in `0,1,2,3` for each
point in table order. [verify.py](verify.py) reconstructs all
`C(507,2)=128,271` squared distances and checks every physical unit edge
against that word. Its sparse radical multiplication uses
`sqrt(a)*sqrt(b)=gcd(a,b)*sqrt(a*b/gcd(a,b)^2)`. Linear independence of the
eight basis elements makes coefficient comparison exact. There are no
floating-point decisions, omitted contacts or assumed inherited edge lists.

From the repository root, CPython 3.11 or later and the standard library:

```sh
python3 -B hadwiger_nelson_parts374_heule133_substitution_gate/verify.py
python3 -O -B hadwiger_nelson_parts374_heule133_substitution_gate/verify.py
python3 -B hadwiger_nelson_parts374_heule133_substitution_gate/controls.py
sha256sum -c hadwiger_nelson_parts374_heule133_substitution_gate/SHA256SUMS
```

Verification is self-contained in this directory. For the separate source
identification, the following downloads four small, hash-pinned Heule
coordinate files into an external directory:

```sh
python3 -B hadwiger_nelson_parts374_heule133_substitution_gate/build.py \
  --inputs /scratch/hn-parts374-heule133-inputs --download
```

The source reconstruction reuses the existing, hash-pinned catalogue parser.
The new geometry checker imports no producer module. Its entire point and
edge lists were compared entry by entry with the discovery computation;
normal and optimized Python runs agree. Controls cover six elementary
metric fixtures and four malformed-certificate cases. This is author-run
checking, not an independent-author review or proof-assistant formalization.

Canonical edge-stream SHA-256 (compact JSON plus newline):

```text
f6e03736b7aac9fc5753c7b1e3c562beba70d3896d122308922d4860cf0fb73c
```

## Discovery, provenance and stopping boundary

One ordinary four-colour SAT query was run on the whole strict graph, with
four Boolean variables per vertex, exactly-one clauses at each vertex and
four unequal-colour clauses per edge. There were no pins, precolourings or
restricted colouring libraries. Kissat 4.0.4 returned SAT in approximately
0.52 seconds, and the decoded word was checked directly. The 60-second
initial cap was not increased. No further support, phase, omission, host or
terminal-relation search followed the positive colouring.

The verified word makes the solver's soundness irrelevant to the theorem.
The published parent non-four certificate was not replayed and is not a
premise of this negative result. No five-colour or non-four certificate is
claimed for the replacement. The selected substitution is retired; no
continuation is justified merely by the parent's positive signal.

Upstream Heule repository commit:
`bb414955a6ef5f49f7df2b245b1e778aa67c068a`.
The source file `553.vtx` has SHA-256
`7e43a0250f4e54f362ffec98dcc0d364edd06d3d0963931b1ec7c32cc846d4fb`.
The Parts exact table is the existing
[points.tsv](../hadwiger_nelson_parts509_completion_census_degree9/points.tsv),
first published at commit `b892f4b734897d59d357cfccdbfe087d20b7a1a9`.
All imported implementation and input hashes appear in [inputs.json](inputs.json).
[validation.json](validation.json) records the actual checks and environment.

Parts's [509-point, 2,442-edge construction](https://arxiv.org/abs/2010.12665)
remains the working published vertex record. This 507-point four-colourable
support is not record progress.
