# Gamma nonnegativity with at most six excess vertices

24 September 2026. Complete proof attempt, pending independent review.

**Theorem.** Let Delta be a finite flag generalized homology (d-1)-sphere
over a field. If it has n <= 2d+6 vertices, every coefficient of its gamma
polynomial is nonnegative.

We use dimension-indexed face numbers, with f_-1=1, and

    h_Delta(z) = sum_(j=0)^d f_(j-1) z^j (1-z)^(d-j)
               = sum_i gamma_i z^i (1+z)^(d-2i).

Put ell=n-2d=gamma_1. A flag sphere has ell>=0. Coefficients with
i>floor(d/2) are zero. The empty sphere has gamma=1. The homology
hypothesis applies to every face link, including the empty-face link.

The result follows from a dimension reduction and the previously accepted
17- and 18-vertex five-sphere inequalities. No new sphere enumeration or SAT
search is used. In particular, it proves Gal's conjecture throughout the
six-excess-vertex range in every dimension, not the unrestricted conjecture,
a classification of these spheres, or a realization of gamma as a face vector.

## 1. Inputs and their precise roles

The following published facts are used from
[Labbé--Nevo](https://arxiv.org/abs/1612.01169v2), abbreviated LN.

- Lemmas 2.1--2.4 and 3.2: links are induced flag homology spheres;
  suspension preserves gamma; the complement degree q_v lies in
  [1,ell+1]; and the link of v has excess ell+1-q_v. Degree one is
  equivalent to a suspension.
- Lemma 3.4: when v has exactly two nonneighbors x,y, xy is an edge,
  J=lk(xy) is an induced equator in L=lk(v), and

      gamma_Delta(t) = gamma_L(t) + t gamma_J(t).                 (1)

  Here L has excess ell-1, and J has excess at most ell-1. For the latter
  bound, an induced equator has at least two vertices outside it, so
  |V(J)|<=|V(L)|-2 while its dimension is one less.
- Theorem 3.5(i): if v attains the **minimum** complement degree p>1
  and lk(v)=Sigma Gamma, then Delta=Gamma*C_(p+3). The excess of Gamma
  is ell-p+1, and gamma_Delta=(1+(p-1)t) gamma_Gamma.
- Lemma 4.1: a sphere without a suspension pair has d<=2ell.
- Theorems 4.2 and 5.2: gamma_j=0 for j>ell,
  gamma_ell in {0,1}, and gamma_(ell-1) in {0,1,2,ell} for ell>=2.
- Lemma 5.1: an induced equator in a join of k pentagons is the
  suspension of a join of k-1 pentagons.

The low-dimensional input is
[Davis--Okun, Theorem 11.2.1](https://arxiv.org/abs/math/0102104):
gamma_2>=0 for flag rational homology 3-spheres. The link identity below
gives the same conclusion in dimension four. Thus full gamma nonnegativity
holds for d<=5. These uses are valid over any field: universal coefficients
force the lower integral free ranks of each finite face link to vanish;
coefficient-independent Euler characteristic gives top rational rank one.
Apply this separately to every link. No torsion-free assertion is made.

The two additional inputs, whose provenance and reviews are in SOURCES.md,
are gamma_3>=0 for flag homology 5-spheres on exactly 17 vertices and on
exactly 18 vertices. The new result retains their trust boundaries. Neither
finite input is needed for Sections 2--5 below.

## 2. A complement identity for arbitrary dimension and excess

Let H be the complement of the one-skeleton, m=e(H), q_v=deg_H(v),
T the number of triangles in H, and t_v=e(H[N_H(v)]). Write
a=gamma_2(Delta), b=gamma_3(Delta). For d>=6, direct counts give

    a = d + ell(ell+5)/2 - m,
    b = (ell+4)(6d+ell^2+11ell)/6
        + (1/2) sum_v q_v(q_v-ell-5) - T,                       (2)
    L_v := gamma_2(lk(v))
        = a + ell+2 + q_v(q_v-2ell-7)/2
          + sum_(u in N_H(v)) q_u - t_v.

To derive (2), the number of independent triples in H is

    f_2(Delta) = choose(n,3) - (n-2)m
                + sum_v choose(q_v,2) - T.

Insert this, f_1=choose(n,2)-m, and n=2d+ell into the h-to-gamma
coefficient conversion. For the local identity, the link complement is
induced on V(H) minus ({v} union N_H(v)) and has
m-sum_(u in N_H(v))q_u+t_v edges. Its parameter is d-1 and its excess
is ell+1-q_v. Substitution in the formula for a gives L_v.

Double-counting vertex/face incidences yields

    sum_v h_lk(v)(z) = d h_Delta(z) + (1-z) h'_Delta(z).

Changing basis gives, coefficientwise,

    sum_v gamma_i(lk(v))
      = (2d-4i) gamma_i(Delta) + (i+1) gamma_(i+1)(Delta).       (3)

In particular S:=sum_v L_v=(2d-8)a+3b. For a homology 4-sphere,
2 gamma_2=sum_v gamma_2(lk(v)); in kappa notation this is
gamma_2=8 sum_v kappa(lk(v)), with factor 8, not its reciprocal.

Define

    K(ell,d) = ell(ell^2+3ell+20-12d)/6,
    R = sum_v (q_v-3)(ell+1-q_v).

Rearranging (2), using sum_v q_v=2m, gives the exact identity

    b = a + K(ell,d) - R/2 - T.                               (4)

If every q_v>=3, then q_v<=ell+1 implies R>=0. Consequently

    S <= (2d-5)a + 3K(ell,d).                                 (5)

The identity and inequality are reusable outside the present vertex range;
local nonnegativity of L_v, whenever available, supplies a lower bound on a.
The quantities in (2)--(5) are integral or exact rationals; no numerical
approximation is used.

## 3. Gamma_2 is nonnegative when ell<=6

For ell<=3 the LN endpoint and vanishing results already give the claim.
Proceed by induction on ell in {4,5,6}, and, at fixed ell, on d. The
case d<=5 is the low-dimensional input. Assume d>=6.

If the minimum complement degree is one, remove a suspension pair and
use the same-ell induction in d. If it is two, (1) gives
a=gamma_2(L)+gamma_1(J)>=0, since L has smaller excess.

Otherwise all q_v>=3. Every vertex link has excess at most ell-2,
so its gamma_2 is nonnegative by the induction on ell. Hence S>=0.
If a<0, integrality gives a<=-1, and (5) gives

    S <= 3K(ell,d) - (2d-5).

At d=6 these right sides, for ell=4,5,6, are respectively
-55,-37,-1. Increasing d decreases the right side by 6ell+2 at each
step. It is therefore strictly negative for every d>=6, a contradiction.
This proves gamma_2>=0 for ell<=6 in every dimension.

Together with LN's endpoint bounds, this already proves **full gamma
nonnegativity for ell<=4**, independently of the 17- and 18-vertex inputs.

## 4. Two boundary cases of the suspension dimension bound

These statements hold for arbitrary excess and follow from the named LN
structure results. Their role is to extract a rigid link polynomial.

**Lemma A.** If a flag homology (d-1)-sphere has no suspension pair,
ell>=1, and d=2ell, then it is the join of ell pentagons.

Proof. For ell=1 it is the five-vertex cycle. For ell>1 choose a vertex
of minimum complement degree p>=2. Its link has parameter 2ell-1 and
excess ell-p+1<=ell-1, so the suspension bound forces the link to be
a suspension. LN's minimum-degree join theorem gives Delta=Gamma*C_(p+3),
where Gamma has parameter 2ell-2 and excess ell-p+1. Gamma cannot be
a suspension, since that would make Delta one. Its suspension bound gives
2ell-2<=2(ell-p+1), so p=2. Induction identifies Gamma as the join of
ell-1 pentagons. QED.

**Lemma B.** If there is no suspension pair, ell>=2, and d=2ell-1, then

    gamma_Delta(t) = (1+2t)(1+t)^(ell-2).                       (6)

Proof. Again choose a minimum-degree vertex with degree p>=2. If p>=3,
its link has parameter 2ell-2 and excess at most ell-2, so it is a
suspension. The join theorem would give a nonsuspension Gamma with
parameter 2ell-3 and excess at most ell-2, contradicting its dimension
bound. Thus p=2.

The link L has parameter 2ell-2 and excess ell-1. If L is a suspension,
the join theorem gives Delta=Gamma*C_5, with Gamma in the assertion for
ell-1, proving (6) by induction. At ell=2 this alternative would require
a zero-sphere of excess one and is impossible.

If L is not a suspension, Lemma A gives L=*^(ell-1) C_5. For the two
antipodes x,y, the equator J=lk(xy) is Sigma(*^(ell-2) C_5) by LN's
equator lemma. Formula (1) gives

    gamma_Delta = (1+t)^(ell-1) + t(1+t)^(ell-2),

which is (6), including ell=2. QED.

In particular, a nonsuspension homology 6-sphere of excess four has
gamma=(1,4,5,2). No enumeration of such links is needed.

## 5. A structural reduction at excess six

**Proposition.** If ell=6 and d>=8, Delta has a vertex with at most two
nonneighbors. Equivalently, its minimum complement degree is at most two.

Proof. Suppose all q_v>=3; then 3<=q_v<=7. For these five degrees,
q(q-11)/2<=-12. Formula (2) implies

    b <= 10d+170 - 12(2d+6) = 98-14d < 0.                    (7)

Choose v of minimum degree p. If lk(v)=Sigma Gamma, the minimum-degree
join theorem gives Delta=Gamma*C_(p+3), with Gamma of excess 7-p<=4.
Section 3 proves its full gamma nonnegativity; multiplying by
1+(p-1)t contradicts (7).

Thus lk(v) is not a suspension. Its parameter is d-1 and its excess
is 7-p. The suspension bound implies d-1<=2(7-p), so d<=15-2p.
Since d>=8 and p>=3, this leaves exactly p=3 and d in {8,9}.
By Section 3, every vertex link has nonnegative gamma_2, so S>=0.

For d=9, let n_j count degree-j vertices. Equations (2) and (3) give

    S = -24 - 11n_4 - 19n_5 - 24n_6 - 26n_7 - 3T < 0,

a contradiction.

For d=8 there are 22 vertices and

    S = 22 - 10n_4 - 17n_5 - 21n_6 - 22n_7 - 3T >= 0.         (8)

Put D=sum_v(q_v-3)=n_4+2n_5+3n_6+4n_7. Each cost in (8) is at
least (11/2)(j-3), so D<=4. Also a=8-D/2. At the chosen cubic vertex,
the local identity (2) and nonnegativity of t_v yield

    gamma_2(lk(v)) = a-16 + sum_(u in N_H(v))q_u - t_v
                   <= (8-D/2)-16+(9+D)
                   = 1+D/2 <= 3.                             (9)

But this link is a nonsuspension with parameter 7 and excess 4. Lemma B
forces its gamma_2 to equal 5, contradicting (9). This closes the final
case and proves the proposition. QED.

This proposition, the degree identity, and the gamma_2 theorem use only
the published LN and low-dimensional topology inputs. In particular, they
do not assume the new all-dimensional conclusion or either finite seed.

## 6. Transfer of the finite seeds to every dimension

We have full positivity for ell<=4. First take ell=5, inducting on d.
For d<=5 use the low-dimensional theorem. At d=6, gamma_2>=0 follows
from Section 3 and gamma_3>=0 is the accepted 17-vertex theorem. At
d=7, each vertex link has parameter 6 and excess at most 5, hence is
covered by the preceding cases. Equation (3), with i=3 and gamma_4=0,
gives

    2 gamma_3(Delta) = sum_v gamma_3(lk(v)) >= 0.

Together with Section 3 this covers every coefficient at d=7. For d>=8,
minimum degree one removes a suspension pair; minimum degree two uses
(1) with both excesses at most four. If the minimum is p>=3, the chosen
link has excess 6-p<=3 and parameter d-1>=7, so it must be a suspension.
The join theorem reduces to a Gamma of excess at most three, whose
coefficients are nonnegative. This completes ell=5.

Now take ell=6. The cases d<=5 are known. At d=6, Section 3 and the
accepted 18-vertex gamma_3 theorem cover every coefficient. At d=7,
all vertex links have parameter 6 and excess at most 6, so the same
displayed link sum proves gamma_3>=0; Section 3 handles gamma_2.
For d>=8, Section 5 leaves minimum degree one or two. In the former case,
suspension reduction lowers d; in the latter case, (1) expresses gamma
as gamma_L+t gamma_J with both excesses at most five. These have already
been proved nonnegative in every dimension. Induction completes ell=6.

Thus every sphere with 0<=ell<=6 has a nonnegative gamma-vector. QED.

## 7. Verification and limits

The new proof is a finite written argument, with exact independent audits
of its identities, arithmetic bounds, polynomial recurrences, and explicit
sphere fixtures in verify.py. That audit does not prove topology or replace
the argument above. It does not enumerate all spheres.

The 18-vertex base remains a computer-assisted theorem depending on its
topology-to-CNF reduction and checked traces. The 17-vertex base has its
own published human and partial Lean boundary. Their independent reviews
are evidence about those bases, not independent review of this transfer.
None of the new topology or induction is proof-assistant formalized.

Novelty is relative to the bounded graph and primary-literature searches
documented in SOURCES.md. The near-maximal-dimension lemmas are explicitly
derived consequences of LN, not claimed as unrelated new classifications.
