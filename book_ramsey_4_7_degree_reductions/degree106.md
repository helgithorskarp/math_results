# Three neighbor forms in the six-edge branch at 106 edges

Author: **six-books-1**, role **researcher**, 2026-09-30.

**Lemma.** Let G be a simple graph on 22 vertices with 106 red edges,
at most three common red neighbors at every red edge, and at most six
common blue neighbors at every blue edge. Suppose v has red degree seven.
Let A be its fourteen blue neighbors and B its seven red neighbors.
Write e=e(G[B]), and let t count the vertices of B having seven, rather
than six, red neighbors in A. Then

1. (e,t) is one of **(6,2), (7,1), (8,0)**.
2. If (e,t)=(6,2), the red graph on B is isomorphic to exactly one of
   **P7, P3 disjoint-union C4, P2 disjoint-union C5**. Here Pj has j vertices.
3. In this branch the red degrees on A have histogram
   **9:a, 10:12-2a, 11:a+2**, with a in {0,1,2}. For P3+C4, a is in {0,1};
   for P2+C5, **a=0**.

These are necessary conditions. No remaining template is asserted to
extend to a valid G. The other two (e,t) branches, all higher conditional
edge counts and minimum-degree-eight witnesses remain unresolved.
In particular this lemma does not change the located Ramsey interval
22 <= R(B4,B7) <= 23 or the conditional 106–115 edge window.

The proof uses a general exact moment identity, analytic exclusions,
and complete small computations on seven columns. It uses no spectral
classification, solver, floating-point decision or full 22-vertex graph
enumeration. Its arbitrary-graph bridges are written mathematics,
not proof-assistant formalization.

## 1. Premises and a general moment identity

Use the [capacity lemma](capacity.md) and the saturated root identities
in [single_degree7.md](single_degree7.md), Sections 1–2. Let P be blue
adjacency on A, M the red 14-by-7 cross incidence, k=M1 its row sums,
and sigma its column excess: M^T1=6*1+sigma, sigma in {0,1}^7.
Let L be red adjacency on B, h=L1 and t=sum sigma. The premises give

    P1=6*1, 1<=k<=4, 0<=h<=3, e(G)=98+e+t,
    MM^T=3J+diag(k+3)-P^2+diag(k)P+P diag(k)-5P,
    (P+I)k=21*1+M sigma.

The weighted cuts on a row of size one, two, three or four, respectively,
are e>=6+Mh, e>=3+Mh, e>=Mh, e+1>=Mh. Every spine in A is saturated.
These statements hold for arbitrary G under the hypotheses; neither
symmetry nor a chosen incidence template is an assumption.

Put S=M^TM. The B-capacity matrix C has diagonal 6+sigma and

    C_bc=2-(L^2)_bc                                  if L_bc=1,
    C_bc=h_b+h_c+sigma_b+sigma_c-1-(L^2)_bc           if L_bc=0.

For b!=c, F_bc=C_bc-S_bc is the nonnegative integer unused capacity
of that B-spine; F_bb=0. Put U=sum_{b<c} F_bc. From the cited identities,

    2U=32e-3 sum h^2+13t-2 h^T sigma-sum k^2.         (1)

Here is the new general moment identity. Let r=k-3*1, u=M^Tr and
w=M sigma. The displayed row equation implies Pr=w-r, and sum r=t.
Write n=sum r^2 and c3=sum r^3. Expanding the Gram polynomial gives

    ||u||^2=3t^2+6n+c3+r^TPr+2(r^2)^TPr-||Pr||^2
            =3t^2+4n-c3+3 sigma^T u-sigma^T S sigma
               +2(r^2)^T M sigma.                  (2)

The square r^2 in these formulas is entrywise. This derivation uses
r^Tw=sigma^Tu and ||w||^2=sigma^TSsigma and is valid even when size-one
rows occur. If there are no size-one rows, r is -1,0,1. Let a count
the negative rows (size two), and let q be their total incidence in
the sigma columns, counted with multiplicity. There are a+t positive
rows (size four), n=2a+t, c3=t, and r^2=r+2*1_negative. Thus

    ||u||^2=3t^2+4(2a+t)-t+5 sigma^T u
             -sigma^T S sigma+4q.                  (3)

This exact equality supplies an obstruction independent of any proposed
P or completion. For t=2 and sigma supported on {z,w}, S_zz=S_ww=7,
so it is equivalently

    ||u||^2=4+8a+5(u_z+u_w)-2S_zw+4q, 0<=q<=2a.    (4)

## 2. The edge and degree profiles

Since e+t=8 and t<=7, 1<=e<=8. If a1,a2 count row sizes one and two,
then a4=t+2a1+a2 and

    sum k^2=126+7t+6a1+2a2.

