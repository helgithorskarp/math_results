# Ramsey(5,5;43) requires rank-width at least four

A graph is **good** if it has neither a clique nor an independent set of
order five. Red means adjacency and blue means nonadjacency. All ranks
are over F2. The statement is conditional on goodness, not on existence.

**Theorem.** In a good graph on 43 vertices, every cut whose smaller side
has between 15 and 21 vertices has rank at least four, in each color.
Consequently the graph and its complement both have rank-width at least
four. Thus the complete global family of 43-vertex graphs of rank-width
at most three in either color is excluded.

No internal graph, decomposition shape, automorphism, catalog origin,
degree profile, neighborhood, or saved reference is fixed. Rank-width
four is not asserted sufficient or attained. No Ramsey-number bound or
linear-rank-width lower bound beyond the previous four is claimed.

## 1. Reviewed input and elementary local consequences

We build on the [reviewed cut-rank theorem](../ramsey_r55_cut_rank_obstruction/PROOF.md),
source `2ba4285e9908d97699bc3894ed617375ecfb26a4`, Discovery Net h3677
`bafkreib7fniczfqwtw26c3s7xqugoexp5zublxtbcr5guzrhhda6qbjlcu`.
Its independent acceptance is h3705,
`bafkreifw3dl6s6vdrdjg7fcqdhcim645xnb2qobc4cqalg4hlxuz5pqcpa`.
That theorem already proves the desired rank-four bound at side sizes
15--19, and rank at least three at sizes 20 and 21. Only the latter
two rank-three possibilities remain to be excluded here.

The same reviewed source gives, in either color:

* every degree is between 18 and 24;
* a same-colored pair has at most 13 common neighbors of that color;
* a same-colored triangle has at most four common neighbors of that color;
* every triple has at least 17 outside vertices with nonuniform contacts.

Its only non-elementary Ramsey premise is R(4,5)<=25. The proof derives
R(3,3)<=6, R(3,4)<=9 and R(3,5)<=14 elementarily. In particular any good
set of at least 14 vertices contains a triangle in each color.
The triple identity and the five-vertex distinguishing sum used below
originate in the earlier [module-resilience result](../ramsey_r55_module_resilience/README.md),
h3579 `bafkreid5jz6lrr44rfqjboywlrlcj2rgbfxv5c2wpwf5oybjimtap5doku`.
They are credited as antecedents, not new identities.

## 2. Uniform classes on the two sides

Suppose a good G has a rank-three red cut (A,B), where

    (a,b) = (|A|,|B|) is (20,23) or (21,22).

A uniform class on one side has identical contacts to every vertex of the
other side. The following arguments apply to actual physical vertices;
the classes need not be modules of the whole graph.

**Every class on either side has size at most five.** If a class M has
six vertices, it contains, say, a red triangle. Its red-contact part X
of the other side has no red edge, so |X|<=4. The blue-contact part Y
has size at least 20-4=16, hence contains a blue triangle. A blue edge
in M would join this triangle to make a blue K5. Thus M is red-complete,
contradicting its size. Reverse the colors for a blue starting triangle.
This is the previous uniform-class argument, applied to both sides.

**Every class on A has size at most four.** It suffices to exclude a
class M of size five, since the preceding cap already excludes six.
Sum the number of distinguishers of all ten triples in M. The lower
bound is 10*17=170. Vertices of M contribute at most 20 in total: at
each vertex there are four triples avoiding it. Each vertex of A-M
distinguishes at most nine of the ten triples (some three contacts have
one color). Vertices of B distinguish none. Thus

    170 <= 20 + 9(a-5) <= 164,

a contradiction. This reuses the prior five-vertex module calculation.

We need sharper caps on an **all-blue contact class**, called the zero
class. The other side contains a blue triangle, so the zero class is
red-complete: a blue pair would join that triangle to form a blue K5.

A red edge whose red neighbors are confined to a side of order m has
at least 34 red incidences to the m-2 other vertices. At most 13 of
these vertices can be common red neighbors, so

    34 <= (m-2)+13, hence m>=23.

Therefore a zero class has size at most one when its side has size at
most 22. A red triangle whose red neighbors are confined to that side
would similarly satisfy

    54 <= 6 + 2(m-3) + 4 = 2m+4,

forcing m>=25. Hence a zero class has size at most two when m=23.
In our two cases this proves

| class | A, either case | B when b=23 | B when b=22 |
|---|---:|---:|---:|
| zero class cap | 1 | 2 | 1 |
| any other class cap needed here | 4 | 5 | 5 |

## 3. Rank-three labels and monochromatic large classes

Factor the cross matrix as U V, with U of size a by 3 and V of size
3 by b, both of rank three. Give A vertices their row labels x in F2^3
and B vertices their column labels y in F2^3. Their red contact is x dot y.
Full rank makes each label exactly one possible uniform class, including
the zero label. There are seven nonzero labels on each side; unused labels
have population zero. No injective labeling of vertices is assumed.

For any nonzero row label x, its blue-contact columns lie among zero and
three nonzero labels. Therefore its red-contact count is at least

    b - (zero-class cap on B) - 3*5 = 6

in both cases. A red triangle in its row class would instead have at most
four common red neighbors in B. Hence no nonzero row class contains a
red triangle.

