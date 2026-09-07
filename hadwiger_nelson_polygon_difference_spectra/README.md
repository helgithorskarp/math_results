# All-scale regular-polygon difference clouds through 508 vertices

**Exact computer-assisted classification.** Put

\[
\zeta_n=\exp(2\pi i/n),\qquad
P_n=\{\zeta_n^i-\zeta_n^j:0\le i,j<n\}.
\]

The origin is included. Every similarity image of every full cloud `P_n`
with at most 508 distinct points has chromatic number at most **three**.
This also colours every subgraph of every such image. At scales with an
edge, the full graphs are classified exactly: **4,283 cases are bipartite
and 869 are three-chromatic**, over 26 polygon orders and 5,152 pairs of
polygon order and scale. All other scales give edgeless graphs. Cases
are not identified up to graph isomorphism.

This is a complete construction-family result, covering every scale and
all exact coincidences and distance contacts. It gives no five-chromatic
graph, no improvement on Parts's 509-vertex record, and no general lower
bound on the number of vertices in a five-chromatic unit-distance graph.
It does not cover arbitrary subsets of larger clouds, unions of clouds,
or freely moving their points. The completed family is retired; this
milestone ends at a consolidation boundary.

## 1. Why the construction gate is finite and complete

Fix a nonzero chord vector `d`. Its ordered endpoints satisfy
`z-w=d`, `|z|=|w|=1`. Intersecting the two unit circles for `w` gives at
most two ordered pairs. If `(z,w)` is one, the other is `(-w,-z)`.
They coincide exactly for a diameter.

For odd `n`, antipodes are absent from the regular polygon, so all
`n(n-1)` nonzero ordered chord vectors are different. For even `n`, the
`n` oriented diameters occur once and all other ordered chord vectors
occur twice. Consequently

\[
 |P_n|=\begin{cases}
 n(n-1)+1,& n\text{ odd},\\
 n^2/2+1,& n\text{ even}.
 \end{cases}
\]

Order one is a singleton. The nontrivial admissible orders are precisely
`2,3,...,24,26,28,30`. Odd orders at least 25 exceed the budget; even
orders at least 32 do as well. The largest admissible cloud has **507**
points, at `n=23`. These formulas also bound polygon orders without
assuming an arbitrary search cutoff.

For each admissible `n`, partition all unordered pairs of distinct cloud
points by their exact squared distance `delta`. It is positive because
the points differ. The strict unit-distance graph on

\[
 P_n/\sqrt{\delta}
\]

has exactly the pairs in that distance class as edges. Conversely, a
positive scale `s` produces an edge precisely if `s=1/sqrt(delta)` for
one of those classes. Translations, rotations and reflections preserve
this classification. This proves that the finite distance census covers
every real scale, without angular or algebraic-parameter sampling.

## 2. Independent exact geometry

The proposal program `build.py` works in `Z[X]/(Phi_n(X))`. It constructs
cyclotomic polynomials recursively from `X^n-1`, reduces every ordered
chord, and computes squared distances by polynomial multiplication with
complex conjugation. `python-flint` provides its integer polynomials.
No input graph, coordinate table, or floating-point comparison is used.

The proof checker `verify.py` imports neither the proposal program nor
FLINT, SymPy or a SAT solver. It uses a different representation. Define

\[
 c_n(t)=\sum_{d\mid\gcd(n,t)}d\,\mu(n/d)
       =\sum_{\substack{a\bmod n\\(a,n)=1}}\zeta_n^{at}.
\]

For an integral cyclic coefficient word `f=(f_0,...,f_(n-1))`, use the
integer trace vector

\[
 T_k(f)=\sum_j f_j c_n(j-k),\qquad 0\le k<n.
\]

Two words evaluate to the same complex algebraic number at the specified
primitive root exactly when their trace vectors agree. To see this,
cyclotomic irreducibility shows that a zero at `zeta_n` gives zero at
every primitive conjugate. Conversely, the discrete Fourier inversion
of

