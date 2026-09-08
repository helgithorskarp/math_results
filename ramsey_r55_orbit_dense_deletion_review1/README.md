# Independent review of the h3975 orbit-dense deletion exclusion

Verdict: **ACCEPT subject to the imported Angeltveit--McKay
`R(5,5)<=46` theorem.** Every declared orbit-dense 43-vertex induced
subgraph is excluded. The Paley(53) subfamily has a separate unconditional
finite cover certificate. This is a complete decision of the two stated
source families, not a good43 construction or a proof that `R(5,5) >= 44`.

The independent checker imports no reviewed module. It reconstructs the
Paley quadratic-residue graph and 53-clique cover, derives the two-cycle
template's 54 pair orbits by direct translation, checks the exact parameter
counts and strict-density endpoint, and probes the receiving interface on a
fresh cyclic order-47 graph. The source and reviewer find different physical
blue five-sets in that probe. [REVIEW.md](REVIEW.md) gives the proof audit and
trust boundary.

From the repository root, using CPython 3.11 or later and a fresh scratch
path:

```sh
python3 -B ramsey_r55_orbit_dense_deletion_review1/reproduce.py \
  . /scratch/research-team-v2/tmp/reviewer-1/review-h3975
```

Expected status: `REPRODUCED_ACCEPT_REVIEW_H3975`. The driver extracts source
commit `379a6369935a0ca0ee5ec61f8503ef64cee6fd1f`, runs its complete replay,
and runs the independent audit in normal and assertion-disabled modes. It
uses Git and the Python standard library, invokes no solver, and keeps
generated inputs outside the repository.
