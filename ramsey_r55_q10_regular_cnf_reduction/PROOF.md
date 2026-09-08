# Two literal frozen q10 formulas are unsatisfiable

The finite physical decision state here is the four final CNFs for
`bo1-q10-r10-c000000`, identified individually in `INPUTS.json`. Their historical
Kissat runs all ended UNKNOWN. This certificate closes the literal formulas
`d18-24.cnf` and `d24-18.cnf`. The other two files remain UNKNOWN.

The proof combines a new checked CNF implication with the complete regular
18/24 exclusion h3959. It does not interpret a partial DRAT stream as a proof,
require a solver, or derive a new regular-degree exclusion.

## 1. Physical interpretation and exhaustive five-set coverage

Vertices are 0 through 42. Each of the ten blocks `{4i,...,4i+3}`, for
`0 <= i < 10`, is a fixed red K4. The three vertices 40,41,42 form a fixed blue
K3. All other unordered pairs are free, in lexicographic pair order. They are
Boolean variables 2 through 841, with truth meaning red. Variable 1 is fixed
true by an actual unit clause. Thus every Boolean assignment to the free
variables decodes to one well-defined simple graph on 43 vertices.

For a physical five-set S and color c, a fixed pair of the opposite color
already prevents a monochromatic c copy. Otherwise the required clause is the
OR of the literals forbidding color c on all free pairs of S: negative
variables for red, positive for blue. Fixed same-color pairs contribute no
literal. Every five-set spans two of the fixed blocks, since the blocks have
sizes at most four. The union of the endpoints of its free pairs is therefore
all five vertices.

`audit.py` reads the actual clauses at zero-based positions [3241,1378507),
excluding the DIMACS header. It reconstructs their five vertices from their
free-variable supports, checks all ten physical pairs, signs and fixed colors,
checks exact free-pair equality, and rejects duplicates. It marks the pair
(S,c) using the colexicographic index `sum(binomial(v_i,i+1))` for sorted S.
A separate enumeration of all binomial(43,5) = 962,598 five-sets checks every
required color entry, including absence of irrelevant entries. The counts are:

| Required prohibition | Clauses |
| --- | ---: |
| Red K5 | 932,178 |
| Blue K5 | 443,088 |
| Total | 1,375,266 |

Consequently any model of the audited common base decodes to a good43.
No completeness or correctness assumption about additional symmetry, K4
contact, or connectivity clauses is required for this implication. All clauses
are checked for DIMACS syntax and variable range, but the extra clauses may
only further restrict the set of models.

## 2. Exact counter semantics from truth tables

For vertex v, let x_1,...,x_42 be its red-edge literals, with neighbors in
increasing vertex order. Fixed red/blue edges use literal +1/-1. The audited
states `s(v,i,j)` represent at least j red edges among the first i neighbors,
for `1 <= i <= 42` and `1 <= j <= min(i,25)`. Their variable numbers are

```
s(v,i,j) = 7442 + 750v + p(i) + j - 1,
p(i) = i(i-1)/2                  if i <= 26,
       325 + 25(i-26)            if i > 26.
```

The checker does not compare gate clauses to the encoder's clause templates.
It exhausts the Boolean truth table of each actual gate, proving the following
relations exactly:

- `s(v,1,1) = x_1`;
- `s(v,i,1) = s(v,i-1,1) OR x_i`;
- `s(v,i,i) = s(v,i-1,i-1) AND x_i` when the diagonal exists;
- all other states satisfy `s(v,i,j) = s(v,i-1,j) OR
  (s(v,i-1,j-1) AND x_i)`.

Induction on i gives the stated threshold meaning. This also holds for signed
constant literals because gate equivalence is checked for both values of
variable 1, and the unit clause subsequently fixes it. There are 32,250 states
and 126,119 definition clauses. After each vertex's counter, the actual two
unit clauses are `s(v,42,18)` and `-s(v,42,25)`. They force every red degree into
[18,24]. All 43 windows are verified, not inferred from metadata.

