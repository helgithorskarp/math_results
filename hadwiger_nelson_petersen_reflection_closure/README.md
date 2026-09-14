# Petersen common-neighbour reflection closure

This package freezes one geometry-first Hadwiger--Nelson construction gate.
It constructs a strict plane unit-distance graph on **290 distinct points and
865 edges**, proves its chromatic number is exactly **four**, and determines
its complete unrestricted four-colour relation on the ten original Petersen
vertices.

The relation is **neutral**: all **540** colour-partition patterns allowed by
the bare Petersen graph extend to the 290-point graph.  The next simultaneous
closure round has 2,085 points, above the declared 508-point budget.  Thus the
source is retired.  There is no five-chromatic graph here, no improvement on
the 509-vertex record, and no exclusion of other common-neighbour sources.

## Exact construction

Let `t=exp(pi*i/10)`, a primitive twentieth root, and work in
`Q(t)` with

```text
Phi_20(t) = t^8-t^6+t^4-t^2+1 = 0.
```

Put `zeta=t^4`,

```text
c = 1/(zeta-1) = -(4+3*zeta+2*zeta^2+zeta^3)/5,
phi = t^2+t^(-2).
```

The base, in terminal order, is

```text
outer_k = c*zeta^k,
inner_k = i*c*(phi-1)*zeta^k,     0 <= k < 5.
```

Its complete unit graph is exactly the Petersen graph: the outer five-cycle,
the inner step-two five-cycle, and five spokes.

For a finite physical support `S`, define one simultaneous reflection round

```text
R(S) = S union {p+q-r : p-r and q-r are distinct unit vectors in S-S}.
```

The added point is at unit distance from both `p` and `q`.  Coincident points
are merged.  Crucially, after every round the code discards the generating
incidence list and reconstructs **every** unit pair from the coordinates.
Starting from `S0`, the exact census is:

| support | points | strict unit edges | unit two-paths | next round |
|---|---:|---:|---:|---:|
| `S0` | 10 | 15 | 30 | 40 |
| `S1` | 40 | 75 | 390 | 290 |
| `S2` | 290 | 865 | 7,320 | 2,085 |

`S2` is triangle-free.  A deterministic exhaustive three-colour search,
after a sound colour-permutation pin on one edge, closes in 11 recursive
nodes.  Each of the 540 supplied words is a directly checked proper
four-colouring, so the chromatic number is exactly four.

## Complete terminal relation

Patterns are restricted-growth strings on the ten base vertices, so they
encode colour partitions up to global colour permutation.  At most four
blocks are allowed.  Exactly 540 patterns respect all 15 Petersen edges.
`certificate.json` contains one 290-symbol proper colouring for every such
pattern.  The checker enumerates the bare relation independently, rejects
duplicates or omissions, checks all 467,100 word-edge inequalities, and
checks the ten terminal colours of every word.  Consequently every bare
pattern extends, with no solver premise.

This is a complete relation only on the declared ten terminals.  It says
nothing about other terminal choices in `S2`, selected subassemblies of the
over-budget `S3`, deformations, or nonsimultaneous growth.

## Reproduce

Final verification needs CPython 3.11 or later and the standard library only:

```bash
python3 -B verify.py --certificate certificate.json --check-expected --controls
python3 -O -B verify.py --certificate certificate.json --check-expected --controls
```

The verifier imports no producer module.  It tests a squared distance by
forming a Laurent polynomial and dividing it by `Phi_20`, rather than using
the producer's quotient-field multiplication.  It regenerates every closure
point, reconstructs all pairwise unit contacts, exhausts three-colourings,
and checks all positive relation words.  Six damaged-certificate controls
must be rejected.

Optional certificate regeneration uses
`python-sat==1.9.dev15` and CaDiCaL 1.9.5:

```bash
python3 -m venv /tmp/hn-petersen-venv
/tmp/hn-petersen-venv/bin/pip install -r requirements-discovery.txt
/tmp/hn-petersen-venv/bin/python produce.py --output certificate.generated.json
cmp certificate.json certificate.generated.json
```

The SAT solver only discovers positive words.  No UNSAT result, proof trace,
floating-point predicate, external graph file, or omitted large artifact is
used by the final verifier.

The compact certificate is 181,601 bytes with SHA-256
`1ca143efc5ef185c78c7e293b56a3cf057b9c35c44f5ce893d9ff2911a6e6862`.
The point and complete-edge stream hashes are respectively
`657a8b97bee69ce87f1451257c2690f8351275cf33916cfd49793f52cf151fe3`
and
`f6e4b473a84e0379178606661243d94162008452e9d6a2b47c95f09dd6f74c20`.

## Scope and campaign context

This was the first declared incidence family under the R4 geometry-first
gate.  The at-most-508 member has a positive four-colouring and a neutral
complete interface, so the prescribed stop rule fires without widening or
pivoting to another source in the same pass.  The result is a finite
construction checkpoint, not a restricted-family lower bound for the plane.

[Parts's primary source](https://arxiv.org/abs/2010.12665) gives the exact
509-vertex, 2,442-edge five-chromatic construction used as the order record.
[Haugland's 2026 paper](https://arxiv.org/abs/2608.04542) concerns the distinct
Moser-spindle-free restriction and does not improve that unrestricted order.
The live primary-source and team-evidence refresh on 2026-09-14 found no
published sub-509 replacement; this is a working literature conclusion, not
a proof about unpublished graphs.

See [PROOF.md](PROOF.md) for the exact argument and trust boundary.