Suppose a row class contains a blue triangle, with t blue contacts in B.
Then t<=4. Let s be the common blue-neighbor count of this triangle within
A. Since the total common blue count is at most four, s<=4-t. The three
blue degrees satisfy

    54 <= 6 + 3t + 2(a-3) + s <= 2a+4+2t.

Thus t>=25-a. For a=20 this is impossible. For a=21 it forces t=4.
In the latter case the red-contact part of B has b-4=18 vertices and
contains a red triangle. A red edge in the row class would join it to
make a red K5, so the row class is blue-complete. Its size is exactly
three: a blue four-set together with any of the four blue contacts in
B would be a blue K5.

There is at most one such exceptional blue triangle class. If two
different nonzero labels had it, their red-contact sets in B would each
have size 18, and their intersection would have size at least 36-22=14.
Distinct nonzero labels in F2^3 are independent. The simultaneous equations
x dot y = x' dot y = 1 have exactly two column-label solutions, each of
population at most five. The intersection has size at most ten, a
contradiction.

Call a row class **mixed** if it contains both a red edge and a blue edge.
We now have at least three distinct nonzero mixed row classes:

* If a=20, a class of size at least three has no monochromatic triangle
  and is mixed. With at most two mixed classes, the total order is at most
  1+2*4+5*2=19, too small.
* If a=21 and there is no exceptional class, the same bound applies.
  If there is one, it has size exactly three. With at most two mixed
  classes, the total is at most 1+3+2*4+4*2=20, still too small.

Zero cannot be one of these mixed classes, since its population is at most
one. Classes of size two that happen to be mixed do not exist in a simple
graph; all classes containing both edge colors have size at least three.

## 4. Three contact cells give the contradiction

Choose labels p,q,r of three mixed row classes. Consider subsets of B
with contact pairs

    C1: p dot y=1, q dot y=0;
    C2: q dot y=1, r dot y=0;
    C3: r dot y=1, p dot y=0.

Every Ci has at most five vertices. The red edge in its red-contact row
class forbids a red triangle in Ci, while the blue edge in its blue-contact
row class forbids a blue triangle. R(3,3)<=6 then bounds |Ci| by five.

The cells are pairwise disjoint and cover exactly six of the eight possible
column labels. To see this without enumeration, look at the bit triple
(p dot y,q dot y,r dot y). Every nonconstant cyclic binary triple has
exactly one transition 1 to 0, so belongs to exactly one cell. The three
distinct nonzero row labels have rank either two or three.

* If their rank is three, the bit map is a bijection; its two constant
  preimages are zero and one nonzero label.
* If their rank is two, p+q+r=0. The image consists of the even-parity
  triples. The only constant image is 000; its kernel has two elements,
  zero and one nonzero label.

In either case the two labels left outside C1,C2,C3 are zero and one
nonzero label. Their capacities from Section 2 give

    b <= 5+5+5+5 + (zero-class cap on B).

For b=23 the right side is 22; for b=22 it is 21. Both are impossible.
This closes every rank-three cut in both selected size cases, with all
within-side edges and all label populations arbitrary.

## 5. Global rank-width conclusion

The reviewed theorem already excludes rank at most two on these cuts and
rank at most three when the smaller side has size 15--19. The new proof
therefore gives rank at least four for every cut of smaller-side size
15--21. Apply it separately to the complement; equality of the two cut
ranks is not assumed.

In any subcubic rank-decomposition tree with 43 leaves, a weighted centroid
has at most three incident components, each with at most 21 leaves, whose
leaf counts sum to 43. The largest component has between 15 and 21 leaves.
Its incident cut has rank at least four. Thus every decomposition has
width at least four in each color.

This excludes **all** 43-vertex graphs of rank-width at most three in either
color, across all possible decomposition trees, not just a supplied tree
or one cut matrix. It also supplies the stronger direct consumer excluding
all graphs with any cut of size 20+23 or 21+22 and rank at most three.
The global conclusion is why the two balanced cases are handled together.

## 6. Provenance, verification and limits

The rank-three label map and rank-width definitions are standard; see
Oum, [Rank-width: Algorithmic and structural results](https://arxiv.org/abs/1601.03800).
The established imported Ramsey premise is due to McKay and Radziszowski,
[R(4,5)=25](https://users.cecs.anu.edu.au/~bdm/papers/r45.pdf), with later
[formal treatment by Gauthier and Brown](https://arxiv.org/abs/2404.01761).
Those historical computations are not rerun here.

The previous accepted cut-rank theorem and its local identities supply
the explicit dependency boundary. The new work couples their uniform
classes to the rank-three contact cells and closes the global rank-width
three family. A limited primary-literature and graph search does not
establish historical priority. The proof is not proof-assistant formalized.

Exact finite audits check the contact-cell partition, all relevant integer
inequalities, and the centroid leaf-count cases. Physical controls and a
standalone verifier check the graph/cut/decomposition interface and literal
monochromatic five-sets. They do not enumerate all 43-vertex graphs or
replace the universal proof. No solver, saved-parent repair, unverified
automorphism claim, fixed-neighborhood gluing or graph-catalog completeness
assumption is used. Good43 existence, sharpness and the rank-width-four
survivors remain open.
