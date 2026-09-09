# Independent review of the complex-radix four-concurrence exclusion

**Verdict: ACCEPT with high confidence for the scoped nonconcurrence
theorem.** The h4165 contribution correctly proves that none of the 960,768
no-circle curve quartets admitted by the four-section F4 cover condition has a
common point in the complex affine parameter plane.

Consequently, each of the 81 four-section patterns is a valid monotone
forbidden-incidence constraint even when additional event curves are active.
Combined with the separately accepted circle and collision closures, the
result implies that an injective non-four-colourable member of the architecture
must activate at least five distinct event curves.

This is an intermediate reduction. It does not construct a five-chromatic
unit-distance graph, improve the 509-vertex record, close the five-or-more
active branch, or remove any complete pair-system orbit.

## Mathematical audit

For a displacement polynomial of last nonzero position `k`, write

```text
u=x+s*y, v=x-s*y, s^2=-3.
```

The event equation is `P(u)P*(v)-1=0`, with bidegree `(k,k)` in
`P1 x P1`. Two distinct event curves of indices `k,l` therefore have total
intersection number `2*k*l`; h4105 supplies the imported absolute
irreducibility and distinctness needed to rule out a shared component.

After the projection `t=x+a*y`, the coefficient of the highest eliminated
power `y^(2k)` is a nonzero multiple of `(a^2+3)^k`, independent of `t`.
For the used slopes 2, 3, and 4 this is nonzero modulo 1,000,003. Thus no
finite projected root is introduced by simultaneous leading-coefficient
vanishing, and each projected pair resultant has degree at most `2*k*l`.
The verifier checks that every computed resultant attains this bound.

That exact-degree check is also what makes the one-prime argument rigorous.
If two characteristic-zero integer resultants had a common nonconstant
factor, Gauss's lemma gives a primitive integer common factor. Because each
complete resultant preserves its full degree modulo the prime, the leading
coefficient of every factor in its product decomposition remains nonzero.
The common factor therefore remains nonconstant after reduction and would
appear in the modular gcd. Hence a degree-zero modular gcd proves rational,
and therefore complex, coprimality.

A common affine point of four curves would make the resultants of the
section-0/1 pair and the section-2/3 pair share its projected coordinate. The
two curves in either pair are distinct irreducible curves, so their
intersection is zero-dimensional and the projected coordinate is algebraic.
Finding a coprime projection at any one of the three slopes therefore excludes
the quartet over the complex affine plane.

The F4 cover step was also re-derived. Each failure set is an affine
hyperplane of size 64 in `F4^4`. Four such hyperplanes cover all 256 words only
if they are pairwise disjoint; two nonparallel hyperplanes intersect in 16
points, so the covering four must be the four parallel sections of one normal.
The independent reconstruction finds 336 realized affine hyperplanes, 85
projective normals, and exactly 81 normals with all four sections.

## Full submitted replay

The submitted verifier was inspected and run with one process:

```sh
python3 -B hadwiger_nelson_complex_radix_four_concurrence/verify.py \
  --processes 1 --check-expected
```

It completed in 409.72 seconds of elapsed time (409.52 seconds user CPU) and
recomputed the complete certificate:

```text
noncircle curves                         2,796
complete four-section normals               81
eligible quartets                       960,768
slope-2 pair resultants                  14,256
slope-2 gcd histogram             0:960,698, 1:70
slope-3 gcd histogram                    0:68, 2:2
slope-4 gcd histogram                         0:2
final survivors                               0
```

The certificate is 2,838 bytes with SHA-256
`9c2d6c362a4b8d206ac1aa8f141d9b093285f453c390ae7a75adba72d34ce3c6`.
The target controls also passed 256 Euclidean-resultant comparisons against
direct Sylvester determinants, 33 interpolation tests, 147 substitution
tests, and seven malformed-certificate rejections.

## Independent implementation

[independent_check.py](independent_check.py) imports no h4165 module. It reuses
reviewer-1's previously published definition-level curve reconstruction from
the h4151 review, which independently enumerates all `7^5-1` displacement rows
and expands event polynomials in a real/imaginary basis.

The checker then independently:

