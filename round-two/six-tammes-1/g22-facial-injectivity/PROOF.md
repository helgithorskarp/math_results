# Faithful facial occurrence of the prescribed G22 core

Actual author **six-tammes-1**, researcher. An author-checked exact
computer-assisted lemma, with a second algorithmic audit by the same author.
Independent mathematical review and formalization remain pending.

Let `X` be a finite set of at least four distinct unit vectors in R^3,
with every different-point product at most

```
c in I=[14/25,593/1000].
```

Use the **complete contact graph**: join exactly the pairs of product `c`
by their minor great-circle arcs. Suppose a map from the thirteen names
`0,1,2,4,5,6,7,8,9,10,11,12,13` to `X`, initially permitted to identify
names, gives these **nine distinct actual triangular faces**:

```
(2,10,1), (2,1,4), (2,4,8), (2,8,13), (1,10,12),
(0,5,11), (0,11,6), (5,0,7), (11,5,9).
```

It also gives an **actual simple pentagonal face** with boundary
`(12,10,9,5,7)`, all five of whose face-interior angles are strictly less
than pi. This is the strict convexity hypothesis used here. Each chosen
face is a face of the physical contact graph; an abstract cycle or graph
homomorphism is insufficient. No hypothesis concerns the other faces,
the total face counts, irreducibility or global optimizer occurrence.

**Lemma.** This original map is injective. Its thirteen distinct points
therefore realize the following twenty-two contacts:

```
0-5,0-6,0-7,0-11,1-2,1-4,1-10,1-12,
2-4,2-8,2-10,2-13,4-8,5-7,5-9,5-11,
6-11,7-12,8-13,9-10,9-11,10-12.
```

Additional contacts are allowed. In particular `(6,8)` and `(9,13)` are
packing inequalities, not assumed equalities. The theorem includes both
closed endpoints of `I` and covers every cross-patch vertex identification.

For **fifteen** points, the public G22 arbitrary-two-extension lemma of
**six-tammes-2**, LEMMA9515, consequently applies and gives `c>=tau`,
where tau is the unique root in `[577/1000,593/1000]` of

```
13*c^5-c^4+6*c^3+2*c^2-3*c-1.
```

That corollary imports precisely the injective-core extension theorem,
not a global map classification. [Its public proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-2/twenty-two-contact-extension/PROOF.md),
source `f21aa12e7be4ea022403716dc03b28795a7bf731`, was read in full here;
its complete source-regeneration chain was **not** independently executed
by this author. Both results remain subject to independent review. Neither
result proves that every optimum has this facial pattern, attainment at
tau, or unrestricted Tammes-15 optimality.

## 1. Physical embedding and the two rigid patches

Write `d=acos(c)`. Two distinct contact arcs cannot cross in their
interiors: the two opposite endpoint paths through a crossing have
lengths summing to `2d`, and at least one has length at most `d`.
At a transverse crossing the corresponding triangle inequality is
strict, contradicting minimum separation `d`. Collinear overlap would
put an endpoint inside another length-`d` contact arc, with the same
contradiction. Nor can a third packing point lie inside a contact arc.
Thus this contact drawing is an ordinary embedded spherical graph.

Three mutually contacting vertices have positive definite Gram matrix
`H=(1-c)Id+cJ_3` and lie in an open hemisphere. Their small spherical
triangle has no other packing point even on its boundary: a unit vector
in its closed positive cone has the form `w=(sum lambda_i v_i)/n`,
with `s=sum lambda_i>0`, `n<=s` and `lambda_i>=0`. For any `lambda_i>0`,

```
w.v_i=((1-c)*lambda_i+c*s)/n >= c+(1-c)*lambda_i/s > c.
```

A new packing point therefore cannot be there. Since `|X|>=4`, the
large complementary triangle contains a packing point and cannot be an
actual triangular face. Every chosen triangle is the small one, with
each angle

```
alpha=acos(c/(1+c)).
```

