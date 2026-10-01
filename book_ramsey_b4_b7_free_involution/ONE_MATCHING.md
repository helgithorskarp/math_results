# One entirely matching orbit forces eight blue uniform pairs

Actual author **six-books-2**, role **researcher**, 2026-10-01.
The shared campaign signature does not identify independent authorship.

**Theorem.** For every free color-preserving involution of every ordinary
red-B4/blue-B7-free coloring of K22, if any two-vertex orbit has all ten
cross blocks matching, there are at least **eight blue uniform pairs**.
The inside edge of that orbit has either color. All red uniform densities,
matching signs and other inside colors are covered.

**Density lemma.** In such a coloring, the presence of an entirely
matching orbit gives the necessary tradeoff **3b-2r>=15**, where r,b
count red/blue uniform orbit pairs. This lemma uses only the page caps,
without the prior uniform minima as premises. It also gives a cubic
normalization and a nonnegative integer identity below.

**Corollary.** If there are exactly seven blue uniform pairs, **all eleven
orbits are incident with uniform pairs**. In particular, the preceding
three-red/seven-blue equality profile at total ten requires full uniform
support eleven. No equality witness, absence of denser involution
colorings, or involution in every hypothetical unrestricted witness is
asserted. The located unrestricted Ramsey gap remains 22..23.

The eight-blue theorem uses the prior [three-red theorem](TWO_RED.md) and
[BLUE_SIX.md](BLUE_SIX.md)'s direct eight-blue lemma for two entirely
matching orbits. The new exclusion below handles exactly one. BLUE_SIX.md
also supplies the seven-blue minimum for the ten-total corollary. The
old finite NINE.md and EIGHT.md computations are not premises.
**All the new proofs here are analytic; computation is author validation.**

## 1. A cubic ten-orbit normalization

A valid coloring means at most three red common neighbors on every red
spine and at most six blue common neighbors on every blue spine. Books
are ordinary, noninduced subgraphs. Label the eleven two-vertex orbits
(i,0),(i,1), and use R,D for the red/blue uniform graphs. Every other
cross block is one of two red matchings, by the involution.

Let W have +1 on R, -1 on D and zero on matching pairs. Let S have +/-1
on parallel/crossed red matchings and zero on uniform pairs; both
matrices have diagonal zero. Put u=W1=deg_R-deg_D. For a matching pair ij,
the opposite-color spines have exact page counts

    2Rpages_ij=9+u_i+u_j+(W^2)_ij+S_ij(S^2)_ij,
    2Bpages_ij=9-u_i-u_j+(W^2)_ij-S_ij(S^2)_ij.

For completeness, an outside two-point orbit has doubled red contribution
(1+W_ik)(1+W_jk)+S_ij S_ik S_jk and doubled blue contribution
(1-W_ik)(1-W_jk)-S_ij S_ik S_jk. The inside mates contribute zero at
matching spines. Summing the nine outside orbits gives the identities.
Thus (W^2)_ij<=0 at matching pairs.

Choose an entirely matching orbit h and let I be the other ten. Its W
row and u_h vanish, so every h-i pair has combined page count nine.
Validity forces three red and six blue pages, hence

    (S^2)_hi=-(3+u_i)S_hi.

Switch the labels in each I orbit so that S_hi=+1. This changes no color
or uniform pair. With L=S[I,I], the row action becomes

    1^T (L+diag(3+u_i))=0.

Write r_i=deg_R(i), b_i=deg_D(i). Among i's nine I partners there are
9-r_i-b_i matching pairs. If p_i have positive sign, the action gives

    2p_i-(9-r_i-b_i)=-3-r_i+b_i,   so p_i=3-r_i.

Consequently **A=R union {positive matching pairs} is cubic on I**.
Its complement E=J-I_10-A is six-regular; D is a subset of E. The
same-label red graph in either I layer is A. Cross-label red adjacency
is the symmetric binary matrix

    C=E+R-D+F,     F=diag(epsilon_i),

where epsilon_i is one for a red inside edge and zero for blue. Here
R,D,A also denote their zero-diagonal adjacency matrices. Conversely,
every cubic A, every R subset A and D subset E, and all inside flags
reconstruct a free-involution coloring satisfying all forty h-cross
spines at exact caps. Other spines need not satisfy the caps. This is
an exact reduction of the h-spine necessary system, not host feasibility.

The actual red degrees in I are 10+r_i-b_i+epsilon_i. An inside-red
spine has 2r_i pages, and an inside-blue spine has 2b_i pages. Thus

    epsilon_i=1 implies r_i<=1;
    epsilon_i=0 implies b_i<=3.                      (1)

No global degree theorem is being imported.

## 2. An exact nonnegative triangle identity

Put M=A^2+C^2. For every edge ij of A, the same-label red spine has
one common red neighbor in h and M_ij in the two I layers. Thus

    M_ij<=2,       sum_{ij in E(A)} M_ij<=30.        (2)

All sums over graph edges below are unordered. Define Q by triangle
contributions on I:

