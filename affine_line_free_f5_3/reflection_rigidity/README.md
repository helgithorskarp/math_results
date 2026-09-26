# A 71-point candidate has at most one affine symmetry

**Computer-assisted theorem.** If a line-free subset of $\mathbb F_5^3$
has 71 points, its affine automorphism group is trivial or has
order two. In the latter case the sole nonidentity symmetry fixes a
plane pointwise.

The [proof](PROOF.md) closes the line-reflection construction family
with a uniform bound of 70, and bounds the relevant order-four families
by 68. Together with the prior [odd-order symmetry obstruction](../odd_symmetry/README.md),
these imply the group restriction.

The exact value of $r_5(\mathbb F_5^3)$ remains unresolved. The teammate's
separate [upper-bound-71 theorem](../upper_bound71/README.md), published
during this work, gives bounds **70–71**. A 71-point candidate may be affine-asymmetric.
The plane-reflection family remains open. Peer review is pending.

## Replay

Requires Python 3.10+ and a C++20 compiler named `g++`; tested with
Python 3.11.2 and GCC 12.2. No Python package, solver, external dataset,
or network access is needed. From the repository root:

```sh
python3 affine_line_free_f5_3/reflection_rigidity/verify.py --check-expected
```

This runs all five complete forbidden-mask enumerations, the first
direct layer case, two complete and differently implemented planar
censuses for order four, normalization checks, and 14 geometric controls.
The expected status is `LARGER_CANDIDATES_HAVE_AT_MOST_ONE_REFLECTION`;
all five large-set completion counts are zero.

To repeat every slower direct layer enumeration:

```sh
python3 affine_line_free_f5_3/reflection_rigidity/verify.py --full --check-expected
```

The direct cases are partitioned into five fixed complete domains and
run with at most two child processes. This adds several minutes. It
checks every listed candidate five-tuple by actual line incidences,
and agrees with the faster representation on every output field.

The checking build uses address and undefined-behavior sanitizers:

```sh
python3 affine_line_free_f5_3/reflection_rigidity/verify.py --sanitize --check-expected
```

The full release replay and default sanitizer replay both passed and
produced identical [expected output](EXPECTED.json). Source and evidence
hashes are in [SHA256SUMS](SHA256SUMS).

## Evidence and scope

The five line-reflection domains cover every invariant set larger than
70 by an explicit deletion and normalization argument. The second
implementation independently generates the planar points and transverse
lines; it does not import the first program's geometric model.

For order four, one program enumerates subsets of each relevant size
and uses opposite slope pairs; the other walks all 33,554,432 planar
subsets and checks every slope. Their complete allowed-layer histograms
agree. The planar maximum 16 is also verified.

These checks are by the same author and do not constitute independent
peer review. The group conclusion imports the prior order-three
obstruction and elementary odd-prime exclusions at size 71. The current
replay does not repeat that prior computation; no general 72-point SAT
exclusion is a premise. See [SOURCES.md](SOURCES.md).

No new 71-point witness, improved numerical bound, or sharpness of
the two family bounds is claimed. The result removes line reflections
and order-four constructions and reduces every remaining nontrivial
affine symmetry to a single plane reflection.
