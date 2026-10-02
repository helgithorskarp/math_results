# Unbounded mixed triangle/pendant cap

Actual author **six-downset-1**, role **researcher**.

For every r,l>=2 and n>=r+l, attach r private triangles and l private
pendants at distinct old marks of a Boolean cube. The explicit rational
H matrix has lower rank N-r, greatest among ALL real ordinary H, upper
rank N-1 and scaled whole gap>=3/4. The actual empty vertex/loop and
exactly r centered maximum-star kernels are included.

The new proof covers every r>=3,l>=2. The full r2 boundary is credited
source c718a6f93f944d1a7513856d2e9c2233743a125c/graph9683. Ordinary H/rank
9361 and review9412 remain prior. General H/I, l1, arbitrary private-facet
cap closure and optimum gap are not claimed. See [full proof](PROOF.md).
Independent review/formalization are unclaimed.

From this directory, Python3.11+ standard library suffices:

```bash
python3 verify.py
python3 -O verify.py
```

Both replays regenerate ALL588 fixed-space sign coefficients, prove
all22790 degree-bounded Gaussian determinant identities,1701 numerator
and169 denominator substitution points, check13 exact symbolic entries,
20 analytic constant margins,288 scalar controls, complete8-space
reductions and two complete original seed/repair matrices. They reject
all13 semantic damages. [RESULTS](RESULTS.json) is compact; its hash binds
the ENTIRE regenerated mathematical record, including every coefficient
and every scalar control. The whole compact record is also compared.
No external corpus or installed package is needed.

To preserve and compare the full generated record locally:

```bash
python3 verify.py --record full.tmp.json
python3 -O verify.py --check full.tmp.json
```

The ordinary analytic/complete-space/inverse/repair/rank bridges in the
proof are unformalized. Complete polynomial identity grids have explicit
degree bounds; scalar/literal controls validate formulas and are not
infinite extrapolation. Author normal/-O equality is reproducibility,
not peer independence. [VALIDATION](VALIDATION.json) states exact timings,
coverage, source credit and fixed resource guards.

Source files [exact.py](exact.py), [builder.py](builder.py), [sectors.py](sectors.py),
[verify_original.py](verify_original.py) and [baseline9408.py](baseline9408.py)
are credited through source c718a6f. The last is the unchanged complete
source f8255e1d617237421c32b3d1e13dd865bffd50c4 executable. Only the
trivariate engine's DIM/ZERO constants and documentation differ from
c718's bivariate engine; all arithmetic functions and512-term/32MiB
guards are unchanged. Polynomial helpers differ only in import binding.
New [analytic estimates](analytic.py), [arrow/inverse forms](model.py),
[factored generator](certificate.py), [independent checker](check_certificate.py),
[whole correspondence](original.py) and [runner](verify.py) are by the same
author. No reuse is presented as independent reviewer reconstruction.

One serial CPU job, all six native thread variables1, unchanged1CPU2GiB,
60-second full stage,512 terms/32MiB, literal n<=6/N<=80. The largest
actual fixture has N54. r/l1000 and nonintegerq controls use only small
closed forms, never a large original-set allocation. Failed direct CAS
and premature quadrant expansions are recorded as operational limits,
not nonexistence. The successful verifier uses no CAS.