* If all three edges of a triangle belong to A, let q be the number
  marked R. Its contribution is 6-2q+q(q-1)/2, taking values 6,4,3,3.
* If exactly two edges belong to A and the third is marked D, let q be
  the number of those two A edges marked R. Its contribution is 2-q.
* If exactly one edge belongs to A and the other two are marked D,
  its contribution is one.
* Add sum_i r_i epsilon_i.

Every summand is a nonnegative integer. The exact identity is

    sum_{ij in E(A)} M_ij=60+4r-6b+Q.                (3)

Here is its derivation, so no triangle census is a premise. For an
A-edge ij put lambda_ij=(A^2)_ij. Since A is cubic on ten vertices,
E^2=2J+I_10+2A+A^2. The baseline A^2+E^2 therefore sums to
60+6t_A, where t_A is the number of A-triangles.
Writing U=R-D, the term EU+UE sums to

    4r-6b-2 sum_{ij in R} lambda_ij
             +2 sum_{ij in D} lambda_ij.

This follows by cyclicity of the trace, or by counting the changed
length-two walks: AE+EA=6J-2A-2A^2. The term U^2 contributes

    sum_A (R^2)_ij+sum_A (D^2)_ij-sum_A (RD+DR)_ij.

On an A-triangle with q red markings, its contributions are
6-2q from the baseline/linear correction and q(q-1)/2 from R^2.
An A-A-D triangle contributes two from the D linear correction and
minus q from RD+DR. An A-D-D triangle contributes one from D^2.
No other triangle contributes. Finally, EF+FE vanishes on A edges;
UF+FU contributes sum_i r_i epsilon_i and F^2 is diagonal. These
are exactly the summands defining Q, proving (3).

Combining (2),(3) gives 6b-4r>=30+Q>=30, hence **3b-2r>=15**.
The derivation covers every cubic skeleton, marking and inside choice.

## 3. The three-red/seven-blue boundary with exactly one matching orbit

Suppose r=3,b=7, and h is the only entirely matching orbit. Then every
I vertex has r_i+b_i>0. Equation (3) has baseline thirty, so Q=0,
and every A-edge in (2) has M_ij=2. Vanishing of Q forces:

1. A is triangle-free, since every A-triangle costs at least three.
2. For every D-edge with a common A neighbor, both incident A edges
   at that neighbor are R-marked.
3. No two D edges have A-adjacent opposite endpoints.
4. Every R-incident vertex has epsilon_i=0, hence b_i<=3 by (1).

For an A-edge ij, expand C^2 entrywise. Triangle-freeness gives
(A^2)_ij=(AR+RA)_ij=(R^2)_ij=0. Condition 3 gives (D^2)_ij=0,
and condition 2 gives (AD+DA)_ij=(RD+DR)_ij. Condition 4 removes
inside-flag contributions on R edges; on other A edges C_ij=0.
On these edges ER+RE has entry r_i+r_j-2R_ij, and ED+DE has
entry b_i+b_j-(AD+DA)_ij. The mixed terms cancel by condition 2.
Thus M_ij=2 is exactly

    b_i+b_j=2+r_i+r_j-2R_ij.

If t_i=b_i-r_i this reads

    t_i+t_j=0 on R edges,  and 2 on other A edges.   (4)

**No isolated R edge.** A cross-label red spine has AC+CA pages, with
no pages from h. If ij is an isolated R edge, its endpoints' inside
flags vanish. At that A-edge triangle-freeness gives

    (AC+CA)_ij=4-(AD+DA)_ij.

Any D contribution to the last term would, by condition 2, require
another R edge at i or j. There is none. This spine has four red pages,
contradicting the cap three.

A three-edge graph with no isolated edge has all edges in one component:
two edge-containing components would each need at least two edges.
A triangle is
excluded by A's triangle-freeness, so R is either K1,3 or P4. This
classification is written and does not use a graph catalogue.

### 3.1 Red star

Let c be its center and let k=b_c. Equation (4) forces each leaf's
blue degree to be 4-k. The four star vertices have total blue degree
12-2k. All six remaining I vertices have no R incidence, so each has
positive blue degree. Their degree sum is 14-(12-2k)=2+2k. By (1),
k<=3; positivity forces k>=2. Thus k=2 or3.

If k=2, all six outside vertices have blue degree one. The center has
two blue neighbors, neither a red-star leaf nor h, so both lie outside.
They are blue leaves sharing a blue center, which is impossible.
Indeed their pair cannot be red: for a red uniform pair, summing its
two red-spine page counts gives the necessary condition
|N_D(i) union N_D(j)|>=3. Their union size is one, so they are matching.
Their W-square entry is at least one, from the shared blue center;
all other terms are nonnegative since neither leaf has another blue
link. This contradicts the matching W-square inequality. The union
condition follows by replacing every nonblue outside block by matching:
the sum is at least9 minus that neighborhood-union size, while at most6.

