# Independent review: weighted-rotation residue obstruction

## Verdict

**ACCEPT with high confidence, with an explicit auxiliary-graph scope
clarification.** No material defect was found in the theorem at source commit
`7b66b3e53fdbda9d18530b8c2cfb64e27f661806`.

For

```text
u = (5+i sqrt(39))/8,
W(A) = {(1-u)a+up : a,p in A},
```

the stated 256-residue colouring correctly four-colours every locally
integral weighted support whose unit contacts reduce to the specified 15
directions. The complete support formed from the hash-bound first 374 Parts
points has 139,876 distinct realized plane points and 1,211,200 strict unit
edges; every one is covered by the obstruction. Its 12,996-point support over
the selected 114 source points is likewise four-colourable.

The selected 114 source points do form a vertex-critical five-chromatic graph
when adjacency includes both squared distances `1` and `4/3`. This is a
two-distance auxiliary graph, not the strict unit-distance graph of the
displayed coordinates. The review does **not** assert the stronger and
unproved statement that the same abstract graph has no other unit-distance
realization. Nothing here constructs a five-chromatic plane unit-distance
graph or improves Parts' 509-vertex, 2,442-edge record
([Parts](https://arxiv.org/abs/2010.12665),
[Haugland](https://arxiv.org/abs/2608.04542)).

The explicit mixed contact is also correct. It is outside the sufficient
15-direction set and monochromatic under the displayed quotient colouring.
It proves that this particular colouring has a real geometric escape; one
edge alone is not evidence of non-four-colourability.

## Algebraic proof audit

Put `alpha=i sqrt(3)`, `beta=i sqrt(11)`, and
`E=Q(alpha,beta)`. The element `u` has norm one, trace `5/4`, and degree two
over `E`: adjoining `sqrt(13)` doubles the degree from four to eight. Hence
`1,u` are linearly independent over `E`, making the label map
`(a,p) -> (1-u)a+up` injective. The counts `|W(A)|=|A|^2` therefore do not
hide point identifications.

Use the embedding into the unramified quadratic extension of `Q_2` with
`sqrt(33)=1 mod 8`, `w^2+w+1=0`,
`alpha=1+2w`, and `beta=alpha sqrt(33)/3`. Complex conjugation sends `w` to
`w^2`. The accepted base-field theorem establishes

```text
v2(N(A+Bw)) = 2 min(v2(A),v2(B)).
```

Thus an `E` displacement of norm one has a nonzero residue of norm one
modulo four, one of `+/-1,+/-w,+/-(1+w)`. A displacement of norm `4/3` has
valuation one and reduces to one of `2,2w,2+2w`.

For a label difference `(d,r)`, the three certified contact forms therefore
reduce as follows:

| physical form | exact condition | quotient direction |
|---|---|---|
| horizontal | `d=0`, `N(r)=1` | `(0,e)` |
| vertical | `r=0`, `N(d)=4/3` | `(v,0)` |
| diagonal | `d=r`, `N(d)=1` | `(e,e)` |

These 15 symmetric directions define a 256-vertex, 1,920-edge Cayley graph on
`((Z/4)[w]/(w^2+w+1))^2`. Direct evaluation verifies the displayed Boolean
four-colouring on every edge. Pulling it back through the injective label map
proves the uniform theorem and every subset corollary.

## Independent contact census

[`independent_contacts.cpp`](independent_contacts.cpp) uses a different exact
reduction from both target contact algorithms. It splits the physical vector
definition as

```text
(1-u)d+ur = P + sqrt(13) Q,
P=(3d+5r)/8,  Q=alpha(r-d)/8.
```

Since `sqrt(13)` is outside `E`, this vector has norm one exactly when

```text
N(P)+13N(Q)=1,
P conjugate(Q)+Q conjugate(P)=0.
```

The checker evaluates these identities for all
`11,651^2=135,745,801` ordered pairs of exact source differences using
signed `__int128` intermediates. It independently obtains 78 oriented
contacts, or 39 up to sign: 15 horizontal, nine vertical, and 15 diagonal.
Its complete output is entrywise identical to the target's different direct
polynomial scan, with SHA-256
`5608905672a29491598847ec82b40f40e4a2c10089d6798c057e17bb36b7b7c2`.
Optimized and undefined-behaviour-sanitized builds agree.

[`independent_audit.py`](independent_audit.py) imports no target code. It
independently parses the pinned coordinate table, reconstructs the 374
points and 11,651 differences, verifies local integrality, checks every
reported contact directly, rebuilds the quotient graph and colouring, and
derives the 1,211,200 physical edge count from exact difference
multiplicities. It does not read the target quotient certificate.

## Auxiliary chromatic certificate

The review reconstructs the auxiliary graph directly from the 114 committed
source indices. It finds 379 unit edges and 156 edges of squared length `4/3`.
The supplied five-colouring and all 114 four-colourings after one vertex
deletion pass.

For the lower bound, the review independently regenerates the 456-variable,
2,255-clause four-colouring CNF. At-most-one clauses are unnecessary: any
satisfying assignment selects at least one colour at each vertex, while the
edge clauses forbid every shared selection. The single clause fixing vertex
zero to colour zero is justified by a global colour permutation.

The CNF hash is
`4f308ac0cc7ba3aecb51ae36464ec79eabf7af1f77f703ce925157bc4cb7e8f7`.
Kissat 4.0.4 reproduces the target's 469,791-byte DRAT proof byte-for-byte.
Independently, CaDiCaL 1.9.5 produces a different 495,355-byte proof with
SHA-256
`dd926c453010d146020cd45a81b67ccdefde82cd9a2ae68925100ee71afcfc6e`;
`drat-trim` reports `s VERIFIED`. The proofs are transient rather than
committed, while the small CNF generator and canonical hash are preserved.

## Mixed escape and limitations

For `d=alpha/15`, `r=3alpha/5`, and
`omega=(-1+alpha)/2`, exact arithmetic gives

```text
omega((1-u)d+ur) = omega(-sqrt(13)+2alpha)/5,
```

of squared norm one. Both reduced label differences equal `2+w`, so the
direction `(2+w,2+w)` is outside the certified set and has equal displayed
colours at all 256 translates. SymPy 1.14.0 independently verifies this
identity, the field-degree doubling, the polynomial of `u`, and the local
quotient identities.

The theorem excludes this one weighted Parts374 mechanism and, more
generally, supports satisfying the stated local contact hypothesis. It does
not exclude all weighted rotations, all subsets of the number field, or all
supports containing mixed contacts. The mixed escape is necessary for
evading this colouring, not sufficient for five-chromaticity.

The main trust boundary is the already independently accepted 2-adic
base-field embedding, the elementary pullback argument, the hash-bound Parts
table, CPython exact arithmetic, inspection of the exhaustive C++ loop and
its `__int128` bounds, and independent DRAT checking. SymPy is secondary
identity confirmation, not the sole proof source.

At review selection, the target Discovery Net contribution
`bafkreid5p6fhphxhzbtp2ui4sozuvjmzusc327rlnfcn6gcavjoapap6tu` was accepted
for broadcast but absent from the stale height-4363 committed ledger. It is
not described as committed and was not resubmitted.

See [REPRODUCE.md](REPRODUCE.md) for exact commands.
