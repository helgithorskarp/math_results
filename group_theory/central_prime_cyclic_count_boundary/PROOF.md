# Central prime extensions at the normalized cyclic-count boundary

Author: Iris, **studio-researcher-2**, researcher.
Version: 1, 2026-10-05. Status: local proof draft awaiting an independent
internal check. This proves a conditional extension statement, not the
campaign's classification of all nonsolvable groups.

For a finite group X, let c(X) count its cyclic subgroups, including the
trivial subgroup, and put

$$\eta(X)=\frac{c(X)}{2^{\omega(|X|)}}.$$

Here omega counts distinct prime divisors. Write
$$\delta(n)=\frac{\tau(n)}{2^{\omega(n)}},\qquad \delta(1)=1,$$
where tau is the positive-divisor function. Thus delta(n) is at least 1.

## Precise statement

**Central-extension lemma.** Let p>5 be prime and let

$$1\longrightarrow N\longrightarrow G\overset{\pi}{\longrightarrow}
A_5\times C_m\longrightarrow1$$

be an exact sequence of finite groups, with N isomorphic to C_p,
N contained in Z(G), and gcd(m,30)=1. No restriction on the prime
exponents of m is assumed.

Then G is isomorphic to A_5 times an abelian group K of order pm, with
N contained in K and K/N isomorphic to C_m. More precisely:

1. If p does not divide m, then K is cyclic of order pm and
   $$\eta(G)=4\delta(m).\tag{1}$$
2. If m=p^a r with a>=1 and gcd(r,30p)=1, then exactly one of the
   following group types occurs:
   $$\begin{array}{c|c}
   K&\eta(G)\\\hline
   C_{p^{a+1}r}&2(a+2)\delta(r)\\
   C_{p^a}\times C_p\times C_r&2(ap+2)\delta(r).
   \end{array}\tag{2}$$

In particular, eta(G)<=6 holds precisely in these cases:

- p does not divide m, K=C_{pm}, and m is squarefree or has exactly
  one squared prime and all other exponents 1;
- p divides m, m=pr with r squarefree and gcd(r,30p)=1, and
  K=C_{p^2r}. In this case eta(G)=6.

Thus every group in this conditional class with eta<=6 is
A_5 x C_k, gcd(k,30)=1, with k squarefree (eta=4) or with exactly
one prime exponent 2 and all others 1 (eta=6). Conversely the specified
group types give those counts and admit the indicated central kernel.

The hypothesis N<=Z(G) is an input. This document does not prove
centrality for an arbitrary normal elementary-abelian kernel, that its
prime exceeds 5, or that the quotient has this form. Those are separate
research obligations. It also does not exclude other radical-free groups.

## 1. Split only over the A_5 factor

Let H be the preimage under pi of A_5 x {1}. H is normal in G, and
H/N is A_5. Since p>5, 60 is invertible in F_p. We give the needed
splitting proof directly, rather than importing a Schur multiplier or
assuming the whole extension splits.

Identify N additively with F_p. Choose a section s:A_5->H with s(1)=1.
Since N is central, write

$$s(x)s(y)=\alpha(x,y)s(xy),\qquad \alpha(x,y)\in\mathbb F_p.$$

Associativity gives

$$\alpha(x,y)+\alpha(xy,z)=\alpha(y,z)+\alpha(x,yz).$$

Set

$$t(x)=60^{-1}\sum_{z\in A_5}\alpha(x,z).$$

Summing the cocycle identity over z and using the bijection z->yz
gives

$$\alpha(x,y)=t(x)+t(y)-t(xy).$$

Hence s'(x)=(-t(x))s(x) is a homomorphism and pi composed with s'
is the identity on the A_5 factor. Its image A is isomorphic to A_5,
intersects N trivially, and commutes with N. Therefore

$$H=N\times A.$$

A_5 is perfect and has trivial center; elementary justifications are
given below. As N is abelian, H'=A. The derived subgroup H' is
characteristic in H, so A is normal in G. This normality step is
essential: an arbitrary complement need not be normal merely because
it complements a normal subgroup.

## 2. Identify the entire remaining factor

Put K=C_G(A). For g in G write pi(g)=(x,b), and let a in A be the
unique element mapping to (x,1). For every u in A, write pi(u)=(u_0,1).
Then

$$\pi(gug^{-1})=(xu_0x^{-1},1)=\pi(aua^{-1}).$$

Both conjugates lie in A, and pi is injective on A. Consequently they
are equal, and a^{-1}g lies in K. Thus G=AK. Also

$$A\cap K=Z(A)=1.$$

Since A and K commute, multiplication gives an internal direct product
G=A x K. Centrality places N in K. The image of K under pi lies in
{1} x C_m, since its A_5 component centralizes all of A_5 and that
center is trivial. Conversely G=AK makes this image the whole cyclic
factor. We obtain an exact sequence

$$1\longrightarrow C_p\longrightarrow K\longrightarrow C_m
\longrightarrow1.$$

Choose a lift v in K of a generator of C_m. Every element of K is
zv^j for some z in N. Since N is central, all such elements commute.
Therefore K is abelian. This uses that K/N is cyclic: an abelian
quotient alone would not imply that K is abelian.

## 3. Classify the abelian extension

An abelian finite group is the direct product of its Sylow subgroups.
For every q!=p, the q-Sylow subgroup of K maps injectively and onto the
q-Sylow subgroup of C_m, hence is cyclic. This accounts for a cyclic
factor C_r, where m=p^a r and p does not divide r.

If a=0, the p-Sylow subgroup of K is N=C_p. All Sylow subgroups of K
are cyclic and have pairwise coprime orders, so K=C_{pm}.

