# Effective all-threshold transfer to spatial and prior neighborhoods

This author proof makes a finite dilated-martingale certificate usable on an
entire neighborhood of possibly diffuse contraction pairs. It gives explicit
spatial, relative-weight and variance budgets, with no atom-count or minimum
positive-mass hypothesis. Independent acceptance is pending. The unrestricted
dimension-three Gaussian-majorisation problem remains open.

The input is a reference coupling accepted by R2's existing mechanism.
For reference source radius squared B, scatter V>0, dilation a>1, relative
spatial radii alpha_x,alpha_y, and relative weight errors rho_x,rho_y, set

```text
e=1-1/a, t=1+alpha_x, beta=V/B,
P=alpha_x+alpha_y+4t(rho_x+rho_y),
L=e beta/(48t)-P.
```

If 0<=rho_x,rho_y<=1/2 and **L>0**, then every contraction pair in this
whole neighborhood has every favorable Gaussian hinge at every

```text
s>=88 B t^3/L.
```

At zero perturbation this is exactly the existing R2 variance schedule.
The new linear-in-parameter spherical margin absorbs perturbations on the
entire unbounded parameter range. No enormous low-threshold mesh or minimum
cloud-mass floor is used. The actual perturbed laws need not admit a
center-law martingale; a checked control illustrates that distinction.

Read [PROOF.md](PROOF.md) for the continuum theorem and
[HANDOFF.md](HANDOFF.md) for the finite-cover interface. The certificate
requires the actual pair to be contractive. It does not infer contractivity
from proximity or certify every unresolved input.

From this directory, CPython 3.11 or later, standard library and Git:

```sh
python3 -B verify.py
python3 -B -O verify.py
python3 -B certificate.py TUBE_INPUT.json
python3 -B verify.py --input TUBE_INPUT.json --certificate TUBE_CERTIFICATE.json
sha256sum -c SHA256SUMS
```

Expected audit status: `ROBUST_MARTINGALE_LOCALIZATION_PASS`. The finite
producer checks the reference coupling and exact rational budgets. The
Gaussian endpoint and geometric measure argument remain written mathematics.
The separate supplied-record checker imports no producer code. Normal and
optimized runs must match [EXPECTED.json](EXPECTED.json). `INPUTS.json`
pins the precise source versions used, retrievable with a full Git checkout.
No new all-variance Kneser--Poulsen consequence or global defect improvement
is claimed. [SOURCES.md](SOURCES.md) credits the accepted R2/R8 inputs and
separates this effective transfer from existing qualitative stability.
