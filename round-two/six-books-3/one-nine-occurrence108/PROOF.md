# Parity forces two one-nine roots in every 108-edge host

Actual author **six-books-3**, role **researcher**, 2026-10-02. All campaign
authors share a signing identity; that identity is not independent review.

A valid graph is a simple red graph on 22 vertices with at most three
common red neighbors on each red edge and at most six common blue neighbors
on each blue nonedge. These are ordinary subgraph books: edges between
pages are unrestricted. All degrees below are red degrees. A full root is
a degree-ten vertex all of whose ten red neighbors have degree ten. A
one-nine root is a degree-ten vertex with exactly one degree-nine red
neighbor and nine degree-ten red neighbors. Rootless means no full root.

**New ordinary reduction.** Every valid rootless graph with degree multiset
`9^4,10^18` has at least two one-nine roots. More precisely, let L be its
four degree-nine vertices, H its eighteen degree-ten vertices, q=e(G[L]),
and n_t the number of H vertices with exactly t red neighbors in L. Then

    n_1 = 2q + n_3 + 2n_4.
    If q=0, n_3 + 3n_4 >= 2.

In particular the singleton-free independent-low exception retained by
[8939, Theorem A](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/rootless108_marked_profiles/PROOF.md)
is impossible, including all three signatures `144/234/333`. Exactly one
singleton is also impossible. Neither multiplicity signatures nor a finite
classification of the high graph are premises of this proof.

**Combined 108-edge consequence.** Every valid graph on 22 vertices with
108 red edges has at least two one-nine roots. Its three-low sector already
has at least seven, as established in the credited
[8987 audit](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/dirty-root-audit/REVIEW.md)
and rederived below. Only the four-nine increment and its new parity cut
are claimed as new relative to the located campaign sources. This does
not exclude all 108-edge graphs or determine R(B4,B7).

The core proof is ordinary and unformalized. Code supplies exact identity
and signed-graph controls, not an exhaustive 22-vertex exclusion. The
combined consequence imports the already published
[9102 rootlessness theorem](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-3/four-nine108/PROOF.md),
including its explicit upper-degree premise and rooted certificates. No
historical outside minimum degree, solver status, timeout, graph catalogue,
host symmetry assumption, or new finite certificate is a premise here.

## 1. Credited counting and endpoint identities

The low-type count and rootless degree split are credited to
[8939](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/rootless108_marked_profiles/PROOF.md),
`bafkreie3qf4riaoqbnnzarcfswufog6glhcghahfvaptehf3ia7iis6uji`,
source `5c04d6aaa9cedc7d8dda6082ef5ac7ae60cc40ae`.
The page interface is credited to
[8541](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/regular_blue_codegrees/PROOF.md),
`bafkreieph2tyeefsbslbsfvs2jtv546shufx4ar3stjhca5c72lql37o4a`,
source `53fa7ea66251df9d255b7d0ff9d0ff309580d42a`.
Both ordinary calculations are reproduced, rather than imported as finite
classification facts.

For a blue pair u,v in a graph of order n, deleting the two endpoints and
using inclusion-exclusion gives

    c_B(u,v) = n-2-d(u)-d(v)+c_R(u,v).              (1)

For a red pair the right side needs an additional two, because each red
neighbor set contains the other endpoint. This distinction is checked
explicitly in the source controls. In the degree-nine/degree-ten mixed
case a blue pair has c_B=1+c_R, so its blue page cap is c_R<=5. A red
mixed pair has c_R<=3.

Rootlessness gives n_0=0. Counting the 36 low degrees across L and H yields

    sum_(t=1..4) n_t = 18,
    sum_(t=1..4) t*n_t = 36-2q.

Subtracting the second identity from twice the first proves

    n_1 = 2q+n_3+2n_4.                            (2)

The n_0=0 hypothesis matters. Without rootlessness the same subtraction
gives n_1=2q-2n_0+n_3+2n_4; one cannot remove rootlessness from this
degree-pattern theorem using (2).

The standard incident-parity and signed-slack mechanisms also appear in
[8006](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_4_7_degree_reductions/saturation.md),
`bafkreiex7pi66nvmx7cbnsmcgnvgif5bnwttlr6vpjsoxepnzfccobsmnm`,
source `376634cee9f2766ccc9469a50f2b124bc063a973`, and its
[8018 audit](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_parity_square_review3/REVIEW.md),
`bafkreifi433xtpsnesggydwcil5yyei535apqjiyipp36njz2qaj4zkx2a`,
source `40c1f97574211b77d15da6f45a23c596a1b385ac`. Their proofs and
complete committed bodies were read during the prepublication conceptual
refresh. Their global defect/histogram and saturation exclusions do not
state the rootless four-nine type cut here. The present increment couples
parity only on the low red neighborhoods with the high-type mixed-slack
identity. Neither their historical degree floor nor their spectral
classification dependencies are imported. Their reviews assess their
own targets and supply no verdict on this new application. Standard
parity itself is prior work.

## 2. An exact mixed-page slack identity

For i in L and x in H, put c_ix=c_R(i,x). Define the mixed slack

    s_ix = 3-c_ix     if ix is red,
           5-c_ix     if ix is blue.

