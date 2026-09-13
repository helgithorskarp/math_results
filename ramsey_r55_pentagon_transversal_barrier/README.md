# A complete-cover countermodel to the pentagon-incidence projection

**The final all-pentagon milestone failed.** No hypothetical good43 class was
excluded, no good43 was verified, and no Ramsey bound changed. This package
preserves an exact reason to stop the tested transversal approach.

The existing seven-defect graph `control43.edges` simultaneously satisfies
the specified global pentagon-cover constraints and every numerical
pentagon-incidence inequality tested here. In particular, **every one of its
1,052,049,481,860 vertex sets of size 21 contains an induced C5**. Its full
pentagon hypergraph is physically realized, with 18,535 pentagons and 12,946
joined-edge pentagon incidences. It nevertheless has one red and six blue
monochromatic five-sets. This is a countermodel to the sufficiency of the
specified necessary system, not a Ramsey graph or a new construction.

[PROOF.md](PROOF.md) defines that system precisely and proves the certificate
join. The new calculation uses the entire pentagon hypergraph and vertex
transversals; it does not extend the component catalogue or solve a physical
edge-color formula. The external `N5=21` theorem explains why the cover
condition is necessary for good43. The control's cover is checked directly
without using that external computation.

The cover certificate is a complete binary decision tree with 408,771 nodes
and 204,386 leaves. Leaf partitions supply exact upper bounds on a pentagon-free
vertex set. A separate checker recognizes pentagons through explicit labeled
cycle patterns, reconstructs every branch, and checks all 688,492 leaf pair
witness conditions. It accepts no search cap, missing child, or heuristic bound.

Using CPython 3.11+ and g++ with C++17 support, run from this directory:

```sh
python3 -B reproduce.py /tmp/new-pentagon-transversal-replay
sha256sum -c SHA256SUMS
```

The scratch directory must be new and outside the repository. Expected status:
`REPRODUCED_FINAL_INCIDENCE_BARRIER`, with `final_gate_met=false` and zero
`global_good43_decisions`. The recorded clean replay took 79.31 seconds;
the independent cover check took 72.09 seconds. [EXPECTED.json](EXPECTED.json)
contains the complete compact output, including all seven physical defects.

The 30,159,116-byte proof is regenerated in scratch and omitted from Git.
Its SHA-256 is
`94a7e9c0fda102dbb0d811a1108c68cd6646450d28e82be0025a087b5372a3a3`.
Source, the small control graph, expected results, and provenance are included.
The proof computation needs no solver, floating point, external catalogue,
private data or omitted input. The unformalized proof, two algorithms,
language semantics and ordinary hardware remain trust boundaries. Author
checks are not independent peer review.

The two-pass all-pentagon trial is exhausted. No quantitatively finishable
all-good43 residual was established. The lane is parked and the slot requires
reassignment within R(5,5); this checkpoint does not authorize a third pass,
a stronger cover threshold, a physical gluing reformulation, or a return to
any earlier queue. No mathematical graph claim is submitted for this failure.
