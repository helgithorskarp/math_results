# Independent internal check of the modular-family supplement

Checker: Iris / **studio-researcher-2**, researcher, 2026-10-05.
Checked author: Rowan / studio-researcher-4. Separate board task10;
this does not expand Nova's core E check or change the shared target.

Exact supplement SHA256:
`09e718b545780412c31f54d1f002c4bf72d74cfa17b92ccf922585e3d4406be5`.
Author code SHA256:
`3b5b6d306d21a94f30ef457ff39a5dd897ada12aaaac568af2883818d885a90a`.
Author compact output SHA256:
`77183f0a4cbcc15c1af16b793c4c8c3ce2eeed81eb9783ff6a6562ff3ebb2fb8`.
All three transferred hashes were reproduced before checking.

**Structural conclusion:** the odd-prime statement, its exact count,
the nonsplit extension by V, and its noncentral equality are correct.
The characteristic-two comparison is correct and must remain separate.
These are classical solvable p-groups, not counterexamples to the selected
nonsolvable eta<=6 classification. Historical novelty is not accepted.

## Independent reconstruction by affine permutations

On Z/(p^2), let t(x)=x+1 and s(x)=(1+p)x. The multiplier has order p,
and s t s^(-1)=t^(1+p). The maps t^a s^b, 0<=a<p^2 and 0<=b<p,
are all distinct: their value at0 identifies a and their slope identifies b.
They are closed under composition, giving a faithful group of order p^3
isomorphic to the displayed semidirect product.

Reduction modulo p makes every affine map a translation. Its kernel is
V=<t^p,s>. The two generators commute, both have order p, and their
p^2 products are distinct. Thus V is elementary abelian of dimension2.
It is normal as the kernel of the residue action, and

    t s t^(-1)=t^(-p)s.

In coordinates on the basis (t^p,s), conjugation by t is therefore
(u,v)->(u-v,v), a nontrivial transvection. This independently proves
noncentrality without assuming the author's coordinate multiplication.

For odd p, the slope of (t^a s^b)^p is1 and its translation is

    a sum_(j=0..p-1)(1+p)^(jb)
      = a[p+p b p(p-1)/2] = p a modulo p^2.

The final simplification uses p odd; division by2 is not applied in
characteristic2. Every element outside V has a not divisible by p,
hence has order p^2. A complement to V would have order p and contain
an element outside V, which is impossible. This extension by V is
nonsplit although the same group splits over its different cyclic kernel
<t>. Splitting is a property of the specified exact sequence.

The kernel has p^2-1 nonidentity elements of order p; the other
p^3-p^2 elements have order p^2. Counting generators of cyclic subgroups
therefore gives

    c(M_p)=1+(p^2-1)/(p-1)+(p^3-p^2)/(p(p-1))=2p+2.

For Q=C_p, both reciprocal-totient sums A_p(Q),B_p(Q) equal1. The
kernel count is p+2 and p^(d-1)=p, so the core lower bound is2p+2.
There are no short lifts in any nonidentity quotient coset. The only
p-coprime quotient element is the identity, which acts trivially. Thus
both defects vanish, while V is noncentral. All equality hypotheses of
the exact E formula are respected.

The action norm is zero for odd p: writing T=I+J with J^2=0 gives
sum_(j=0..p-1)T^j=pI+p(p-1)J/2=0 over F_p. The lift t has p-th power
t^p, a nonzero kernel vector, so the affine norm equation cannot cancel
it. This corroborates the direct affine-power calculation.

For p=2 the group is D8. Its translations t,t^3 have order4, while
the two outside elements t s,t^3 s have order2. The four-element
kernel V4 has three nonidentity involutions. Hence the full order
histogram is1,5,2 at orders1,2,4 and c=7. The bound is6, and the
two short lifts contribute defect (1/2)*2/phi(2)=1. Their order-two
subgroups complement V, so this kernel extension splits. The separate
characteristic-two claim in the supplement is therefore also correct.

## Independent finite method and scope

`affine_controls.py` constructs the permutation group by closure from
the two actual affine permutations. It identifies V through the residue
action, checks its commuting order-p basis and transvection, computes
orders by cycle decomposition, and compares those orders with literal
powers. It deduplicates literal cyclic-subgroup sets and checks an exact
reciprocal-totient sum. It imports no author code and uses no modular
normal-form group multiplication.

It compares every mathematical output field of the author's p=2,3,5
fixtures and adds the changed prime7. The fixed compact reference input
is included and checked against its SHA256 before any comparison.
Expected cyclic counts are7,8,12,16. For odd p all nonidentity quotient
cosets contain p^2 lifts of order p^2; for p=2 the sole nonidentity
coset has two short and two long lifts.

Run from Iris's repository root:

```sh
python3 internal_checks/iris_rowan_modular_v1/affine_controls.py \
  --output /tmp/iris-modular-affine.json
```

The completed run returned `INDEPENDENT_AFFINE_CONTROLS_PASS` in about0.14
seconds on Python3.12.14. The maximum finite group size is343 and permutation
degree49. One process, standard library,
exact integers and Fraction. The computation supports the small evidence;
the uniform odd-prime proof is the argument above. This is an internal
check, not formal verification or external peer review.

No general equality-to-centrality statement is justified by E. This
example has a rank-two kernel and solvable quotient, and its kernel is
not a minimal normal subgroup: <t^p> is a proper nontrivial normal line.
It does not undermine the checked rank-one A5-times-cyclic specialization.

## Optional minimal-kernel clarification, separate pending claim

Assuming E's odd-prime equality conditions, equality DOES imply centrality
when V is a minimal nontrivial G-normal subgroup. Here is a short argument
for Rowan to challenge separately; it is not inserted into the accepted
core E artifact or represented as already independently checked.

The action image P in GL(V) must be a p-group. Otherwise choose a prime
q!=p dividing its order, an image element y of order q, and a preimage h
in Q. Write o(h)=p^a u with p not dividing u. The element h^(p^a) has
p-coprime order, so equality makes its action trivial. But its image
y^(p^a) still has order q, a contradiction.

A p-group acting on the additive set V has orbits of p-power sizes.
The fixed-vector count is congruent to |V|=0 modulo p and includes0,
so it contains at least p vectors. Thus C_V(G) is a nonzero normal
subgroup of G inside V. Minimal normality forces C_V(G)=V, so V is
central. The modular-family kernel fails precisely this minimality input.
At p=2 no such conclusion follows from E: the nontrivial C3 action on
the minimal normal V4 in A4 attains the Hall bound.
Indeed A4 has element counts1,3,8 at orders1,2,3, giving c(A4)=8,
equal to c(V4)c(C3)=4*2. Its three order-two lines are permuted by C3,
so V4 is minimal normal and noncentral.

This optional claim is a structural clarification of equality, not a new
campaign target. Its proof still depends on the exact odd-prime E
equality condition and awaits a different researcher's check.
