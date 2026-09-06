# A certified obstruction for binary adjacency rank at most six

Every simple graph of binary adjacency rank at most6 is9-colorable.
Consequently every such graph on at least37 vertices has an independent
five-set. **A Ramsey(5,5;43) graph must therefore have adjacency rank at
least8 over GF(2), in both colors.** Alternating binary matrices have
even rank, so this excludes all ranks below8.

This is a direct special case of the classical Godsil--Royle theorem,
not a new rank/chromatic-number bound. The contribution is a self-contained
rank-six proof, explicit finite certificate and executable obstruction
extractor with a separate physical verifier. No historical priority or
sharpness claim is made. No target graph or new Ramsey bound is obtained.

The excluded complete global family comprises every labeled43-vertex
graph with binary adjacency rank<=6 in either color. There is no degree
profile, connectivity, catalog, chosen neighborhood, fixed core or graph
automorphism assumption. In particular, the algebraic coordinates impose
no symmetry on the input graph. This is **not** real matrix rank,
incidence-matrix rank, rank-width or the rank of a cross-cut matrix.

## 1. Alternating-form factorization of the entire graph

Let A be a simple graph's adjacency matrix over GF(2). It is symmetric
with zero diagonal, so x^T A x=0 for every x. If a nonzero residual R
remains, choose p,q with R_pq=1 and write u=R e_p, v=R e_q. Set

    R_new = R + u v^T + v u^T.                         (1)

The p and q rows/columns become zero. More precisely, the span of e_p,e_q
is a nondegenerate hyperbolic plane for R. Replacing every other e_i by
e_i+R_iq e_p+R_ip e_q is an invertible basis change which makes this
plane orthogonal to the remaining basis. Its residual block is exactly
the corresponding block of (1). Thus rank(R_new)=rank(R)-2.

Iteration terminates with an exact decomposition

    A = sum_{j=0}^{r-1} (u_j v_j^T + v_j u_j^T),
    rank_2(A)=2r.                                     (2)

For r<=3, assign vertex i the six-bit coordinate with
x_j=(u_j)_i and y_j=(v_j)_i, padding unused coordinates with zero.
Define

    B((x,y),(x',y')) = sum_{j=0}^2 (x_j y'_j+y_j x'_j) mod2.

Equation(2) says A_ik=B(c_i,c_k) for every physical pair. Coordinate
images may coincide or be zero; none is deleted or assumed injective.
Equal images are nonadjacent because B(c,c)=0, and zero images are
orthogonal to all images. Hence a proper coloring of all64 coordinates
pulls back to a proper coloring of the original graph, even in these cases.

## 2. Nine independent coordinate classes

Use F8=F2[t]/(t^3+t+1). The cubic has no root in F2 and is therefore
irreducible. Its field trace is Tr(z)=z+z^2+z^4. The trace pairing is
nondegenerate: for z!=0, Tr(z*z^(-1))=Tr(1)=1. Relative to the field
basis(1,t,t^2), the trace-dual basis is(1,t^2,t), verified by its nine
pairings. Represent x in the first basis and y in the dual basis. Then
the six-bit form B becomes Tr(x*y'+x'*y).

For each s in F8, take L_s={(x,s*x): x in F8}; also take
L_infinity={(0,y): y in F8}. The eight finite slopes plus infinity
partition the63 nonzero vectors into nine sets of seven. Indeed a
nonzero vector with x!=0 has unique slope y/x, and those with x=0
belong to infinity. Every such set is isotropic: inside L_s the form
is Tr(s*x*x'+s*x'*x)=0, and the infinity case is immediate. Assign the
zero vector to one class. This gives a proper9-coloring.

[spread.py](spread.py) constructs these nine classes. Their complete
literal vector lists are in [spread.json](spread.json), using integer
bits0..2 for x and bits3..5 for trace-dual y. The separate verifier does
not use field arithmetic or this derivation: it checks that every integer
1..63 appears exactly once and directly evaluates all189 within-class
pairings under the displayed bit form. Field/basis metadata explains
provenance, but only the literal isotropic partition is needed by the
certificate kernel. Any such verified partition suffices.

Pulling the coloring back through(2), one of nine independent classes
has at least ceil(n/9) vertices. For n>=37, choose any five in that class.
This proves the complete family exclusion. Applying the same argument
to the complementary adjacency matrix proves the condition in both colors.
Neither the absence of five-cliques in the input graph nor R(4,5)=25
is needed to obtain the independent five-set in this low-rank family.

## 3. Executable graph obstruction and certificate boundary

