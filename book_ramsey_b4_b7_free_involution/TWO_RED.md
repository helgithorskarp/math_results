# Two red uniform orbit pairs are impossible at every blue density

Author: **six-books-2**, role **researcher**, 2026-09-30.

**Lemma.** Every ordinary red-B4/blue-B7-free coloring on 22 vertices
with a fixed-point-free color-preserving involution has at least three
fully red orbit pairs and at least seven uniform orbit pairs. Inside
colors are arbitrary, and the statement holds for every such involution.
This is a written analytic proof with author computational validation;
it is not formalized or independently peer reviewed.

Let a valid ordinary red-B4/blue-B7-free coloring on22 have a free
color-preserving involution. Use the eleven-orbit representation and
page identities of [the earlier free-involution lemma](PROOF.md).
The new claim is that exactly two red uniform pairs are impossible,
with no restriction on the number of blue uniform pairs, inside colors
or matching signs. Together with the earlier zero/one-red exclusions
this proves **at least three red uniform orbit pairs** for every such
involution. The earlier at-least-seven-total-pair bound is retained.
There is no unrestricted Ramsey decision or all-involution exclusion.

## 0. Definitions and the page identities used here

Label the two vertices of orbit i as i0,i1. A cross block between
orbits is fully red, fully blue, or one of the two red matchings.
Write W_ij=1,-1,0 in these respective cases. Write S_ij=1 for a
parallel red matching, -1 for a crossed red matching, and zero for
a uniform block. Both matrices are symmetric with zero diagonal;
u_i is the row sum of W. The inside color epsilon_i is one for red
and zero for blue. Switching orbit labels conjugates S by diagonal
signs and is always allowed. A uniform orbit pair is an unordered
pair of orbits, not an edge inside an orbit.

A red spine has at most three common red neighbors and a blue spine
at most six common blue neighbors. For a matching pair ij their
respective page counts are

    [9+u_i+u_j+(W^2)_ij+S_ij(S^2)_ij]/2,
    [9-u_i-u_j+(W^2)_ij-S_ij(S^2)_ij]/2.

Consequently

    -3-u_i-u_j+(W^2)_ij <= S_ij(S^2)_ij
                              <= -3-u_i-u_j-(W^2)_ij.       (1)

Thus (W^2)_ij<=0, and equality gives
(S^2)_ij=-(3+u_i+u_j)S_ij. For a uniform pair, the two spines
from a fixed endpoint have exact combined page counts

    red:  sum_{k != i,j}(1+W_ik)(1+W_jk)+2(epsilon_i+epsilon_j),
    blue: sum_{k != i,j}(1-W_ik)(1-W_jk)+2(2-epsilon_i-epsilon_j). (2)

Their caps are six and twelve, and their difference is (S^2)_ij.
A saturated sum therefore gives (S^2)_ij=0. These follow by counting
neighbors in each of the nine third orbits; the literal derivation
is also given in Section 1 of PROOF.md. If neither endpoint of a
matching pair has a red uniform link, its pages simplify to

    red: t;                       blue: 9-t+z,             (3)

where t counts positive triangles of three matching signs and z
counts common blue uniform neighbors. These two caps force z=0.

Here we assume exactly two red uniform pairs and exclude it. The
zero/one-red exclusions and the at-least-seven-total conclusion are
the only earlier results used, both proved in PROOF.md. There is no
assumption on the total blue uniform density.

## 1. Low cliques and attachment capacities

Call the endpoints of the two red uniform pairs active and all other
orbits low. For two low orbits forming a matching, red=t and
blue=9-t+z, so z=0. Thus the induced blue uniform graph on low
orbits is a union of cliques; a common active blue neighbor also forces
their pair blue. Each low clique has size at most three: a blue pair
inside a clique of size r has at least11-r+4(r-2)=3r+3 outside
summed blue pages, bounded by12. A three-clique saturates this lower
bound and cannot have any outside blue uniform link, and all its
inside colors are red.

The low blue neighbors N_i of an active orbit lie in one singleton
or pair, and t_i=|N_i|<=2. In a low two-clique, let m1 count active
orbits blue to just one of its vertices, and m2 those blue to both.
Its combined outside blue sum is9+m1+3m2. Hence m1+3m2<=3.
In particular, if an active orbit has t_i=2, that pair's two inside
colors are red and no other active orbit attaches to either vertex.
Call this the exclusive-pair observation.

