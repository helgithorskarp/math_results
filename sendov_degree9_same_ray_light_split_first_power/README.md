# Complex-heavy light splitting and an angular first-power sector

Actual author **six-sendov-1**, role **researcher**, 2026-10-01.
Complete ordinary author proof with exact finite evidence;
unformalized, independent review pending. The three explicit prior
mathematical premises are listed in [PROOF.md](PROOF.md), Section5,
and [LITERATURE.md](LITERATURE.md).

For degree-nine disk-root polynomials with a sixfold heavy critical
point and two light critical points, the first-power inequality holds
at a marked root when the two light points lie on a common ray from
it and the heavy reciprocal is at least the average light magnitude.
The heavy point may be nonreal and nonradial. The inequality is strict
at interior marked roots; boundary equality is the binomial family.
The explicit angular sector in PROOF.md also allows noncollinear light
points. Actual nonreal examples in both sectors have exact Rouche
certificates. The unrestricted degree-nine target remains open here.

The new uniform moment estimate E>=1/128 gives a normalized squared
origin gain at least (s-t)^2/7168 over merging common-phase lights.
A chord at most (s-t)^2/645120, together with the specified real-mean
slack, retains an actual origin gain at least (s-t)^2/21504. These are
conditional functional bounds, not unrestricted polynomial stability.
An exact lower-r countercomparison shows why the splitting principle
cannot discard its heavier-reciprocal condition.

## Reproduction

Use Python3.10+ and its standard library only; recorded interpreter3.11.2.
From the repository root run sequentially, one intensive mathematical
job at a time and every numerical-library thread one:

    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B sendov_degree9_same_ray_light_split_first_power/verify.py
    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B -O sendov_degree9_same_ray_light_split_first_power/verify.py

Each prints the same JSON record with result **PASS**:

- **7854** strictly positive complete dominance coefficients in two
  closed b cells, tensor degrees32,16,6; all global/cell inverse
  identities, every affine/de Casteljau entry and both complete
  Fraction affine references agree;
- all complete moment endpoint/binomial and Chebyshev/Gaussian norm
  identities, plus direct/Horner heavy-mean and radius substitutions;
- **1431** original Gaussian controls, including1170 nonreal heavy,
  448 unequal-light and450 degenerate b-face controls;
- **160** signed noncollinear-light origin controls, exact phase
  perturbation identities and the two complete heavy modulus bounds;
- two actual nonreal disk-root polynomial examples, including a
  noncollinear-light example, exact full derivatives and marked roots,
  origin/polar identities for the base example, and three full
  coefficient/derivative/reciprocal scaling controls;
- the exact lower-r splitting barrier N(original)=1 and
  N(merged)=3713329/30625, with its negative cross term;
- **10** altered manifests rejected through explicit exceptions
  in either Python mode.

The required compact [expected.json](expected.json) is compared in full;
the verifier never implicitly regenerates it. All full sign tensors are
regenerated in memory and discarded. No floating proof input, solver,
external ledger, coefficient corpus or network access is needed.

Normal/optimized elapsed **10.122/11.127s**,
peak child RSS **28296/28388KiB**.
These fit the existing1CPU2GiB scope. No extra resources are needed;
elapsed values depend on host load. The compact canonical kernel SHA256 is

    a0bbfcd4e5ec750e61f92d89eff5f2bde63eeb6ffdd957e7555deb0af6f863c7

The fully cleared margin SHA256 is

    e6f7c361be8fb3a794b772df0f7901d3bd99ffd1c2a65085b5b7921b3cb91901

## Dependencies and trust boundary

The new checker establishes the7854 dominance signs and exact controls.
It does not re-prove the prior full complex6+2 abstract origin lemma or
the prior full complex6+1+1 polar mean lemma and its independent
1/45 refinement. The current results explicitly require them; exact
quantified statements and direct links are in
PROOF.md Section5. Their separate published checkers were replayed
normally this pass, with commit-matching executable/fixture bytes,
in319.299/50.843s and408720/69344KiB respectively. Their older sign
counts are separate evidence, not included in7854. The reviewer
refinement checker at33fcc46a21f433b71ab101f2b048f15be5d02782 was also
replayed in isolated optimized Python:8.118s,61244KiB, verified=true,
uniform_mean_gap_gamma=1/45 and result SHA256
c91e45b78855cc672f2ad91cc51e127ad1b4ed4eea67b6598c2ffcb4efa17e0a.
Its208 additional derivative signs remain separate. Review8184
confirms both8148 claims; it does not audit the new sector theorem.

Use the same one-thread environment to replay the separate premises,
sequentially from the repository root. The reviewer code requires
CPython3.11+ as stated in its own reproduction guide:

    python3 -I -B sendov_degree9_critical_six_two_first_power/verify.py
    python3 -I -B sendov_degree9_radial_sixfold_critical_first_power/verify.py
    python3 -I -B -O sendov_radial_sixfold_polar_review3/verify.py --check sendov_radial_sixfold_polar_review3/RESULTS.json

[algebra.py](algebra.py) and [certificate.py](certificate.py) openly
reuse the author's generic exact arithmetic with source provenance in
LITERATURE.md. [kernel.py](kernel.py) constructs the fresh complex-heavy
moments and entire dominance margin; [verify.py](verify.py) checks the
complete finite evidence and original-coordinate controls. Neither
hash matches nor same-author replays are independent mathematical review.
The analytic triangle estimates, Bernstein interpretation, communication
identities, scaling and polynomial deduction remain ordinary written
mathematics outside a formal proof kernel.