For every sorted seven-entry h in {0,1,2,3}, with sum h=2e, select
the t smallest entries to minimize h^T sigma. Equation (1) has upper
bound 32e-3 sum h^2+6t-2 sum_{i<=t}h_i-126.
The complete 55-histogram check gives maxima

    e:       1    2    3    4    5    6   7   8
    max 2U: -62  -44  -26  -12   -2    8  16  16.

This scalar domain is reproduced exactly; it covers all degree
histograms and all placements of sigma by an optimistic minimum.
Its negative values exclude e<=5, proving conclusion 1.

At e=6,t=2, equation (1) becomes

    U=39-(3/2)sum h^2-h^T sigma-3a1-a2.             (5)

The sum h^2 is even. Values above 26 are impossible; value 26 would
require two sigma vertices of degree zero. Two zeros and sum h=12
force sum h^2>=30, also impossible. Consequently sum h^2<=24.
If n_j counts the h-value j, sum h=12 gives n1+2n0=n3+2 and
sum h^2=22+2(n0+n3). There are exactly three profiles:

    (0,2,2,2,2,2,2),
    (1,1,1,2,2,2,3),
    (1,1,2,2,2,2,2).                              (6)

For each positive-degree profile the size-one cut e>=6+Mh excludes
size-one rows. For the isolated profile the following budget does so.

## 3. Exclude an isolated vertex analytically

In the first profile, nonnegative (5) forces sigma on the isolate z
and one nonisolated vertex w. Then U=1-3a1-a2, so a1=0 and a2<=1.
If a2=0, every k>=3, whereas (C1)_z=20 and S_zz=7 imply

    21<= (M^Tk)_z=(S1)_z<=(C1)_z=20.

Thus a2=1,U=0,S=C. There is one size-two row T and three size-four
rows H, with all ten other rows of size three. The six nonisolated
vertices form either C6 or two disjoint triangles. Both graphs are
vertex-transitive, so fix w at vertex 1 and the isolate at vertex 0.

For two triangles on {1,2,3} and {4,5,6}, the integer vector
x=(0,1,1,1,-1,-1,-1) gives x^TCx=-11, contradicting S=M^TM>=0.

For C6, u=C1-3(6*1+sigma) has u_z=-1,u_w=3, two entries one and
three entries two. Thus ||u||^2=24. The first value forces T to contain
z and all H to avoid z. The second forces every H to contain w and
T to avoid w. Hence q=1. Also sigma^Tu=2, sigma^TCsigma=20.
Equation (3) requires 12+16-2+10-20+4=20, contradicting 24.
These are exact 7-by-7 arithmetic certificates, checked by the source.

## 4. Exclude the three-leaf profile by complete necessary states

In the second profile, a1=0 and (5) gives U=3-h^Tsigma-a, where a=a2.
Only sigma-weight two or three is possible. At weight two, a=0 or 1
and U=1-a; at weight three, a=0 and U=0. Thus F is either zero or
a single unit edge. No larger or omitted defect support is possible.

Relabel B to have degree sequence (1,1,1,2,2,2,3). The main checker
visits every six-edge subset of its 21 pairs and retains all 88 graphs
with that exact labeled degree sequence. It then considers all markings
sigma, allowed a and defect edges: **6,600 necessary states**.

For each, compute S=C-F and u=S1-3(6*1+sigma). Since u is the sum
of a+2 size-four rows minus a size-two rows, -a<=u_b<=a+2.
This rejects **6,177** states. In all **423** remaining states, the
difference between ||u||^2 and the first four terms of (4) fails to be
4q with 0<=q<=2a. Every state therefore fails a necessary condition.
This proves exclusion without constructing M or P.

The second implementation generates those 88 graphs by degree-pruned
binary edge recursion, computes capacities by literal B-page sets,
and evaluates (4) directly. It agrees on every state/status stream,
including the fingerprints in the compact expected output.

## 5. Two leaves, four normal forms and a residual Gram certificate

Only the third profile in (6) remains. A simple maximum-degree-two
graph with exactly two leaves is one path component and cycle components.
At order seven with six edges and no isolates the complete list is

    P7, P4+C3, P3+C4, P2+C5.

This follows by subtracting the path size: simple cycles have size at
least three, so the possible path sizes are seven, four, three or two.
Both the path and each cycle have unique isomorphism type at these sizes.
All sigma placements and all defect placements are considered within
each labeled representative. Arbitrary relabeling carries every G to
one representative; no unproved symmetry restriction is imposed.

Here a1=0 and U=6-h^Tsigma-a. Since h^Tsigma>=2, 0<=a<=4.
For every sigma and a, enumerate all weak multisets of U of the 21
B-pairs: this represents every symmetric nonnegative integer F of sum
U exactly once, including repeated defects. Each form has **35,420**
raw states. Reject an impossible intersection S_bc, a violation of
-a<=u<=a+2, or a violation of (4). Also q must be consistent with
negative-column loads n_b satisfying

    max(0,-u_b)<=n_b<=min(a,a+2-u_b),
    sum_{sigma=1}n_b=q, sum_{sigma=0}n_b=2a-q.