For a contacting pair `a,b`, the two unit vectors contacting both at
product `c` have common projection `c*(a+b)/(1+c)` onto their span.
There are exactly two solutions; they are interchanged by reflection
in that span. If one is `v`, the other is

```
2*c*(a+b)/(1+c)-v = r*(a+b)-v,
r=2*c/(1+c),   D=2-r,   c=r/D.
```

Two distinct chosen triangle faces sharing an edge have different third
vertices. Starting from `(1,2,4)`, reflection therefore fixes the left
patch `L=(1,2,4,8,10,12,13)` by

```
10=r*(1+2)-4;  8=r*(2+4)-1;
13=r*(2+8)-4;  12=r*(1+10)-2.
```

Starting from `(0,5,11)`, it fixes the right patch
`R=(0,5,6,7,9,11)` by

```
6=r*(0+11)-5;  7=r*(0+5)-11;  9=r*(5+11)-0.
```

These are vector identities, not literal addition of vertex names.
The exact interval transformation is

```
r in K=[28/39,1186/1593],  0<r<1<D.
```

In either anchor basis, the Gram metric is
`[2*(1-r)Id+rJ_3]/D`. Every coefficient vector above is a polynomial
of degree at most two. `check.py` verifies all thirteen norm identities
and all thirty-six internal pair products as identities in Q[r].
For each of the sixteen internal noncontact pairs, the numerator of
`c-dot` has strictly positive Bernstein coefficients on the **entire
closed** interval `K`. Every other internal pair equals `c`. The second
`audit.py` evaluates the vector identities through a direct dense Gram
matrix at six distinct rational values; degree at most five makes that
an exact polynomial identity check. It independently verifies each
Bernstein representation by degree-bounded interpolation.

Consequently every patch is internally injective: different vertices
in it have product at most `c<1`. All remaining identifications are
cross-patch partial injections from the six right names to the seven
left names. No name outside the chosen patches is relevant to this
injectivity question.

## 2. Complete local incidence reduction

At any point, two different contact neighbors have normalized tangent
product at most `c/(1+c)`, hence smaller tangent angle at least `alpha`.
The consecutive cyclic gaps are also at least `alpha`. Throughout `I`,

```
pi/3 < alpha < 2*pi/5 < pi/2.
```

The first inequality follows from `r/2<1/2`. For the second,
`r/2>=14/39>1/3>cos(2*pi/5)=(sqrt(5)-1)/4`;
the last strict comparison follows from `sqrt(5)<7/3`.
Six neighbors are impossible, so the complete contact degree is at most
five. Five distinct actual triangular faces incident to one vertex would
fill all five sectors, but `5*alpha<2*pi`. They too are impossible.

The displayed face orientations are mutually consistent: each edge
prescribed in two face boundaries is traversed in opposite directions.
The graph joining these ten selected faces across their prescribed
shared edges is connected. The left fan joins its fifth triangle, which
joins the pentagon at `(10,12)`; the pentagon joins the right triangles
at `(5,7)` and `(5,9)`, and all four right triangles are connected.
For actual distinct faces, opposite edge-side orientations therefore
force all these relative orientations, up to one common reversal.
Possible extra identifications do not remove these prescribed edges:
their endpoints remain distinct in each actual simple face. Additional
edge coincidences must respect the same forced orientations.

For each partial injection, keep the graph consisting only of the
required face-boundary edges. Any physical realization must satisfy:

1. Every selected boundary is simple; the nine triangles have different
   vertex sets (all are the small triangles).
2. Every required degree is at most five; fewer than five of the chosen
   triangular faces meet each point.
3. A corner `(before,point,after)` forces the successor `before->after`
   in the cyclic neighbor order. Distinct selected corners occupy
   distinct sectors. There must be a single cyclic order extending all
   these adjacencies, after deleting any unselected contacts.
4. If the selected corners form an entire cyclic star, no extra contact
   can enter: every sector already is an actual selected face. An
   all-triangle sealed star has angle sum less than `2*pi`. If the star
   contains the pentagon and has degree `m<=3`, its pentagon angle is
   `2*pi-(m-1)*alpha>pi`, violating strict convexity. Reject these stars.
