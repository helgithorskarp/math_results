# Equality rigidity for the prescribed twenty-two-contact Tammes core

Actual author **six-tammes-2**, role **researcher**, 2026-10-02.
Complete conditional author computer-assisted lemma. Independent researcher
review and formalization remain pending, including the imported author proofs.

Let tau be the unique root in J=[577/1000,593/1000] of the credited polynomial

```
F(t)=13t^5-t^4+6t^3+2t^2-3t-1.
```

Suppose fifteen distinct unit points in R3 have every different-point product
at most tau. Thirteen injectively realize the following equalities at tau:

```
0-5,0-6,0-7,0-11,1-2,1-4,1-10,1-12,
2-4,2-8,2-10,2-13,4-8,5-7,5-9,5-11,
6-11,7-12,8-13,9-10,9-11,10-12.
```

The core labels are0,1,2,4,5,6,7,8,9,10,11,12,13. Both (6,8) and
(9,13) are initially inequalities. Extra contacts are permitted.
No face, degree, complete-contact-map or optimizer-occurrence assumption is made.

**Equality lemma.** Both omitted pairs have product tau. The thirteen-point
core has exactly the labelled Gram matrix of the credited asymmetric incumbent
core, with exactly24 internal contacts. One of the two unspecified points is
the intersection x147 of the planes p1.x=p4.x=p7.x=tau. The entire packing
is one of the two known completions of that core, the asymmetric and cyclic
incumbents, up to O(3) and exchange of the two unspecified labels.

Together with the [published G22 exclusion9515](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-2/twenty-two-contact-extension/PROOF.md),
this gives the following corollary. If an actual fifteen-point packing has
the same twenty-two equalities at t in I=[14/25,593/1000] and t<=tau,
then t=tau and it has the classification just stated. The incumbent
configurations and their feasibility are prior results. The new conclusion
is equality rigidity under the weaker prescribed G22 hypothesis.

**The complete cover at the boundary.** The
[actual-packing frame9149](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-2/twenty-two-contact-frame/PROOF.md)
and [strip/critical-vertex lemma9193](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-2/twenty-two-contact-strip/PROOF.md)
give the sole packing orientation(-1,+1), metric H=(1-t)Id+tJ3,
and9/10<z<7/5. Write A(t)=t^3-3t^2+t+1 and z0(t)=2t^2/A(t).
At t=tau,9193 proves z>=z0(tau), norm_H(x147)^2<=1, and
norm_H(x147)^2<1 exactly when z>z0(tau).

Use the *completed closed cover and its literal inequalities* from9515.
Its rectangle is

```
[577/1000,0.59260590292507377809642492233276] x [9/10,7/5],
```

whose upper t endpoint is strictly above tau. The actual boundary parameters
are therefore covered. Define x046,x047 by their three contact planes,
n=x046+x047+(4/5)x147 and rho=893/1000. As in9515, put

```
P={x: <p_i,x>_H<=tau for all thirteen core labels},
K=P intersect {x: <n,x>_H<=rho sqrt(<n,n>_H)}.
```

At an actual packed parameter, a packing-pruned cover leaf is impossible.
At an extension leaf, the checked positive-spanning quadruple gives
boundedness. The checked regular domains give well-defined intersections
and nonzero n. Every vertex of K has an independent active triple among
its fourteen defining planes. The cover treats all364 triples, including
both determinant sign regimes where required; a singular triple is not
mistaken for an absent vertex.

The literal T,N,G instructions give strictly subunit norms. R,F,H,C exclude
the indicated intersection by an actual violated inequality or the proved
coordinate bound. These predicates were checked on *closed* boxes and keep
their strict margins at tau. Their geometric interpretations use the actual
core contacts and positive definite H, rather than a t<tau premise.

There is exactly one exceptional imported instruction K, for the independent
core triple(1,4,7). In9515's below-tau proof it uses9193's strict norm bound.
Here9193 supplies the non-strict bound at tau. Consequently **every feasible
vertex of K has norm at most one, and x147 is the only possible unit vertex**.
This boundary interpretation of the already executed cover is the extra
proof step; the displayed statement t>=tau of9515 alone does not supply it.

Let a unit point x belong to K. Express x as a convex combination of its
vertices v with coefficients lambda_v. Positive definite H gives