Suppose a>=1, and let P be the p-Sylow subgroup of K. Then |P|=p^{a+1},
N<=P, and P/N=C_{p^a}. Choose z generating N and x in P lifting a
generator of P/N. P is generated by x,z, which commute, and

$$x^{p^a}=z^t\quad\text{for some }t\in\mathbb F_p.$$

If t!=0, then z belongs to <x>, and x has order p^{a+1}. Thus P is
cyclic. If t=0, x has order exactly p^a, <x> intersects N trivially,
and P=<x> x N=C_{p^a} x C_p. These are all possibilities; no
classification of arbitrary groups of order p^{a+1} is needed.

Combining with C_r gives precisely the two types in (2). In particular,
for a=1, the two lifts of the p-part are C_{p^2} and C_p x C_p.
Centrality alone does not choose between them.

## 4. Exact counts and the sharp boundary

Partitioning elements according to the cyclic subgroup they generate
gives the elementary identity

$$c(X)=\sum_{x\in X}\frac1{\varphi(o(x))}.\tag{3}$$

For groups X,Y of coprime orders, the order of (x,y) is o(x)o(y), and
phi is multiplicative on these two coprime orders. Summing (3) yields

$$c(X\times Y)=c(X)c(Y)\quad\text{if }\gcd(|X|,|Y|)=1.\tag{4}$$

The element-order histogram of A_5 is

$$\begin{array}{c|rrrr}e&1&2&3&5\\\hline
\#\{x:o(x)=e\}&1&15&20&24.
\end{array}$$

These numbers come from the even cycle types on five letters:
identity, double transpositions, 3-cycles, and 5-cycles. Consequently

$$c(A_5)=1+15+20/2+24/4=32.$$

For cyclic C_n there is exactly one subgroup per positive divisor, so
c(C_n)=tau(n). In particular c(C_{p^{a+1}})=a+2.

For P=C_{p^a} x C_p with a>=1, there are p^2-1 elements of order p,
giving p+1 cyclic subgroups of order p. For each 2<=j<=a there are
p^{j+1}-p^j elements of order p^j, giving p subgroups of that order.
Including the trivial subgroup therefore gives

$$c(C_{p^a}\times C_p)=1+(p+1)+(a-1)p=ap+2.\tag{5}$$

All prime divisors of K exceed 5. Applying (4), and carefully keeping
the prime p only once in omega, yields:

- If p does not divide m, omega(|G|)=4+omega(m), and
  c(G)=32*2*tau(m), proving (1).
- If m=p^a r with a>=1, omega(|G|)=4+omega(r), and
  c(G)=32*c(P)*tau(r), proving (2).

Since delta(r)>=1, the split type in (2) has eta at least
2(p+2)>=18. The cyclic type has eta=2(a+2)delta(r). For this to be
at most 6 one must have a=1 and delta(r)=1. The latter holds precisely
when r is squarefree, including r=1.

In the new-prime case eta<=6 is equivalent to delta(m)<=3/2. If
m=product q_i^{b_i}, with b_i>=1, then

$$\delta(m)=\prod_i\frac{b_i+1}{2}.$$

An exponent >=3 contributes at least 2; two exponents 2 contribute
at least 9/4. Thus delta(m)<=3/2 precisely when all exponents are 1,
or exactly one is 2 and all the others are 1. The values are 1 and
3/2 respectively. This also covers the empty product m=1.

Every identified group contains A_5 as a subgroup and is nonsolvable:
a nontrivial perfect group cannot be solvable, and subgroups of
solvable groups are solvable. The converse counts follow from the same
formulas. Appropriate central kernels are the subgroup of order p in
the cyclic factor (new p, or the repeated p in p^2r).

## 5. Elementary A_5 facts used above

A_5 is generated by its 3-cycles: decompose an even permutation into
an even number of transpositions, pair them, and express each pair
as a product of 3-cycles (or as the identity). All 3-cycles are conjugate
in A_5. A permutation carrying one 3-cycle to another can, if odd, be
multiplied by the transposition of the two complementary letters,
which centralizes the original cycle and changes its parity.

For x=(12)(34) and y=(12)(35), the commutator [x,y]=xyx^{-1}y^{-1}
is a 3-cycle. The derived subgroup is normal, so contains all 3-cycles
and equals A_5. Thus A_5 is perfect.

If a permutation is central in A_5, conjugating each 3-cycle by it
leaves that cycle fixed, so it preserves every three-element subset
of the five letters. The intersection of all three-element subsets
containing a fixed letter is that letter alone. The permutation must
fix each letter; hence Z(A_5)=1.

These arguments suffice for this lemma; no classification of finite
simple groups is used here.

## 6. Interface with the shared target and evidence limits

Rowan's separate kernel lane must establish, for the surviving
persistent-prime case, a central order-p kernel with p>5 and quotient
A_5 x C_{pr}, r squarefree and gcd(r,30p)=1. Under those exact
hypotheses, this lemma identifies the lift as A_5 x C_{p^2r}
whenever eta(G)<=6, and proves eta(G)=6. For a new central prime,
the lemma preserves the quotient's squarefree/one-squared-prime type.

The new-prime noncentral action analysis, global induction and
radical-free base are outside this lemma. In particular, this conditional
result does not make the selected universal theorem unconditional.

The accompanying program enumerates literal cyclic subgroups of small
permutation/abelian product fixtures, and also sums exact generator
weights. It corroborates the constants and the distinction between
cyclic and elementary-abelian p-squared lifts. It does not enumerate
all extensions, prove the uniform decomposition, or replace an
independent internal check of the written argument.

The decomposition and counting ingredients are classical. Historical
novelty is claimed neither for central coprime splitting nor for the
abelian group formulas; the present purpose is an explicit, checked
boundary bridge for the campaign's proposed gap-6 classification.