## 2. Adjacent red pairs leave only shape A plus low cliques

Write the red pairs as ab,ac. The inside color epsilon_a is zero:
a red inside edge would have four red pages from those two pairs.
The pair bc must be uniformly blue, since otherwise its W^2 entry
has the common red neighbor a and no negative term. Let t_a,t_b,t_c
be the low attachment sizes and z=|N_b intersection N_c|.

The red ab sum is8-|N_a union N_b|+2 epsilon_b<=6, and the ac sum
is analogous. The blue bc sum gives

    t_b+t_c+z <= 2(epsilon_b+epsilon_c).              (5)

If t_a<=1, a red sum with epsilon_b=1 would require a union of size
at least four, impossible. Thus epsilon_b=epsilon_c=0. Equation(5)
then gives t_b=t_c=0, contradicting either red sum. Therefore t_a=2.
By the exclusive-pair observation, N_a is disjoint from N_b,N_c.
The red sums yield2 epsilon_b<=t_b and2 epsilon_c<=t_c. With(5),
z=0 and t_b=2 epsilon_b,t_c=2 epsilon_c.

If t_b=2, any k in N_b has no other active blue link. The pair c-k
is matching and its W^2 entry has the positive term from their common
blue neighbor b, without a negative term: c's sole red neighbor is a,
and k is not blue to a. This violates W^2_ck<=0. Thus t_b=0;
the same argument gives t_c=0. Up to relabeling the entire active
pattern is

    A: red01,02; blue03,04,12,34.

Its remaining six orbits H have arbitrary blue clique components of
sizes1..3, and only matching links to the five displayed orbits.
All six displayed uniform sums saturate: their red outside sums
are six; blue12 has outside sum eight and inside sum four; blue03/04
have outside sum ten and inside sum two; blue34 has outside sum
twelve and inside sum zero. Inside colors are zero at0,1,2 and one
at3,4. This is a complete analytic classification.

## 3. Disjoint red pairs leave shapes B and C plus low cliques

Write the red pairs ab,cd. The other four active pairs are matchings
or blue. Let g_ab count distinct endpoints among c,d blue to a or b,
and similarly g_cd. Each g<=2. Each red sum is exactly

    9-g_ab-|N_a union N_b|+2(epsilon_a+epsilon_b) <= 6. (6)

Its union has size at most four, so epsilon_a+epsilon_b<=1;
similarly epsilon_c+epsilon_d<=1. For an active blue pair ij the
other two active orbits contribute zero, so its blue sum gives

    t_i+t_j+|N_i intersection N_j|
                                 <=1+2(epsilon_i+epsilon_j). (7)

Suppose t_i=2. Its low pair is exclusive with both inside colors red.
If d_i is its active blue degree, the blue sum at i-k, k in N_i,
has outside count11+d_i and inside count2-2 epsilon_i. Thus
epsilon_i=1 and d_i<=1. In fact d_i=0: if i-j is active blue,
the matching j-k has a common blue neighbor i. Its only potential
negative W^2 term is at j's red mate, which does not attach to the
exclusive pair. Hence W^2_jk>=1, impossible.

Conversely epsilon_i=1 implies t_i=2. If t_i<=1, (6) requires g=2,
t_i=1 and its red mate's t=2; that mate also has epsilon=1,
contradicting the previously proved bound on their inside-color sum.

Now t_i=2 would give epsilon_i=1, its red mate j has epsilon_j=0
and t_j<=1, and its active blue degree is zero. Equation(6) forces
t_j=1 and j blue to both endpoints c,d of the other red pair.
Neither c nor d can have attachment size two because its active
blue degree is positive. Their inside colors are therefore zero.
Equation(7) at j-c and j-d gives t_c=t_d=0. The red pair cd has
only one distinct active blue neighbor and no low attachment, violating
(6). Consequently every active inside color is zero and every t_i<=1.
Equation(7) simplifies to t_i+t_j+|N_i intersection N_j|<=1.

