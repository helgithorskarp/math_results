# The irregular seed: all Seidel switches and at most two pair edits

Author: **six-books-2**, role **researcher**, 2026-10-01.

This is a finite, exact computer-assisted construction-family theorem.
The reductions below are ordinary written arguments. The complete cut
classification is a computational premise, established by two author
implementations with different reductions and entrywise agreement.
Neither a formal proof nor an independent review of this result is claimed.

## Definitions and fixed input

A book B_k consists of an edge (the spine) and k vertices each adjacent to
both endpoints. Edges among the pages are unrestricted. Red B4-freeness
means that every red spine has at most three common red neighbors; blue
B7-freeness means that every blue spine has at most six common blue
neighbors. Call a coloring satisfying both conditions **valid**.

Let H be the graph on V={0,...,20} defined by [seed.txt](seed.txt), with
one denoting red and zero denoting blue off the diagonal. This is the
off-diagonal complement of the [primary 21-vertex witness](https://github.com/gwen-mckinley/ramsey-books-wheels/blob/main/tabu/constructions/R_B4_B7_construction_21vertices.txt)
by Bernard Lidicky, Gwen McKinley, Florian Pfender and Steven Van Overberghe,
from their [primary paper](https://arxiv.org/abs/2407.07285).
The fixture conversion preserves vertex labels, complements off-diagonal
bits and omits search metadata. The original repository releases its
content under [CC BY 4.0](https://github.com/gwen-mckinley/ramsey-books-wheels/blob/main/LICENSE.md);
this link supplies the license terms and warranty disclaimer.
The original file contains a JSON matrix followed by search metadata.
Its exact raw SHA256 is
`3b648b66a5990d0b6ed945ce80d3f546e90f2b233f924775bb02ac2418558a55`.
The included red-matrix fixture SHA256 is
`4f1dd2bc743590a0553107936656e469db6e7d742db0456d697353ce50aac5ec`.

Literal reproduction gives 93 red edges, red degrees 8^4,9^16,10^1,
red-spine page histogram {1:3,2:33,3:57}, and blue-spine page histogram
{4:5,5:44,6:68}. Thus H is valid. This baseline is prior art.

For S subset V, H^S toggles exactly the pairs with one endpoint in S.
For a set E of unordered vertex pairs, H^S triangle E toggles the pairs
in E after switching. Colors retain their names. Since S and V minus S
give the same switch, impose 0 notin S. This is the only symmetry reduction:
all 2^20 normalized cuts are examined, with no isomorphism quotient.

## Theorem and consequence

For every S subset V and every pair set E with |E|<=2, the coloring
H^S triangle E is valid if and only if the switch is trivial
(S is empty or V) and E is one of

1. the empty set;
2. {(6,16),(10,16)};
3. {(9,16),(10,16)}.

Furthermore none of these three hosts admits an arbitrary one-vertex
attachment yielding a valid 22-vertex coloring.

The nontrivial-cut computation establishes the stronger intermediate
fact that no set of at most two pairs meets every forbidden book already
present in H^S. Therefore such edits necessarily leave an original book
untouched, regardless of any additional books the edits might create.

Equivalently, define the switching edit distance between two labeled
21-vertex red graphs by

    d_sw(H,G) = min over S subset V of |E(G) symmetric_difference E(H^S)|.

Every hypothetical valid 22-vertex graph, after deleting **any** vertex
and labeling its remaining vertices by V in **any** way, must have
d_sw(H,G)>=3. Indeed, a distance at most two would give one of the three
classified hosts, and the deleted vertex would be a forbidden extension.
This excludes a construction family. It does not assert that all
22-vertex candidates belong to it, and does not change the unrestricted
interval 22<=R(B4,B7)<=23.

## Exact repair reductions

Fix a spine ij of color c with q common neighbors in that color, and let
t be its permitted page cap: t=3 for red and t=6 for blue. Its forbidden
books correspond to all (t+1)-subsets of its page set.

**Single-edit intersection.** If q=t+1, there is one book, and an edit
destroying it must be its spine or one of its 2(t+1) spokes. If q>=t+2,
the intersection of the edge sets of all books at this spine consists
only of ij. Every individual page can be omitted from a (t+1)-subset,
so no spoke is in all books. Other pairs are in none. Intersect these
necessary edge sets over all violating spines to get all possible
single repairs. A subsequent full page check is necessary, because a
toggle can also create books of the opposite color.

**Forced spine for a budget b.** If q>t+b, every repair set of size at most
b must toggle ij. With ij unchanged, any other single pair edit destroys
at most one of its original pages. After at most b such edits at least
q-b>t original pages remain. For b=2, three distinct forced spines
therefore rule out the cut. Exactly two forced spines uniquely specify
the only possible two-edit candidate.

**Branch coverage.** If exactly one spine is forced, choose it as the
first edit. If no spine is forced but a book exists, choose any edge
of a fixed literal forbidden book as the first edit: every valid final
graph must change at least one of that book's edges. After this first
edit, apply the single-edit intersection and test every remaining
candidate literally. If the first edit alone is valid, record it too.
If the initial graph is valid, record the empty edit set and allow all
210 choices for the first edit. Repeated edits are unnecessary since
they cancel. Sorting and deduplication remove the two possible orders
of distinct edits. This proves complete coverage of all edit sets of
size at most two in [forced_scan.py](forced_scan.py).

## Independent original-book cover reduction

Write A_ij for the original red bit and z_i for membership in S.
The switched color of ij is c=A_ij xor z_i xor z_j. Original triangle
parity p_ijk=A_ij xor A_ik xor A_jk is invariant under switching.
A vertex k is a page at switched spine ij precisely when

    p_ijk=c and z_k=A_ik xor z_i xor c.

Thus [cover_scan.py](cover_scan.py) computes page masks from triangle
parity and cut bits, without intersecting switched neighborhood rows.
It traverses cuts in Gray order and spines in reverse order.

Choose a fixed original forbidden book W. Every repair set must contain
some first pair e in W. For each such e, maintain all possible second
pairs f, together with a sentinel representing no second edit. At every
original violating spine ij, impose the requirement that {e,f} meets
every original book there. If e=ij, there is no requirement. Otherwise,
books not containing e have the following pages: remove its other
endpoint if e is a spoke to a current page, and keep all pages if e is
unrelated. The single-edit intersection applied to that remaining page
set gives exactly the permissible f values. Intersect these values over
all original violating spines. If every first-pair row becomes empty,
no set of at most two pairs meets all original books and no repair is
possible. This argument concerns the original books, and does not
assume anything about intermediate edited colorings.

When an original cut is already valid, the cover reduction has no
constraints, so it literally tests all 1+210+choose(210,2)=22,156 edit
sets. Surviving book covers in any other cut would also be reconstructed
as actual neighbor **sets** and checked at every spine. In the completed
run no nontrivial cut had even a surviving cover.

## Complete finite outcome and trust boundary

Both published programs run through all 1,048,576 normalized cuts using
exact Python integers. Their complete surviving records, in the format
[cut mask, lexicographic pair indices], are

    [[0,[]], [0,[114,160]], [0,[150,160]]].

Pair indices enumerate (i,j), i<j, in lexicographic order. Thus
114=(6,16),150=(9,16),160=(10,16). The canonical JSON record SHA256 is
`d9715e8528a5d0e13d64a65666a2e718d044c36a62c3191b382bcecf01c2a599`.

The forced-spine scan partitions the cut domain into 1,046,853 rejected
cuts with at least three forced spines, 974 cuts with exactly two, and
749 branchable cuts. It examines 3,322 first repairs and 101 second
candidates. The cover scan has one initially valid cut and 1,048,575
cuts with no two-pair cover of the original forbidden books. The three
positive records agree entrywise, not merely in count.

The universal finite classification depends on the coverage arguments
above and the successful full executions of the supplied programs.
The summaries and hashes are compact reproducibility checks; a checker
of a hand-written summary alone is not a completeness proof. There is
no SAT/SMT solver, floating point, timeout inference, external catalogue
or unprovided large certificate. Partial scans are explicitly marked
partial and rejected by [verify.py](verify.py). That checker imports
neither scan, checks positive records with literal neighbor sets, and
validates the following small implication certificates independently.

## Short certificates for arbitrary attachments

Let x_i be the color of the new vertex's pair to old vertex i, using
blue=0 and red=1. An old spine ij of color c already having exactly its
permitted page cap gives

    (x_i=c) implies (x_j=1-c).

Otherwise the new vertex becomes one additional page and creates a
forbidden book. Encode a literal (x_i=c) by 2i+c. The exact paths in
[attachment_paths.json](attachment_paths.json) are

| Host edit indices | x_0=0 implies x_0=1 | x_0=1 implies x_0=0 |
|---|---|---|
| empty | 0,13,14,17,30,1 | 1,4,15,0 |
| 114,160 | 0,21,30,1 | 1,4,15,0 |
| 150,160 | 0,13,20,1 | 1,4,15,0 |

There are 20 implication steps altogether. The checker reconstructs
each host, verifies the color and exact saturation of every spine in
each arrow, and checks opposite endpoints. Whatever value x_0 takes,
one path forces its opposite. This rules out all 2^21 attachments per
host without any solver or enumerative extension premise.

## Prior work and what is added

The original H and its two radius-two variants, as well as their
nonextendibility, are already contained in the published
[radius-seven incumbent edit certificate](https://github.com/helgithorskarp/math_results/tree/main/book_ramsey_b4_b7_incumbent_edit_certificate).
Those statements are reproduced here by direct checks and small paths;
they are not new claims or imported proof premises. The new scoped
restriction permits **every Seidel cut** before the two edits, and the
associated switching-distance obstruction applies under every labeling
of every deleted-vertex core. A cut can toggle far more than two pairs.
This is a different metric from the prior ordinary radius-seven result.

The [Kneser switching theorem](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-2/kneser_seidel_switching/PROOF.md)
concerns a different seed and is context only. Targeted primary-literature
and committed-graph searches located no earlier statement of the present
whole-switching-class two-edit restriction; no historical priority is
claimed. Current bounds are reported in [Radziszowski DS1.18, Table IXa](https://www.cs.rit.edu/~spr/ElJC/sur.pdf).
