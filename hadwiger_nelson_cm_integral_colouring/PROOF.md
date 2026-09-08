# Integral CM coordinates and rational unit-edge angles

Write `UD(X)` for the graph on a specified subset `X` of the complex plane,
joining distinct points when their usual Euclidean distance is one.

**Theorem.** Let `K` be a CM number field with a specified embedding in the
complex plane, and let `O_K` be its ring of algebraic integers. Let `m` be the
order of the finite group of roots of unity in `K`. Then

\[
\chi(\operatorname{UD}(O_K))=
\begin{cases}
2,&m\text{ is a power of }2,\\
3,&m\text{ has an odd prime divisor}.
\end{cases}
\]

In particular, no finite subset of a translate, rotation, or reflection of
`O_K` is four-chromatic or five-chromatic. This concerns integrality at the
physical unit scale. It does not assert a colouring of all of `K`, of arbitrary
fractional ideals, or of arbitrary rescalings of `O_K`.

**Corollary.** Every finite plane unit-distance graph in which the angles
between the unit-edge directions in each connected component are rational
multiples of pi is three-colourable. A four-chromatic graph therefore needs an
irrational relative unit-edge angle in at least one of its components.

The proof is uniform in the field, conductor, number of vertices, and shape of
the selected support. The executable certificates are implementation controls;
they are not a finite replacement for this proof.

## 1. An additive three-colouring of roots-of-unity steps

For every positive integer `n`, set `A_n=Z[zeta_n]`, with
`zeta_n=exp(2*pi*i/n)`. We construct an additive homomorphism

\[
\tau_n:A_n\longrightarrow\mathbb F_3
\quad\text{such that}\quad
\tau_n(\zeta_n^j)\in\{1,-1\}\quad(j\in\mathbb Z).
\tag{1}
\]

It need not be a ring homomorphism. Additivity suffices: endpoints whose
difference is a root step have different images in the three-element colour
set. Negative root steps are covered by additivity too.

First take `q=p^e`, a prime power, and put `L=p^(e-1)`. Choose signs
`epsilon_0,...,epsilon_(p-1)` with sum zero modulo three. One uniform choice
has its first `k` signs positive and the rest negative, where

\[
k\in\{0,1,2\},\qquad k\equiv2p\pmod3.
\]

There are at least `k` available positions, and the sum is `2k-p=0 mod3`.
For `p=2` the signs are `(1,-1)`; for `p=3` all three signs are `-1`.
Define

\[
\tau_q(\zeta_q^{r+jL})=\epsilon_j,
\qquad 0\le r<L,\quad0\le j<p.                 \tag{2}
\]

This assignment respects all integral linear relations. Indeed,

\[
\Phi_q(X)=1+X^L+\cdots+X^{(p-1)L}.
\]

The powers with exponents below `(p-1)L` form an integral basis of `A_q`.
For each `r<L`, the remaining power is minus the sum of the previous `p-1`
powers in that residue class modulo `L`. Equation (2) respects precisely this
relation because the signs sum to zero. Thus it defines an additive map, and
every power of `zeta_q` has nonzero image.

Now factor `n` into pairwise coprime prime powers `q_1,...,q_s`. Multiplication
induces an isomorphism of free abelian groups (indeed of rings)

\[
\bigotimes_{r=1}^s\mathbb Z[\zeta_{q_r}]
\ \simeq\ \mathbb Z[\zeta_n].                 \tag{3}
\]

For completeness, the map is surjective: if
`t_r=(n/q_r)^(-1) mod q_r`, the Chinese remainder identity gives

\[
\zeta_n=\prod_r\zeta_{q_r}^{t_r}.
\]

Both sides of (3) are free abelian of rank
`product phi(q_r)=phi(n)`. A surjection between free abelian groups of the
same finite rank has zero kernel, proving (3). Here we use the usual
irreducibility and degree formula for cyclotomic polynomials.

