# Excluding eight moving 3-cycles

**Theorem.** A graph on 43 vertices with neither a clique nor an independent
set of order five has no automorphism of cycle type `1^19 3^8`.
Together with the [seven-cycle exclusion](../ramsey_r55_order3_seven_cycle_obstruction)
and its sparse-motion predecessor, every automorphism of order three has
at least **nine moving 3-cycles**, and hence at most 16 fixed vertices.

This is a computer-assisted structural exclusion. It supplies no
43-vertex witness or improved Ramsey lower bound. Types with nine through
fourteen moving 3-cycles are not excluded here.

## 1. A local deficit bound

Color edges red and nonedges blue. The established theorem `R(4,5)=25`
implies that every vertex has between 18 and 24 neighbors in each color:
a color neighborhood has no same-color `K_4` and no opposite-color `K_5`,
so its size is at most 24.

Suppose there are eight moving 3-cycles and 19 fixed vertices. Each moving
cycle is a monochromatic triangle, since rotation is transitive on its
three unordered pairs. Fix a triangle `C_i` of internal color `c_i`.
Write `a_i` for its number of fixed neighbors in color `c_i`, and
`w_ij in {0,1,2,3}` for the number of color-`c_i` neighbors in `C_j` of
each vertex of `C_i`. The latter number is uniform by invariance.
Let `m_i` count the indices `j` for which `w_ij=3`.

The common color-`c_i` neighborhood of `C_i` has at most four vertices.
Any edge of that color inside it would complete a `K_5`; if it had five
vertices, they would therefore form an opposite-color `K_5`. Its fixed
part has size `a_i`; each complete cross block contributes all three
vertices of another moving cycle. Consequently

```text
a_i + 3m_i <= 4,
2 + a_i + sum_(j != i) w_ij >= 18.                    (1)
```

Define

```text
delta(w) = 2 - w + 3*[w=3],
delta(0),delta(1),delta(2),delta(3) = 2,1,0,2.
```

Eliminating `a_i` in (1), with seven other moving cycles, gives

```text
sum_(j != i) delta(w_ij) <= 2.                         (2)
```

This is the required replacement for the exact equality in the earlier
seven-cycle proof. In particular, complete blocks have deficit two;
they must not be treated as negative deficits. The new argument does
**not** assume that every cross block is a perfect matching in one color.

An exact audit of all `4^7=16384` cross-weight vectors and all 20 possible
fixed counts finds 52 feasible pairs `(a_i,(w_ij)_j)`. Existence of a
feasible `a_i` is equivalent to (2). More explicitly: the all-two vector
allows `a_i=2,3,4`; one weight one allows `a_i=3,4`; two weights one or
one weight zero require `a_i=4`; one weight three requires `a_i=1`.
These cases number `3+14+21+7+7=52`.

## 2. Exhaustive internal colors and normalizations

Label the moving vertices `3i+s`, for `0<=i<8` and `s in Z/3Z`, with
rotation `s -> s+1`. Vertices 24 through 42 are fixed.

Global color reversal lets the number `r` of internally red triangles
lie in `{0,1,2,3,4}`. Permuting the eight moving cycles puts those red
triangles first. These operations preserve both forbidden-set conditions.
Thus five cases suffice; this does not assume all triangles have one color.

For moving cycles `i<j`, write three red edge bits `b_ij,0..2`, where the
edge from `3i+s` to `3j+t` is red precisely when `b_ij,t-s` is true.
Independently shifting the origins in cycles 1 through 7 cyclically
rotates each corresponding anchor word `b_0j`. Every binary word of
length three has a rotation in

```text
000, 100, 110, 111.
```

Therefore impose `b_0j,0 >= b_0j,1 >= b_0j,2`. These shifts commute with
rotation and leave every fixed-to-moving incidence unchanged. Constant
words have nonunique choices; selecting any one suffices, with no
uniqueness claim or division by an orbit size.

Each fixed vertex has an eight-bit red incidence signature, one bit for
each moving triangle. Arbitrarily permuting fixed vertices puts these
signatures in nondecreasing lexicographic order. It preserves the anchor
normalization. All normalized invariant graphs retain a representative
among the five formulas. `audit.py` checks these relabelings on explicit
43-vertex invariant colorings for all 256 internal color profiles, including
constant anchor words and repeated fixed signatures.

## 3. The complete formulas

True means red. The 407 primary Boolean variables are ordered as follows:

1. 84 cross-edge bits: lexicographic pairs of moving cycles, then differences
   0,1,2.
2. 171 fixed-fixed edge bits: lexicographic pairs in vertices 24 through 42.
3. 152 fixed-to-moving incidence bits: fixed vertex first, then moving cycle.

The eight internal triangle colors are constants determined by `r`.
These represent every edge orbit under the specified permutation.

Every one of the `binom(43,5)=962598` five-sets contributes clauses saying
its ten pairs are not all red and not all blue. Constant true literals
make a clause redundant; constant false literals are removed. Repeated
literals and duplicate clauses are removed. No five-set is skipped on
heuristic or catalog grounds.

For each moving-cycle pair and each internal color that occurs at an
endpoint, three auxiliary gates record

```text
u = [delta(w)>=1],  v = [delta(w)>=2],  z = [w=3].
```

Each gate is defined by all eight truth-table implications on the three
cross-edge bits. An implication for input valuation `x` consists of the
three literals falsified by `x` together with the asserted output literal.
Exactly one input valuation occurs, so these eight clauses force the
correct output and admit it. Endpoints with the same internal color share
these gates. Endpoints with opposite colors use separate gates.