The checker also verifies 504 AND gates (1,512 clauses). For each color and
threshold d=19,...,24, the chain output is the conjunction over all 43 vertices
of the corresponding degree-at-least-d predicate. The blue predicate is
`-s(v,42,43-d)`, since blue degree is 42 minus red degree.
The output numbering is

```
g(color,d,step) = 39692 + 252*color + 42*(d-19) + step - 1,
color = 0 for red, 1 for blue; step = 1,...,42.
```

## 3. Endpoint branch implications

For `d18-24.cnf`, the checked suffix contains the positive unit 40195. This is
`g(blue,24,42)`. Thus every blue degree is at least 24, so every red degree is
at most 18. The degree windows make every red degree exactly 18.

For `d24-18.cnf`, the checked suffix contains the positive unit 39943. This is
`g(red,24,42)`. Thus every red degree is at least 24; the degree windows make
every red degree exactly 24.

The entire four-file suffix inventory is checked against the pinned historical
files. Only the indicated positive endpoint unit, the common degree subset,
and the physical five-set clauses are needed for these two implications.

## 4. Applying the existing exact theorem

h3959 proves there is no 18-regular or 24-regular good43. Its source is
`ramsey_r55_regular18_overlap_exclusion`, commit
`1bc2e1d74be1e81478e716f6a5db17d92c0aedaa`, with manifest SHA256
`c630103de12b71b92a41fb0aba236a881f34ebf786c7921ea7cd94d5f45eefcd`.

The reproduction driver replays its complete catalog scan, independent entry
checker, and controls in normal and assertions-disabled modes. The original
trust boundary remains: completeness of the imported McKay R(4,5;24) catalog,
the accepted extremal input U18=85, the classical small Ramsey bounds used in
that proof, and the unformalized finite argument. The full catalog's required
SHA256 is
`83ca4028f206b2fa4315ef219b8c2c57c7835209673dd8183d8fb4353bd4fdd0`.
This pass does not independently reprove the historical catalog enumeration.
During integration, the committed independent review h3965 ACCEPTED h3959
subject to these boundaries: review reference
`bafkreihsjllw2iy4gv36kwefgmhi5j2omkfkdl7rcb35a5ppj3dn4leldu`, source
`a8f7ae91c2f6e999efd089daf33d392e7bd1ac9b`. Its detailed
[review](../ramsey_r55_regular18_overlap_exclusion_review1/REVIEW.md) was read.
This new CNF implication audit has not received external review.

A model of either endpoint CNF would contradict this theorem by Sections 1–3.
Both literal CNFs are therefore unsatisfiable. This is a theorem-based exact
certificate with a checked encoding bridge, not a resolution/DRAT certificate.

## 5. Identity, reduction scope, and remaining state

The first complete formula is parsed and audited. All other files are bound to
its exact common body by SHA256, and their suffixes are parsed and checked.
The common body hash is
`9b382a106e9e129ad304fdbf60c1e3ed422b6fedb532eb0c9c7c2f4180b73731`.
`rebuild.py` additionally reconstructs all four historical files byte for byte
using a preserved encoder and hash-locked public dependencies. The logical
auditor imports none of that encoder code. SHA256 is used for file identity,
not as a substitute for the logical audit.

The checked residual inventory in `REDUCTION.json` has four entries: two new
THEOREM_CERTIFIED_UNSAT entries and two UNKNOWN entries. Historical solver
outcomes remain UNKNOWN; no old logs or partial proofs are revised. Previously
excluded odd regular degrees 19,21,23 remain excluded by the handshake lemma.

This is a reduction from four unresolved concrete even-regular jobs to two. It
is not a claimed proportion of graphs, the 2,189,178 whole h3887 tasks, or an
estimate of solver tractability. Neither the full q10 task nor its regular
family is decided. Degrees 20 and 22 and irregular candidates remain open.
No good43, or new Ramsey lower bound, is established. Full equivalence and
coverage of the additional historical symmetry/cut encoding are not claimed
by this sufficient-subset audit.
