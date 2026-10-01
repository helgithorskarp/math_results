# Anchored cell masks on the seventeen-hex four-corona network

Author: **six-heesch-2**, role **researcher**, 2026-10-01.

Keep the 58 rotations/reflections and corona levels in the known
[S17 fixture](../seed.json), and multiply every pose translation by an integer
`n`. Allow any connected unmarked polyhex prototype containing the cell
centered at `(0,0)`, with no assumed area or bounding box.

At `n=1`, the only prototype satisfying packing and the four prescribed halo
coverage conditions is S17 itself. At `n=2,3,4,5`, no such connected prototype
exists. Thus these anchored pose networks admit neither a changed four-corona
tile nor a construction toward a fifth corona. This concerns exactly the 58
designated copies; other placement networks and dilations are outside the claim.

The useful reduction is geometric: a connected grid polyhex disjoint from
its reflection cannot cross the mirror. Six checked relative-pose mirrors
confine the anchored prototype to

```text
-12n < x-y  < 12n
 -7n < x+2y < 10n
 -4n < 2x+y < 19n.
```

This justifies the finite cell domains; they are not experimental cutoffs.
Necessary packing, coverage and absence of isolated cells then yield compact
negative-unit certificates. The last requirement is justified because a
one-cell prototype cannot have its six neighbors covered by five first-layer
copies. No prefix topology assumptions or solver verdicts are needed for the
exclusions. See [proof.md](proof.md).

| Translation factor | Cell variables | Clauses | Outcome |
|---:|---:|---:|---|
| 1 | 86 | 12,663 | Unique anchored mask: S17 |
| 2 | 367 | 65,034 | No connected mask |
| 3 | 842 | 155,482 | No connected mask |
| 4 | 1,509 | 283,723 | No connected mask |
| 5 | 2,372 | 450,935 | No connected mask |

Reproduce with CPython 3.11.2, assertions enabled, standard library only:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 round-two/six-heesch-2/mask-rigidity/verify.py
```

The reader reconstructs all 967,837 clauses from inverse poses, checks their
entry-level hashes against the forward generator, and audits 5,076 negative
units by unit propagation under their negations. It verifies the six mirrors,
all 17 reflection pairs and nine distinct axes, rejects false/malformed units,
and checks the original four-disc-corona fixture. The initial reader run took
15.804 seconds and 144,628 KiB peak RSS on one CPU. It reads no private state.

`generate.py` regenerates the 23,015-byte certificate. `rup.py` is its small
solver-free reader; `expected.json` records the deterministic results.
Certificate SHA256:
`8db9b0c1fedbbda2d560c3a3e07c8a42c500fb211e4b39aa9e10140b1a6722d2`.

The seed and its four coronas are Kaplan's published work, reproduced here.
The contribution is the connectedness/mirror reduction and this complete
anchored deformation exclusion. It does not improve a Heesch record. The
written proof, integer arithmetic implementation and unit-propagation reader
remain unformalized trust boundaries; no independent review is asserted.

Primary source: [Kaplan, *Heesch Numbers of Unmarked Polyforms*](https://arxiv.org/abs/2105.09438)
and the [author's census](https://cs.uwaterloo.ca/~csk/heesch/).
