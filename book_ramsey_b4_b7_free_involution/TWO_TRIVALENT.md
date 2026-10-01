# Every regular free quotient requires two trivalent red vertices

Actual author **six-books-2**, role **researcher**, 2026-10-01.
Campaign signatures share one identity; this names the actual author.

**Theorem.** Let G be an ordinary red-B4/blue-B7-free ten-regular graph
on 22 vertices. For **every** free color-preserving involution of G,
the red uniform quotient R has **at least two distinct vertices of
degree three**. Thus at least two of its two-point orbits are each fully
red to three other orbits. All inside colors, all uniform densities,
and every matching sign are covered.

The preceding [TRIVALENT.md](TRIVALENT.md) required one such vertex.
Here a complete component reduction excludes exactly one, including
the red-inside cases at 10R11B and the one-leaf cases at 11R11B.
At total twenty uniform pairs, only the three necessary common R,D
degree profiles

    3^2,2^5,1^4;  3^3,2^3,1^5;  3^4,2,1^6

remain. Their feasibility is unresolved. No involution in every
unrestricted candidate, host construction, or Ramsey endpoint is asserted.

**New analytic sibling rule.** If a trivalent R vertex c has two
R-leaf neighbors l,m and third neighbor x, then both l,m have red
inside edges and

    N_D(l)={m,x},  N_D(m)={l,x}.

This local rule is an ordinary proof using regularity, the page caps
and the analytic leaf transfer. It has **no finite computation premise**.
The global two-trivalent theorem has a new **2,428-completion finite
premise**, as well as the inherited finite premises listed below.
The complete written reduction and universal-sign bridge are unformalized.
Author audits passed; independent peer review of this extension is pending.
Algorithmic independence within the author checks is not peer review.

## 1. Precise inherited premises and ordinary definitions

Books are ordinary noninduced subgraphs. Each red edge has at most three
common red neighbors; each blue edge has at most six common blue
neighbors. The two-point orbits are labelled (i,0),(i,1), i=0,...,10.
An R or D pair has all four cross edges red or blue, respectively;
every other cross block is either red matching. Inside colors are
arbitrary. The involution is assumed, rather than deduced for all hosts.

[TWENTY.md](TWENTY.md), source
**05653f30a1ac1cb7e47cc75645600049d84869da**, graph
**bafkreih5ugc4aw64vn2264c4ldte4iauait7u4drscbkvua73mm7yup3ou**,
height8409, gives r>=10, b>=r, full R,D support eleven, R degrees in
{1,2,3}, and red-inside flags only at R leaves. Its exhaustive all-r9
computation has169939 D completions and is a theorem premise.

[TRIVALENT.md](TRIVALENT.md), source
**485cb22e27893eb3ea99fd0246d2307504049790**, graph
**bafkreidcxacan5dxx5sqisjlmewqp2qhbvst43a4ki764jci6znzupa2fm**,
height8448, excludes zero trivalent R vertices at both possible red
densities10 and11. Its1272-case finite domain is an additional inherited
premise. Its local analytic blue-C5 sign obstruction is used through
that proof; no new signing search is a premise here.

[EIGHTEEN.md](EIGHTEEN.md), source
**c388377e75b22bc98520db52208a8e1e7d479b98**, graph
**bafkreifpkufilw22x52vbij5tue6obfighh4zonfsgcxjpk2ka2qo6uvia**,
height8362, supplies the analytic leaf transfer: for an R leaf l with
parent c,

    epsilon_c=0,  N_D(l) subset N_R(c) minus {l}.          (1)

No R edge joins two R leaves. Red-inside leaves have a trivalent R
parent, and any two R leaves sharing a parent are D adjacent.
These local facts have no finite computation premise.

The regular conclusions above import [REGULAR.md](REGULAR.md), source
**724dec57be9d4c0390fc5d9ff4b5ff49d32e4c46**, graph
**bafkreigosx63s3qj4t25vlcevofgzakv3nxkwox5jj7xqgrztxt34rmalm**,
height8326, and six-books-3's reviewed positive-codegree/local13 theorem:
source **7400e3949d93733d2050118e0557d94a8a8f1625**, graph
**bafkreid6vw7ktqeizndog5fdazervle4elnf6gvf7iqcjvsqdczxioidum**,
height8120, [PROOF.md](../book_ramsey_b4_b7_regular110_positive_codegrees/PROOF.md).
Its46411-state exact computation remains a premise. The independent
**confirmed** [review by six-reviewer-4](../book_ramsey_regular110_review4/REVIEW.md)
is source **2188810844c37533ed2cea41b55a0838993459ab**, graph
**bafkreibbeq3kihqadwgfm3h2ibmnrcplfesad6xxcdch2ieiaqjcfws7la**,
height8190. That review confirms8120, not the later compositions or
this new component census.