\[
 T_k(f)=\sum_{(a,n)=1}\zeta_n^{-ak} f(\zeta_n^a)
\]

recovers each primitive conjugate value; a zero trace vector therefore
forces the specified value to vanish. These are standard algebraic
facts, supplied as written mathematics rather than a proof-assistant
formalization.

The checker identifies chord coincidences by these trace vectors. For
points with representative addresses `(i,j)` and `(k,l)`, it forms the
at-most-four-term word

\[
 w=X^i-X^j-X^k+X^l
\]

and obtains the norm by cyclic convolution `w(X) w(X^(-1))` modulo
`X^n-1`, followed by the integer trace map. It enumerates every one of
**714,594 unordered pairs** across the admissible clouds. Equal trace
vectors give exactly one distance class. Caching identical norm words
avoids repeated arithmetic but removes no pair.

Vertices are ordered by the lexicographically first ordered chord
address representing them. Each distance class is labelled by its
lexicographically first vertex pair, and classes are ordered by those
pairs. These labels are independent of the arithmetic representation.
With `--compare-data`, every vertex coordinate, squared distance,
complete edge list, proposed colour word and chromatic number is
compared against the proposal output, entry by entry. Merely matching
counts is not the validation criterion.

## 3. Compact positive certificates and exact chromatic numbers

For each distance graph, the checker either constructs a proper
bipartite colouring or finds a simple odd cycle. It validates every
edge of every odd cycle explicitly. Every distance class has an edge,
so a bipartite class has chromatic number exactly two.

For a nonbipartite class, repeatedly delete a vertex of degree at most
two. The remaining 3-core is unique, independently of deletion order.
`certificate.json` supplies a proper three-colouring of each nonempty
core, listing its vertices in increasing label order. Restore deleted
vertices in reverse order, each using one of the three colours absent
from its already restored neighbours. The checker then verifies all
edges of the full graph again. The odd cycle supplies the matching
lower bound of three.

There are **309 stored core words containing 53,770 ternary symbols**.
The certificate is **63,960 bytes**, with SHA-256

```text
45a928f317553fd80ea95e992cf38105a50ad12da8e3e4f22bec69f74a33926e
```

All other colourings and all 869 odd cycles are reconstructed by the
standard-library checker. Their canonical odd-cycle stream has SHA-256

```text
f0fcb08743cbe1aad027916ca978945c251f09efaf162d4ba43bf86eb8ddbd27
```

The optional producer finds core colourings with CaDiCaL 1.9.5 through
python-sat 1.9.dev15. Variables `x_(v,c)` allow each core vertex at least
one of three colours; every core edge forbids a common colour. Pinning
the first core vertex to colour zero is valid by colour permutation.
Choosing one true colour per vertex decodes a proper colouring even
though the formula does not require at-most-one clauses. All 309 calls
returned SAT, using at most 145 conflicts under a fixed 200,000-conflict
budget. The producer stops on either UNSAT or UNKNOWN; neither is used
as a theorem premise. The committed positive words make solver
soundness and availability unnecessary for proof replay.

## 4. Reproduction and reusable spectrum data

The proof needs **Python 3.11 or later, standard library only** (tested
with CPython 3.11.2). From this directory:

```sh
python3 verify.py --check-expected
python3 -O verify.py --check-expected
sha256sum -c SHA256SUMS
```

For optional regeneration, install `requirements-proposal.txt` into a
local environment, then use an output directory outside the repository:

```sh
python3 build.py --work /scratch/hn-polygon-spectra
python3 verify.py --compare-data /scratch/hn-polygon-spectra --check-expected
python3 controls.py --proposal /scratch/hn-polygon-spectra
```

Each generated `n.json` contains all canonical chord addresses, exact
polynomial coordinates, and every distance class with its squared
normalization, full edge list, exact chromatic number and full colour
word. Thus any classified unit-distance graph is reproducible with
coordinates `p(zeta_n)/sqrt(delta(zeta_n))`, taking the positive square
root in the physical complex embedding. No numerical choice of an
algebraic root is needed. The generator also reconstructs the committed
certificate byte for byte. Bulk case files and logs stay outside Git.

