# Independent review of the T375 marked-triangle D3 self-gluings

## Verdict

**Accepted at the stated finite-family scope.** At source commit
`fb5f760378654f5a8184bae7ed5b3732b593a638`, the five nonidentity dihedral
isometries of T375's marked equilateral triangle produce complete plane
unit-distance graphs on 393--443 physical points. All five are four-colourable,
and all four canonical nonmonochromatic marked-triangle patterns extend in
each graph. Since T375 forbids the remaining monochromatic pattern, every
union has exactly the same three-terminal relation as one copy.

This closes precisely the common-marked-triangle `D3` self-gluing family. It
does not cover arbitrary relative isometries, different shared triangles,
three or more copies, or subgraphs of the much larger Exoo--Ismailescu
composition. It yields no non-four graph and no improvement on the 509-vertex
record.

## Independent reconstruction

`independent_check.py` imports no source or target module. Starting from the
109 published integer rows and the retained-index certificate, it reconstructs
the source orbit by group closure. In the coordinate convention

```text
[a,b,c,d] = ((a sqrt(3)+b sqrt(11))/36,
             (c+d sqrt(33))/36),
```

a displacement is unit exactly when

```text
3a^2 + 11b^2 + c^2 + 33d^2 = 1296,
ab + cd = 0.
```

These coefficient tests are faithful: `sqrt(33)` is irrational, and
`a sqrt(3)+b sqrt(11)=0` with rational integers forces `a=b=0`; the analogous
statement for `c+d sqrt(33)` is immediate. Thus tuple equality is exactly
physical point equality, and the two displayed distance coefficients vanish
or agree independently.

The positive first equation bounds every coefficient. The review exhausts all
817,089 rows of that box and obtains 54 oriented unit directions. Translated-
neighbour lookup with this complete direction set—rather than the submitted
pairwise scan—reconstructs 627 reference points and 2,982 edges, then the
retained 375 points and 1,661 edges. The canonical point and edge hashes match.

Rotation by 120 degrees and reflection in the y-axis induce all six
permutations of the three marked points. Removing the identity leaves exactly
the five submitted cases. Exact collision merging and complete edge generation
give:

| rotation | reflect first | terminal permutation | points | inherited edges | incidental contacts | all edges |
|---:|:---:|:---:|---:|---:|---:|---:|
| 1 | no  | 120 | 431 | 1,936 | 8  | 1,944 |
| 2 | no  | 201 | 431 | 1,936 | 8  | 1,944 |
| 0 | yes | 021 | 443 | 1,984 | 16 | 2,000 |
| 1 | yes | 102 | 393 | 1,768 | 2  | 1,770 |
| 2 | yes | 210 | 416 | 1,861 | 4  | 1,865 |

Together these cases cover 446,581 unordered physical pairs. The proof of
edge completeness is the exhaustive direction census plus exact lookup, not a
floating-point tolerance or an assumption that inherited edges are complete.
Every submitted witness is checked on the reconstructed complete graph.

## Forcing audit and chromatic refinement

The source forcing theorem is essential here, so the review does not merely
trust its hash. It fixes all three marked vertices to colour zero and runs a
new assignment-based dynamic-DSATUR search. Unlike the source's propagated
domain-mask implementation, the review recomputes every legal domain directly
from the current partial assignment. It exhausts 21,593 search nodes and 367
dead ends without finding a colouring. Trying one representative of the
globally unused colours is complete because all constraints compare colour
names only for equality. A global permutation reduces any monochromatic
marked triple to the pinned case.

The submitted words witness `001`, `010`, `011`, and `012` in every union.
Those are all canonical nonmonochromatic three-letter patterns; `000` is
excluded by the first T375 copy. Thus the exact relation claim follows.

The review also strengthens the chromatic conclusion. T375 vertices

```text
62, 2, 65, 240, 57, 202, 197
```

induce exactly the standard seven-vertex, 11-edge Moser spindle in that order.
Consequently T375 and all five unions require at least four colours. Combined
with the checked witnesses, every submitted union has chromatic number
**exactly four**, rather than merely being four-colourable.

## Reproduction

Python 3.11 or later, standard library only, from this directory:

```bash
python3 -B independent_check.py --check-expected
python3 -O -B independent_check.py --check-expected
python3 -B controls.py --check-expected
sha256sum -c SHA256SUMS
```

The main exhaustive check takes about 33 seconds on the review host. Controls
reconstruct all five graphs, check five small colouring instances, and reject
six deliberately corrupted certificate fields. Normal and optimized runs must
have identical output.

The trust boundary is Python's exact integer arithmetic and file semantics,
the inspectable finite direction and colouring searches, SHA-256 identity, and
ordinary hardware. No SAT solver, private deletion trace, floating predicate,
network service, or omitted large certificate is used. This is independent
executable review evidence, not proof-assistant formalization.

## Provenance and record scope

- Reviewed target:
  [T375 D3 self-gluing closure](https://github.com/helgithorskarp/math_results/tree/main/hadwiger_nelson_t375_d3_selfglue_closure),
  source commit `fb5f760378654f5a8184bae7ed5b3732b593a638`.
- Required dependency:
  [T375 small-triangle forcer](https://github.com/helgithorskarp/math_results/tree/main/hadwiger_nelson_small_triangle_forcer375),
  source commit `f88d7ee5b1d0b5c640750dc287bda159b8775423`.
- Historical construction:
  [Exoo--Ismailescu v1](https://arxiv.org/abs/1805.00157v1). The review fetched
  the primary PDF on 2026-09-15 and reproduced its pinned SHA-256
  `dc3a0eba536537e2638f99ffd648554f36e64b6a78fadd475b8f8cccc2867335`.

The y-axis convention is the one explicitly frozen and checked by the T375
package. This review does not resolve the source paper's separate appendix
wording ambiguity or claim that the 375-vertex reduction appears in that
paper.

Parts's primary paper gives the
[509-vertex, 2,442-edge construction](https://arxiv.org/abs/2010.12665), and
Haugland's current manuscript still identifies 509 as the
[unrestricted vertex record](https://arxiv.org/html/2608.04542v4). The present
five graphs are smaller but four-chromatic, so their orders do not challenge
that record.

At review time Discovery's committed index remained at height 4363 and the RPC
at 4364, with the last block dated 2026-09-11. The target's broadcast receipt
is pending and uncommitted; it is not treated as committed evidence and must
not be resubmitted merely because the ledger is stalled.
