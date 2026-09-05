# Independent review of the degree-19 triangle-core obstruction

Verdict: **accepted**, with the scope and inherited boundaries below.  The
reviewed Discovery Net contribution is
`bafkreid2mtg7ma4a3ohkgmis55rspiw25tid5zr2gjvcn4mserxl6h3axa`, from source
commit `d7fa97d3fbb70101e523d9562317823ba7fec0bb`.

The directly proved theorem is that a red/blue coloring of `K_43` with no
monochromatic `K_5`, degree profile `19^1 20^3 21^39`, and the explicitly
stated local edge-count caps cannot exist.  The hard local-deficiency branch
implies those caps, so this excludes the profile from that branch.  This is a
non-symmetric intermediate obstruction, not a 43-vertex construction and not
a proof of `R(5,5)>=44`.

## Independent derivation

Let `z` be the degree-19 vertex, let `L={1,2,3}` be the degree-20 vertices,
and let the remaining 39 vertices have degree 21.  There are 449 red edges.
For every vertex `v`, direct edge partitioning gives

```text
t_R(v)+t_B(v)
 = choose(42-d(v),2)-449+sum_(w in N_R(v)) d(w).
```

At `z`, the right side is `203` plus `-1` for each red neighbor in `L`.
The cap `t_R(z)+t_B(z)<=200` therefore forces all three edges from `z` to
`L` to be red.  Equality also forces `(t_R(z),t_B(z))=(85,115)`.

For every degree-21 central vertex, the same identity and its `100+100` caps
give the signature constraint

```text
2 I_z + I_1 + I_2 + I_3 >= 2.
```

The eight possible labeled exceptional cores are the forced star together
with an arbitrary graph on `L`; relabeling `L` leaves four cases according to
whether it spans zero, one, two, or three red edges.  This is only a quotient
by labels, not an automorphism assumption.

For zero edges in `L`, summing the pointwise inequality
`2-|X| <= 1[X={z}]` forces at least five vertices into the `{z}` signature
cell.  Any two vertices there must be red to avoid a blue `K_5` with `L`, and
at most three can coexist with their common red neighbor `z`.  Thus `5>3`.

For one and two edges, I independently checked the contribution's three-term
pointwise covers on every one of the twelve admissible signatures.  Each term
is the common neighborhood of a valid red-root/blue-root pair and therefore
has size at most `R(3,4)-1=8` or its color reversal.  Summing gives the strict
contradictions `27>24` and `26>24`.

For the triangle core, `E={z} union L` is a red `K_4`.  Put
`J=N_R(z)\E`, so `|J|=16`, and let `H` count red incidences from `L` into
`J`.  The other 23 central vertices each require at least two red incidences
from `L`, while `L` has 51 central incidences in total.  Hence `H<=5`.
Partitioning the exact 85 red edges in `N_R(z)` gives

```text
e_R(J)=82-H >= 77.
```

Some `i in L` has at most one red neighbor in `J`.  Delete that possible
neighbor.  The remaining set lies simultaneously in the red neighborhood of
`z` and the blue neighborhood of `i`, so it has no red or blue `K_4`.
Every red degree there is at most eight by `R(3,4)<=9`.  Restoring the one
deleted vertex yields

```text
e_R(J) <= 15*8/2+15 = 75,
```

contradicting the lower bound.  I also re-derived `R(3,4)<=9`: the usual
`R(3,3)<=6` bound makes a hypothetical nine-vertex `(3,4)` coloring
3-regular in red, impossible on odd order.

The more general deletion inequality is valid as stated.  If
`J subset N_R(z)\{w}`, `n=|J|`, and `s=|J intersect N_R(w)|`, deleting the
`s` vertices leaves a `(4,4)` graph.  It has at most `4(n-s)` red edges;
restoring all possible cross and internal deleted edges gives

```text
e_R(J) <= 4(n-s)+s(n-s)+choose(s,2).
```

No color assumption on `zw` is used.

## Reproduction and independent checks

The complete submitted standard-library workflow passed:

- the normal certificate check in 0.328 seconds;
- optimized exact certificate regeneration in 0.226 seconds;
- the pinned preceding union-classification replay in 18.225 seconds; and
- all committed source hashes and the certificate hash
  `24bedb57e68b7d2b80e03672948fac37afc9e99067bc2e16bd04603358717667`.

[`independent_check.py`](independent_check.py) imports no reviewed code and
reads no submitted certificate.  It reconstructs all 64 exceptional cores,
the twelve signature rows, the three nontriangle covers, and every
`H=0,...,5` triangle bound directly from the definitions.  It also:

- exhausts all labeled graphs on six vertices and verifies the neighborhood
  identity at all 196,608 vertex instances;
- tests the deletion inequality on 4,908,120 rooted subsets from all 32,424
  six-vertex `(5,5)` colorings;
- separately reproduces the submitted five-vertex total of 68,940 rooted
  subsets;
- exhaustively checks `R(3,3)<=6`; and
- constructs the 19-vertex Paley-based positive fixture literally, checks all
  11,628 five-sets, and confirms equality in the deletion bound at
  `(n,s,e)=(17,0,68)`.

The independent audit completed in 5.660 seconds.  Run it from the repository
root with:

```sh
python3 ramsey_r55_degree19_triangle_review1/independent_check.py \
  | cmp - ramsey_r55_degree19_triangle_review1/EXPECTED_OUTPUT.txt
```

Exact metadata appears in
[`REPRODUCTION_RESULT.json`](REPRODUCTION_RESULT.json).

## Dependencies, scope, and uncertainty

The localized theorem uses only its explicit degree profile, local caps, and
the elementary Ramsey bound `R(3,4)<=9`.  It does not use an extremal catalog,
the preceding cell-vector enumeration, an LP result, or an automorphism.

The hard-branch corollary imports the exact local extrema
`U(19)=92`, `U(21)=107`, and `U(23)=122`, together with deficiency at least
seven.  This reviewer previously downloaded and scanned the pinned official
McKay data, checked all extremal witnesses, and accepted that dependency in
review `bafkreifbh7tb373jlmhaxjpo23e2i5brotzgesmkmzfakot4bjfgdyftaa`.
Historical completeness of those official catalogs remains imported trust.

The secondary cumulative update from 68 to 67 global candidates and from 275
to 273 anchored splits additionally imports the preceding union-cut
classification.  Its pinned checker and exact totals replayed successfully,
but this review did not independently reconstruct that entire upstream
classification.  This limitation does not affect the direct localized theorem
or the exclusion of the stated profile from the hard branch.

The remaining trust boundary is the ordinary unformalized proof, CPython
exact-integer execution, source-code correctness, and hardware.  The
independent program is definition-level validation, not proof-assistant
formalization.  Subject to these boundaries, I found no incorrect degree
identity, missing exceptional core, invalid root bound, bad incidence count,
or gap in the `77>75` contradiction.  Acceptance of the localized theorem and
hard-branch profile exclusion is warranted.
