# The expectation route needs the actual parent distribution

Theo,2026-10-06. Author analysis for Quinn's existing cost lane; no different
researcher acceptance, new target, growth theorem or publication claim.
Full410 remains unsolved. This is an objection to a tempting intermediate
uniform-parent bound, not a rejection of Quinn's expectation strategy.

For a uniform input permutation, conditioned on the relative order of its
smallest n ranks, rank n+1 lies uniformly in the n+1 gaps among those original
points. This remains true conditioned on the completion history, since that
history is a deterministic function of their relative order. To see the law,
each fixed order on n ranks has m!/n! extensions in S_m; each of its n+1
insertion positions for the next rank has m!/(n+1)! extensions. Auxiliary
points change current positional gap indices but not this uniform law on
the ORIGINAL gaps. One must translate each choice to the current gap just
before the next original point, as in the checked algorithm.

A constant conditional mean repair cost cannot hold for EVERY reachable
parent, even with no auxiliaries. Take n>=3 and the original parent

    p_n=(n-1,n-2,...,1,n).

It avoids classical2143, so all its rank-prefix insertions were legal and
it is reached without auxiliaries. Its legal current gaps are0,1,n.
For a next original gap g=2,...,n-1, the rightmost legal earlier gap is1.
After t repairs, an auxiliary has been placed before each of the first t
low suffix points. The rightmost legal gap before a still blocked desired
gap is2t+1; the remaining unprotected decreasing suffix blocks every gap
from2t+2 through n+t-1. The desired gap is g+t. Thus repair stops precisely
at t=g-1. Earlier gaps can become blocked again; they are irrelevant to
this RIGHTMOST boundary assertion and are not claimed all legal.

Accordingly the costs are c_0=c_1=c_n=0 and c_g=g-1 for2<=g<n. Their sum is
(n-2)(n-1)/2, so the conditional mean under the next original-gap choice is
(n-2)(n-1)/(2(n+1)), which grows linearly. This rules out any constant mean
cost bound asserted separately for every reachable parent. It also rules
out a sum-of-gap-cost bound of the form alpha*N+beta*n with fixed finite
alpha,beta uniformly over these parents, since N=n here.

This parent has probability1/n! under the actual uniform source law. Its
unconditional contribution is therefore tiny; it gives NO obstruction to
a constant or sublogarithmic unconditional mean, a useful amortized
potential, or a positive-density completion theorem. A weighted proof must
retain the distribution of rare costly parents and their future branches.
That is the falsifiable next distinction, not a reason to fit another
finite constant or sample a larger favorable table.

`cost_distribution_objection_controls_v1.py` uses the already independently
checked literal greedy simulator to complete every one of these original-gap
extensions for n3..16. It checks all147 cases, zero earlier guards, every
claimed last-stage cost and exact summed cost. The simulator tests every
gap and the complete occurrence sets of every actual child. These are
same-author controls for this new argument; its uniform induction and
conditional probability law need a different researcher's check before
use in a proof or source. No new source/graph original is planned for this
method warning alone. Quinn retains the completion/cost task, and the full
target and all earlier accepted/public scopes remain unchanged.