Neither g_ab nor g_cd can be zero. If g_ab=1, both a,b attach to
distinct low vertices k,l. All active blue edges go to the sole
opposite endpoint c. Equation(7) makes t_c=0; equation(6) for cd
requires both a-c,b-c blue and t_d=1. The matching c-k has common
blue neighbor a; its only negative W^2 term can be at d, forcing
k in N_d. Similarly l in N_d, impossible since k!=l and t_d=1.
Thus g_ab=g_cd=2.

The active blue graph is a spanning subgraph of K2,2 with no isolated
vertex: either a two-edge matching, a three-edge path, or all four
edges. Each red pair needs a low attachment. Equation(7) forbids a
blue edge between two attached active endpoints, so four blue edges
are impossible. In the other cases there is exactly one attached
endpoint in each red pair, and they form a nonblue cross pair. For
the three-edge path these are the endpoints of its sole cross nonedge;
for the matching, attaching both endpoints in one red pair would
prevent attachment in the other. The matching-spine W^2 condition
at an unattached opposite endpoint and an attached low vertex forces
the two low attachments to be the same singleton k.

To spell out the latter step, normalize the active blue matching as
ac,bd with attachments at a,d, or the path as ac,bd,bc with those
same attachments. For k in N_a, the pair c-k is matching; its common
blue neighbor a gives+1 and its sole possible opposite uniform term
is c's red mate d. Thus k must also be in N_d. Both sizes are one.

At blue a-k its outside sum is10+(r_k-1), where r_k is its low
clique size. Its inside sum is4-2 epsilon_k, at least two. The cap12
forces r_k=1 and epsilon_k=1. Normalize to

    B: red01,23; blue02,13,04,34;
    C: the same plus blue12.

The six outside orbits H are again blue cliques of sizes1..3 with
only matching links to the five active displayed orbits. In B all
displayed uniform sums saturate; in C all except the extra blue12
sum saturate. This classification has no enumeration premise.

## 4. A diagonal shift absorbs every outside clique

For either normal form, write C_H=S_H,H and set

    T=C_H+diag(u_h:h in H).

T is real symmetric. Every displayed-to-H pair is matching and
has (W^2)_ih=0. The general matching identity says
(S^2)_ih=-(3+u_i+u_h)S_ih. Moving u_h into T gives

    S_display,H T+S_display,display S_display,H
                                      =-diag(3+u_i) S_display,H. (8)

This has exactly the same displayed-row equations as when H has
only matchings. The diagonal of T and blue zero entries inside H
do not need any further classification or spectral bound.

## 5. Shape A contradicts linearity

Switch H so S_0,H=a is all ones. Write p1,p2=S_1,H,S_2,H and
q1,q2=S_3,H,S_4,H, and let P=S_{1,2},{3,4}. Saturated uniform
pairs with0 make all four rows balanced six-sign vectors. Uniform12
and34 give p1 dot p2=-(PP^T)_12 and q1 dot q2=-(P^TP)_12.
The mixed matching inequality gives P_ij(p_i dot q_j) in{-2,0};
balanced-row parity2 modulo4 forces-2. The same parity forces the
rows of P parallel/opposite. Switch them to P all positive. All
six row dot products are-2. Thus the squared norm of their total
sum is4*6+2*6*(-2)=0. In particular p=p1+p2 and q=q1+q2
satisfy q=-p and ||p||^2=12+2*(-2)=8.

Equation(8) gives U T+P V=-3U and V T+P^T U=-V.
Summing gives pT=-p and qT=q, incompatible with q=-p and p!=0.
This excludes A for every outside clique pattern.

## 6. Shape B contradicts symmetry

Switch H so a=S_4,H is all ones. Write x=S_03,y=S_12,p=S_14,
q=S_24 and r_i=S_i,H. As in the earlier six-pair proof, saturated
uniform04/34 make r0,r3 balanced, the other four uniform pairs
make them orthogonal to r1,r2, and matching14/24 give
a dot r1=-p-yq, a dot r2=-q-yp. Orthogonality to a balanced
six-sign vector makes these sums2 modulo4, so p=yq. Switch to
x=y=p=q=1. Then a dot r1=a dot r2=-2. At matching12,
(W^2)_12=-2 and (S^2)_12=1+r1 dot r2; inequality(1) restricts
r1 dot r2 to[-6,-2]. Each row has exactly two positive coordinates,
so its possible dot products with another such row are{-2,2,6}.
Therefore r1 dot r2=-2.

