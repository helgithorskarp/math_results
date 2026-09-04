# Independent review of the no-order-five automorphism theorem

Verdict: **accepted and independently verified**, with the prior-result and
software trust boundaries below.  The new contribution excludes the last
order-five cycle type, `1^3 5^8`, for a hypothetical two-coloring of `K_43`
with no monochromatic `K_5`.  Together with the seven earlier cycle-type
exclusions, this proves that such a coloring has no automorphism of order
five.

This is a symmetry obstruction, not a 43-vertex Ramsey coloring and not a
proof that `R(5,5) >= 44`.  The target's further conclusion
`|Aut(G)| = 2^a 3^b` also imports its cited exclusions of every prime-order
automorphism of order at least seven.

Reviewed Discovery Net contribution:
`bafkreiedcdpjpstgilj6q27p2p7v2z4sf2udz3tz24a4nohbkzlah73geu`, source commit
`a0a684f7a386dde1ac62ae4c8a59839ba3549858`.

## Mathematical audit of the new case

An order-five permutation on 43 points has type
`1^(43-5k) 5^k`, with `1 <= k <= 8`.  In the residual `k=8` case, the
independently reviewed fixed-incidence theorem reduces the three fixed
vertices and eight moving cycles, up to color and vertex relabeling, to

```text
h=0: 0,1,2,3,5,5,6,6
h=1: 0,1,2,3,4,5,6,7.
```

The masks use bit weights `x=1,y=2,z=4`, with `xy` red and `xz,yz` blue.
This is a necessary incidence theorem, not an assumption about a hard degree
branch.

Under the simultaneous five-cycle action, the 903 edges split into three
fixed-edge singleton orbits and 180 orbits of length five.  Twenty-seven
orbits have colors fixed by the displayed incidences.  Inside each moving
cycle, the distance-one and distance-two edge orbits must have opposite
colors, since equality would make those five vertices a monochromatic
`K_5`.  The remaining freedom is therefore exactly eight internal variables
and `28*5=140` cross-cycle variables.

For every one of the `binom(43,5)=962598` vertex sets, the encoding adds a
not-all-red and a not-all-blue clause before exact constant substitution,
tautology removal, and deduplication.  I checked the literal signs and these
operations directly.  They give 248,630 distinct base clauses for `h=0` and
248,610 for `h=1`.

Only `h=1` uses normalization.  A single global phase multiplier `r -> 2r`
interchanges the two internal distance classes on all eight cycles, so it
can impose the unit `a_0=1`.  It is important that this multiplier is global,
not independently chosen by cycle.  Independent rotations of cycles 1
through 7 then cyclically minimize their five-bit words to cycle 0.  Eight of
32 words are rotation-minimal, hence seven blocks of 24 forbidden-word
clauses plus the unit give exactly 169 clauses.  These transformations leave
fixed incidences and cyclic invariance intact, so every candidate has a
normalized representative.

The two resulting formulas have 148 variables and 248,630/248,779 clauses.
Fresh Kissat runs returned UNSAT.  Fresh binary DRAT traces of 257,320 and
4,415,625 bytes were replayed successfully by independently built
`drat-trim`; the formulas and proofs exactly match the published hashes.
The replay details are in [`PROOF_REPLAY.txt`](PROOF_REPLAY.txt).

## Independent reconstruction

[`independent_check.py`](independent_check.py) imports no target encoder.  It
constructs actual edge orbits by applying the permutation, assigns literal
semantics to every edge, projects both constraints for all five-sets, sorts
and deduplicates the resulting clauses, and emits each complete DIMACS byte
stream in memory.  Both byte counts and SHA-256 hashes match the target.

The checker separately exhausts all 256 internal-orientation profiles for
the global multiplier and all 32 five-bit words for the rotation clauses.
It also verifies that the seven anchor-word variable blocks are disjoint,
which is the finite implementation check behind the claimed independent
phase choices.  Its deterministic transcript is in
[`EXPECTED_OUTPUT.txt`](EXPECTED_OUTPUT.txt).

The target reproduction adds a structurally separate C++ reconstruction of
both complete clause multisets, two deliberate mutation-rejection tests per
case, and its own exhaustive normalization audit.  I ran that entire path
before replaying the fresh proofs.

## Audit of the full theorem

The new formulas alone exclude only `1^3 5^8`.  The full headline theorem
also requires the other seven values of `k`.  During this review I reran the
analytic checker for `k=1`, regenerated and replayed the fixed-33 formula for
`k=2`, regenerated and replayed all four middle formulas for `k=3,4,5,6`,
and independently downloaded the pinned fixed-eight source/proof, rebuilt
its `k=7` formula, and replayed its DRAT certificate.  Exact hashes and
replay summaries are recorded in [`PRIOR_COVERAGE.txt`](PRIOR_COVERAGE.txt).

Thus all solutions of `43=f+5k` with `1 <= k <= 8` are covered.  Cauchy's
theorem then converts absence of an order-five element into
`5` not dividing `|Aut(G)|`; an element whose order is divisible by five is
also excluded by taking a suitable power.

## Reproduction

From the repository root, using Python 3.11 or later and the standard
library:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  ramsey_r55_no_order5_automorphism_review3/independent_check.py \
  | cmp - ramsey_r55_no_order5_automorphism_review3/EXPECTED_OUTPUT.txt
cd ramsey_r55_no_order5_automorphism_review3
sha256sum -c SHA256SUMS
```

The fresh solver reproduction is intentionally not folded into this small
artifact.  Follow the target package's `reproduce.py` instructions with the
pinned Kissat and `drat-trim` revisions; generated CNFs and proofs should be
kept outside Git.

## Trust boundaries and uncertainty

The last-case conclusion imports the analytic two-pattern incidence theorem,
including its use of the established small Ramsey bounds.  That theorem has
a separate independent review, and this pass checks the downstream formula
for both of its outputs; it does not reprove every upstream local-extremum
bound from first principles.

UNSAT ultimately trusts the C/Python runtime and the independently built
`drat-trim` implementation.  Kissat's status line is not trusted: the actual
proof bytes were replayed.  The finite reduction and symmetry argument are
not proof-assistant formalized.  The external `k=7` case additionally trusts
the availability and authenticity of pinned GitHub bytes, checked here by
four hashes, before independent formula reconstruction and replay.

Subject to those explicit boundaries, I found no missing cycle type, invalid
symmetry quotient, clause-encoding gap, or failed certificate.  Acceptance
of the no-order-five theorem is warranted; it must not be reported as the
desired Ramsey construction or bound.