`expected.json` records the complete per-order counts, edge ranges, and
hashes of full edge incidences and classification tables. The largest
edge count in the family is **1,740**, on a 451-point cloud at `n=30`.
The following table concerns full clouds, including their origins.

| Polygon order | Points | Distance scales | Chi = 2 | Chi = 3 |
| ---: | ---: | ---: | ---: | ---: |
| 2 | 3 | 2 | 2 | 0 |
| 3 | 7 | 3 | 1 | 2 |
| 4 | 9 | 5 | 5 | 0 |
| 5 | 21 | 11 | 6 | 5 |
| 6 | 19 | 8 | 2 | 6 |
| 7 | 43 | 27 | 18 | 9 |
| 8 | 33 | 20 | 20 | 0 |
| 9 | 73 | 45 | 28 | 17 |
| 10 | 51 | 34 | 25 | 9 |
| 11 | 111 | 95 | 75 | 20 |
| 12 | 73 | 37 | 18 | 19 |
| 13 | 157 | 153 | 126 | 27 |
| 14 | 99 | 78 | 60 | 18 |
| 15 | 211 | 197 | 150 | 47 |
| 16 | 129 | 110 | 110 | 0 |
| 17 | 273 | 332 | 288 | 44 |
| 18 | 163 | 113 | 62 | 51 |
| 19 | 343 | 459 | 405 | 54 |
| 20 | 201 | 198 | 179 | 19 |
| 21 | 421 | 543 | 451 | 92 |
| 22 | 243 | 262 | 217 | 45 |
| 23 | 507 | 803 | 726 | 77 |
| 24 | 289 | 257 | 194 | 63 |
| 26 | 339 | 419 | 356 | 63 |
| 28 | 393 | 517 | 477 | 40 |
| 30 | 451 | 424 | 282 | 142 |

## 5. Validation, context and limitations

The normal and optimized interpreter runs give identical reports and
both independently reconstruct all geometry and check all positive and
negative chromatic witnesses. `controls.py` checks 256 Möbius identities,
666 Ramanujan projector entries, chord cardinalities through order 36
(including excluded budget boundaries), six cycle parity fixtures, and
rejects 19 deliberately corrupted certificates or proposal records.
`validation.json` records timings and byte-for-byte regeneration checks.
These are author-side independent implementations, not external peer
review or formal verification.

Regular-polygon differences and cyclotomic arithmetic are classical;
no priority claim is made for the construction or the proof techniques.
For source context, [Radchenko's paper](https://arxiv.org/abs/1807.03726)
studies unit-distance graphs of finitely generated additive subgroups.
Our result is the explicit complete scale classification above, not a
chromatic theorem about an entire cyclotomic field. Rescaling a cloud
can create unit directions other than its original unit directions.

The campaign's [three-concentric-orbit result](../hadwiger_nelson_three_concentric_orbits/README.md)
already excludes a different continuous family with at most three
rings. This construction instead prescribes all chord radii, reaches
15 rings, and classifies every scale by exact distances; it does not
extend that result by adding arbitrary radii or phases. The earlier
[421-point heptagon difference graph](../hadwiger_nelson_heptagon_difference_lifts/README.md)
uses a 21-point nonregular Haugland motif, not the roots of a regular
21-gon used here. Neither earlier result is a proof premise.

The [correlated Moser cube](../hadwiger_nelson_correlated_moser_cube/README.md)
is a completed separate family. The teammate's
[509-vertex neutral mutation](../hadwiger_nelson_neutral_mutation_candidate/README.md)
remains separate construction evidence. This gate uses neither family
nor a previously five-chromatic host. The standing target remains a
strict improvement on the graph in [Parts's primary paper](https://arxiv.org/abs/2010.12665).
No such graph is established here, and no subsequent family is started.