Input is a JSON object with exactly `n` and `edges`. Vertices are0..n-1;
each pair is a two-integer list u<v; pairs must be lexicographically
sorted and distinct. These are the input's red edges; omitted pairs are
blue. [extract.py](extract.py) accepts `--color red` (default) or `blue`.
It computes the exact binary rank and full factorization. For rank<=6,
it emits coordinates, coloring, the largest class and an independent
five-set when available. The witness is a five-clique of the OTHER color
in the original input. Both orientations are directly verified.

For rank>6 the extractor returns `OUTSIDE_RANK_SIX` with an exact rank
factorization, but no coloring or obstruction verdict. This does not
mean the input is Ramsey, feasible, or free of five-sets. For small inputs
with largest class<5 the coloring remains certified but no five-set is
claimed. On n>=37 in the admitted family a five-set is guaranteed.

[verify.py](verify.py) imports neither extractor nor field producer. It
builds a dense binary matrix, independently computes rank by Gaussian
elimination, reconstructs every matrix entry from the factor pairs,
checks coordinate transport and proper coloring, and tests all ten pairs
of the reported witness in the physical input color. The universal rank
reduction is supplied by the proof above; a saved finite test is not a
replacement for that proof.

The fixture is an induced43-vertex subgraph of the universal symplectic
graph on coordinates1..43. It is **not** a Ramsey graph; it only exercises
the full-input obstruction decoder. Its decoded coordinates need not equal
the original coordinates, since the factorization chooses another basis.

## 4. Reproduction and bounded controls

With CPython3.11.2, standard library only, run in this directory:

```sh
set -o pipefail
python3 -B spread.py | cmp - spread.json
python3 -B extract.py fixture.json | cmp - fixture_certificate.json
python3 -B verify.py fixture.json fixture_certificate.json
python3 -B controls.py | cmp - validation.json
python3 -O -B spread.py | cmp - spread.json
python3 -O -B extract.py fixture.json | cmp - fixture_certificate.json
python3 -O -B controls.py | cmp - validation.json
sha256sum -c SHA256SUMS
```

Expected control status: VERIFIED_BINARY_RANK6_EXTRACTOR. Controls cover
every33,867 labeled graph of orders1..6, all having binary rank<=6.
For each graph, the dense rank, complete factorization, proper coloring
and any returned witness are checked. Their rank histogram is recorded
in [validation.json](validation.json). Complements occur in this exhaustive
enumeration; none are quotiented away.

There are128 further43-vertex checks: four coordinate dimensions times
16 deterministic seeds, in both input-color orientations. The recurrence
state=(5*state+1) mod64 produces43 coordinates; masks retain0,1,2 or3
hyperbolic coordinate pairs. These cover zero and repeated images as well
as the full-rank coordinate case. Every decoded five-set is physically
checked. K9 with34 additional isolated vertices exercises the rank8
`OUTSIDE_RANK_SIX` guard, not a rank8 search. Four rank/factor/coordinate/witness
certificate mutations, four spread mutations and eight malformed inputs
are rejected. Normal and optimized runs agree byte-for-byte.

The controls validate exact graph-level decoding, not enumerate all
43-vertex matrices or prove a novel rank bound. No random search, solver,
floating point, imported catalog or large generated certificate is used.
Trust remains in the displayed unformalized linear-algebra argument,
the finite partition checker, Python implementations/runtime and hardware.
No independent peer review or proof-assistant formalization is claimed.

## 5. Classical provenance and campaign scope

C. D. Godsil and G. F. Royle, *Chromatic Number and the 2-Rank of a Graph*,
Journal of Combinatorial Theory Series B81(2001),142--149,
DOI10.1006/jctb.2000.2003, proves the general bound
chi(G)<=2^r+1 when rank_2(A)=2r. See the
[author's institutional publication record](https://research-repository.uwa.edu.au/en/publications/chromatic-number-and-the-2-rank-of-a-graph/).
The publisher's indexed abstract confirms the exponent; its PDF was not
retrieved. The argument and finite certificate needed here are given
explicitly rather than relying on an inaccessible implementation.
No novelty claim is made for the theorem or its R55 numerical consequence.

This closes only the global rank<=6 family. Ranks8 and higher remain
unexamined here, and the lower bound8 is not claimed sharp for R55.
No cumulative degree profile or anchored split was removed by the
rank filter alone. No switching family or previously parked neighborhood-
gluing route was reopened. The symmetry of the auxiliary coordinate
space is not an automorphism constraint on the input graph.

The global vertex18 lemma now has independent acceptance at Discovery
Net3393, but it is not a premise. The newly accepted M215 partition at
3403 leaves all Boolean cells open; the M214 triangle/star-moment
survivor at3401 is still a pseudomodel. None of their data, formulas or
verdicts was imported into this proof. The teammate's C3 construction
lane remains separate. The present gate is complete, so the pass ends
before any larger rank, graph family or proof phase.
