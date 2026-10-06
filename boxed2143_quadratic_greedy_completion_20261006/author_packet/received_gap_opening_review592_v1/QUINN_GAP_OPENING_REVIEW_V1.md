# Independent check of greedy completion and its missing cost obligation

Theo, literature-researcher-4, checks Quinn581, literature-researcher-3,
2026-10-05. ENTIRE submitted partial scope ACCEPTED with the exclusions
below. This is an internal team check, not external peer review or a novelty
certificate. Full target410 is UNSOLVED. Proved universal termination and
its exponential length bound do not establish the required growth result.

The separate seven-file packet, its manifest and three named dependencies
are frozen unchanged in `received/quinn_gap_opening_v1`. Packet manifest
SHA256 is `b6c3e69dcbeae419076ecba29a96348f40e3bdb449aea2b35df758284dd63706`;
uniform proof SHA256 is
`6d533385aa52398fb314a9c5496f29e8e155d31b65f622d6ca93ada0ddf381cb`.
Lengths and hashes match before and after reproduction. No acceptance from
534/552/570 is inherited by the new claims.

## Uniform two-gap lemma and termination

In the already checked maximum-insertion criterion, a blocking minimum at
position j has nearest greater positions L,R on both sides with p[L]<p[R],
and forbids gaps j+1,...,R. Insert a new global maximum at gap k, now position
k. A minimum before k has a right greater neighbor no farther right than k,
so cannot forbid k+1 or k+2. The new maximum has no greater neighbor. The
first suffix point, at k+1, has the new maximum as nearest greater neighbor
on its left; it exceeds every possible right neighbor, so does not block.
Every later minimum starts forbidding only at gap>=k+3. Thus k+1 is legal
and k+2 is legal whenever there is a suffix. Here the criterion describes
creation of a new box; actual child avoidance also requires the parent to
avoid, as it does throughout this construction.

When desired gap g is blocked, gap0 is legal and the rightmost legal k<g
exists. There is a suffix since k<g<=current length. After an auxiliary at k,
the desired gap is g+1 and gap k+2 is legal. If g+1 is already legal, this
stage stops repairing. Otherwise its rightmost preceding legal gap is at
least k+2, giving distance at most (g+1)-(k+2)=(g-k)-1. Using the rightmost
legal gap at or before the desired gap makes this inequality valid in the
terminal branch too, with distance0. Each stage needs at most its initial
distance auxiliaries. This explicit branch resolves the informal word
"before" in the author's termination prose; the submitted code and result
use the correct at-or-before convention for the child distance.

Each insertion is legal into an avoiding parent, starting empty. Every stage
terminates, so processing source ranks1..m constructs an avoiding completion.
Insertion immediately before the next already present source point to the
right preserves their prescribed order; auxiliary points have no source
identity. The original source values are inserted in increasing rank order,
even with auxiliaries in between. Thus their standardized subsequence is
exactly the input. At stage i, the initial distance is at most N_(i-1), so
N_i<=2N_(i-1)+1. Starting N_0=0 gives N_m<=2^m-1. This uniform bound is
correct but supplies no useful sub-m-log-m cost or positive density.

## Independent complete finite reproduction

My NEW `check_quinn_gap_opening_v1.py` imports no author executable. It tests
new boxes by literally choosing the two points before the inserted maximum
and the point after it, checking every unselected interior value. Every new
box must use that maximum as its third selected point, which makes this
literal test complete. A separate direct nearest-greater scan agrees with
this test for every visited word. Every actual child also undergoes the full
literal quadruple/interior occurrence scan.

All704 avoiding parents of lengths0..6, all4098 legal children and every
child's insertion gaps reproduce the two-gap certificate. An additional
31898 full child occurrence tests independently check the literal
new-maximum gap test. The complete ordered control stream is
`45b4ccdeb52091c6f7efc24e850401bb59c0c77ffa0c25c18713c67e7aa20e38`.

I independently run the exact greedy rule on ALL873 source permutations
of lengths1..6. Every histogram, output-length sum, first worst fixture,
stage cost, output/tag/auxiliary trace and complete ordered input stream
matches both copies of the author's small-domain controls. Each insertion
has an empty COMPLETE literal occurrence set and every output recovers its
source order and ranks. These controls also establish that the specifically
tested inequality N<=2m-3 holds on the complete m4..6 domains; no later
minimality follows.

The exact27-point fixture is completed from scratch using the literal gap
test for EVERY gap at EVERY decision. All52 complete child words, source
identities, rightmost-gap choices, blocker witnesses, tracked distances,
stage costs and empty full occurrence sets match the certificate. The
output has52 points and25 auxiliaries, exceeding51=2*27-3. Its27 original
points standardize to the specified input. Repairs at zero-based step25
and38, source ranks16 and23, act immediately before an earlier auxiliary.
This invalidates the specified charging of every repair to a previously
unrepaired original point, without rejecting every possible linear cost
argument or any average/positive-density bound.

The whole independent run takes1.898s,18280KiB peak RSS, Python3.11.2, one
process. The output `quinn-gap-opening-reproduction-v1.json` preserves all
52 fixture steps, all873-input control summaries/streams and full counts.
No cap or incomplete count is used. Larger seeded random diagnostics,
deletion minimality, recursive-family asymptotic formulas and any asserted
distribution are excluded from this acceptance; they are author exploration,
not dependencies of the proved scope.

## Complete conditional subsequence-fiber bridge

Suppose for infinitely many m, at least epsilon*m! distinct inputs, with
fixed epsilon>0, have avoiding completions of integer lengths in [m,K(m)]
where K(m)=o(m log m). For a fixed output of length n, each m-position
subset supplies at most one standardized input, so the number of distinct
preimages is at most binomial(n,m). Multiple subsets realizing the same
input only reduce that number; auxiliary tags are not counted as part of
an output permutation. With variable output lengths this gives

epsilon*m! <= sum_(n=m)^K a_n binomial(n,m)
           <= (K-m+1) binomial(K,m) max_(m<=n<=K) a_n.

The binomial coefficient is at most (eK/m)^m. Since eventually K<=m log m,
its logarithm is O(m log log m)=o(m log m); also log(K-m+1)=o(m log m).
The integral lower bound log(m!)>=m log m-m+1 and the trivial upper bound
m log m give log(m!)=(1-o(1))m log m. Therefore one length n_m in [m,K]
satisfies log a_(n_m)>=(1-o(1))m log m. Since n_m<=K=o(m log m) and
n_m>=m->infinity, log a_(n_m)/n_m->infinity. This proves exactly the full
negative limsup alternative conditionally, without padding or an ordinary
limit claim. Markov also gives the submitted sufficient density condition
if the expected length under uniform S_m is m*f(m) with f=o(log m): at
least half the inputs have length<=2m*f(m), rounded harmlessly to an integer.
No such expectation or cost/density theorem is currently proved.

This review accepts the full requested uniform operation, completion bound,
source preservation, conditional asymptotic bridge, exact27-point failure
and complete small controls. It supplies no unrestricted useful cost bound,
all-constant obstruction, statistical expectation, global minimality or
growth theorem. Earlier accepted/public/graph scopes remain unchanged.

Reproduce with a fresh output:

```sh
python3 -B check_quinn_gap_opening_v1.py --output /tmp/quinn-gap-opening-independent.json
```

The complete written review, independent code/output and frozen author
packet/dependencies are pinned in `QUINN_GAP_OPENING_REVIEW_MANIFEST_V1.json`.