The multilinear map taking a pure tensor to
`product tau_(q_r)(x_r)` modulo three induces an additive map on (3).
Consequently

\[
\tau_n(\zeta_n^j)=\prod_r\tau_{q_r}
          (\zeta_{q_r}^{t_rj})\in\{1,-1\},     \tag{4}
\]

as required. For `n=1`, take ordinary reduction of integers modulo three.
This proves (1) for every conductor without enumeration.

The implementation evaluates (4) on the standard power basis. More
explicitly, write the least residue of `t_r*j mod q_r` as
`r_r+b_r*(q_r/p_r)`. Its factor in (4) is the sign indexed by `b_r`.
For `z=sum a_j*zeta_n^j`, colour by `sum a_j*tau_n(zeta_n^j) mod3`.

## 2. Why CM integral unit differences are root steps

A CM field is a totally imaginary quadratic extension of a totally real
field. Its nontrivial involution `c` is physical complex conjugation and
satisfies

\[
\sigma(c(x))=\overline{\sigma(x)}
\]

for every embedding `sigma:K -> C`. This can be seen by writing
`K=F(sqrt(-d))`, with `F` totally real and `d` totally positive. Under every
embedding the added square root is purely imaginary. No Galois hypothesis on
`K/Q` is needed.

If `alpha` is an algebraic integer in `K` and `|alpha|=1` in the specified
plane embedding, injectivity gives `alpha*c(alpha)=1` as an equality in `K`.
Every embedding therefore sends `alpha` to a number of absolute value one.
It follows that `alpha` is a root of unity. One elementary version of this
standard Kronecker argument is as follows: every power of `alpha` is an
algebraic integer of bounded degree with all conjugates of absolute value one.
The coefficients of its monic minimal polynomial are bounded elementary
symmetric sums. There are only finitely many possible integer polynomials,
and hence finitely many possible powers. Two powers coincide and `alpha` is
nonzero, so it has finite multiplicative order.

The same bounded-degree argument shows that `mu(K)`, the roots of unity in
`K`, is finite. A finite subgroup of the complex unit circle is cyclic; write
`mu(K)=<zeta_m>`. Since `-1` belongs to it, `m` is even and at least two.

For vertices `x,y` in `O_K`, their difference is integral. We have proved

\[
|x-y|=1\quad\Longleftrightarrow\quad x-y\in\mu(K). \tag{5}
\]

Thus the connected components of `UD(O_K)` are exactly the additive cosets
of `Z[mu(K)]=Z[zeta_m]`: every edge stays in one coset, and an integral linear
combination of roots can be traversed by steps from `mu(K)`, including their
negatives. Translate each coset to this subgroup and apply `tau_m` from (1).
This proves the upper bound three. Representatives can be chosen from any
enumeration of the countable ring; on a finite connected input, a chosen root
vertex and unit-edge paths already provide the required translation.

If `m=2^e`, evaluate the power-basis polynomial at `1` modulo two instead.
This descends to `Z[zeta_m]` because `Phi_m(1)=2`, and takes every root step to
one. It gives a proper two-colouring. The edge from `0` to `1` proves equality.

If an odd prime `p` divides `m`, let `eta=zeta_m^(m/p)`. The points

\[
0,\quad1,\quad1+\eta,\quad\ldots,\quad
1+\eta+\cdots+\eta^{p-2}
\]

give an odd closed unit cycle: consecutive differences are powers of `eta`,
and the last-to-first difference is `eta^(p-1)`. The vertices are distinct by
the geometric-series formula, since a proper consecutive sum of the `p`th
roots is nonzero. Additional edges cannot destroy this odd cycle. Hence the
graph is not bipartite and has chromatic number exactly three. This completes
the theorem.

## 3. Cyclotomic integer supports and the rational-angle corollary

