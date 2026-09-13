# Seven completion points are necessary in the sealed Parts pool

## Result

Let G = L union S be Jaan Parts's 509-point five-chromatic plane
unit-distance graph, with the accepted decomposition into a fixed 374-point
large block L and a 135-point small block S. Let Q5 be the 168 level-one
completion points involving sqrt(5), and put U = S union Q5, a sealed exact
303-point pool.

This package proves the following finite-family theorem:

> If X is a subset of U, |X| <= 134, and the strict unit-distance graph on
> L union X is not four-colourable, then |X intersect Q5| >= 7.

Thus a record construction in this exact pool must delete at least eight
points of S and add at least seven points of Q5. The new exhaustive strata
are five and six completion points. The four-completion selector is retained
as a control agreeing with the stronger pre-existing all-plane four-point
augmentation closure. Counts zero through three are imported from the
accepted Parts criticality and one-, two-, and three-point closures.

This is a construction-search reduction, not a new five-chromatic graph and
not a global lower bound. It says nothing about changing L, points outside
the sealed level-one pool, or candidates using at least seven Q5 points.

## Certificate

For D contained in U, call D a killing set when L union (U minus D) has a
supplied proper four-colouring. Any non-four-colourable L union X must meet
every killing set: if X and D are disjoint, that colouring restricts to
L union X.

The compact [certificate](certificate.json) contains 5,528 such positive
witnesses, packed at two bits per pool vertex. The standard-library verifier
checks all of them against the accepted complete exact edge list, making
7,907,307 retained pool/cross-edge checks. It then rebuilds three independent
selector CNFs. Each asks for a 134-point hitting set with exactly 4, 5, or 6
selected Q5 points. Transparent binary ripple counters are tested by 640
exhaustive small truth-table checks.

Each selector has 8,462 variables and 34,530 clauses:

| selected Q5 points | SHA-256 |
|---:|---|
| 4 | 5bc7b03d5358059482db5884658396f8ffad47afd41520dae8d2589634d0357c |
| 5 | d4c34d606e33b16737b1cd44165f849a075a2f2f4f0993a4e2d823967615a322 |
| 6 | 5149b4eacb099be3809a186ec0f4242b57cc7d9e28bbf11527a3ac23db9703e9 |

All three are UNSAT by separately checked DRAT refutations. [PROOF.md](PROOF.md)
gives the logical bridge, imported premises, proof hashes, and stopping rule.

## Reproduction

From the repository root, Python 3.11 or newer suffices for the solver-free
checks:

    python3 -B hadwiger_nelson_parts509_five_four_swap_search/verify.py
    sha256sum -c hadwiger_nelson_parts509_five_four_swap_search/SHA256SUMS

The verifier rebuilds every selector byte-for-byte and must end with
VERIFIED_PARTS_POOL_Q5_AT_LEAST_SEVEN_REDUCTION.

DRAT proofs can be regenerated with CaDiCaL 3.0.1 and checked by drat-trim:

    cadical -q selector_q5.cnf /scratch/selector_q5.drat
    drat-trim selector_q5.cnf /scratch/selector_q5.drat

Repeat with q4 and q6. A successful check prints s VERIFIED. Solver search is
not trusted: every lower-side UNSAT result is checked by the proof checker,
while every killing clause has a direct positive colouring witness.

The optional [search program](search_cegar.py) reproduces the
counterexample-guided loop with python-sat 1.9.dev15. Keep its large
checkpoints outside the repository. A bounded seven-completion run stopped
after four selector models and 688 seconds; its last 508-point model still
admitted nine of the twenty interface patterns. That is an open search
checkpoint, not an exclusion or candidate claim.

## Sources and scope

The exact coordinate/edge pool is imported from the separately checked Parts
completion packages in this repository. The unrestricted benchmark is Jaan
Parts, Graph minimization, focusing on the example of 5-chromatic
unit-distance graphs in the plane,
[arXiv:2010.12665](https://arxiv.org/abs/2010.12665). Haugland's newer
2,131-point graph addresses the additional Moser-spindle-free restriction,
not the unrestricted vertex record
([arXiv:2608.04542](https://arxiv.org/abs/2608.04542)).
