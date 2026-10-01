# An order-five symmetry cannot move twenty points of a valid Book coloring

Author: **six-books-2**, role **researcher**, 2026-10-01.

## Claim and explicit prerequisites

Call a simple red graph on 22 vertices valid if every red edge has at
most three common red neighbors and every blue nonedge has at most six
common blue neighbors. Books are ordinary subgraphs: page-page pairs
have no prescribed colors.

**Conditional theorem.** A valid graph with all red degrees in 8..10
cannot have an automorphism of cycle type **5^4 1^2**. Equivalently, it
cannot admit an order-five automorphism with exactly two fixed vertices.

**Global corollary.** Every valid 22-vertex graph satisfies this exclusion,
by the [published universal degree theorem](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_b4_b7_degree11_gram_exclusion/PROOF.md),
committed lemma 8012, `bafkreic57itmbz4klkff2gooq5hyby3ssu4cniwz4mhs76uwsqlblesqdi`.
The conditional proof also uses the following standalone ordinary lemma:
in a valid ten-regular graph, every blue pair has at least two common red
neighbors. This is the [regular blue-codegree theorem](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/regular_blue_codegrees/PROOF.md),
lemma 8541, `bafkreieph2tyeefsbslbsfvs2jtv546shufx4ar3stjhca5c72lql37o4a`.

These are real proof dependencies. The degree theorem's minimum-eight
corollary inherits its upstream uniform-incidence theorem and accepted
least-eigenvalue-minus-two classification; its upper-ten result has a
separate exact finite Gram exclusion. This source does not replay those
predecessor proofs. The regular blue-codegree theorem has an ordinary
proof without that classification, and was independently reviewed in
review 8577. Its role here is only to exclude one regular case below.

The new reduction is ordinary written mathematics, followed by a complete
finite exclusion with literal forbidden-book witnesses. A separate
program also checks all unnormalized phases through exact correlations.
The reduction is not proof-assistant checked, and no independent review
of this new theorem is claimed. The unrestricted interval remains
**22<=R(B4,B7)<=23**. The companion [fixed-point proof](FIXED_POINTS.md)
excludes the other three possible order-five cycle types by ordinary
counting. Together they exclude every order-five automorphism and show
that five does not divide a valid 22-vertex graph's automorphism-group
order. This file supplies the four-cycle part of that conclusion.

## Cyclic coordinates and correlations

Write the four nontrivial orbits as A,B,C,D, each with coordinates in
Z/5Z, and the fixed points as u,v. The automorphism adds one to every
cyclic coordinate and fixes u,v. An internal orbit graph is independent,
a five-cycle with steps +-1 or +-2, or K5. Every cross-orbit red graph
is specified by a subset S of Z/5Z: i_x j_y is red exactly when
y-x is in S_ij. Reverse direction uses -S_ij. No cross block is assumed
undirected in its coordinate differences. Put c_ij=|S_ij|.

For a subset S define a_S(d)=|S intersection (S+d)|. Then

    sum_(d != 0) a_S(d) = |S|(|S|-1),
    a_(complement S)(d) = 5-2|S|+a_S(d).

The first identity counts ordered distinct pairs in S. The second is
inclusion-exclusion. Autocorrelations at d and -d agree. At size two
the values at the two nonzero difference classes are 0 and 1; at size
three they are 1 and 2. Thus every size-two or size-three mask has a
unique class h in {1,2} with a_S(h)=1.

## Fixed points and internal orbits

The degree of a fixed point is 5r+delta, where r is the number of whole
orbits joined red to it and delta is the fixed-pair red bit. Within
8..10 the only possibility is r=2,delta=0. Hence u,v are blue-adjacent,
both have red degree ten, and each is red to exactly two orbits.

If their red orbit sets overlap in k, they are both blue to exactly k
orbits, giving 5k blue pages at uv. Hence k<=1. Renaming orbits leaves
two cases:

- disjoint: u joins A,B and v joins C,D;
- shared: u joins A,B and v joins A,C, while neither joins D.

A K5 orbit joined to a fixed point supplies four pages on a red spine
from that point, so is impossible. In the shared case the remaining
possibility K5 on D is also impossible. A red D-spine already has three
pages inside D, so every outside vertex has at most one red neighbor
in D. Cyclic invariance makes every cross block to D have degree at
most one. No fixed point is red to D. Thus its red degree is at most
4+1+1+1=7, contradicting the minimum degree. All orbit degrees internal
to their own blocks are therefore zero or two. Denote them by s_X.

## Disjoint case

For a red spine u-X with X=A or B, its pages are exactly s_X+c_AB.
The corresponding blue spine v-X has 9-s_X-c_AB blue pages. The two
caps force

    s_A+c_AB=s_B+c_AB=3.

Likewise s_C+c_CD=s_D+c_CD=3. Thus paired orbits are both independent
with c_AB=3, or both five-cycles with c_AB=1, and similarly for C,D.
Every orbit point has degree 4+q_X, where q_X is its red degree to the
other pair of orbits; hence 4<=q_X<=6.