For `A_n=Z[zeta_n]`, every unit difference is a root of unity by Section 2
(the real cases `n=1,2` give just the ordinary integers). The roots of unity
in `Q(zeta_n)` have order `lcm(n,2)`. Here is a short justification useful for
the exact checker: if their group has order `h`, then `lcm(n,2)` divides `h`
and `phi(h)<=phi(n)`, since `Q(zeta_h)` is a subfield. For even `N`, every
strict multiple of `N` has strictly larger totient: increasing an existing
prime exponent multiplies the totient by that prime, and adjoining a new
odd prime multiplies it by at least two. Applying this with `N=lcm(n,2)`
forces equality. Thus the directions are the powers of `zeta_n` and their
negatives, all separated by (1).

This also proves `chi(UD(A_n))=2` for power-of-two `n` (including `n=1`),
and `chi(UD(A_n))=3` otherwise. The same bounds hold for arbitrary finite
supports, coefficient boxes, integer sumsets, and windows inside this ring
at the same physical unit scale.

For the corollary, treat each connected component separately. Rotate one of
its unit-edge directions to `1`. All its other oriented unit differences are
then roots of unity. Finitely many edges admit a common conductor `n`.
Translate a root vertex to zero and follow paths: every resulting vertex lies
in `Z[zeta_n]`. The map (1) gives a proper three-colouring. Components with no
edges are harmless. Only the specified edges need satisfy the angle
hypothesis; the statement does not claim that additional unit edges in an
arbitrary drawing have rational angles.

## 4. The boundary and the computational checks

The distinction between integral coordinates and an entire CM field is
essential. In `Q(zeta_132)`, take `b=i*sqrt(3)`, `c=i*sqrt(11)`,
`w=(1+b)/2`, and `u=(5+c)/6`. The points

\[
0,1,w,1+w,u,uw,u(1+w)
\]

form the seven-vertex Moser spindle. Its two diamonds force their nonadjacent
tips to share colours in every three-colouring. Their common tip then forces
the other two tips equal, contradicting the bridge between those tips. The
word `(0,1,2,0,1,2,3)` is a proper four-colouring. The direction `u` satisfies
`3u^2-5u+3=0`; its quadratic trace is `5/3`, so it is not an algebraic integer.
This gives an exact failure of an attempted whole-field strengthening.

The public fixture is the 256-point set
`{sum b_j*zeta_30^j : b_j in {0,1}, 0<=j<8}`. Its points are distinct because
these eight powers form a rational basis. The producer tests the exact norm
of every one of its 32,640 differences. The independent verifier instead
matches differences against the 30 root directions, whose completeness was
proved above. Both give 1,240 strict unit edges. The stored word uses three
colours, and the unit triangle `0,1,zeta_30^5` proves the lower bound three.

For 44 selected conductors, the producer constructs a functional using (4)
and cyclotomic polynomials by exact monic division. The independent verifier
reconstructs the polynomials from Ramanujan power sums by Newton identities,
then iterates multiplication by `X` in `F_3[X]/Phi_n`. All 7,321 root powers
have nonzero functional values. Corrupt functional, polynomial, edge-list,
and colour-word controls are rejected. A separate exact seven-point check
verifies the denominator boundary above. No SAT result is used.

## Sources and status

The arithmetic ingredients are standard. See Milne,
[Algebraic Number Theory, v3.08](https://www.jmilne.org/math/CourseNotes/ANT.pdf),
Corollary 5.6 for the bounded-conjugates root-of-unity result and Section 5's
CM-field discussion for the conjugation property. The argument is included
above to make the bridge to Euclidean distance explicit.

Radchenko's
[Unit distance graphs and algebraic integers](https://arxiv.org/html/1807.03726v1)
discusses root-of-unity generated additive groups and notes their finite unit
degree. It also constructs a non-CM source with infinitely many unit
directions; this theorem makes no general claim about non-CM integral points.

The tensor colouring and its consequences are recorded here as a uniform
source obstruction for the HN campaign. Targeted primary-literature searches
did not identify this precise colouring statement; no priority claim is made.
This is a written mathematical proof with exact executable controls, not a
proof-assistant formalization or an independently reviewed contribution.