Equation(8), with u4=-2 and u1=u2=0, gives

    aT=-a-r1-r2,           r1T=-a-3r1-r2.

But the exact Gram entries imply

    (aT) dot r1 =2-6+2=-2,
    a dot(r1T)  =-6+6+2=+2.

These must agree because T is symmetric. The contradiction excludes
B without any condition on T's diagonal or outside clique sizes. The
short symmetry obstruction is also independently given in
[six-reviewer-1's review](../book_ramsey_free_involution_review1/REVIEW.md).
The additional work here is the complete arbitrary-blue-density case
reduction and diagonal shift, which make it apply to all two-red patterns.

## 7. Shape C contradicts balanced-row parity

Use a=S_4,H all ones. Uniform04 still makes r0 balanced. The new
blue12 replaces its matching sign by zero; u1=-1 and u4=-2, while
(W^2)_14=0. Thus (S^2)_14=0, so a dot r1=0 and r1 is balanced.
The saturated red01 pair has (S^2)_01=r0 dot r1=0. Two balanced
six-sign vectors have dot product2 modulo4 and cannot be orthogonal.
This excludes C at every outside blue density.

All possible exactly-two-red patterns have been excluded. The earlier
zero/one-red exclusions imply the at-least-three-red-pair conclusion.
Software checks are validation, not a premise. The proof uses no
degree theorem, peer global112-edge cut, solver, catalogue, exhaustive
matching-sign enumeration or floating-point inference. Its explicit
trust boundary is the unformalized written case/page/linear-algebra proof.


## 8. Validation and scope

Run the standard-library validation from the repository root:

```sh
python3 book_ramsey_b4_b7_free_involution/check_two_red.py --scratch /tmp/book-two-red-check
```

The fast quotient census and a separate literal-page/set-based checker
both cover 642,323 normalized color patterns after the written low-clique
reduction. They compare every one of 198 necessary survivor patterns
and all 7,341 inside-color assignments, and recover the exact A/B/C
normal forms without enumerating full matching signings. These are
necessary patterns, not valid Ramsey graph witnesses. The separate
checker uses literal two-point neighbor sets and Boolean constraint
backtracking rather than the fast census's bitset formulas and
2,048-bit flag carrier. Both programs are authored by six-books-2;
algorithmic independence is not independent peer review.

Exact vector controls validate eight rank-one blocks, 720 normalized
A row tuples, 2,160 normalized B row tuples and all 400 ordered pairs
of balanced six-sign rows for C. Deterministic literal controls cover
336 lifted graphs across all seven outside clique-size partitions,
61,760 matching-spine checks, 6,080 uniform sum/difference checks and
10,080 diagonal-shift residual checks. These sampled full-size lifts
can violate the book caps; they test identities and are not constructions
or exhaustive matching-sign certificates.

[README.md](README.md) supplies versions, compact expected output,
primary literature and the earlier validation. The proof uses only
integer page counts, complete elementary cases, parity, linearity and
symmetry. There is no solver, floating-point, peer degree/core theorem,
external catalogue or computation-completeness premise. The trust
boundary is the unformalized written argument. Colorings with at least
three red uniform pairs remain open here; no unrestricted 22-vertex
nonexistence or claim that every witness has an involution is made.

## 9. A seven-pair corollary using the independent four-blue bound

The independently authored
[review by six-reviewer-1](../book_ramsey_free_involution_review1/REVIEW.md)
confirms the earlier two-red/seven-total lemma and proves at least four
blue uniform pairs at arbitrary uniform density. Combining that result
with the new three-red lemma leaves exactly the color count **three red,
four blue** if there are seven uniform pairs. This corollary uses the
review's four-blue bound; Sections 1--7 do not. The reviewer has not
reviewed this two-red extension. The sharp relaxed operator residuals
16 and 16/5 and shorter Gram obstructions belong to that review and are
not claimed as new here. Its complete written proof was read for this
integration; its computation was not replayed.
