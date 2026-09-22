# Exponent-four local Ehrhart parity is a binary quadratic invariant

Fix the ambient lattice `Z^d`. Let `P` be bounded, full dimensional and
half-integral (`2P` is a lattice polytope), with a fixed integral
actual-facet description. Call a nonempty face **bad** if its affine span
contains no lattice point. Suppose bad faces exist. Let `g` be their minimum
codimension, `k=d-g`, and `M` the bad faces of codimension `g`.

At every `F in M` assume there are exactly `g` active facets. Their independent
row map is `C_F:Z^d -> Z^g`; set `G_F=Z^g/C_F Z^d`. Assume `4G_F=0`.
This is an exponent assumption, not a bound of four on the group order.
Facet rows need not be primitive. The presentation and ambient lattice are
part of the hypotheses.

Write the Ehrhart quasipolynomial uniquely as

    L_P(n)=A(n)+(-1)^n B(n),  A,B in Q[n].

## The theorem

For each `F in M`, let `b` be the class of its active right side and let
`q_j` be the class of the `j`th standard basis vector of `Z^g`.

**Group obstruction.** Either `G_F=C_2`, with every `q_j=b`, or

    G_F = C_4 x F_2^s,  b=(2,0),  s>=0.                (1)

In particular, two or more independent `C_4` factors, and noncyclic groups
of exponent two, are impossible at a locally simple minimum bad face.
In (1), every coordinate class is `(2,0)` or `(epsilon_j,x_j)` with
`epsilon_j in {1,3}` and `x_j in F_2^s`.

Let `h` be the number of `(2,0)` columns and `m=g-h` the number of odd
columns. The `(s+1) x m` binary matrix with columns `(1,x_j)` has full row
rank. Define its kernel and a quadratic form on it by

    D={z in F_2^m : sum z_j=0, sum z_j x_j=0},
    Q(z)=wt(z)/2 + sum_{epsilon_j=3} z_j  (mod 2).       (2)

The weight is even on `D`, so this is well defined. Its polar form is
`beta(z,w)=z.w`. Put `R=D intersect D^perp`, `ell=dim D=m-s-1`, and
`rho=dim R`. Let `Delta_F` be the even-minus-odd local cone coefficient.
Then

    Delta_F = 2^(-g) sum_{z in D} (-1)^Q(z).            (3)

Consequently:

- `Delta_F=0` exactly when `Q` is nonzero on `R`.
- Otherwise `Q` descends to a nonsingular form `Qbar` on `D/R`, and

      Delta_F=(-1)^Arf(Qbar) 2^(-g+(ell+rho)/2).        (4)

  Here `ell-rho` is even. Equivalently its nonzero magnitude is
  `2^(-h-s-1-rank(beta)/2)`.

For `G_F=C_2`, instead `Delta_F=2^(-g)`.
The definition of the Arf invariant used here is
`sum_i Q(u_i)Q(v_i) mod 2` for a symplectic basis of `D/R`.
On the zero vector space it is zero.

The global consequence is

    deg B <= k,
    [n^k]B = (1/2) sum_{F in M} vol_k(F) Delta_F.       (5)

Volume is normalized by `lin(F-F) intersect Z^d`; a lattice cube and a
point have volume one. If the signed sum is nonzero, the minimal Ehrhart
period is two, `deg B=k`, and the reduced series denominator is
`(1-t)^(d+1)(1+t)^(k+1)`. A zero signed sum proves only a degree drop;
lower coefficients can still vary. This limitation is essential.

**Realization and exact collapse criterion.** Every generating coordinate
profile allowed in (1) occurs as the active profile of the unique bad vertex
of a half-integral simplex. For this simplex `B(n)=Delta/2` is constant.
Its period is one exactly when `Q|R` is nonzero; otherwise its period is two.
Thus (2)--(4) are a complete collapse criterion for this realization class.

The new scope is the group obstruction and this uniform geometric
quadratic-form criterion. Finite character filters, quadratic Gauss sums,
Arf theory, and local Euler--Maclaurin formulas are classical. The cyclic
order-four predecessor is recovered at `s=0`; its arbitrary even cyclic
order theorem is outside the present exponent-four scope. No claim about
all nonsimple faces, exponent eight, or all period-collapse polytopes is made.

## 1. A minimum bad face imposes a common involution