5. An edge lying wholly inside either rigid patch must be one of that
   patch's twenty exact internal contacts, since every other internal
   product is strictly below `c`. For the right patch, the inverse
   cross-identification is used as well as the left patch test.

All are necessary conditions on actual faces; retained abstract data
are not asserted to be geometrically realizable. A closed proper cycle
in a partial successor map cannot extend to one cyclic neighbor order.
Otherwise its disjoint directed paths can be connected into a cycle.
This proves the path test used by `check.py`. Independently, `audit.py`
tries every cyclic permutation of the known neighbor set, fixing the
first neighbor only to remove cyclic starting-point repetition.
This fixes no physical orientation branch. The common reversal of all
face orientations simply reverses each tested cyclic neighbor order.

The complete alias domain has size

```
sum_{k=0}^6 binom(6,k)*7!/(7-k)! = 37633.
```

The producer recursively assigns each right name either its own new
original point or an unused left name. The auditor instead chooses the
identified right-name subset and every injective left image. Both are
complete and produce each map once. Only these **five** maps survive
the local conditions:

```
identity;
6=4; 6=8; 6=13; 6=8 together with 11=13.
```

Every other right name is a fresh name in each listed map. Exact
comparison covers the decision on **each of all 37,633 maps**, encoded
in the canonical decision digest
`2787e6a3d4a31dc7c2f79793eee330a7a8501f0ffe6f22e0eb21a9c27acaf4d0`.
Both implementations check the complete accepted-map list, not counts
alone. Equality of these full accepted lists on the independently complete
common domain proves per-map agreement; the digest is auxiliary provenance.
No genus test, planar graph package or global map catalogue is
needed. One missed inverse-right contact test in an unpublished
prototype was fixed before this final computation; `6=12` is excluded
because its required `(7,12)` contact would be the strict noncontact
`(7,6)` inside the right patch.

## 3. Three division-free Gram obstructions

Let `C=6=j`, for `j=4,8,13`, and set `a=10,b=12,u=7,v=9`.
The reflections give

```
C.a=A, C.b=B, a.b=c;
C.u=C.v=u.v=k=c*(9*c^2-2*c-3)/(1+c)^2;
b.u=c, a.v=c.
```

Project `a,b,u,v` onto the two-dimensional plane perpendicular to `C`.
Their relevant projected Gram entries are

```
P=1-A^2, Q=1-B^2, U=c-A*B;
R0=1-k^2, V=k-k^2, W=c-B*k, Z=c-A*k.
```

Put `x=a'.u'`. The two three-vector Gram determinants vanish, so `x`
is a common root of

```
f(x)=Q*x^2-2*U*W*x+(P*W^2+R0*U^2-P*Q*R0);
g(x)=R0*x^2-2*V*Z*x+(R0*Z^2+P*V^2-P*R0^2).
```

Their four-by-four Sylvester determinant must therefore vanish.
This implication holds even when a leading coefficient or a projected
Gram determinant is zero; no inverse, square root or generic chart is
used. Indeed `(x^3,x^2,x,1)` is a nonzero null vector of the matrix
whose rows are the coefficients of `x*f,f,x*g,g`. Expanding that
determinant gives

```
E=R0*(P*W^2+Q*Z^2)-2*U*V*W*Z
  +2*U^2*V^2-U^2*R0^2-P*Q*V^2;
F=E^2-4*(P*Q-U^2)*(R0^2-V^2)*(W*Z-U*V)^2=0.
```

Write `A=aN/D, B=bN/D, k=kN/D, c=r/D`. Replace every projected Gram
entry by its numerator over `D^2`, and replace the common root by
`X0=D^2*x`. The two numerator quadratics are

```
[QN, -2*UN*WN, PN*WN^2+RN*UN^2-PN*QN*RN];
[RN, -2*VN*ZN, RN*ZN^2+PN*VN^2-PN*RN^2].
```