If k=3, each leaf has blue degree one and t=0. Every nonred A neighbor
of a leaf is one of the six outside vertices and has blue degree two
by (4). Call such a vertex x. It cannot have an A neighbor y outside,
since both have positive blue degree and (4) would require b_x+b_y=2.
It cannot meet c, whose three A edges are the red star. Therefore x's
three neighbors are precisely the three star leaves. Each leaf has two
such outside neighbors, so there are exactly two x vertices. They and
the red star form an isolated K3,3 component of A. The remaining four
vertices would be cubic, hence induce K4, contradicting triangle-freeness.
Both star cases are excluded.

### 3.2 Red path

Label its vertices0,1,2,3 in order. The only possible extra A-edge
within this four-point set is03, since02 and13 make triangles. But (4)
on the red path makes t-values (t,-t,t,-t), so03 would have endpoint
sum zero instead of two. Thus the path is induced in A.

The core blue degrees are (1+t,2-t,2+t,1-t). They are integers at most
three by (1), forcing t in {-1,0,1}. Every outside vertex has positive
blue degree and red degree zero.

If t=0, every nonred A neighbor of the path has blue degree two by (4).
Such a vertex cannot meet another outside vertex, whose blue degree is
positive. All its three neighbors would lie in the four-point path,
but any three path vertices include an adjacent pair, making a triangle
in A. This is impossible.

If t is +/-1, a path vertex with t_i=-1 has a nonred A neighbor x
outside, because the path is induced and A is cubic. Equation (4)
forces b_x=3. Again x has no outside A neighbor. Its core A neighbors
must all have t_i=-1 by (4), but there are only two such core vertices.
Three distinct neighbors are impossible. This excludes the last cases.

Therefore exactly one entirely matching orbit cannot coexist with
three red/seven blue uniform pairs.

## 4. The eight-blue theorem and full-support corollary

The prior three-red theorem gives r>=3. The new tradeoff then gives
b>=7. If b=7 it forces r<=3, hence r=3. Two or more entirely matching
orbits are already excluded at b=7 by BLUE_SIX.md's direct eight-blue
lemma. Exactly one is excluded by Section 3. Therefore **any entirely
matching orbit requires b>=8**. Conversely b=7 leaves none, so uniform
support is eleven. BLUE_SIX.md and TWO_RED.md give r>=3,b>=7 globally,
so at total ten the only counts are3R7B and support eleven. QED.

## 5. Exact author controls and primary scope

Python3.11+ standard library only, from repository root:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 -O book_ramsey_b4_b7_free_involution/one_matching_controls.py
```

[one_matching_controls.py](one_matching_controls.py) imports no campaign
program. Explicit guards survive -O. Output matches
[one_matching_expected.json](one_matching_expected.json). All arithmetic
is exact. The final CPython 3.11.2 replay took 3.947 seconds and
16688 KiB peak child RSS on Linux, sequentially with numerical threads one.
There is no solver, floating point, external graph catalogue,
large omitted corpus or exhaustive matching-sign premise.

Controls cover all16 possible red counts and all31 blue counts on
three explicit cubic templates, giving 1488 scalar identities with
deterministic sampled markings and I inside colors. Both h inside colors
give 2976 lifts and 687456 literal spines:119040 h-cross,
267840 same-layer,297600 I-cross including inside,2976 h-inside.
All65472 normalized adjacency rows match. Matrix identities
are checked against literal22-vertex pages. Triangle contributions are
independently counted over triples, including all four A-triangle red
mark counts. A separate positive control realizes Q=0 and all fifteen
M entries equal two, with r=3,b=7 and full support ten. Its isolated
red cross spines have four pages, so it is not a valid host: the aggregate
equality system alone is insufficient. All455 three-edge subsets on
six points validate the written star/path classification; they are not
a global skeleton census or a theorem premise. The five written core
degree patterns are checked directly.

This is ordinary unformalized analytic mathematics, author audited;
independent peer review of this extension is pending. The inherited
three-red theorem has the credited
[review4](../book_ramsey_free_involution_review4/REVIEW.md) confirmation.
The shared-blue-leaf observation was also used in
[FOUR_BLUE.md](FOUR_BLUE.md) and is rederived here. No earlier finite
census, unrestricted degree theorem or historical classification is used.
The known two-layer/block-circulant representation is not claimed new.

Primary sources reopened live2026-10-01:
[Lidicky--McKinley--Pfender--Van Overberghe, Table1](https://arxiv.org/html/2407.07285v2),
[Radziszowski DS1.18 TableIXa](https://www.cs.rit.edu/~spr/ElJC/sur.pdf),
[Wesley Section3](https://arxiv.org/html/2410.03625v2), and
[Dai--Lin abstract](https://arxiv.org/abs/2606.07214). The located unrestricted
interval stays22..23; diagonal/difference-two constructions do not decide
this difference-three target. The primary21-vertex baseline was exactly
reproduced earlier as validation, not new research. The general upper
flag-algebra certificate was not replayed. Bounded searches do not prove
historical priority of the cubic normalization or triangle identity.
The campaign increment is the scoped arbitrary-density matching-orbit
tradeoff, the one-orbit equality obstruction, and full support at seven
blue pairs. Denser patterns and equality attainment remain open.
