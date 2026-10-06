# Greedy gap opening: proved termination, failed cost bound, missing entropy

Quinn, workday4, 2026-10-05. New author uniform partial proof and exact finite
counterexample, awaiting Theo's separate whole-scope check. None is covered by
534/552/570, any current public source or graph original. Full410 is unsolved.

The exact construction and relaxed full-target bridge are specified in
GAP_OPENING_ENTROPY_PLAN_V1.md. Here are the claimed scope and evidence.

## Uniform operation and universal completion

After insertion of a largest value at gapk, gapsk+1 and, if a suffix exists,
k+2 are legal for another maximum. For any point before this new root, its
nearest greater successor is at or before the root, so its blocker interval
cannot cover either claimed gap. The root has no greater neighbor. The first
suffix point has this root as nearest greater predecessor, greater than every
possible successor; it is not a blocker. Any later minimum's interval starts
strictly after gapk+2. This proves the assertion via accepted kernel444.
The proof does not assume an arbitrary tree's current labeling avoids.

For the actual completion, all parents DO avoid: start empty and insert only
at legal gaps. If a desired gapg is blocked, the rightmost legal earlier gapk
exists because0 is legal. Insert an auxiliary new maximum there. The tracked
gap becomesg+1, while the rightmost legal gap before it is at leastk+2. Thus
d=g-k falls by at least1. In at most its initiald steps the desired gap is
legal, and the next input rank can be inserted. The suffix needed in the lemma
exists becausek<g. Desired gaps are tracked before the next existing original
point to the right; previous auxiliary points count in every current gap.

Processing original ranks in ascending order and retaining their original
positional order produces an avoiding output containing the input as a
standardized subsequence. At stagei with current lengthN_(i-1), its repair
distance is at mostN_(i-1), so N_i<=2N_(i-1)+1 and N_m<=2^m-1. This is a valid
universal completion bound, far too large to prove the agreed growth target.
No amortized linear, sublogarithmic or average bound is claimed.

## Exact failure of a tempting linear bound

The specified all-input hypothesis tested was N(sigma)<=2m-3 for everym>=4.
It agrees with all complete input sets through6 and saturates on the two-
descent family (q,...,1,m,...,q+1) in the tested even sizes. Those finite
facts did not prove it. A seeded m512 input has output length1100, and greedy
deletion reduces that failure to the following m27 input:

    2,1,22,5,4,20,7,25,3,6,24,18,14,13,12,17,9,16,15,23,27,8,19,11,10,26,21.

Its exact greedy output has52 points,25 auxiliaries, whereas2m-3=51.
The complete52-step compact certificate contains every inserted value and
source identity, each rightmost-gap choice, its blocker witness and decreasing
repair distance, plus the complete empty literal-occurrence set of every child.
The27 selected source points recover the displayed input by standardization.
No global minimality is claimed. Source ranks16 and23 each repair a point
that was itself an earlier auxiliary guard. Thus an argument charging each
repair to a previously unrepaired original point is invalid.

The small control exhausts all avoiding parents through6 and all their legal
insertions, testing the two-gap statement against literal occurrences. It
also completes every original input through6 and directly checks every child
and source order. Counts/hashes and compact worst fixtures are included.
These are author controls and this52-step literal certificate is another
same-author validation, not independent review.

The recursive family tau0=1, tau_(h+1)=2143[tau_h,tau_h,tau_h,tau_h] has tested
input/output lengths(4,5),(16,25),(64,113),(256,481),(1024,1985). It did not
falsify the linear bound and no formula is asserted from this table. The
original random512 failure, all deletion steps, and full diagnostic source/
outputs remain durable outside the compact review packet. A single bad input
refutes the quantified coefficient2 claim, not every constant or a positive-
density bound. The route needs an actual entropy-cost theorem before further
sampling or a claim of full growth.

## Relaxed full-target bridge and trust boundaries

If a fixed positive fraction of S_m for infinitely many m has avoiding
completions of length at mostK(m)=o(m logm), count preimages bybinomial(n,m).
An output word yields at most one standardized pattern per m-position subset;
therefore epsilon*m!<=sum_(m<=n<=K)a_n binomial(n,m). Since
log binomial(K,m)<=m log(eK/m)=o(m logm), one n betweenm andK satisfies
log a_n>=(1-o(1))m logm. Consequently(log a_n)/n tends to infinity along
these choices because n<=K=o(m logm). This proves the FULL negative target
conditionally, with no padding assumption or ordinary-limit claim. The
positive-density/sublogarithmic cost hypothesis is UNPROVED for this greedy
rule and all other constructions considered here.

All computations use exact Python integers and checked kernel444. Literal
quadruple checking is separate same-author reduction. No solver, floating
arithmetic or proof-assistant certificate is used. Diagnostics have explicit
time/point caps; incomplete runs yield no completed-input cost. Reproduce the
small controls with gap_opening_probe_v1.py in a fresh directory, then the
fixture with gap_opening_certificate_v1.py. Preserve original JSON outputs.
The next meaningful milestone is a structural cost/density invariant or its
uniform obstruction, not merely a larger favorable table. Theo's independent
check must cover uniform termination, positional/rank preservation, the entire
subsequence-fiber/asymptotic bridge and the literal27-point cost certificate.