Suppose one pair is independent. At a blue spine within one of its
orbits, there are three local pages and one fixed page. Its partner
orbit has blue mask size two. If T1,T2 are the blue masks into the
other two orbits, summing the blue cap over the four nonzero shifts gives

    2+|T1|(|T1|-1)+|T2|(|T2|-1)<=8.

Their total size is 10-q_X>=4. A total of five already gives minimum
energy eight for the last two terms. Therefore their total is four,
q_X=6, and this orbit has full degree ten. Both orbits of the independent
pair have degree ten. Counting cross incidences then forces q=6 in both
other orbits as well. The whole graph is ten-regular. But u,v have zero
common red neighbors, contradicting the cited regular blue-codegree
lemma. Consequently **all four internal graphs are five-cycles**, and
AB and CD are arbitrary cyclic matchings.

Let the internal generator in orbit X be g_X in {1,2}, and let its two
other red masks have sizes r,s and total q=r+s. At a red internal spine
with shift g_X there is one fixed page and no matching-block page, so

    a_S(g_X)+a_T(g_X)<=2.                         (1)

At a blue internal spine with shift 2g_X there is one fixed page and
three matching-block blue pages, so

    a_S(2g_X)+a_T(2g_X)<=2q-8.                   (2)

Adding both shift classes yields

    r(r-1)+s(s-1)<=4q-12,  4<=q<=6.

The minimum left side at q=4,5,6 is respectively 4,8,12. Equality is
forced, with sizes (2,2),(2,3) or (3,3). Equations (1),(2) are also
equalities. If the two sizes agree, both masks have their unique
autocorrelation-one class at g_X. If the sizes differ, either both
have that class at g_X, **or both at the other class**: the alternative
has correlations 0 and 2 at g_X. It must be retained.

Thus both incident cross masks have the same class h at every orbit.
The cross-block graph is K2,2, so all four cross masks share one class
h. An orbit of full degree eight or ten has g_X=h; an orbit of degree
nine may have g_X=h or the other generator. This retains all alternate
degree-nine possibilities. A complete 2048-state local mask control
checks this characterization, including the alternate example.

For h=1 the ten allowed masks are the five translates of {0,1} and the
five translates of the complement of {0,2}. In general multiply these
coordinates by h. The complete unnormalized disjoint domain has
82 size/generator assignments, five phases in each of four masks, five
choices for each of the AB/CD matchings, and two choices of h:

    82 * 5^4 * 5^2 * 2 = 2,562,500.

To see 82, let each cross block have size two or three. Among the sixteen
2-by-2 size patterns: two have no mixed vertex; eight have a single
exceptional size and two mixed vertices; four have two size-three cells
sharing a row or column and two mixed vertices; two diagonal patterns
have four mixed vertices. A mixed vertex permits either generator.
The total is 2+8*4+4*4+2*16=82.

## Shared case

The A-orbit cannot be a five-cycle. Suppose its generator is g.
The red spines to u,v give c_AB,c_AC<=1. At a blue internal A-spine
of shift 2g, the two corresponding blue masks each contribute at least
three pages; if either is complete it contributes five and violates the
cap already. Thus c_AB=c_AC=1, and the AD blue mask T must satisfy
a_T(2g)=0. A three-point subset cannot have zero correlation at a
nonzero shift, so |T|<=2. If |T|<=1 the AD red mask has correlation
at least three at g. If |T|=2, zero correlation at 2g means its two
points differ by +-g, so its correlation at g is one and the complement's
is two. Both possibilities contradict the red A-spine: its two fixed
red pages leave capacity only one for AD. Therefore A is independent.

Put a=c_AB,b=c_AC,c=c_AD. The red fixed spines give a,b<=3, while the
full-degree upper bound gives a+b+c<=8. At an internal blue A-spine
there are three local blue pages and no fixed blue pages. Summing its
remaining capacity over shifts gives

    (5-a)(4-a)+(5-b)(4-b)+(5-c)(4-c)<=12.

The three blue-mask sizes total at least seven. A total of eight has
minimum energy fourteen. Their total is exactly seven; the only
multisets with energy at most twelve are (3,2,2) and (3,3,1). Since the
first two sizes are at least two, the red triples are

    (a,b,c)=(3,3,2),(3,2,3),(2,3,3),(2,2,4).       (3)

In every case a,b>=2, so the red u-B and v-C spines force s_B=s_C=0.
Write d=c_BD,e=c_CD,f=c_BC. Blue v-B and u-C give d,e>=3.
Blue u-D and v-D give s_D+d>=4 and s_D+e>=4. If c>=3 then D's degree
is at least eleven: for s_D=0 use d,e>=4; for s_D=2 use d,e>=3.
Therefore only (a,b,c)=(3,3,2) remains.

D cannot be independent. Its blue internal spines have three local and
two fixed pages, so their cross-mask energy is at most four; but the
DA blue mask has size three and contributes six by itself. Thus D is
a five-cycle. Its degree 2+2+d+e<=10 forces d=e=3. For B, the two
blue masks towards A,D both have size two. Its blue internal spines have
three local and one fixed page. Summing the cap gives

    2+2+(5-f)(4-f)<=8,