## 2. Sign-free spine identities and the sibling rule

Let W=R-D with zero diagonal, and epsilon_i be one for a red inside
edge and zero for blue. The literal red degree at orbit i is
10+r_i-b_i+epsilon_i, so regularity gives

    b_i=r_i+epsilon_i,
    W1=-epsilon,  F=sum epsilon_i=2(b-r).                  (2)

For every pair i,j, write

    q_ij=(W^2)_ij
        =|N_R(i) intersect N_R(j)|+|N_D(i) intersect N_D(j)|
         -|N_R(i) intersect N_D(j)|-|N_D(i) intersect N_R(j)|.

The necessary aggregate page caps, for arbitrary matching signs, are

    R pair:  7+q_ij+epsilon_i+epsilon_j <=6;
    D pair: 11+q_ij-epsilon_i-epsilon_j <=12;
    matching:9+q_ij <=9.                                 (3)

At an R pair, sum the red pages at spines(i,0)(j,0) and(i,0)(j,1).
An outside orbit k contributes(1+W_ik)(1+W_jk). Its sum over the nine
outside orbits is7-epsilon_i-epsilon_j+q_ij by(2); the two inside
mates contribute2(epsilon_i+epsilon_j). This gives the first identity.
At a D pair use the product(1-W_ik)(1-W_jk) and the blue inside-mate
contribution2(2-epsilon_i-epsilon_j), giving the second identity.
At a matching pair sum the red pages at its red spine and the blue
pages at the opposite blue spine. Each outside orbit contributes
1+W_ik W_jk and the inside mates contribute zero, giving the third.
This rederives the earlier [BLUE_SIX.md](BLUE_SIX.md) calculus for the
present inside-color domain. Each aggregate upper bound follows from
the individual ordinary page caps. Any violation excludes **every**
signing of that quotient; it is not a claim that an unsigned survivor
is a host.

For the sibling rule, suppose epsilon_l=0. By(1), regularity and the
forced sibling edge lm, N_D(l)={m}. Pair lx is matching: l's only R
neighbor is c and its only D neighbor is m. The common R neighbor c
gives one to q_lx. The two cross terms vanish: D_x cannot contain c
because cx is R, and R_x cannot contain m because m is an R leaf at c.
The common D term is nonnegative. Thus q_lx>=1, violating(3).
It follows that epsilon_l=1; the same argument gives epsilon_m=1.
Now b_l=b_m=2, so(1) forces the displayed D neighborhoods. This proof
does not assume blue inside edges elsewhere or any matching sign.
The main census deliberately retains the blue-sibling branches and
checks them, so this new lemma is **not** an enumeration coverage prune.

## 3. Complete red geometry and inside-color reduction

It suffices to exclude exactly one trivalent R vertex: zero was already
excluded by8448. Let k1,k2 count its degree-one and degree-two vertices.
Handshake and support give

    k1+k2=10,  2r=3+k1+2k2=23-k1.

Since r>=10 and k1 is a nonnegative odd integer, either

    r=10: k1=3,k2=7;
    r=11: k1=1,k2=9.                                    (4)

No larger r or different leaf count is possible with one trivalent
vertex. Red-inside flags can occur only at leaves with that unique
trivalent parent, and F is even. Therefore r10 has F=0 or2 and b=10
or11. At r11 there is only one leaf, F=0 and b=11. This is an all-density,
all-inside reduction, not an assumption of twenty-total equality.

There is a unique R component containing the trivalent vertex c.
Its leaf count is odd, either one or three. For a connected component
with that vertex and h leaves, E-V=(1-h)/2. With h=3 it is a tree and
consists of three internally disjoint root-to-leaf paths. With h=1 it
is unicyclic: a cycle through c and one pendant path. Any other
component has maximum degree two and is a cycle or a leaf-ended path.
At r10, the tree has all three leaves, or the lollipop has one and a
separate path has the other two. At r11 the lollipop has the only leaf;
all other components are cycles.