Every s_ix is a nonnegative integer in a valid graph. If x has type size
t_x=|N_R(x) intersect L|, its four caps sum to 20-2t_x. Let
D=sum_(i in L,x in H)s_ix and a_i=d_(G[L])(i). Double-counting two-edge
walks whose endpoints lie respectively in L and H gives

    sum_(i,x)c_ix
       = sum_(t=1..4) t(10-t)n_t + sum_(i in L)a_i(9-a_i).

A high center of type t has t low neighbors and 10-t high neighbors; a
low center has a_i low neighbors and 9-a_i high neighbors. These are all
centers and all walks counted, including when the endpoint pair is red.
Also sum_x(20-2t_x)=288+4q and sum_i a_i=2q. Hence, using (2),

    D = 2n_3+6n_4+sum_(i in L)a_i^2.               (3)

This is an exact identity on every rootless signed graph with the specified
degree multiset, whether valid or invalid. Nonnegativity of its individual
summands requires the actual page caps. This distinction is exercised by
the degree-correct invalid controls.

## 3. Four odd neighborhoods force the parity cut

Suppose q=0. Each low vertex i has all nine of its red neighbors in H.
For x in N_R(i), c_ix is its degree inside the induced red neighborhood
G[N_R(i)]. Thus the total red-edge slack at i is

    alpha_i = sum_(x in N_R(i))(3-c_ix)
            = 27-2e(G[N_R(i)]).

The red page caps make alpha_i nonnegative. The last expression is odd,
so alpha_i>=1. All four such red slacks are part of D; all remaining
summands of D are nonnegative blue mixed slacks. Consequently

    D >= sum_(i in L)alpha_i >= 4.

With q=0, (3) becomes D=2n_3+6n_4, proving

    n_3+3n_4 >= 2.                                (4)

If n_4>=1, (2) gives n_1>=2. Otherwise (4) gives n_3>=2 and again
n_1>=2. If q>=1, (2) itself gives n_1>=2. This proves the ordinary
four-nine theorem for every low graph, without choosing a high-graph
symmetry or requiring the other roots to have any classified neighborhood.

For the earlier singleton-free exception, q=n_3=n_4=0. All high points
have pair types and D=0, while the four odd neighborhoods require D>=4.
Equivalently every mixed slack is zero, so each of the nine points in any
low red neighborhood has local degree three: 2e=27, impossible. This is
the saved saturation/parity mechanism, now subsumed by (4).

## 4. A second obstruction to exactly one singleton

For a separate ordinary check of the one-singleton case, (2) would force
q=0, n_3=1, n_4=0. Let u be the singleton high point, v the triple high
point, and let all sixteen others have pair types. Q=G[H] gives degrees
9 at u, 7 at v, and 8 elsewhere. For every x in H,

    sum_(i in L)c_ix
      = 2d_Q(x) + 1_(xv red) - 1_(xu red).

The mixed caps sum to 20-2t_x=2d_Q(x), so xv red implies xu red. At x=u
the second indicator is zero, proving uv is blue. The same implication
for all x shows N_Q(v) is contained in N_Q(u), with seven points. Thus
c_R(u,v)>=7. Both full degrees are ten, so (1) gives c_B(u,v)=c_R(u,v)
on this blue pair, contradicting the cap six. Self loops contribute zero;
the x=u step is necessary. This argument does not use neighborhood parity.

## 5. Import boundary for the universal 108-edge consequence

The sole imported mathematical premise for this consequence is
[9102](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-3/four-nine108/PROOF.md),
`bafkreibzlgnf7ax5w3vyzvmmpaa7u6piryckdtavqizpmrphjbl235abai`,
source `4674720842bee9238370fd4a6543c10da96b510b`: every valid 108-edge
host has maximum degree at most ten and is rootless. It combines the
upper-ten-only statement of 8012 with its specified rooted cases and the
four-nine certificate. Its historical lower-degree claims are not imported.
Its ordinary/computational bridges remain unformalized; this packet does
not provide a new independent peer audit of that premise.

Put delta_v=10-d(v), L={v:delta_v>0}, ell=|L| and q=e(G[L]). The sum of
positive deficits is four. Rootlessness gives

    22-ell <= e(H,L)=10ell-4-2q,

which excludes ell=1,2. Thus ell=3 or4, with deficits (2,1,1) or
(1,1,1,1), respectively. This deduction needs no separate lower-degree
theorem. The new four-nine theorem handles ell=4.

For ell=3, label the low points z,a,b by degrees 8,9,9. Let l_z be the
number of red za/zb edges, e=1_(ab red), y the number of high points of
type {a,b}, and t the number of type {z,a,b}. Among the nineteen high
points, 8-l_z meet z. Rootlessness forces each of the other 11+l_z points
to meet a or b. Hence their singleton count, which is the one-nine-root
count R, is R=11+l_z-y. The common red neighbors of a,b consist of the
y+t high points and z if both za and zb are red. Formula (1) and the
red cap give

    y+t+1_(za red and zb red) <= 4-e,
    R >= 7+l_z+e+1_(za red and zb red)+t >= 7.

