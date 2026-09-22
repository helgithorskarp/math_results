# A nonempty planar marginal relaxation at size71

Work in V=F_5^3. A line-free set contains no complete five-point affine
line. Write H_0={z=0}, H_1={z=1}, q=(0,0,1), and

    A = {(x,y,0): x,y in {0,1,2,3}}.

The grid A is a line-free set of size16. This is one possible maximum
planar section, not a classification of all maximum sections.

## 1. The exact relaxation and theorem

For each affine plane H, let F_H be the following family of subsets T:

- T is line-free and7<=|T|<=16;
- T intersect H_0=A intersect H and q is omitted whenever q is in H;
- if H=H_1, then |T|<=10 and each affine line of H contains at most three
  points of T.

Let Q be the set of vectors y in[0,1]^V such that sum_v y_v=71 and

    y restricted to H belongs to conv{1_T : T in F_H}

for every one of the155 affine planes. Local distributions share all
one-point marginals. We do not require their joint distributions on
intersections to agree.

**Theorem. Q is nonempty.**

Consequently, even imposing every valid linear inequality of every F_H,
the exact total mass71, and the stated fixed data does not exclude this
branch. This includes section sizes at least seven. It does not refute a
method with additional integrality, shared pair or line distributions,
global section-spectrum identities, or other cross-plane conditions.

There is no assertion that an actual71-point set with this grid section
exists. The theorem is an exact counterexample to infeasibility of a
specified fractional relaxation.

## 2. Why maximum/parallel-small sections are relevant

The standard planar bound is r_5(F_5^2)=16. It follows from the classical
affine blocking-set theorem; the included finite enumeration also verifies
the needed upper bound without that theorem. Any larger planar line-free
set would contain a line-free17-subset, and the program checks every such
subset.

Suppose S is a71-point line-free set. Every plane section has size at most16
and at least7, because the other four parallel sections contain at most64
points. Put d_H=16-|S intersect H|. Each of the31 parallel classes has five
nonnegative deficits summing9. A point lies in31 planes and a pair of
distinct points in six, so

    sum_H |S intersect H| = 31*71 = 2201,
    sum_H |S intersect H|^2 = 6*71^2+25*71 = 32021,
    sum_H d_H^2 = 1269.

If every section had at least11 points, every deficit would be at most5.
For five nonnegative integers summing9 and at most5, the largest sum of
squares is41, from(0,0,0,4,5). All other partitions have square sum at
most35: if the largest entry is5 and the next is at most3, concentrating
the remainder gives at most25+9+1; if the largest entry is at most4,
the bound is4^2+4^2+1=33. The total1269=31*41-2 is therefore impossible.
Some plane has at most10 points.

Its four parallel companions contain at least61 points, so at least one
has16 points. An affine change of coordinates makes these planes H_1 and
H_0. A shear that fixes H_0 pointwise can move a hole of H_1 to q.
The shape of the maximum section remains to be handled; the theorem above
addresses the admissible grid shape A.

Finally, a small section of size at most10 cannot contain four collinear
selected points. If a line has k selected points, its six containing
planes have total selected incidence71+5k. A section of size at most10
and five sections of size at most16 give at most90, contradicting91 when
k=4. These are exactly the distinguished-small-plane restrictions used
in F_{H_1}.

## 3. Compact integer certificate

The point convention is i=25z+5x+y, with0<=x,y,z<5. Let D=1000000.
[CERTIFICATE.json](CERTIFICATE.json) provides integers a_v in[0,D] and,
for each plane H, a list of pairs(T,c_{H,T}) with positive integer
coefficients summing D. Sets are stored as25-bit masks relative to the
listed increasing point indices of that plane.

The verifier checks directly:

1. The records contain all155 distinct affine planes. Its independent
   all-pairs construction gives all775 affine lines,30 in each plane.
2. Every component T is line-free and respects all fixed points. On H_1
   it has size10 and no four collinear points. On the other planes its
   size is14,15, or16.
3. With

       mu_{H,v} = (1/D) sum_{T contains v} c_{H,T},
       x_v = a_v/D,

   every mu_{H,v}>=x_v. On H_0, x=1_A, and x_q=0. The total is

       M = sum_v x_v = 73999401/1000000.

4. Define

       alpha = 55/(M-16) = 55000000/57999401,
       y_v = x_v                 if v in H_0,
       y_v = alpha*x_v           otherwise.

   Then0<alpha<1 and sum_v y_v=16+55=71, exactly.
5. For every plane H and every positive component T, put

       delta_{H,v}=1-y_v/mu_{H,v}    when mu_{H,v}>0.

   The verifier checks0<=delta<=1 and

       sum_{v in T} delta_{H,v} <= |T|-7.                 (1)

   A point with mu=0 belongs to no positive component, so no division by
   zero is needed. For a forced selected point, mu=y=1 and delta=0.

All these checks use integers or exact rational arithmetic. No floating
LP result is a premise. The certificate contains1996 mixture terms and
has SHA256

    47963275a3cef806cdd0cfbea357e5180a7df9865b763313dda9d431bac9ab0a

## 4. Exact local distributions by bounded deletion

For a finite set T and integer k, the polytope

    {d in[0,1]^T : sum d<=k}

is the convex hull of incidence vectors of subsets of T of size at most k.
To see this, a vertex cannot have two fractional coordinates: perturb
them in opposite directions. It cannot have exactly one fractional
coordinate either: if the sum constraint is slack, perturb that
coordinate; if tight, the integral right side and other integral
coordinates force it to be integral. Thus all vertices are incidence
vectors of the stated subsets.

Fix H and first sample a component T with probability c_{H,T}/D.
By(1) and this elementary polytope fact, there is a distribution on
deletion sets B subset T with |B|<=|T|-7 and

    Pr(v in B | T)=delta_{H,v}      for each v in T.

Retain R=T minus B. Then |R|>=7. Deletion preserves line-freeness,
all upper size bounds, and the no-four-collinear condition on H_1.
All forced selected points remain because their deletion probability is
zero; forced absent points were absent from T. Hence R belongs to F_H.
For each v in H,

    Pr(v in R)=mu_{H,v}(1-delta_{H,v})=y_v.

Thus y restricted to H is in conv(F_H), for every H. This proves the
theorem with the same y for all planes. No common joint distribution of
the R across different planes is asserted or needed.

## 5. Evidence and limitations

HiGHS, via SciPy1.17.1, found exploratory local mixtures using a complete
finite planar enumeration and cutting-plane optimization. The coefficients
were rounded down to denominator D; the remaining mass in each plane was
put on an existing valid component. Coordinatewise minima of the resulting
local marginals supplied the a_v. The integer certificate was then checked
from the geometry definitions. Neither optimality, enumeration completeness,
nor any solver soundness assumption is used to verify this existence
certificate. Large catalogues, LP models, logs and the discovery environment
are omitted from publication; the complete compact witness is included.

A proposed shortcut using at most one deletion per component failed its
exact check. The verified argument above permits at most |T|-7 deletions
and preserves the necessary lower cardinality. This is a substantive
distinction: coordinatewise domination alone would only prove membership
in a downward-closed family without the lower bound seven.

The main target r_5(F_5^3) remains unresolved in this work. The certificate
does not improve the70-point construction, exclude71 or72, establish a
major extremal theorem, or certify the exploratory SAT runs. It closes
the precisely defined pointwise planar relaxation as an exclusion route
for the grid branch. Independent review, formal verification and a
historical priority claim are not supplied.
