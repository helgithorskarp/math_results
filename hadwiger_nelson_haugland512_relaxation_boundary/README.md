# The frozen Haugland 512-refinement relaxation is satisfiable

The saved odd-cycle relaxation on **739 Boolean variables and 295,375
clauses is SAT**. The compact certificate supplies a directly checked
assignment. Its corresponding vertex partition cannot be completed to a
four-colouring: the zero part contains the five-cycle

```text
81 -- 4 -- 5 -- 149 -- 473 -- 81
```

in the original pinned Haugland G1 graph.

This resolves the previously unqueried final formula. It proves that these
147,686 odd-cycle constraints are insufficient for the intended refutation,
and that this particular satisfying assignment is not a graph colouring.
It does **not** decide whether G1 admits any four-colouring with equal
endpoints, refute Haugland's published construction, or improve the
509-vertex record. The full endpoint-forcing certificate remains absent.

## The exact reduction and its scope

The source is the fixed 740-vertex, 3,985-edge G1 in the
[exact Haugland reconstruction](../hadwiger_nelson_haugland2131_exact_reproduction/README.md).
Its complete strict edge list is certified by the
[sibling census](../hadwiger_nelson_haugland2131_strict_edges/README.md).
Here the computation operates on that pinned edge list. No coordinates,
points, or unit edges are changed or newly discovered.

Identify the nonadjacent endpoints 0 and 5 to obtain an abstract quotient Q
with 739 vertices and 3,983 edges. Its labels are the original labels with
5 omitted: `q(5)=0`, `q(v)=v` for `v<5`, and `q(v)=v-1` for `v>5`.
A four-colouring of Q is equivalent to a four-colouring of G1 in which the
endpoints agree. **Q is a proof quotient, not a claimed unit-distance drawing.**

Encode four colours as pairs of bits `(x,y)`. A proper four-colouring exists
exactly when some Boolean partition x makes both induced parts bipartite;
a bipartition of each part supplies y. Equivalently, every odd cycle C of Q
must meet both x-parts. Its two Boolean clauses are

```text
OR(x_v : v in C),     OR(not x_v : v in C).
```

The anchor triangle with original labels `(0,13,42)` permits the sound pins
`x_0=x_12=0`, `x_41=1` in quotient order. Any proper four-colouring can have
its three anchor colours renamed `00,01,10`. This is only colour renaming;
no geometric symmetry assumption is imposed.

The frozen formula F contains these pins and the clauses for a finite
subcollection of odd cycles. It began with all 1,051 quotient triangles.
Exactly 512 iterations requested a Boolean model and appended fundamental
monochromatic odd cycles found in its two parts. The last iteration added
293 cycles without another query. F therefore has 147,686 cycles, whereas
the last queried intermediate formula had 147,393. The final F was UNKNOWN
at that earlier boundary.

## Checkable obstruction at the boundary

The new certificate assigns the 739 variables with part sizes 351 and 388.
Every one of F's clauses is satisfied. The quotient five-cycle

```text
80 -- 4 -- 0 -- 148 -- 472 -- 80
```

lies entirely in the zero part. It is the image of the original five-cycle
shown above, and its vertex set is absent from the frozen cycle family.
For any second bit y, one of its five edges is monochromatic in y; it is
already monochromatic in x. Thus **this x cannot extend to a four-colouring**.
The conclusion concerns this explicit partition, not every model of F.

The SAT assignment also proves that F has no sound refutation. Accordingly,
the frozen family cannot establish the endpoint inequality by refutation.
The example settles this truncation boundary without deciding the larger
colouring problem. The missing cycle is recorded as an obstruction witness;
it was not appended as another refinement.

## Verification

[verify.py](verify.py) imports neither the discovery code nor a SAT package.
Using Python's standard library, it checks:

- pinned source, CNF and cycle-archive identities;
- the quotient, its anchor triangle, every saved simple odd cycle, and the
  complete triangle inventory;
- exact equality between the CNF clause multiset and the saved cycle clauses;
- the Boolean certificate against every clause and every saved cycle;
- both five-cycles, their quotient correspondence, their monochromaticity,
  and omission from the frozen family; and
- seven malformed-input controls.

[EXPECTED.json](EXPECTED.json) is the exact output. Solver soundness is not
needed for the SAT conclusion: all literals and edges are checked directly.
Identifying G1 with its geometric realization retains the published source's
exact-coordinate and transcription boundary; this package does not repeat
that geometry proof or claim a new physical graph.

## Reproduce without publishing generated data

The 11,432,915-byte CNF and 5,049,100-byte cycle archive stay outside the
repository. Their deterministic reconstructor and compact certificate are
published. From the repository root, with Python 3.11.2 and the optional
`python-sat==1.9.dev15` dependency installed in a scratch environment:

```sh
/scratch/hn512-venv/bin/python \
  hadwiger_nelson_haugland512_relaxation_boundary/reconstruct_frozen.py \
  /scratch/hn512-frozen
python3 hadwiger_nelson_haugland512_relaxation_boundary/verify.py \
  /scratch/hn512-frozen
```

Create the environment first if needed:

```sh
python3 -m venv /scratch/hn512-venv
/scratch/hn512-venv/bin/pip install -r \
  hadwiger_nelson_haugland512_relaxation_boundary/requirements.txt
```

The output directory must be empty and outside the repository. The
reconstructor replays the archived 512-round computation; it does not
continue beyond it or accept a different resulting formula. Its six helper
functions and all 29 main statements through archive generation are AST
identical to the preserved original implementation. Only path handling and
final identity checks differ, and the unused proof-replay branch is removed.
It was checked against the preserved source rather than rerun during this
closure milestone. The original execution took about 79 seconds; native
solver execution must reproduce the two pinned hashes below. If it does not,
reproduction fails explicitly. SAT solving is used to reconstruct the frozen
artifact, not as a premise of the final certificate check.

If the archived files are already available, only `verify.py` is needed.
No solver is invoked by that verifier.

```text
source graph SHA-256:
201196679760fc329fff548346b843a821646ce5ffc326a91cc24598effc299d
frozen CNF SHA-256:
57058179a7ca8dd5d74c9711f202a53378b1adba9001786687dd92e82d3cf038
frozen cycle archive SHA-256:
bac6fe6962012d4ae5c79e65e9ad5dc39383bfd5c40d651f9cff877ac61b5a63
739-character Boolean word SHA-256:
1002de2d90819965ce5582811915bad4e394134eb94726c3d9ba171918988a04
```

## Resource and claim boundaries

The single new static solve used CaDiCaL 1.9.5, returned SAT in 2.17 seconds
with 3,317 conflicts, and stayed within the unused original allowance.
Combined with the earlier 279,984 conflicts, this is 283,301, below the
original 400,000 discovery cap. No new refinement round, cycle constraint,
geometry pool, or candidate pilot was run. Counts and timing describe this
execution; they are not mathematical premises.

This is a scoped negative certificate for a frozen proof relaxation. Neither
the standard odd-cycle reduction nor the source construction is claimed as
novel. The 512-refinement route is closed and left at this boundary. Any new
mechanism remains subject to the standing requirement for genuine
non-four-colourability evidence before substantial expansion.