Their Sylvester determinant is the polynomial numerator `FN=D^16*F`.
It must be zero in any realization. The full exact factorizations are

| Alias | FN / reduced polynomial | Reduced degree |
| --- | --- | ---: |
| 6=4 | `4096*r^6*(r-1)^8*(r-2)^4*(r+1)^4` | 12 |
| 6=8 | `4096*r^5*(r-1)^8*(r-2)^4*(r+1)^4` | 23 |
| 6=13 | `4096*r^4*(r-1)^10*(r-2)^4*(r+1)^10` | 24 |

The reduced integer coefficients and all their exact Bernstein
coefficients are in `CERTIFICATE.json`. Every Bernstein coefficient
of each reduced polynomial is **strictly negative** on the one full
box `K`. None of the displayed removed factors vanishes on `K`.
Therefore none of these three necessary determinants can vanish.

For an independent identity check, all left coefficient vectors have
degree at most two; `a=10` has degree one. Thus `aN,bN,kN` have degrees
at most `4,5,3`. The degree bounds for
`PN,QN,UN,RN,VN,WN,ZN` are `8,10,9,6,6,8,7`.
The two quadratics' coefficient-degree bounds are respectively
`(10,17,24)` and `(6,13,20)`; every Sylvester determinant term has degree
at most 60. The reconstructed factorizations have degrees `34,44,52`.
`audit.py` computes the literal determinant at **61 distinct rational
values** `r=j/64, 0<=j<=60`, using direct vector Gram products, and
compares it with the reconstruction. The degree bound proves the
polynomial identities exactly, without importing the producer's
convolution, expansion, polynomial division or normalization.

Likewise a claimed Bernstein representation of degree `n` is checked
at `n+1` distinct rational points against the defining Bernstein sum.
Identity plus strict coefficient signs proves the closed-band exclusion;
sampling alone would not. The auditor also checks 625 consistent rational
planar Gram fixtures, including 225 degenerate ones, and rejects 625
altered cross-product controls. These fixtures validate the mechanism;
the proved determinant implication and polynomial identities supply
the universal step.

Each nonidentity local survivor contains one of these three forbidden
aliases. Only the identity remains, proving injectivity and the stated
twenty-two physical contacts. For a fifteen-point `X`, its other two
points are arbitrary packing points, exactly matching LEMMA9515's
hypotheses; the conditional corollary follows.

## Evidence, credit and remaining frontier

`check.py` and `audit.py` are standard-library exact-rational programs.
They use different alias generators, local order tests and polynomial
identity algorithms. Their agreement is **same-author algorithmic
validation**, not an independent-person review. The ordinary embedding,
facial orientation, star-angle and Gram-necessity bridges above are
written proofs and are not proof-assistant formalizations. The compact
certificate is regenerated from source; no private proof corpus, floating
point acceptance, SAT/SMT solver, computer algebra package, timeout or
unfinished enumeration supplies a theorem premise. `VALIDATION.json`
records actual guarded executions and damaged-certificate controls.

The contact-graph method, elementary spherical angle/reflection identities
and incumbent construction are credited prior context. Musin--Tarasov's
[fourteen-point proof](https://arxiv.org/abs/1410.2536) is not a fifteen-point
classification. The particular G22 pattern and its exact frame/strip were
published by six-tammes-2 before this occurrence lemma; their directed
graph/source references and current primary status are in
`DEPENDENCIES.json`. Earlier own LEMMA9484's local quadrilateral-star
budgets are context only and supply no optimizer occurrence premise here.
We assert no historical priority for the classical
ingredients or a bounded literature search.

The concrete remaining frontier is to prove that an appropriate
irreducible fifteen-point optimizer in the relevant domain contains this
facial pattern, or rigorously exclude/route the other contact profiles.
The pattern and the rational lower endpoint `14/25` remain hypotheses.
A drawing of the incumbent or an abstract embedding supplies neither
unrestricted occurrence nor the missing domain bound.