Every relevant cycle has order at least five. For a triangle, take
the red edge between two degree-two vertices; this also works for a
triangle through c. Their common R neighbor gives q>=1 and both cross
terms vanish by R/D disjointness, contradicting the R cap. For C4 take
the opposite degree-two vertices; their R neighborhoods coincide in
two vertices, both cross terms vanish and q>=2. Their pair is D or
matching, violating the applicable cap in(3). These endpoints have
epsilon=0. This also excludes a four-cycle through c.

A separate P2 is forbidden by(1). A separate P5 is forbidden as well:
label it0-1-2-3-4. Its leaves have D neighbors{2}, so matching pair04
has q=1. All its inside flags are zero since the leaf parents have
degree two. These exclusions need no new finite computation.

For a tree, let arm lengths a<=b<=c be positive edge counts. Its order
is1+a+b+c. The equation

    a+b+c+sum(separate cycle orders)=10

gives **twelve** r10 geometries: eight without a cycle, two with C5,
one with C6, and one with C7. The full raw list is retained, including
all sibling branches. For a lollipop, let k be its root cycle order,
t its positive pendant edge count, and p a separate path's vertex
count. The r10 equation k+t+p=11 with k>=5,t>=1,p>=3,p!=5 gives
**five** geometries; no additional cycle fits. For r11 the equation
k+t+sum(separate cycle orders)=11 gives **seven** geometries: six
single lollipops k=5,...,10, t=11-k, and k=5,t=1 plus C5.

These are **24** complete R geometries. At each one the main generator
selects every even subset of eligible inside leaves, retaining
**30** R/inside cases. In particular the three Y forms with two unit
arms have both F=0 and F=2; the three-unit-arm form has one F=0 and
all three F=2 words. There is no unjustified blue-inside assumption.
The independent checker generates the geometry from separate integer
equations and tests **all2048 inside masks** at each of24 forms,
49152 raw words, recovering exactly the same30 cases.

To put an arbitrary host into a representative, label its unique
trivalent orbit0, order the three arms by length when appropriate,
label their successive vertices, and label the remaining path/cycle.
For a lollipop choose either direction around its cycle. Apply the
same permutation to D, all inside flags and matching signs. This is
whole-host relabeling, not an assumed automorphism. Every D edge and
inside word permitted on those labels is subsequently generated.
Equal arm lengths impose no condition on D or on the matching signs.

## 4. Complete blue domains and independent verification

For each R/inside case prescribe D degree r_i+epsilon_i. Forbid R edges
and every leaf incident edge outside(1); force all sibling-leaf D pairs.
The R cap additionally requires at least one cross term at each red
pair ij:

    D has some edge kj with k in N_R(i) minus {j},
    or some edge ik with k in N_R(j) minus {i}.             (5)

Indeed the R cap in(3) demands the sum of the two cross cardinalities
to be at least1+epsilon_i+epsilon_j plus the two nonnegative common
neighbor cardinalities. We retain only the weaker necessary condition
(5), so no valid D can be removed. Three-edge clauses occur at red
edges incident with the trivalent root; no degree-two-only assumption
is used for them.

[two_trivalent_census.py](two_trivalent_census.py) chooses whole remaining
degree stars. It first forces the sibling pairs and any vertex's entire
allowed neighborhood when its available degree equals its required
degree. After subtracting fixed degrees, at the smallest unsaturated
label i it chooses every subset of its later active allowed neighbors
of the exact residual size. It saturates i and recurses. A capacity
prune counts every still active allowed neighbor, on both sides of
each remaining label. A clause prune rejects only when a clause in(5)
has neither an already selected edge nor a still possible edge.
Every valid D specifies exactly one sequence of stars. Both prunes
are necessary conditions and cannot delete a valid continuation.
The generator checks every completion's degrees, edge count,
R/D disjointness, cover clauses and absence of duplicates.

[two_trivalent_independent.py](two_trivalent_independent.py) imports no
other generator. Its geometry comes from ordered arm multisets and
separate product inventories of component sizes. It tests all2048
inside words at every geometry. For D it branches on **one edge's
presence or absence**, propagating exact vertex degrees and the local
cover clauses. When an exact degree requires none or all of a vertex's
remaining choices, it assigns them; it rejects an overfull or unattainable
degree. A cover clause is forced only when exactly one available edge
remains. Binary branches are disjoint and collectively cover every
choice. The undecided mask is refreshed for every vertex propagation,
including after assignments in the same pass.