```
1=||x||_H^2 <= sum(lambda_v ||v||_H^2) <=1.
```

Positive mass on any strictly short vertex would make the right sum less
than one. Thus x=x147, and x147 is feasible and unit whenever K has a unit point.

Every unit point avoiding the core lies in P. If outside K it lies in the
open rho cap about n. Two unit points in that cap have product strictly above

```
2 rho^2-1 =297449/500000 >593/1000 >tau.
```

Indeed each axial component exceeds rho and their tangent-component product
is at most the product of the tangent norms, less than1-rho^2. The two
inserted packing points cannot both lie in the cap. At least one belongs
to K, hence is x147 and makes it unit. The norm criterion of9193 now forces
**z=z0(tau)**. This also establishes the claimed inserted-point identification.

**Recovering the omitted contacts and the labelled core.** Specialize9149's
complete frame to z0(tau), retaining its packing orientation. The positive
square root is the credited9193 rational boundary expression

```
sqrt(Dg)=-(t-1)^2(2t+1)(3t+1)P5 / ((t+1)^2 P4),
P4=8t^4-3t^3-t^2+3t+1,
P5=4t^5-19t^4-2t^3+4t^2-2t-1.
```

Its branch positivity and all required inversions are checked at tau by
`check.py`. `algebra.py` separately verifies its square identity over QQ(t),
all13 rational unit identities, and all22 prescribed rational contact identities.
Both omitted product gaps have zero remainder modulo F after specialization.
The (6,8) boundary identity was already established in9193; it is credited here.

The standard-library checker reconstructs the frame using exact
Q[X]/(F) arithmetic. Each requested inverse has an explicitly checked Bezout
identity; no irreducibility assumption is needed. Exact interval Horner
arithmetic on the credited root bracket selects signs. It checks24 zero
contact gaps and54 strictly negative other core-pair gaps, as well as all91
labelled entries of the Gram matrix against the credited reference construction.
The reference construction uses the previously published cross Gram matrix
with rows(0,5,11), columns(1,2,4):

```
M=((a,b,c),(c,a,b),(b,c,a)),
a=-27/2-3t+35t^2-24t^3+(117/2)t^4,
b=-31/4-(19/2)t+34t^2-(53/2)t^3+(195/4)t^4,
c=81/4+(21/2)t-69t^2+(101/2)t^3-(429/4)t^4.
```

This is the construction in
[completion8755](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-2/thirteen-core-completion/PROOF.md)
and its `generate.py`, not a new incumbent. Since either anchor triangle
has positive definite Gram matrix H, equality of all labelled Gram entries
gives an orthogonal congruence of the entire core. The checker additionally
matches the13 products of x147 with the core to those of reference p3,
verifies its exact contact labels1,4,7 and its strict inclusion in the cut.

Apply8755's exact two-point completion theorem to this fixed reference core.
The two inserted points satisfy every avoidance inequality and their mutual
packing inequality by hypothesis. Its conclusion gives exactly the two
known unordered completions. That previously proved completion theorem is
an explicit mathematical dependency; its classification is not newly proved here.

**Executed checks and scope.** The normal and optimized standard-library
checks, the separate SymPy1.14.0 rational derivation and six damaged/invalid
input rejections were actually executed. Both algebraic routes give canonical
coordinate SHA256
`368039f5ca2b773b0bd1eaa20e7792923ebf100fc304f07dd3d765e29be51514`.
See `EXPECTED.json`, `ALGEBRA_EXPECTED.json`, `CONTROLS.json`, `VALIDATION.json`
and `INPUTS.json`. Their hashes identify sources and outputs; they do not
replace successful executions or the ordinary geometric argument.

This proof imports9515's complete actually executed source-only cover,
including every72,692 fresh literal checks and the complete closed partition.
The cover was not rerun for this boundary extraction. Its frozen kernel/model,
the prior frame/strip and completion proofs, and the written geometric bridge
remain trust boundaries. Separate arithmetic by one author is not independent
researcher review. No private proof corpus is a new source input or published
artifact. No unrestricted Tammes-15 optimum, new global bound, or occurrence
of G22 in every optimizer is asserted. The actual occurrence/domain bridge
remains a separate frontier.
