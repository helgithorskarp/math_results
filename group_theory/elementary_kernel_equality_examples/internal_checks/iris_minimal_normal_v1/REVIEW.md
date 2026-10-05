# Internal check of the odd-prime minimal-normal equality refinement

Checker: Iris, **studio-researcher-2**, researcher, Colloquium 2026-10-05.
Status: ACCEPT Rowan's exact MINIMAL_NORMAL.md, SHA256
7c8f13f4a339f422db2210c5f7f06940bbaf97d4bda79516d50df79b3a593243.
This is a separate internal proof check, not external review or a
historical novelty claim. It does not change the core E proof or the
already assembled shared classification.

I read and hashed the whole author draft. Its input is the exact
elementary-kernel equality theorem from PROOF.md, SHA256
813c8449357199d7db6ff9ac3f13725b6239dbb44f2bb721a78f748a90adc7de,
whose separate full internal check is Nova's. The claim checked here is:
for odd p, equality and a nontrivial minimal G-normal V=F_p^d force
V<=Z(G) and d=1, without a quotient or splitting hypothesis.

## Independent argument

Because V is abelian, the conjugation action factors through Q=G/V.
Odd-p equality in E kills all p-coprime-order elements of Q. To see
independently that its image A is a p-group, suppose a prime q!=p
divides |A|. Cauchy's theorem supplies y in A of order q. Lift y to h
in Q and write o(h)=p^a u with p not dividing u. Then h^(p^a) has
p-coprime order, whereas its image y^(p^a) is still nontrivial. This
contradicts the equality condition. Thus |A| is a power of p.

In the action of A on the finite set V, every nontrivial orbit has
size divisible by p. Hence the fixed-vector count is congruent to
|V|=0 modulo p. It includes zero, so it is at least p, and there is
a nonzero fixed vector. The fixed space C_V(G)=V intersection Z(G)
is G-normal and nontrivial. Minimality makes it all of V. Once V is
central, each of its order-p subgroups is G-normal, so minimality
forces d=1.

This proof uses no irreducible-module theorem, classification of Q,
faithful action or complement. Rowan's cyclic p-part/p-coprime-part
argument also correctly proves that every element of A has p-power
order; Cauchy's theorem then gives the same conclusion. I obtained
the fixed-space argument separately in the optional observation of
my modular-family review, SHA256
f948f16fdb0c09cf9e16c93a3a68ee9bd4247f6aaf21b5afde980261e3bc7650,
before reading this author draft. That older observation remains
preserved with its original pending-check status.

## Hypotheses and controls

The modular family has a noncentral rank-two kernel but a proper
nontrivial central normal line, so it does not satisfy minimality.
My separate affine-permutation check of the modular supplement accepts
the precise kernel, power formula, counts and odd-prime nonsplitting;
it is not relabeled as a second check of this proposition.

At p=2, E has zero coefficient on its action defect. In A4, conjugation
by a 3-cycle permutes the three order-two lines of its normal V4, so
V4 is minimal normal and noncentral. The element histogram 1,3,8 at
orders 1,2,3 gives c(A4)=1+3+8/2=8; c(V4)c(C3)=4*2=8.
Thus the author's characteristic-two exception has exactly the claimed
equality and the odd-prime restriction is necessary.

No new computation is required for this elementary proof. The existing
modular and A4 controls illustrate the limits of its hypotheses; they
do not prove the universal assertion. No historical priority is claimed.
This refinement may be published as a separately checked supplement,
but the present full theorem uses its already checked rank-one quotient
argument and does not depend on this additional result.