Local simplicity implies that every subset `I` of the `g` active facets
cuts a face of codimension `|I|`: at a relative-interior point of `F`, solve
for a direction preserving the rows in `I` and strictly decreasing the
others. Independence permits this, and a sufficiently small step preserves
all inactive slacks. The resulting face has affine span `C_I x=b_I`.

Every proper subset therefore has an integral affine solution, by minimality
of `g`. Deleting row `j` gives an integer `z` with `C_i z=b_i` for `i!=j`.
In `G_F` this says

    b belongs to <q_j> for every j.                    (6)

The class `b` is nonzero and has order two: an integral solution would
contradict badness, while twice a half-integral vertex of `F` supplies a
solution for twice the right side. The classes `q_j` generate `G_F`.

In a group of exponent at most four, (6) forces either `q_j=b` or
`q_j` of order four with `2q_j=b`. Thus `2G_F` is either zero or `<b>`.
If it is zero, all generators equal `b`, giving `C_2`. Otherwise the
classification of finite abelian groups gives precisely (1). Under this
identification the only allowed order-two column is `(2,0)`, and all
order-four columns have odd first coordinate. They generate the group
exactly when their images `(1,x_j)` span `G_F/2G_F`; one odd column already
supplies the generator `b` of `2G_F`. This proves the rank assertion.

This excludes whole cokernel families using geometric minimality. It does
not assert that such groups cannot occur at other faces of a polytope.

## 2. General finite-group local character formula

This section extends the preceding cyclic character argument without
assuming cyclicity. Pass to the transverse real quotient by `ker C_F`,
retaining the projected lattice `Lambda=pi(Z^d)`. The induced real
isomorphism `C` carries `Lambda` onto `L=C_F Z^d`.
Let the active right-side vector be `b0 in Z^g`, put `v=C^-1 b0`, and set

    K_n={y: Cy<=n b0}.

Lattice points correspond to integer nonnegative slacks `u=n b0-Cy` with
`[u]=n b` in `G_F`. If `lambda_j(xi)=<xi,C^-1 e_j>`, character orthogonality
therefore gives, initially in a convergence chamber,

    exp(-n<v,xi>) S(K_n)(xi)
      = (1/|G_F|) sum_chi chi(-n b)
          product_j (1-chi(q_j) exp(-lambda_j(xi)))^(-1). (7)

It then holds as a meromorphic identity. For every character with
`chi(b)=-1`, (6) ensures `chi(q_j)!=1` for every `j`; its product is analytic
at zero. Since `b` has order two, subtracting odd from even in (7) yields

    Delta_F=(2/|G_F|) sum_{chi(b)=-1}
                         product_j (1-chi(q_j))^(-1).  (8)

Here is the geometric justification that this difference is indeed the
local `mu` jump, rather than an unjustified evaluation of singular sums.
Use one rational scalar product and the induced quotient lattices throughout
Berline--Vergne's cone face identity. For a positive-dimensional cone face,
the active equality set `I` is proper. Its integral solution `z_I` makes
`v-pi(z_I)` lie in that face's direction space. The even and odd transverse
shifts thus differ by a lattice translation. Its `mu` term is unchanged.
After the vertex exponential is removed, its face integral is also unchanged
because the face cone shape and normalized direction volume are identical.
All positive-dimensional face terms, including the full cone, cancel.
Only the vertex term remains. This proves (8) using translation invariance,
with no assumption that individual `mu` values are positive.

For `C_2`, the sole contributing character is `-1` on every `q_j`, giving
`2^(-g)`. The finite-group formula (8) itself is the usual character filter
applied to this geometric setup; no novelty for Fourier orthogonality is
claimed.

## 3. From characters to a binary quadratic form

In (1), characters with value `-1` on `b` are indexed by
`a in {1,3}` and `y in F_2^s`. On an odd column they have value
`i^(a epsilon_j) (-1)^(y.x_j)`. The two choices of `a` are conjugates;
on an order-two column the reciprocal denominator is `1/2`.
Using `(1-i)^(-1)=(1+i)/2` and its conjugate, (8) becomes

    Delta_F=2^(-s-g) Re sum_{y in F_2^s}
          product_{j=1}^m (1+i^epsilon_j (-1)^(y.x_j)). (9)

Expand the product. Orthogonality of the binary characters removes exactly
the subsets with nonzero sum of their `x_j`. Taking real parts removes
exactly the odd-cardinality subsets. For an even subset represented by `z`,
its remaining term is

    Re i^(sum epsilon_j z_j)
      =(-1)^(wt(z)/2 + sum_{epsilon_j=3}z_j).

