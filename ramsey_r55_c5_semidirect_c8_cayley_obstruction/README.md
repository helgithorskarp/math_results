# A complete obstruction for a nonabelian Cayley core on 40 vertices

Every undirected Cayley graph on

\[
G=\langle a,b\mid a^5=b^8=1,\;bab^{-1}=a^2\rangle
  \cong C_5\rtimes C_8
\]

contains a clique or independent set of size five. Consequently, no graph
obtained by adjoining three vertices to such a core, with **all 123 new
edges independently arbitrary**, is a Ramsey (5,5) graph on 43 vertices.
This decides the entire declared construction family, including complements
and relabelings. It does not improve a bound on R(5,5).

The certificate is a 28,220-byte list of 1,918 literal five-vertex subsets.
An independent checker verifies that this list supplies a monochromatic
witness for every one of the 1,048,576 connection sets. No solver, graph
catalogue, degree assumption, or external classification is used.

## Exact family and proof

Write each group element as `(i,j)=a^i b^j`, with `0 <= i < 5` and
`0 <= j < 8`, and give it vertex label `i+5*j`. The multiplication is

\[
(i,j)(k,l)=(i+2^j k\pmod 5,\ j+l\pmod 8).
\]

Multiplication by 2 has order four modulo 5, so it defines an action of
`C8` on `C5`. This gives the stated group of order 40. Its identity is 0.
Choose any inverse-closed set `S` of nonidentity elements, and color the
edge `{u,v}` red exactly when `u^-1 v` belongs to `S`; color all other
edges blue. Empty, full, and disconnected connection sets are included.

The 39 nonidentity elements partition into 19 inverse pairs and the
singleton `{b^4}`. Thus there are exactly 20 independent connection bits.
The checker reconstructs this partition from explicit permutations, using
the left translations

\[
A(i,j)=(i+1,j),\qquad B(i,j)=(2i,j+1).
\]

It checks the relations, forty distinct normal forms, all 1,600 products,
the inverse partition, and symmetry of the resulting physical edge map.
It does not import the producer's multiplication or inverse routines.

Number the inverse classes in lexicographic order. For class `k`, define
an integer truth column `T_k` whose bit at position `m`, for
`0 <= m < 2^20`, is bit `k` of `m`. Let `F = 2^(2^20)-1`. For each literal
five-set `Q` in the certificate, the checker computes

\[
R_Q=\bigwedge_{\{u,v\}\subset Q} T_{c(u,v)},\qquad
B_Q=\bigwedge_{\{u,v\}\subset Q}(F\mathbin{\mathrm{xor}}T_{c(u,v)}),
\]

where `c(u,v)` is the inverse class of `u^-1 v`. These are bitwise ANDs
over **all ten physical pairs**, including any repeated class variables.
Bit `m` of `R_Q` (respectively `B_Q`) is one exactly when `Q` is red
(respectively blue) for connection mask `m`. The checked identity is

\[
\bigvee_{Q\text{ in certificate}}(R_Q\mathbin{\mathrm{or}}B_Q)=F.
\]

It follows that every connection mask has a monochromatic five-set.
Only this identity and the literal group/edge interpretation enter the
computer-assisted proof. The witness list need not enumerate all five-sets,
or representatives of every orbit, for the argument to be valid.

Finally, a monochromatic five-set in an induced core survives the addition
of vertices. On a fixed set of 40 core labels and three further labels,
the 20 connection bits and `3*40 + choose(3,2) = 123` attachment bits
describe `2^143` distinct labeled graphs, all excluded. No automorphism of
the final 43-vertex graph is required. More generally, any larger graph
containing such an induced core is excluded. This theorem concerns this
specified group; it does not classify all groups of order 40 or all regular
40-vertex graphs.

## Reproduction and trust boundary

Requirements: Python 3.10 or later, standard library only. Validated with
CPython 3.11.2. From this directory:

```sh
python3 -B check.py certificate.json
python3 -B reproduce.py
python3 -O -B reproduce.py
```

The checker prints `VERIFIED_C5_SEMIDIRECT_C8_CAYLEY_OBSTRUCTION`,
`connection_sets_covered: 1048576`, `physical_five_sets: 1918`, and
`ramsey_40_cores: 0`. Full replay prints `REPRODUCED_CAYLEY40_OBSTRUCTION`.
The certificate SHA-256 is

```text
faaed6d42fc2ff428389298d67f445586bd620f91108fdc39c07f01c11862dc6
```

`reproduce.py` checks the file manifest, regenerates the certificate byte
for byte, compares the independent check with `expected.json`, and runs
the controls and novelty check. The producer enumerates the 82,251
five-sets through the identity, obtains 13,038 distinct edge supports and
3,356 inclusion-minimal supports, then branches on the connection bits.
The original search visited 33,919 tree nodes and 16,960 terminal
contradictions. Only their 1,918 distinct literal five-sets are retained
in the public certificate. The original full tree remains a private
diagnostic; neither it nor its search statistics is needed by the checker.

The controls compare all 1,600 group products and 40 inverses between
the permutation and formula models; verify the literal interpretation of
all 20,971,520 truth-column bits; inspect sixteen physical graph fixtures;
and reject eight malformed or insufficient certificates. They do not
replace the universal cover check. Both normal and optimized Python runs
use explicit checks rather than removable assertions.

The trust boundary is the displayed finite argument, these unformalized
Python programs, exact integer semantics, and the execution environment.
Producer and checker are separate implementations by the same researcher;
this is not a claim of external review or proof-assistant formalization.
There is no imported Hill–Love, catalogue-completeness, SAT-proof, or
Ramsey local-profile premise, and no required external data.

## Early comparison with prior construction representatives

Every graph in this family contains a regular induced 40-vertex subgraph.
`novelty.py` tests all `choose(43,3) = 12,341` deletion triples in each of
21 saved literal comparison graphs and finds zero regular cores in every
case. This separates the entire new family from those representatives
under arbitrary relabeling and color complementation: both operations
preserve existence of a regular induced 40-vertex subgraph.

The fixtures include the cyclic seed, the previously known two- and
seven-defect representatives, the C3 score-123 construction, its saved
phase-trade winner, and sixteen C2 restart winners. Some representatives
can be isomorphic to one another. This is a check against these saved
graphs, not a classification of all vertices in historical search basins
and not a claim of historical priority for this group obstruction.

`novelty_fixtures.json` contains every literal graph as 903 edge bits, with
bit `k` corresponding to pair `k` in Python's
`combinations(range(43),2)`, starting at the least significant bit.
Source hashes and the original cyclic definitions are provenance only;
no private input is needed. `novelty.py` independently recounts each
fixture's monochromatic five-sets and checks its canonical edge-list hash.
For example, to inspect the previously known seven-defect graph:

```sh
python3 -B novelty.py
python3 -B novelty.py --edges known_secondary_q7
```

The edge-list output starts with `43 m`, followed by its `m` red pairs;
all unlisted pairs are blue. The comparison fixtures are existing
non-Ramsey graphs, not newly claimed low-defect constructions. Their
novelty check is separate from the Cayley-family obstruction proof.