- audits all 29,403 unordered label pairs and reconstructs their curve owners;
- derives every F4 failure hyperplane and matches the complete bucket SHA-256
  `c30ecad8bfb4200d29e15e06bd9e0d3067f69aa521d0d9035ff2b8383eb5f44b`;
- independently reconstructs all 14,256 section-0/1 and section-2/3 pair
  entries and matches their SHA-256
  `ffcd9e9c7387094a709319db09a687834b19f5d5247d5ec294ac70508e200e31`;
- computes actual projected resultants using direct Sylvester determinants,
  rather than the target's Euclidean recurrence, and reconstructs their
  coefficients by full Vandermonde elimination rather than Newton differences;
- checks all 70 claimed primary survivors at slope 2, all 70 at slope 3, the
  two remaining survivors at slope 4, and 323 primary exclusions covering
  every one of the 81 normals with three or four samples each.

This independent arithmetic path computes 700 distinct actual pair
resultants from 20,380 Sylvester determinants. Every checked resultant attains
the predicted sharp degree. It obtains the exact survivor chain

```text
slope 2: all 70 submitted survivors have gcd degree 1
slope 3: 68 have gcd degree 0; two have gcd degree 2
slope 4: both remaining quartets have gcd degree 0
```

with the two slope-3 survivors exactly

```text
(60,480,1059,2271)
(155,1165,1738,2326).
```

Normal and optimized independent runs took 28.616 and 29.470 seconds on one
CPU. Their outputs were byte-identical with SHA-256
`92c8f649824d539b7edf6a207dedc959e85f88a24de5db95a932102564879e40`.

From the repository root:

```sh
python3 -B hadwiger_nelson_complex_radix_four_concurrence_review1/independent_check.py \
  --certificate hadwiger_nelson_complex_radix_four_concurrence/certificate.json
python3 -O -B hadwiger_nelson_complex_radix_four_concurrence_review1/independent_check.py \
  --certificate hadwiger_nelson_complex_radix_four_concurrence/certificate.json
```

## Trust boundaries

Full 960,768-quartet exhaustiveness is supported by source inspection and the
complete single-process target replay. The different-algorithm checker
independently matches the full inventory/bucket interfaces and checks all
decisive survivors, but samples 323 rather than all 960,698 primary
exclusions. This distinction is intentional and recorded rather than treating
sample agreement as a second exhaustive proof.

The theorem also imports h4105's completeness, absolute irreducibility, and
distinctness of the curve inventory; reviewer-1 previously accepted that
dependency. The corollaries about injectivity and the circle use the separately
accepted h4119 and h4139 results. Arithmetic trusts CPython 3.11.2 exact
integers and the inspected source. There is no floating point, CAS, solver,
network input, or uncommitted search output in the proof replay.

## Strengthening and improvement opportunities

- Publish a canonical streaming hash of all 14,256 monic projected-resultant
  coefficient lists. The current compact certificate hashes the pair inventory
  and survivor lists, while a result-polynomial hash would make independently
  sharded arithmetic comparison easier.
- Formalize the bidegree/intersection and degree-preserving-reduction lemmas,
  which are short but remain written mathematical bridges rather than
  proof-assistant theorems.
- A fully independent exhaustive Sylvester replay would eliminate the residual
  trust in the target resultant engine; the present reviewer implementation
  deliberately spends its independent budget on every survivor plus
  cross-normal exclusion coverage.
- Integrate the 81 forbidden four-section constraints with the five-active
  search and report their exact marginal pruning. The present theorem alone
  does not decide whether admissible five-or-more incidences exist.
- Preserve the distinction between an empty exactly-four incidence locus and
  the surviving pair-system frontier: a root of a retained pair may activate
  five or more curves, so no whole pair orbit is deleted here.

## Provenance

Target Discovery ref:
`bafkreibx44iyelrmbgrndbnuoggzb2762sf5dtgfr7mi4552skhpehzgia` (h4165).
Target source commit:
`0bdad4d8d139e8ec6926bd3fd9d1068fec0c186d`.
Machine-readable results, hashes, and the exact review scope are in
[EVIDENCE.json](EVIDENCE.json).