This proves (3), including the factor `2^(-g)`.
Furthermore

    Q(z+w)+Q(z)+Q(w)=z.w,

because `wt(z+w)=wt(z)+wt(w)-2|supp(z) intersect supp(w)|`.
The polar form is alternating on `D`, since all its words have even weight.

## 4. Exact zero and sign, with short certificates

On the radical `R`, `Q` is linear. If `r in R` has `Q(r)=1`, translation by
`r` pairs every summand in (3) with its negative. The sum is zero, and the
word `r` is a direct cancellation certificate.

Otherwise `Q` descends to `D/R`, and every quotient word has `2^rho` lifts.
Split the nonsingular alternating form into orthogonal symplectic planes.
For a plane with basis `u,v`, a direct four-element sum is

    sum_{a,b in F_2} (-1)^(a Q(u)+b Q(v)+ab)
      =2(-1)^(Q(u)Q(v)).

Multiplication over the `(ell-rho)/2` planes gives a nonzero sum of magnitude
`2^((ell+rho)/2)` and sign `(-1)^Arf`. This also proves independence of the
computed sign from the chosen symplectic basis, and establishes (4).
The radical-zero criterion and Gauss-sum calculation are classical; the
argument is included to fix every convention and normalization.

The algorithm uses a binary kernel basis followed by symplectic elimination:
for a pair `u,v` with `u.v=1`, replace each remaining basis word `w` by
`w+(w.v)u+(w.u)v`. The final unpaired words form a radical basis. A nonzero
restriction of `Q` to this basis certifies cancellation. Otherwise the pairs
certify the Arf sign and rank. This is polynomial-size linear algebra in the
provided profile, not an enumeration of `2^(s+1)` characters or `2^ell` words.
It does not find minimum bad faces from arbitrary input inequalities.

## 5. Global assembly and realizability

Berline--Vergne's dimension-specific local Ehrhart formula expresses the
coefficient of `n^j` as the sum over `j`-faces of their `mu` coefficients
times normalized volumes. Faces with lattice affine span have period one;
half-integrality bounds all periods by two. In dimensions above `k` there
are no bad faces; in dimension `k`, (8) supplies exactly their even-minus-odd
variation. Dividing by two gives (5). The stated poles follow from the
standard generating series for a degree-`k` polynomial evaluated at `-t`.

For realizability, start with any allowed generating profile in (1), define

    L={u in Z^g : sum_j u_j q_j=0 in G},

and choose an integer `b0` mapping to `b`. Put `lambda_j=1` for `q_j=b`
and `lambda_j=2` for odd columns. In `R^g` with lattice `L`, set

    P_q=b0-conv(0,lambda_1 e_1,...,lambda_g e_g).        (10)

The apex is strict half-lattice, and every other vertex is integral because
`lambda_j q_j=b`. Every positive-dimensional face contains an integral
nonapex vertex. Thus the apex is the sole bad face. Its actual coordinate
facets have active cokernel `G` and the prescribed classes. A lattice basis
of `L` identifies (10) with an ordinary half-integral simplex in `Z^g`.
All facet equations admit integral coefficients, including the remaining
slanted facet. Consequently `B=Delta/2` exactly, and period collapse is
equivalent to the radical cancellation criterion.

A definition-level count, used by the verifier, is

    L_Pq(n)=#{u in Z^g_>=0 : sum_j u_j/lambda_j<=n,
                              sum_j u_j q_j=n b in G}. (11)

For example, the genuinely noncyclic group `C_4 x C_2` has positive, zero
and negative jumps on profiles

    ((1,0),(1,1)):                    Delta= 1/4,
    ((1,0),(1,0),(1,1)):              Delta= 0,
    ((1,0),(1,0),(1,0),(1,1)):        Delta=-1/8.

These illustrate the invariant, not a priority claim for isolated
collapsing simplices. The cyclic collapsing triangle and its familiar
pyramids are already part of the classical period-collapse literature.

## Trust boundary

The universal proof is unformalized. Its analytic import is the cited
Berline--Vergne construction; the finite group restriction and the binary
calculation are proved above. Code corroborates the statements by direct
character sums, independent word enumeration, finite group generation,
and lattice counts, but does not replace the geometric face and quotient
arguments. It assumes a correctly supplied coordinate profile and does not
recognize all hypotheses of the geometric theorem. No solver, floating-point
arithmetic, external dataset, or claim of independent review is involved.
