# A classified saturated neighborhood has no full extension

Let G be a hypothetical red-blue coloring on 43 vertices with no color K5,
invariant under eleven disjoint 3-cycles and ten fixed points. Suppose four
moving cycles are internally red, the other seven internally blue, and the
four red cycles have canonical Core194 word `100110110110110100`.

We prove that any fixed vertex e blue to all four red cycles is blue to at
most three blue cycles. No fixed-row order is needed for this theorem.

## 1. The maximal branch forces the local family

Write b for the number of blue moving cycles blue to e, and h for the red
neighbors of e among the other nine fixed vertices. Invariance makes each
fixed-to-moving incidence constant on its cycle. Therefore

```
d_red(e)=3(7-b)+h,       d_blue(e)=21+3b-h.
```

The inherited R(4,5)=25 result implies each degree lies between 18 and 24.
Since h<=9, b<=4. If b=4, h=9 and the degrees are 18 and 24. Thus H=N_blue(e)
is exactly the union of the four red and the four selected blue moving
cycles. It has no red K5, and a blue K4 in H would form a blue K5 with e.

Retain the red-cycle coordinates and relabel only the four selected blue
cycles as local cycles 4..7, preserving generator direction. This is valid
for every choice of four cycles, with no assumption that they were the
first four blue cycles in a previously normalized full graph. H has 84
cross-phase primary variables, with fixed internal colors and eighteen
core units. Enumeration of all red five-set and blue four-set prohibitions
gives the exact 11,584-clause local base. It has no degree constraint or
imported full normalizer.

## 2. Complete contact normalization

For blue cycle j define its twelve-bit word

```
W_j=(red(3i,3j+d) : i=0,1,2,3; d=0,1,2).
```

Rotating the coordinates of cycle j shifts each of the four three-bit
blocks by the same amount. Choose a shift minimizing W_j lexicographically
with 0<1. The four choices act on disjoint blue cycles, fix the entire red
core, preserve internal colors, and commute with the order-three action.
Afterwards permute the four blue cycles so their words are nondecreasing.
A tie admits any minimum phase or tied order; existence, not uniqueness,
is sufficient. Sorting does not change any individual contact word.
Consequently every local graph has at least one normalized representative.

For each blue column, exclude every nonminimal twelve-bit assignment by
its negated full-assignment clause. There are 2,720 such assignments per
column, hence 10,880 clauses. These exactly express phase minimality.

For each pair of consecutive columns A,B, use q_k for equality of the
first k bits, k=1,...,11, with q_0=true. Impose, for each position k,

```
q_k => (not A_k or B_k),
q_(k+1) <=> (q_k and (A_k=B_k))     when k<11.
```

The comparator admits A<=B and rejects a first differing pair 1,0. A
canonical graph extends to these auxiliaries by setting each q_k to the
actual prefix-equality value. Both directions of every definition are
included, with constants simplified. Three comparators give 33 variables
and 198 clauses. Gate truth tables and the canonical extension are checked
independently. There is no assumption about the original graph's auxiliary
values; this is a valid existential extension of every normalized graph.

## 3. Four canonical representatives cover all local graphs

The four 84-bit words in representatives.json each decode to a valid local
graph. For each word the file supplies a literal permutation p of the
24 vertices such that

```
red_representative(a,b) = red_seed(p(a),p(b)).
```

The checker verifies this equality for every physical pair, verifies
p commutes with the generator and preserves the red/blue cycle parts,
and independently checks all local forbidden sets and core bits. The seed
is the explicit preceding c194.edges graph. Thus all four words are
actual local models and belong to its equivariant isomorphism class.

Append the four clauses blocking exactly these full primary assignments
to the normalized base. The resulting 117-variable, 22,666-clause formula
has a fully replayed DRAT refutation. Therefore any normalized local graph
must equal one of those four primary words. Combined with Section 2, every
local graph transforms to one of them and hence to the seed. This is a
complete classification, not an inference from finding one witness.

For the labeled count, the blue-cycle group fixing all red vertices
pointwise has size 4!*3^4=1,944. The independent checker enumerates its
physical pullbacks for each of the four words, obtaining four disjoint
sets of exactly 1,944 words. All are models because the transformations
preserve the local hypotheses. Conversely Section 2 sends every local
model into those sets. There are exactly 7,776 labeled local models for
this fixed canonical red core. All are isomorphic to the red 13-regular
seed. The 7,776 sorted 21-digit hexadecimal words followed by newlines
have SHA256 `1dde3b1dbff2d04201427a7114b147a1560c12618037cedf5efdf57dd0be0748`.
The raw list is regenerated, not needed as an opaque proof premise.

## 4. A complete full-extension refutation transfers to the family

Fix the seed H on vertices 0..23. Vertices 24..32 form three additional
internally blue cycles. Vertex e=33 and vertices 34..42 are fixed. Set
e-H blue and every e-outside-H edge red, including all nine fixed edges.
This exactly matches Section 1. All other edge orbits are unknown. There
are 216 primary variables, no auxiliaries, and 131,652 distinct simplified
clauses forbidding every monochromatic five-set on all 43 vertices.
There are no degree bounds, ordering constraints, symmetry cuts or other
full-normalization hypotheses. Thus every full extension in this fixed
neighborhood family is a model of this formula, simply by its edge colors.

Suppose a full graph in the maximal branch existed. Its H normalizes to
one of the four representatives and then to the seed by Section 3. Each
coordinate transformation commutes with the generator and preserves the
cycle-color parts. Extend it by the identity on the three additional
moving cycles and all ten fixed vertices. The full graph remains invariant;
e is still blue to H and red to the outside. No other fixed incidence or
normalizer can obstruct this relabeling, because none is imposed. This
would produce a model of the 216-variable full formula.

That formula has a complete DRAT refutation, replayed twice after fresh
reconstruction. Hence the hypothesized full graph cannot exist. Combining
this with b<=4 proves b<=3. Both the local classifier and full extension
are required: a refutation of one fixed-neighborhood formula alone would
not establish this family-wide conclusion.

## 5. Scope, checks and remaining work

This closes the Core194 maximal attachment branch, not all full extensions
of Core194. Together with the earlier maximal-branch results, all seventeen
remaining full-core classes have b<=3 for their first normalized empty
fixed vertex. Their complete extensions remain unresolved. The new theorem
applies to any empty fixed vertex in the canonical Core194 scope, because
this proof never uses a fixed-row ordering.

The independent formula auditor builds variables by physical pair orbits,
then reconstructs clique clauses by possible-color clique recursion, as
opposed to the producer's phase coordinates and exhaustive subset loop.
It compares every clause, header and EOF. Transformation equality is
checked directly on pairs; clique validity is checked directly on vertex
subsets. Production controls run under normal and optimized Python.
Fresh verification reconstructs all input formulas and representative
information and replays both original proofs again. Full DRAT mode is
used; both traces happen to have zero RAT core lemmas.

The seed is independently accepted, but its proof of existence is also
checked literally here. The finite classification and full extension
use no previous solver verdict. The degree theorem, canonical core cover
and prior boundary are imported at the scopes in README. The ordinary
normalization and transfer proof, exact code/interpreter/hardware, SHA256
and DRAT checker remain trust boundaries. Neither these internal checks
nor source publication are independent peer review or formalization.