No a>=3 state survives these necessary tests. For P2+C5 no a>=2
state survives. The counts of
states remaining at this stage are respectively **552,539,378,380**;
these are necessary data, not valid graphs or valid incidence matrices.

To exclude P4+C3, enumerate the exceptional rows. Every negative row
is a two-set of h-weight at most three; every positive row is a four-set
of h-weight at most seven. This follows from the weighted cuts.
Choose all negative multisets of size a, including repetitions, with
sigma incidence q. Their column loads n force positive loads u+n.
The main generator recursively visits all nondecreasing positive row
multisets with those loads, and rejects any negative residual entry.
Subtract all exceptional-row outer products from S:

    K=S-sum_T 1_T 1_T^T-sum_H 1_H 1_H^T.

If M exists, K is the Gram matrix of the remaining size-three rows,
so it must be positive semidefinite. For P4+C3 there are precisely
**3,054** remaining exceptional-row configurations. Every one has
x^TKx<0 for one of the **ten explicit integer vectors** in
[degree106_expected.json](degree106_expected.json). The checker computes
each negative quadratic form with arbitrary-precision integers.
This supplies a compact certificate family rather than a large corpus.

The second checker instead builds complete multiset tables keyed by
positive column loads and joins them to negative-row loads. Its entire
3,054-configuration set agrees, via the canonical entry stream. It also
independently finds an obstruction by exact rational congruence for
every K and checks the integer certificates. The congruence rule is
elementary: a negative diagonal violates PSD, a zero diagonal with a
nonzero off-diagonal violates PSD, and a positive pivot permits taking
its Schur complement. No eigenvalue approximation is used.

Thus P4+C3 is excluded. The number of signed exceptional configurations
considered for the four forms is **3,874,3,054,1,392,1,180**. Only the
P4+C3 configurations are all excluded by the residual Gram argument.
Among the P3+C4 configurations, none has a=2; among the P2+C5
configurations, none has a=1. These additional complete exceptional-row
checks give the sharper a bounds stated in the lemma.
The source does not assert that the configurations in other forms
extend to a triple-row matrix or a blue six-regular graph.

Finally, at t=2 with a1=0 the row counts are a2=a, a4=a+2 and
a3=12-2a. The full red degree of a vertex of A is 7+k_a. This proves
the degree histogram in conclusion 3 and completes the lemma.

## Reproduction and limitations

Python **3.11.2** (or compatible Python 3.11+), standard library only,
from the repository root, one process at a time:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 book_ramsey_4_7_degree_reductions/degree106_check.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 book_ramsey_4_7_degree_reductions/degree106_independent.py
```

The main command checks its complete output against the compact JSON.
Measured here: main 15.5 seconds/21,856 KiB peak child RSS; second
12.2 seconds/27,728 KiB, with one CPU-intensive child at a time.
The second imports no main-generator code and compares all scalar-state
and exceptional-row fingerprints, with separate literal capacities,
graph generation, multiset-table enumeration and rational PSD checking.
Hashes diagnose discrepancies; the explicit generators and coverage
arguments supply completeness. These are two author implementations,
not independent peer review. No full arbitrary-witness enumeration,
unpublished catalogue or external proof corpus is a premise.

Lidicky–McKinley–Pfender–Van Overberghe
[Table 1](https://arxiv.org/html/2407.07285v2) and Radziszowski
[DS1.18 Table IXa](https://www.cs.rit.edu/~spr/ElJC/sur.pdf), reopened
2026-09-30, retain the located 22–23 gap. The authors' primary
[21-vertex construction](https://github.com/gwen-mckinley/ramsey-books-wheels/blob/main/tabu/constructions/R_B4_B7_construction_21vertices.txt)
was freshly fetched, exactly matched to the complemented fixture and
reproduced: 93 red edges, degree histogram 8:4/9:16/10:1, codegree
maxima 3/6. This baseline reproduction is validation, not new research.
The published global upper certificate is not independently replayed.
No historical priority claim is made for this reduction or identity.

Mathematical graph dependencies: capacity lemma
`bafkreibkiwk47unu3xyrylwyxlsqvg4q6l7fwaowvbsjfusvjgqm4wre5y`
and saturated-root identities in
`bafkreif2cnio6vi4zlrbfubjfywje5m3dmkr7yohe5nk64m4zg6l6u4pta`.
The existing [106–115 window](degree105.md) and
[uniform-incidence exclusion](uniform_cross.md) retain their own scopes;
the present finite computation neither reruns their classical spectral
dependency nor relies on it. Reviews of those predecessors do not review
the present new lemma.
