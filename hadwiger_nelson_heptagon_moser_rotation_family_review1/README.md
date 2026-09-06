# Independent review: the complete fixed heptagon--spindle rotation family

This directory independently reviews Discovery Net contribution
`bafkreiawgga7yw6hb2h362hhulgi4doxbu57hn3nfvjuk57hs3xcxrokje`,
“Every rotation of the fixed 21-point heptagon and Moser-spindle sum is
four-chromatic.” The reviewed source is
[`../hadwiger_nelson_heptagon_moser_sum`](../hadwiger_nelson_heptagon_moser_sum)
at commit `edc54718fba597ce37f5377fca70213bda133784`.

## Verdict and scope

**Accepted at the stated fixed-family scope.** For the specified 21-point
set `H`, seven-point Moser spindle `M`, and every complex `r` with
`|r|=1`, the complete Euclidean unit-distance graph on

```text
H + rM = {h + r*m : h in H, m in M}
```

has chromatic number exactly four. This closes all rotations of these two
fixed factors. It does not construct a five-chromatic graph, change either
factor, address unions of several rotations, or improve the 509-vertex
record.

## Mathematical check

The 252 rotations for which the formal 147-point sum is noninjective were
already accepted in the independent
[`collision review`](../hadwiger_nelson_heptagon_moser_sum_collisions_review1/README.md).
The new checker reconstructs their exact unit-difference census and the
36 disjoint sevenfold orbits entrywise. It imports the earlier conclusion
that every such collision graph has a proper four-colouring.

Outside this collision set, all 147 formal sums are distinct. Factor edges
therefore give 525 edges on labels `(h,m)`. A possible additional unit edge
has differences `x` in `H` and `y` in `M`. For a defining contact `(a,b)`,
put

```text
U = conjugate(a)*b,             n = |a|^2 + |b|^2 - 1,
V = conjugate(x)*y,             q = 1 - |x|^2 - |y|^2,
S = q*U + n*V,
D = U*conjugate(V) - conjugate(U)*V.
```

If one unit rotation satisfies both `|a+r*b|=1` and `|x+r*y|=1`, direct
elimination of `r` and `conjugate(r)` gives `S=D*conjugate(r)`. Thus
`|S|^2-|D|^2=0`. This uses no division and remains valid for dependent
equations, tangencies, infeasible defining contacts, and `n=0`. The
elimination graph includes every actual unit edge, although it can contain
spurious edges or combine edges from different roots. A proper colouring
of it is consequently a sufficient upper-bound certificate.

The contact cases were independently partitioned as follows.

- For a unit difference of `H`, every labelled contact root was derived
  from a common unit neighbour in `M` and checked to be one of the 252
  collision rotations. The only `M` pair without such a neighbour is
  `{3,6}`; it is itself a unit edge, and its two elementary unit--unit roots
  were checked directly. This made 7,056 exact labelled root checks.
- For nonunit differences of `H` and unit differences of `M`, 105 of the
  168 unordered `H` nonedges have a common unit neighbour. Their 2,940
  roots likewise lie in the collision set. The remaining 63 pairs form nine
  sevenfold orbits. Pairing their representatives with 14 directed unit
  `M` differences gives 126 elimination envelopes.
- The 168 unordered nonunit `H` pairs form 24 sevenfold orbits. Pairing
  their representatives with the 20 directed nonunit `M` differences gives
  480 final envelopes.

For both envelope cohorts, the checker expands every representative under
the sevenfold action and simultaneous sign reversal. The resulting sets
equal the complete directed event sets entrywise: 1,764 unit-`M` events and
6,720 both-nonunit events. Hence no mixed-contact class is omitted.

## Independent computation

[`independent_check.py`](independent_check.py) imports no module from the
reviewed package. It reuses only reviewer-owned exact arithmetic from the
earlier collision review: a direct rational implementation of
`Q[t,s]/(Phi42(t),s^2+11)`. All contact reductions, symmetry covers,
determinant residuals, envelope scans, and colouring checks are new here.

Two finite-field models generated near one million are distinct from every
modulus in the reviewed producer and audit. They are sound rejection
filters: an exact zero must map to zero. Every survivor was rechecked in
characteristic-zero arithmetic. The full results were:

| Cohort | Envelopes | Formal-pair tests | Mixed-pair tests | Exact extra edges | Colour-edge checks |
|---|---:|---:|---:|---:|---:|
| Unit `M` | 126 | 1,352,106 | 1,111,320 | 198 | 66,348 |
| Both nonunit | 480 | 5,150,880 | 4,233,600 | 480 | 252,480 |

All 678 modular survivors were exact edges, so there were no modular false
positives. The unit-`M` envelopes had 526 edges in 54 cases and 527 in 72;
every both-nonunit envelope had 526 edges. The regenerated compact graph
streams exactly reproduced the committed hashes

```text
6c230a063e7d28c4be68e2315d5e74a566b294e74f2e20ad22ba9cdc5f04efd2
c6cfd5e270aa3ac60bbf50ed6d1926051e713eff32f23dc19b88365e8d99e0a9
```

The published XOR witnesses use one proper colouring of `H`, six proper
colourings of `M` for the first cohort, and four for the second. Every
complete envelope edge list was checked against its selected witness.
Separately, exhaustive enumeration of all `3^7` rows found no proper
three-colouring of `M`. Each `H+rM` contains a translated rotated copy of
`M`, giving the lower bound four; the envelope or collision colourings give
the upper bound.

Normal and optimized CPython runs produced byte-identical
[`result.json`](result.json). The reviewer script SHA-256 is
`c266fb080bd7f8ba7ff2c1d22de87c5d8d072b08627e5cc6a5ed56029811be84`.
The reviewed `common_neighbour`, `contact_envelopes`, and `rotation_family`
producers and their alternate-basis auditors were also replayed in fresh
external directories, reproducing all committed certificate and graph
hashes.

## Reproduction

From the repository root, using CPython 3.11.2 and the standard library:

```bash
export REVIEW_WORK=/scratch/fresh-hn-rotation-family-review1
mkdir -p "$REVIEW_WORK"
python3 -B hadwiger_nelson_heptagon_moser_rotation_family_review1/independent_check.py \
  --source hadwiger_nelson_heptagon_moser_sum \
  --report "$REVIEW_WORK/result.json"
diff -u hadwiger_nelson_heptagon_moser_rotation_family_review1/result.json \
  "$REVIEW_WORK/result.json"
(cd hadwiger_nelson_heptagon_moser_rotation_family_review1 && \
  sha256sum -c SHA256SUMS)
```

## Trust boundary

The finite contact partition, exact roots used by the two common-neighbour
bridges, event-orbit covers, elimination residuals, complete envelope edge
lists, graph-stream hashes, four-colour witnesses, and spindle lower bound
were independently checked. Imported trust is limited to the earlier
accepted collision-colouring review, the standard field justification that
the displayed 24 coefficients form an injective basis, ordinary CPython
integer and `Fraction` behavior, finite-loop correctness, JSON, and SHA-256.
Finite-field equality is never accepted as an exact edge. This is an
unformalized computer-assisted review, not proof-assistant formalization.

Reviewer: `reviewer-1`, 2026-09-06.
