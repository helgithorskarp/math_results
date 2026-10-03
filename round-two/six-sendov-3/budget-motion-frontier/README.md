# Sharp fixed-budget cubic original-root motion

Actual **six-sendov-3**, role **researcher**,2026-10-03.

For every fixed finite second-surplus budget $D>B_*$ in degree nine,
the largest canonical original-root motion divided by $\eta^{3/2}$
has the sharp limit $qH^{3/2}\sqrt{z_D}(9-168z_D)$. For $D<K_E$,
$H^2P(z_D)=D-B_*$ uniquely determines $0<z_D<1/56$; for $D\ge K_E$,
$z_D=1/56$. [PROOF.md](PROOF.md) gives all definitions and the complete
ordinary proof. Equality forces six equal middle critical coordinates
and two exceptional ones; at the threshold they merge into1+7.

This includes actual families under the EXACT cut $D=K_E$, using
profiles approaching from below, and the near-minimum law
$q\sqrt{H(D-B_*)/\kappa}(1+O(D-B_*))$ after the fixed-budget limit.
The global first-power inequality, the exact minimum-budget cut,
finite-$\eta$ optimizers, numerical collars and a joint shrinking-budget
limit remain outside the result.

Status: **complete ordinary author proof, UNFORMALIZED and independently
UNREVIEWED**, relative to the exact adopted inputs listed in
[dependencies.json](dependencies.json). The8619 rate/cost input has an
independent prior assessment8684. New independent review10082 confirms
the10060/0 cubic law relative to its stated inputs, and review10070
confirms the10036 full-sphere actual chart. Neither reviews this new leaf.
Finite exact checks do not formalize those analytic bridges.
[LITERATURE.md](LITERATURE.md) credits primary finite-sample moment
literature and makes no historical-priority claim for that auxiliary curve.

Python3.12.14 was observed; Python3.11+ and only the standard library
are required. From this directory:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python -I -B verify.py --validation-batch
python -I -B -O verify.py --validation-batch
python -I -B validate.py --output /tmp/sendov-budget-validation.json
```

The entire deterministic exact record hash is
`1a2dab9bf30fa9559eab18375597a57751cd55e9547c612502abf467c763bce4`.
It includes14 rational polynomial identities,5 field polynomial
identities, all21 three-value count cases, all seven two-value cases,
all nine harmonic maps, physical-embedding sign bounds and the actual
attainment gap coefficient. [EXPECTED.json](EXPECTED.json) is the
compact complete record; [SHA256SUMS](SHA256SUMS) seals fixed source.

Optional useful baseline reproduction from the repository root:

```bash
python -I -B round-two/six-sendov-3/budget-motion-frontier/verify.py --baseline-root "$PWD"
```

This reads the ENTIRE source-pinned10060/0 and10036 fixtures, compares
EVERY coefficient of ALL nine cubic harmonic/norm maps and the ENTIRE
least-profile cost polynomial, and explicitly reports that it is
same-author validation rather than a complete prior theorem replay.
The source-only default requires no external fixture, network, solver
or proof assistant. Serial children have a fixed45-second guard;
existing1CPU2GiB limits are unchanged. A timeout or killed child is not
a mathematical conclusion. The measured full validation receipt is
[VALIDATION.json](VALIDATION.json).
