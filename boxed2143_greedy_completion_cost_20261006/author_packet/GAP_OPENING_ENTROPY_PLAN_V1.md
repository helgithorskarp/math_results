# Gap opening and a relaxed completion bridge

Quinn, workday4, 2026-10-05. New author proposal and uniform partial argument;
no different-researcher acceptance is inherited. Full target410 stays fixed.
The method uses the accepted maximum-insertion kernel444, not a new source
definition, and keeps all input points as a relative-order subsequence.

## Precise construction and termination claim

Process input ranks1,...,m in ascending value order. Their positions must
follow their original input order. Track the next source point's desired
gap immediately before its next already present original point to the right,
or at the end if none exists. Auxiliary points have no source identity.
If the tracked gap is legal, insert the next source point as the new maximum.
If it is blocked, insert an auxiliary new maximum at the RIGHTMOST legal gap
strictly before it, update the tracked gap by+1, and repeat. Gap0 is always
legal, so this operation is defined. The rule includes the current auxiliaries
in all gap indices; it must not treat the original-input gaps as consecutive.

Uniform termination lemma proposed for separate check: after a new maximum
is inserted at gapk, gapsk+1 andk+2 are legal whenever the latter exists.
In the child's nearest-greater criterion, every minimum before the new root
has its right greater boundary no farther right than that root. The root has
no greater neighbors. The first point after it has the root as nearest
greater point on its left, larger than every potential greater point on its
right, so it cannot be a blocker. A later minimum's forbidden interval starts
after gapk+2. Thus no blocker covers either asserted gap.

For a blocked desired gapg and its rightmost earlier legal gapk, setd=g-k.
After the auxiliary, the desired gap isg+1 and its rightmost preceding legal
gap is at leastk+2. Therefore its distance decreases by at least1. The suffix
is nonempty becausek<g. There are at most the initiald auxiliaries in a stage.
Every insertion is legal into an avoiding parent, starting empty, so the
result avoids boxed2143. Original positions and ascending source ranks are
preserved. This proves termination and a completion, but gives NO useful
uniform linear/sublogarithmic overhead bound. Counting current points in the
stage bound includes prior auxiliaries; ignoring them is an invalid amortization.

## The full-target entropy obligation

Exact source decoding is not necessary if output fibers are bounded explicitly.
An avoiding output of lengthn contains at most binomial(n,m) distinct input
patterns of lengthm, since each chosen m-position subsequence yields one
standardized permutation. Thus a completion map can forget the source tags
and still has at most that many preimages. Source tags are algorithmic evidence,
not extra data counted as a permutation.

Suppose for infinitely many m a set E_m of at least epsilon*m! distinct inputs,
with one fixed epsilon>0, has avoiding completions of length at mostK(m), where
m<=K(m)=o(m logm). These completions may have different lengths. Their preimage
bound gives

    epsilon*m! <= sum_(n=m)^K a_n * binomial(n,m)
                 <= (K+1)*binomial(K,m)*max_(m<=n<=K) a_n.

Here log binomial(K,m)<=m log(eK/m)=o(m logm), and log(K+1)=o(m logm), while
log(m!)=(1-o(1))*m logm. Therefore one such output length has
log a_n >=(1-o(1))*m logm. Dividing byn<=K=o(m logm) proves unbounded logarithmic
nth roots along a subsequence, hence the FULL negative target410. Output lengths
tend to infinity because n>=m. No padding closure or ordinary limit is assumed.

This bridge is conditional author algebra, not evidence for E_m orK. In particular,
an expected completion lengthm*f(m) withf=o(logm) under UNIFORM S_m would give
E_m of at least half the inputs andK=2m*f(m) by Markov. A random pilot does not
prove that expectation or positive-density claim, and a bad single input does
not disprove it. A proved constant overhead for every input would be stronger.

First falsifiable milestones: validate the precise two-gap/termination operation
against the literal definition on complete small avoiding-parent domains; retain
exact source order and costs for complete small input sets; inspect the stated
greedy rule on specified adversarial families and seeded random inputs to expose
its cost mechanism. Then seek an exact amortized/positive-density proof or a
uniform obstruction. Do not turn larger favorable samples into a growth claim.
All author controls remain same-author evidence pending Theo's separate check.
