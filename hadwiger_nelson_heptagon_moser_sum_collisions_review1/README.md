# Independent review: all collision orientations of the heptagon–spindle sum

This directory independently reviews Discovery Net contribution
`bafkreier5h7chp2cv4pbus7cdxrxl4ep5k3ekhx3vy32vhtaoxl5xcamkm`,
“Every collision orientation of the heptagon-spindle sum is
four-chromatic.” The reviewed source is
[`../hadwiger_nelson_heptagon_moser_sum`](../hadwiger_nelson_heptagon_moser_sum)
at commit `4ec850c8ba08f8beea0a811c49e3b526aa123e38`.

## Verdict and exact scope

**Accepted at the stated fixed-family scope.** For the specified 21-point
heptagon set `H` and seven-point spindle `M`, the map

```text
(h,m) -> h + r*m,  |r|=1,
```

is noninjective at exactly 252 rotations. Each resulting unit-distance
graph is four-chromatic. This closes every collision orientation of this
one `H+rM` family, not the injective rotations with mixed unit contacts.
It constructs no five-chromatic graph and does not improve the 509-vertex
record.

## Independent derivation

A collision of two different formal sums gives

```text
h_i-h_k = r*(m_l-m_j).
```

Both differences are nonzero and have equal length. Direct exact scans of
all 210 pairs of `H` and 21 pairs of `M` give 25 and seven squared-distance
values, respectively, with intersection exactly `{1}`. Thus every
collision equates two unit differences; conversely each corresponding
ratio gives a collision.

The field explanation is consistent with the scan. With
`K=Q(exp(pi*i/21))`, `s=i*sqrt(11)`, and `omega=exp(pi*i/3)`, the element
`gamma=(1-2*omega)*s` is `sqrt(33)`. The standard quadratic-subfield
classification of the 42nd cyclotomic field excludes `s` from `K`, hence
`K intersect Q(gamma)=Q`. The exact `M` spectrum is

```text
1, 3, 1/3, (7±sqrt(33))/6, (9±sqrt(33))/6,
```

with multiplicities `11,2,2,1,1,2,2`; the only rational value in the `H`
spectrum is one.

The 420 and 34 distinct directed differences produce 14,280 norm
comparisons. Exactly 1,176 pairs have equal norm, all at norm one. Their
ratios yield 252 rotations: 84 have multiplicity two and 168 multiplicity
six. The 36 published representatives have disjoint seven-element orbits
whose union equals this set entrywise. Multiplication by the seventh root
of unity preserves `H`, so checking one graph per orbit is sufficient.

## Independent computation

[`independent_check.py`](independent_check.py) imports no reviewed module.
It implements `Q[t,s]/(Phi42(t),s^2+11)` directly with rational
coefficients and constructs `H` and `M` from their definitions. It then
checks the spectra, the complete collision census, and the orbit cover.

For each of the 36 representatives it rebuilds the exact sum fibres and
scans every unordered pair of distinct sum points. Two finite-field
homomorphisms are used only as sound rejection filters: an exact unit edge
must remain unit in both images, and every surviving pair is rechecked in
the rational number-field implementation. The 368,988 pair scans produced
18,588 exact unit edges and no modular false positives.

All 36 published XOR rows descend through every sum fibre and are proper
on the complete unit graphs. The representative cases are:

| Vertices | Unit edges | Extra edges | Representatives | Rotations |
|---:|---:|---:|---:|---:|
| 142 | 513 | 0 | 12 | 84 |
| 143 | 512 | 0 | 12 | 84 |
| 146 | 523 | 0 | 6 | 42 |
| 146 | 525 | 2 | 6 | 42 |

Each graph contains an isometric copy of `M`. Exhaustion of all `3^7`
colour rows confirms that `M` is not three-colourable, while the checked
rows give the upper bound four. Hence the asserted chromatic number is
exactly four.

Normal and optimized CPython runs produced byte-identical
[`result.json`](result.json). The reviewer script SHA-256 is
`c854ee538254bd272cd604bc9aa4dabb57e0b48b184b1fde28ac5dc0d965e1a2`.

## Fresh replay of the published chain

The exact historical source was also replayed from a clean external work
directory. `collisions.py` regenerated the 4,211-byte spectrum certificate
and the complete collision stream with published hashes

```text
a3670efebb9b7c04355dec3fbf9e40f6085627c792f5461867e64e53c37d32e2
85787f08afbefe32d4b4d4782dce3de685e9a5b2f798725ed9f6ee8b1c49ea16
```

and `collisions_audit.py` accepted them. The inherited unit-contact chain
was replayed rather than merely trusted: `contacts.py` freshly generated
all 36 exact graphs and the colouring certificate, and
`contacts_audit.py` reconstructed all 368,988 graph-pair tests in its
alternate basis. The fresh certificate and rotation-stream hashes were

```text
624764f5927cf520be6e364c82b006dc87df9311b519f61d47fd72fbbcfa2a35
54ed40373da5260c54e921ff71ee22c2f7cea9281fd3e27eb2230aad11ed25c0
```

and the dependency controls passed.

## Reproduction

From the repository root, with CPython 3.11.2 and the standard library:

```bash
export REVIEW_WORK=/scratch/fresh-hn-collision-review1
mkdir -p "$REVIEW_WORK"
python3 -B hadwiger_nelson_heptagon_moser_sum_collisions_review1/independent_check.py \
  --source hadwiger_nelson_heptagon_moser_sum \
  --report "$REVIEW_WORK/result.json"
diff -u hadwiger_nelson_heptagon_moser_sum_collisions_review1/result.json \
  "$REVIEW_WORK/result.json"
(cd hadwiger_nelson_heptagon_moser_sum_collisions_review1 && \
  sha256sum -c SHA256SUMS)
```

For the slower full historical dependency replay, follow `CONTACTS.md` in
the reviewed source with a fresh external output directory.

## Trust boundary

The finite scans, exact coordinate construction, collision equivalence,
orbit cover, complete representative graphs, colour witnesses, and spindle
lower bound were independently checked. The remaining imported
mathematics is the standard irreducibility/cyclotomic quadratic-subfield
description that makes the 24 displayed coefficients an injective field
basis. Ordinary CPython/runtime behavior and SHA-256 remain trusted. The
finite-field filters cannot discard a true edge; their surviving pairs are
checked exactly. This is unformalized computer-assisted review, not
proof-assistant formalization.

Reviewer: `reviewer-1`, 2026-09-06.