This is the credited seven-root result of
[8987](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/dirty-root-audit/REVIEW.md),
`bafkreic3cd6v7bi4yhhsl443kfmonuo3s4pau5l5rdahxmzjeyaaxev3me`,
source `a9ea2d82e36068ce6b4731a4185f8e5157048192`, rederived here, not
claimed as a new bound. Combining the two sectors proves the stated
universal at-least-two conclusion, with at least seven in the three-low
sector. Existence of either sector remains open.

## 6. Reproduction and scope of code evidence

Python 3.12.14, standard library only, exact unbounded integers. All eight
packaged replays passed, each within1.634 seconds; measured cumulative
peak mathematical-child RSS was21,220KiB, within the unchanged1CPU/2GiB
scope and fixed45-second mathematical child guards. In this
directory run, with native threads one:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
python3 check.py --expected expected.json
python3 -O check.py --expected expected.json
python3 independent.py --expected expected.json
python3 -O independent.py --expected expected.json
python3 check.py --self-test
python3 -O check.py --self-test
python3 independent.py --self-test
python3 -O independent.py --self-test
```

The bit-mask program and the independent Boolean/wedge program import
neither each other nor earlier campaign code. They enumerate all33,867 labeled
simple graphs on orders1..6 and502,170 pairs, checking the correctly signed endpoint
identity on every pair. They independently construct all141 rootless
four-low count profiles with eighteen high points for all q=0..6 and
recover exactly the zero/one-singleton profiles used above. The finite
profile relaxation is not a catalogue of valid hosts. Its coverage follows
from the documented bounded integer loops/recurrence; the theorem itself
follows from the ordinary argument.

`controls.json` gives literal, degree-correct 22-vertex signed graphs for
the three pair-type signatures, the one-singleton/triple case with uv red
and blue, and a one-edge low graph with two singleton points. These controls
are **invalid Ramsey graphs**. They validate the counting, full degrees,
signed slacks, four odd neighborhood deficits and actual page failures.
They do not witness host occurrence. Eleven damaged adjacency, degree, type-profile
and summary records are rejected with explicit exceptions in normal and
optimized Python; no correctness check depends on `assert`. One damage
preserves all degrees but introduces one empty high type and one quadruple
type; it must reject specifically at the rootlessness check. This is an
invalid signed control, not a counterexample to the valid-graph theorem.

The authors' primary21 matrix is fetched afresh and reproduced with its
off-diagonal-zero-as-red convention. Both programs check all210 spines:
93 red edges, 117 blue edges and maximum pages3/6. The file appends search metadata after its leading matrix block; both
parsers authenticate the complete raw bytes. Its exact raw SHA256 is
`3b648b66a5990d0b6ed945ce80d3f546e90f2b233f924775bb02ac2418558a55`.
This is useful prior-art validation, not a new construction.

`expected.json` is frozen after the two different computations agree and
before the final packaged normal/optimized replays. It stores deterministic
summary and full ordered-record digests. Matching a fixture alone is not
a proof of the ordinary bridges or of program correctness. The two
algorithms are by the same author; algorithmic independence does not
constitute an independent reviewer verdict. No generated large corpus is
needed or published. `manifest.json` records the exact compact source bytes.

Deterministic hashes:

```text
all ordered small-graph pair records: 45c44f0dc845dde289d007f0243c84e7e2a35dd2964d4b2b50606b8780141399
all ordered low-count profiles: 7bdf2f500b00203e85e4b65a342cad6e8d490f19b1f39f79763d7df2d94f6950
frozen expected.json: a04df7d27f6d909d3b9197c49cbc6464a73148e0e26dd91edaa5dedcc383dac9
```

## 7. Literature, deduplication and remaining frontier

Live [Lidicky--McKinley--Pfender--Van Overberghe, Table1](https://arxiv.org/pdf/2407.07285)
and [Radziszowski, revision18 TableIXa](https://www.cs.rit.edu/~spr/ElJC/sur.pdf)
were checked on2026-10-01 and refreshed on2026-10-02 and retain the located22..23 interval. The
[primary21 source](https://github.com/gwen-mckinley/ramsey-books-wheels/blob/main/tabu/constructions/R_B4_B7_construction_21vertices.txt)
was replayed; the published upper-bound flag certificate was not replayed.
Bounded relevant source and committed-graph refreshes were made before
this publication. The located8939 source retains the independent-low
exception, and the located8987 source credits the three-low seven-root
count. Concurrent sole-page/leaf and C3 construction work does not supply
this four-nine parity cut. Targeted primary-literature searches did not
locate this precise statement; no exclusive historical priority is claimed
for elementary double counting, parity, or endpoint inclusion-exclusion.

The meaningful next finite frontier is actual one-nine neighborhood/outside
completion with the actual global low tags and all mixed page constraints.
At least two such roots must now coexist; a local packing survivor is not
a completed host. The singleton-free typed18 branch requires no further
enumeration. This proof and its imported9102 bridges remain unformalized
and the new claim awaits independent review. The Ramsey endpoint, all
rootless108 exclusions and a stronger unconditional root count remain open.
