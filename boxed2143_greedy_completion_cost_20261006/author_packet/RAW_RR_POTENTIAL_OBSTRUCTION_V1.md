# Uniform obstruction to the raw-RR original-gap potential

Quinn / literature-researcher-3, 2026-10-06. AUTHOR uniform partial proof,
pending Theo's separate ENTIRE check. Full target410 remains UNSOLVED. This
rejects one precise all-parent drift method; it does not reject the full
unconditional cost obligation, another potential or useful completion density.

## The precise candidate

For a tagged current completion T let O be its ORIGINAL gaps: immediately
before each original point, and the final gap. Auxiliary points have no gap
weight of their own. Define

    Phi(T,O) = sum_(g in O) #(all consecutive RR pairs in the external path g).

This counts RR even before an L has appeared. The proposed telescoping argument
would require a bound on

    E[cost of next repair + Phi(next) - Phi(current) | fixed source history],

uniformly over every reachable parent on n original ranks. Conditional on this
history, the n+1 ORIGINAL gaps are equiprobable by Theo608/Lyra632; current
auxiliary gaps are not equiprobable. A bound K(n)=o(log n) would be sufficient
to get o(m log m) total expected repairs, since Phi is nonnegative. We disprove
this particular uniform bound, including every constant K, by reachable parents
having NO auxiliaries and NO next repair cost.

## Reachable counterfamily and its old potential

For integers q>=1 and n>=q+1, let b=n-q-1 and take

    p_(n,q) = (1,2,...,b,n,n-1,...,n-q).

The prefix is increasing, and the tail is decreasing and above the prefix.
Any classical2143 occurrence would have its first descent inside the tail;
no later tail entry is above its first selected entry, as a2143 occurrence
requires. Thus p_(n,q) classically avoids2143, and therefore boxed2143. Every
rank restriction has the same increasing-prefix/decreasing-tail form (or is
increasing). Deleting the largest rank preserves that classical avoidance.
Consequently rank-by-rank arrival in the source order inserts each next
original maximum legally, with no auxiliary repair. This is a reachable
state of the specific greedy completion algorithm, with all n points original.

Its maximum tree has an all-left spine of length b as left subtree and an
all-right spine of length q as right subtree. External paths in the left
part have no consecutive RR. In the right part the paths are R^t L for
1<=t<=q and the final R^(q+1). They have respectively t-1 and q consecutive
RR pairs. Thus

    Phi_old = q(q+1)/2.

All paths avoid RR after an earlierL, including boundary cases b=0 and q=1.
Every gap is therefore legal by accepted534. Every next insertion has cost0.

## Exact potential of every child

Use zero-based gaps g0,...,n, so the old maximum n is at position b. There are
n-q=b+1 gaps g<=b, before the old maximum. Inserting the new maximum there
places the old right-spine part inside its right subtree. Each of its q+1
external paths acquires one leadingR and thus exactly one extra consecutive
RR pair; no other path acquires an RR pair. The new original gap before the
new maximum has a path with only one finalR and contributes0. Hence every
one of these n-q children has

    Phi_child = Phi_old + q+1.

For the q+1 remaining gaps write g=b+t, where 1<=t<=q+1, and put r=q+1-t.
The cut is after the old maximum and t-1 tail points. In the new left subtree,
the old tail's right spine has length t-1, and its external paths contribute
t(t-1)/2 RR pairs: the leading edge from the new root is L. The new original
gap before the root is the LAST external leaf of that left subtree, so its
old tail contribution is included exactly once. The new right subtree is a
decreasing tail of length r. Its leading edge is R, giving RR contributions
0,1,...,r across its external paths, totaling r(r+1)/2. Old increasing-prefix
paths contribute0. Therefore

    Phi_child(t) = t(t-1)/2 + r(r+1)/2.

Their sum over t1,...,q+1 is 2*binom(q+2,3)=q(q+1)(q+2)/3. Every child has
n+2 original gaps. Its new original gap is retained; these formulas do not
mistakenly average only over the n+1 old gaps or discard that new gap.

## Unbounded, nonsublogarithmic conditional drift

All next ORIGINAL gaps have probability1/(n+1), with no repairs. Subtracting
Phi_old gives the exact conditional drift

    Delta(n,q) = (q+1)*(n - q(q+5)/6)/(n+1).

For example n4,q1 is the first observed1243 counterexample to a constant1
bound: Phi_old1, child potentials3,3,3,1,1, so Delta=6/5. That finite first
failure alone would not rule out a larger constant.

For every q>=2 now set n=q^3. Since q+5<=3q^2, q(q+5)/6<=n/2; also
n/(2(n+1))>=1/3. Hence

    Delta(q^3,q) >= (q+1)/3.

This tends to infinity and grows at least as a constant times n^(1/3), faster
than log n on this subsequence. No constant or K(n)=o(log n) can bound this
same potential's drift over ALL reachable n-rank parents. This is a uniform
algebraic argument, not an inference from a finite census or a fitted constant.

The parent has source probability1/n! under uniform S_n. The counterfamily
therefore says nothing adverse about an UNCONDITIONAL weighted expected repair
cost or an averaged drift bound over actual source histories. A different
potential could charge its left spine differently. No assertion excludes
those approaches or changes the agreed full target.

## Finite controls and scope boundary

repair_rr_potential_probe_v1.py/.json preserve the original constant1 first-
failure scan and all12 completed source states. Its occurrence function is
the previously checked OPTIMIZED complete occurrence oracle, not a fresh
literal quadruple scan. This correction also applies to641's description of
the original path-cost probe. Executed sources/results remain unchanged.

The separately specified repair_rr_drift_family_v1.py checks only the directed
cases (n,q)=(2,1),(4,1),(8,2),(27,3),(64,4): every gap, every next tree child,
every exact potential and formula, and rank-prefix reachability. Parents,
prefixes and children of size<=28 receive a FULL literal quadruple scan;
the n64 case is explicitly a shape/kernel control, without an invented
literal census. These same-author controls do not supply an independent
check or replace the uniform proof. Their complete result and source hashes
are repair_rr_drift_family_v1.json. No population inference is made.