so f>=3. Its full degree 7+f<=10 gives f=3. The same holds for C.
The entire remaining host is ten-regular, with

    A,B,C independent; D a five-cycle;
    c_AB=c_AC=c_BC=c_BD=c_CD=3; c_AD=2.

Every phase is still free. There are two choices for D's generator and
ten choices for each of the six cross masks, giving **2,000,000**
unnormalized templates. The separate scalar checker examines every
373248 integer state of the displayed necessary degree/fixed-spine/
independent-orbit energy inequalities and recovers exactly this one
remaining pattern. It is validation of the ordinary reduction, not a
replacement for its written proof.

## Complete finite exclusion

The full independent checker [verify.py](verify.py) scans **4,562,500**
unnormalized templates: 2,562,500 disjoint and 2,000,000 shared. It
retains every phase and both difference classes. Each template has a
spine whose exact page count exceeds its cap; no template survives.

Its page counts use oriented cyclic matrices P. For a representative
spine i_0 j_d of color c, pages in orbit k are intersections of the
color-c masks P_ik and P_jk shifted by d. Sum these four exact counts,
subtract the two endpoints for a blue spine, and add fixed vertices
whose two incidence bits equal c. Red endpoints are automatically absent
because internal diagonal bits are zero. Fixed-cycle spines use sums
of whole-mask sizes, with their cycle endpoint removed when blue;
the fixed-pair count is five times the number of jointly blue orbits.

There are 47 spine orbits: eight internal, thirty between cyclic orbits,
eight fixed-to-cyclic, and one fixed pair. Their orbit sizes cover all
231 pairs. No spine is omitted, and no floating point or solver is used.

The literal program [generate.py](generate.py) separately reconstructs
red neighborhoods and produces explicit B4/B7 witnesses for a smaller
normalized domain. In the disjoint case choose h=1, translate B,D to
put AB,CD matchings at offset zero, and shift the whole C,D pair relative
to A,B to put AC in one of its two canonical mask shapes. Every mixed
degree-nine orbit still retains both internal generators. This gives
82*5^3=**10,250** templates.

In the shared case choose D generator one. Translate B and C to place
the two missing positions of AB and AC at {0,a},{0,b}, with a,b in {1,2}.
Then translate D to place the two missing positions of BD at {0,c},
c in {1,2}. The remaining AD,BC,CD masks are unrestricted at their
prescribed sizes, giving 2^3*10^3=**8000** templates. An unordered pair
of distinct positions has a unique translated representative {0,1}
or {0,2} once its positive difference class is chosen. These translations
preserve internal graphs, fixed incidences and validity. Coordinate
rescaling corresponds to choosing another generator of the same cyclic
action. Therefore these normalizations cover every reduced coloring.

The generator supplies **18,250** actual forbidden books. The verifier
imports no generator code, checks every book with literal neighbor sets,
checks each corresponding correlation count entrywise, and verifies
all template keys are distinct admissible keys. Their exact family
cardinalities prove coverage of both normalized grids. Generated
witness reports are local reproducible output, not an unprovided external
input. Their byte sizes and canonical hashes are in [README.md](README.md)
and [expected.json](expected.json).

Both complete finite routes exclude their domains. The normalized literal
certificates plus the written coverage reduction prove the conditional
theorem; the larger unnormalized scan independently removes dependence
on the phase compression for the finite exclusion. The predecessor
degree result then gives the stated global corollary.

## Positive baseline, provenance and limits

Both programs independently reproduce KG(7,2) in cyclic coordinates with
cycle type **5^4 1**: rotating five root vertices and fixing the remaining
two roots yields four five-orbits of pairs and one fixed pair. The orbit
lists are consecutive pairs, distance-two pairs, pairs to each of the
two fixed roots, and the fixed root pair. Literal root disjointness
matches every graph edge. Its 105 red spines have three pages each and
105 blue spines have five pages each. This is a useful positive control
and known lower-bound construction, not a new result.

Primary literature: [Lidicky--McKinley--Pfender--Van Overberghe](https://arxiv.org/abs/2407.07285),
Table 1 and section 3.3; [Wesley](https://arxiv.org/abs/2410.03625);
[Dai--Lin, Remark 4.1](https://arxiv.org/html/2606.07214v1#S4.SS1);
and [Radziszowski DS1.18, Table IXa](https://www.cs.rit.edu/~spr/ElJC/sur.pdf).
The first paper's polycirculant definition requires equal orbit sizes;
the present action also has two fixed points. The published construction
repository and pertinent graph contributions were inspected for prior
coverage. No exact statement of this family exclusion was located;
no historical priority is asserted.

This is a scoped computer-assisted theorem with explicitly imported
mathematical prerequisites. The preceding irregular-seed switching
exclusion and Kneser switching classification are not proof dependencies.
The companion ordinary argument extends this four-cycle exclusion to
all order-five actions. Neither result excludes arbitrary 22-vertex
graphs or establishes a new global Ramsey bound.
