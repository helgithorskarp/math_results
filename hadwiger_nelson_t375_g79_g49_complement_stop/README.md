# A fixed G79–G49 complement does not activate T375

The single complement constructed below has **126 points and 346 complete
unit edges**. It shares T375's marked triangle of side `1/sqrt(3)`, but its
pins need not be monochromatic. The full collision-merged union with T375 has
**466 points and 1,966 complete unit edges**, and the published literal
four-colour word gives its three pins colours **0,0,3**.

This is a negative result for one exact physical construction. It is not a
five-chromatic graph, a sub-509 record improvement, or an exclusion of all
T375 complements. The architecture is retired without another anchor pair,
triangle, frame, phase or decoder count.

## Why this was a concrete complement opportunity

[Exoo and Ismailescu](https://arxiv.org/abs/1805.00157v1) supply G79, which
forces at least one distance-`sqrt(11/3)` pair to be monochromatic, and G49,
which turns equality of its marked pair into a monochromatic small triangle
somewhere among its 18 such triangles. The committed T375 support forbids
its marked small triangle monochromatic.

These implications are existential and do **not** force the particular pair
and triangle chosen here. The test was whether the actual complete contacts
in one capped assembly suppress the alternatives. They do not: in the union
word the chosen G49 input pair has colours 1 and 2, while the receiving pins
have colours 0,0,3. No conditional source relation was promoted to ordinary
non-four-colourability.

## Frozen exact construction

Use the paper convention

```
[a,b,c,d] = ((a*sqrt(3)+b*sqrt(11))/36, (c+d*sqrt(33))/36).
```

Let `B` be the paper's ordered G40 table and `D` its ordered G49 table, both
hash-pinned in `DEPENDENCIES.json`. Coordinates below are complex plane points.
Define

```
r = (119 + 3*i*sqrt(247))/128,
G79 support = B union r*B,
P = [0,0,30,-6], Q = [0,0,30,6],
J(x,y) = (x, 2/3-y),
C = J(B union r*B union (P+D)).
```

Here `P,Q` are in `B`; `D[0]=0` and `P+D[1]=Q`. The multiplier `r` has unit
norm, and `|P-Q|=sqrt(11/3)`, so every intended source copy is an exact isometry.
The G49 vertices with zero-based indices **4,2,3**, in that order, map to
T375's marked coordinates

```
(0,1/3), (-sqrt(3)/6,-1/6), (sqrt(3)/6,-1/6).
```

The G79 and moved G49 copies overlap in exactly the two input endpoints.
Thus `|C|=79+49-2=126 <=136`. The declared union cap was
`375+126-3=498`, before any other overlap was known. The actual overlap with
T375 is 35 points, giving 466 points. The complement has 39 points outside
`Q(sqrt(3),sqrt(11))^2`, so it is not contained in the previously closed
native-lattice high-contact supports or native T375 D3 self-gluings.

Every unit edge is reconstructed. Beyond the edge sets inherited from T375
and the complete complement, there are **47 additional unit contacts** between
the private parts. These are included in the positive colouring certificate.

## Evidence and reproduction

The checker uses only Python's standard library and imports no producer or
sibling executable code. Run from the repository root:

```sh
python3 -B hadwiger_nelson_t375_g79_g49_complement_stop/verify.py --check-expected
python3 -O -B hadwiger_nelson_t375_g79_g49_complement_stop/verify.py --check-expected
python3 -B hadwiger_nelson_t375_g79_g49_complement_stop/controls.py
python3 -O -B hadwiger_nelson_t375_g79_g49_complement_stop/controls.py
```

Normal and optimized results agree. Optional `--export /tmp/hn-t375-complement`
exports every exact coordinate and every unit edge for both supports.
Coordinates are integral coefficients in the basis
`1,sqrt(3),sqrt(11),sqrt(33),sqrt(247),sqrt(741),sqrt(2717),sqrt(8151)`,
divided by **4608**. `certificate.json` gives the colour words, embedding map,
all 47 extra contacts, point/edge hashes and the complete outside-field index
list. All 108,345 unordered union pairs are checked directly.

The optional producer requires `python-sat==1.8.dev24` (CaDiCaL195 backend):

```sh
python3 -B hadwiger_nelson_t375_g79_g49_complement_stop/produce.py --out /tmp/hn-t375-certificate.json
cmp /tmp/hn-t375-certificate.json hadwiger_nelson_t375_g79_g49_complement_stop/certificate.json
```

SAT supplies positive words only. The final certificate uses no negative
solver verdict, floating predicate, restricted colouring palette or omitted
unit edge. See [PROOF.md](PROOF.md) and [PROVENANCE.md](PROVENANCE.md).
This is author-side exact evidence, not independent peer review.

The supported unrestricted record remains [Parts's 509 points and 2,442
edges](https://arxiv.org/abs/2010.12665), also stated by
[Haugland v4](https://arxiv.org/html/2608.04542v4). This fixed four-colourable
union does not change it.
