# Exact four-colour stop for the flexible-fish difference body

Let `F={p_0,...,p_22}` be the reviewed exact 23-point flexible
Hochberg--O'Donnell fish realization with the additional self-contact
`p_10--p_21`.  This package decides the complete strict unit-distance graph on

```text
F-F = {p_i-p_j : 0 <= i,j < 23}.
```

The support has **at most 507 distinct physical points** and chromatic number
exactly **four**.  It is therefore not a five-chromatic construction and does
not improve the 509-point record.

The point cap does not depend on numerical collision detection.  There are
529 ordered addresses, while the 23 diagonal addresses are all the same exact
zero point, giving `529-22=507`.  Other identities may reduce the order
further.  The verifier deliberately avoids claiming an exact order: it proves
that different conservative collision groups cannot coincide and obtains 433
such groups, hence only the rigorous interval

```text
433 <= |F-F| <= 507.
```

## Why the four-colouring covers the complete physical graph

The source contraction certificate isolates each exact coordinate in an
infinity box of radius `10^-25` about a rational midpoint.  An address
`p_i-p_j` is therefore within `2*10^-25` in each coordinate of its rational
midpoint.  For every pair of the 529 formal addresses the verifier uses exact
rational arithmetic to:

1. put all addresses that could coincide into the same conservative group;
2. prove that no two addresses within a group can be a unit apart;
3. prove that points in different groups cannot coincide; and
4. join two groups whenever the squared-distance interval of any represented
   address pair contains one.

This gives a 433-vertex conservative graph with 1,646 possible-unit edges.  A
literal four-colour word is proper on that supergraph and constant on every
possible collision group.  It consequently induces a proper four-colouring
after every actual collision and covers every actual unit edge, whether or not
an unresolved possible edge is genuine.  The smallest excluded squared-unit
gap is greater than `1.71e-5`; the different-group squared-separation lower
bound is greater than `3.99e-4`.

For the lower bound, the fibre `{p_i-p_0}` is an isometric copy of the exact
four-chromatic 23-point contact source because `p_0=(0,0)`.  Hence the actual
complete graph on `F-F` has chromatic number exactly four.

## Construction meaning and stop

The starting source has a genuine forcing feature: its self-contact eliminates
an explicit complete four-colouring of the underlying flexible fish, while
other complete colourings survive.  The difference body overlays 23 translated
copies of this contact source and reaches the record cap without importing an
intact five-chromatic parent.  The checked global four-colouring shows that
this antisymmetric overlap does not amplify the source obstruction to ordinary
non-four-colourability.  The exact source/operation pair is retired here; no
nearby flex root, partial difference set, translation, rotation, shell, or
additional copy is tested or licensed.

This is a scoped construction stop, not a theorem about arbitrary difference
bodies, arbitrary fish realizations, or the minimum order of a five-chromatic
plane unit-distance graph.  The 433 groups and 1,646 edges describe the
conservative proof supergraph, not an asserted exact physical census.

## Reproduction

CPython 3.11 or later and a complete repository checkout suffice for proof
replay; no SAT solver or floating-point test is used:

```sh
python3 -B hadwiger_nelson_flex_fish_difference_fourcolour_stop/verify.py
python3 -O -B hadwiger_nelson_flex_fish_difference_fourcolour_stop/verify.py
python3 -B hadwiger_nelson_flex_fish_difference_fourcolour_stop/controls.py
(cd hadwiger_nelson_flex_fish_difference_fourcolour_stop && sha256sum -c SHA256SUMS)
```

Optional byte-identical regeneration of the positive word uses the pinned
`python-sat` dependency:

```sh
python3 -m venv /tmp/flex-fish-difference-env
/tmp/flex-fish-difference-env/bin/pip install -r \
  hadwiger_nelson_flex_fish_difference_fourcolour_stop/requirements.txt
/tmp/flex-fish-difference-env/bin/python -B \
  hadwiger_nelson_flex_fish_difference_fourcolour_stop/produce.py \
  /tmp/flex-fish-difference-certificate.json
cmp /tmp/flex-fish-difference-certificate.json \
  hadwiger_nelson_flex_fish_difference_fourcolour_stop/certificate.json
```

The verifier replays the source's exact contraction, complete-contact, and
chromaticity checks before the new 139,656-pair calculation.  Five certificate
corruptions must be rejected.  [PROOF.md](PROOF.md) records the interval
argument and [PROVENANCE.md](PROVENANCE.md) fixes the dependency and novelty
boundary.

Parts's strict 509-point construction remains the supported unrestricted
record: [Parts, *Graph minimization, focusing on the example of 5-chromatic
unit-distance graphs in the plane*](https://arxiv.org/abs/2010.12665).