For every triangle the fourteen `u,v` tokens have sum equal to its total
deficit. All negative three-token clauses impose the at-most-two condition
(2). There are also two counters expressing (1):

- At most four true literals among its 19 fixed neighbors in its own color
  together with **three copies** of each of the seven complete-block gates.
- At most 24 false literals among its 19 fixed own-color incidences and
  21 moving cross-edge bits in its own color. Equivalently at least 16
  of these 40 incidences have the own color; adding the two internal
  neighbors gives degree at least 18.

Repeated gate literals in the first counter correctly have weight three.
Negative primary literals are used for blue incidences. These counters
add necessary constraints only; no unproved bound on a fixed vertex's
degree, local deficiency, or exceptional neighborhood is imposed.

### Prefix counters

For an at-most-`k` condition on literals `x_1,...,x_n`, auxiliary `S_ij`
exists for `1<=j<=min(i,k+1)`. It means that the first `i` literals have
at least `j` true occurrences. The clauses are

```text
x_i -> S_i1,
S_(i-1),j -> S_ij                      (where the predecessor exists),
(x_i AND S_(i-1),(j-1)) -> S_ij         (j>1, predecessor exists),
NOT S_n,(k+1)                         (if that variable exists).
```

Induction on `i` shows that any `k+1` true occurrences force the forbidden
last variable, proving soundness. When at most `k` occurrences are true,
setting every `S_ij` to its actual prefix threshold satisfies every clause,
proving completeness of the auxiliary extension. This proof permits signed
and repeated literals. The audit extracts the production counter function
and exhausts 1,734 assignments on small signed and repeated-input examples,
checking both a satisfying threshold extension and propagation of overflow.

### Lexicographic clauses

To impose `A<=B` on two fixed signatures, for each coordinate `q` and each
binary common prefix of length `q`, a clause excludes that common prefix
together with `A_q=1,B_q=0`. If the signatures first differ at `q`, exactly
the matching common-prefix clause tests the required order; clauses for
other prefixes or later coordinates are satisfied. Equal signatures
satisfy every clause. Thus the clauses impose precisely the stated order.
An exhaustive four-coordinate truth table separately checks this schema.

## 4. Independently reconstructed formulas and finite certificates

`generate.py` uses modular differences to build the formulas.
`check_formula.cpp` instead forms all 903 actual unordered vertex pairs,
joins pairs under the permutation with a disjoint-set structure, and obtains
415 edge orbits. Eight are constant internal triangles; 407 are primary
variables. It reconstructs every Ramsey, gate, counter and normalization
clause and compares the complete canonical DIMACS stream byte-for-byte.
This checks full clauses, not merely their number or a selected UNSAT core.

| internally red cycles | variables | full clauses | committed core clauses | RUP additions |
|---:|---:|---:|---:|---:|
| 0 | 7,611 | 585,876 | 460 | 395 |
| 1 | 7,632 | 589,383 | 1,406 | 2,057 |
| 2 | 7,647 | 591,888 | 270 | 302 |
| 3 | 7,656 | 593,391 | 465 | 1,216 |
| 4 | 7,659 | 593,892 | 360 | 118 |

The five committed cores total 97,473 bytes. Their addition-only RUP
certificates total 171,954 bytes and 4,088 additions. The Python certificate
checker first verifies that **every core clause occurs in the full audited
formula**. It then negates each proposed proof clause and applies elementary
unit propagation to the core and previously justified clauses. A conflict
proves the clause is entailed. Every proof ends with a verified empty clause,
so every core, and hence every full formula, is unsatisfiable.

No deletion or RAT reasoning is used in the published certificates.
Keeping all previously justified clauses is sound for RUP. The verifier
rejects incomplete, out-of-range and invalid-addition examples; a separate
brute-force audit checks propagation soundness on 2,560 small cases.
The stored cores and traces also pass external `drat-trim -U` replay.
The actual orbit checker passes optimized and ASan/UBSan builds.

All five internal color cases are thus impossible. By the completeness of
the graph-to-formula reduction and normalizations, cycle type `1^19 3^8`
is impossible, proving the theorem.

## 5. Why the fixed vertices matter

The moving-vertex constraints alone are insufficient. The compact fixture
`moving24.edges` has eight rotating triples, four internally red and four
internally blue, and satisfies the deficit bound at every triangle. An
independent literal check of all 42,504 five-sets finds no monochromatic
one. It has 24 vertices and 138 red edges.

This is a positive test of the relaxed moving-vertex conditions, not a
43-vertex target candidate. The full exclusion proves that it cannot be
extended by 19 fixed vertices while retaining this automorphism and the
Ramsey property. In particular, the preceding matching-cover obstruction
cannot simply be reused at eight cycles.

## 6. Scope and trust

The external graph-theoretic input is McKay and Radziszowski,
[*R(4,5)=25*](https://users.cecs.anu.edu.au/~bdm/papers/r45.pdf).
The new eight-cycle exclusion does not depend on the order-five theorem,
the hard local-deficiency branch, or any Ramsey graph catalog.
The minimum-nine corollary additionally imports the previous exclusions
of one through seven moving cycles.

The reduction and counter/normalization arguments are ordinary unformalized
mathematics. The finite conclusion trusts the small Python and C++ checking
programs and their runtimes. The complete reconstruction and elementary
replay are separate checks by the same researcher, not an independent peer
review. Neither the discovering solver's UNSAT verdict nor an omitted
large proof is needed to reproduce the theorem.