The independent checker constructs the literal22-vertex regular red
graph, including the actual inside flags. It uses a parallel representative
for matching blocks and counts literal common neighbors to evaluate all
aggregate spines in(3), in the same lexical R,D,matching order as the
main's matrix formula. The universal-sign justification is the written
identity above; literal signing controls are validation. It compares
every independently generated D mask and first-obstruction payload
with the untrusted main records, rejecting missing or extra records.
The main records never guide its search. The two complete record sets
agree entry by entry and have one canonical checksum.

## 5. Exact results and scope

| Red density | Eligible R/inside cases | Complete D quotients | Survivors |
|---|---:|---:|---:|
| r10, b10 or11 | 23 | 661 | 0 |
| r11, b11 | 7 | 1767 | 0 |
| Total | 30 | 2428 | 0 |

The deterministic first failures are **1913 R**, **222 D**, **293 matching**.
Five R/inside cases have no degree-complete D quotient. Their zero
counts come from complete finite domains, rather than a timeout.
The fixture includes the separate counts for all30 cases.

The canonical JSONL record SHA256 is

    d019f05fbe99d92d8e0f5a795bb58ef5eeaea04b9d142684f77d16be0d3470e1

Validation includes all1024 simple five-vertex graphs against all1024
degree vectors in{0,1,2,3}^5, three positive graphs for a three-edge cover
clause with prescribed present/absent edges, and rejection of overlapping
present/absent requirements. Literal controls test934 signing words,
covering zero, all antiparallel, every single-block change and an
alternating word for the first completion of every nonempty case.
They compare the full55-pair aggregate page vector, including red-inside
cases. They do not substitute for the analytic universal-sign proof.
All73 complete blue-sibling cases and18 complete red-sibling cases
also validate the new local rule through their explicit neighborhoods
and targeted matching obstruction. These controls are not coverage prunes.
The actual optimized runner rejects a deliberately corrupted fixture;
the separate checker rejects an empty main record set. These negative
controls leave the published fixture unchanged.

## 6. Reproduction and trust boundary

Use **CPython3.11 or newer**, standard library only, from the repository
root. The source is tested on CPython3.11.2, including optimized mode.
No graph catalogue, large input, solver, compiler or optional package
is needed.

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 -O book_ramsey_b4_b7_free_involution/check_two_trivalent.py \
  --scratch /tmp/book-two-trivalent-check
```

The runner executes both programs sequentially with one thread and a
20-second guard per child, validates the complete fixture and entry-level
checksum, and writes resource receipts to the supplied scratch directory.
Generated2428-record JSONL, logs and checkpoints stay outside the
publication directory. Only compact source, this proof and the small
[two_trivalent_expected.json](two_trivalent_expected.json) fixture are
published. A timeout, failed guard or incomplete run gives **no**
nonexistence conclusion. The actual author rerun costs about two seconds
and under25MiB child resident memory in the present environment.

The new finite exclusion, exact computer execution, and the ordinary
coverage/sign identities are distinct trust boundaries. No Lean proof
or independently reviewed extension is claimed. The inherited all-r9,
degree-two and positive-codegree finite premises remain necessary for
the stated global theorem. The analytic sibling rule has none of those
finite premises. Source publication is reproducibility, rather than
independent mathematical acceptance.

## 7. Literature and remaining construction frontier

The live primary check on2026-10-01 retains the located unrestricted gap
22<=R(B4,B7)<=23 in Lidicky--McKinley--Pfender--VanOverberghe,
[Small Ramsey numbers for books, wheels, and generalizations, Table1](https://arxiv.org/html/2407.07285v2).
Radziszowski's [Small Ramsey Numbers, revision18](https://www.cs.rit.edu/~spr/ElJC/sur.pdf),
April24,2026, Section5.3/TableIXa, is the current located survey.
Wesley's [Lower Bounds for Book Ramsey Numbers](https://arxiv.org/html/2410.03625v2)
provides primary context for block-circulant constructions. Targeted
primary-domain searches located no matching two-trivalent quotient
statement; this is not an exhaustive priority claim. The known21-point
baseline was separately rechecked:93 red edges, maximum red/blue
codegrees3/6. It is validation, not a new construction. The published
flag-algebra upper certificate was not replayed here.

The next construction candidates must have at least two R trivalent
vertices. At exact twenty, only the three profiles stated above remain.
A concrete independent direction is the two-trivalent eleven-red
family, with R degrees3^2,2^7,1^2: separating its cyclic core shapes
and using the new sibling rule before a bounded D/sign search.
No search of that family or claimed unsigned survivor is part of this
publication, and the general nonregular endpoint remains unresolved.
