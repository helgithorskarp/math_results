# Prior-stationary Gaussian contacts and Brownian witnesses

Any strict bounded-law failure of three-dimensional Gaussian majorisation
can be selected at a heat contact that is ordered for **every prior on one
finite support**. At the touching prior, each active Gaussian input
component assigns the same probability to the source and target top sets.
The contact also obeys a joint prior/threshold curvature condition.

The [proof](PROOF.md) represents its flux by the covariance of Gaussian
noise energy with a bounded conditional-expectation martingale. An adverse
dimensionless margin kappa forces a signed event of probability at least
kappa^2/96 by time 1-kappa^2/48. At least half that probability lies in an
explicit bounded region of the six-dimensional Brownian state space, and
the adverse observable has an explicit neighborhood of persistent sign.

These are new necessary restrictions on a possible nonlocal contact.
They do not supply a violating contraction, an unconditional flux sign,
the full conjecture, or a new Kneser--Poulsen consequence. The proof is an
author argument pending independent review. Classical prior optimality
and Brownian tools, and the earlier team contact-set work, are credited
in [SOURCES.md](SOURCES.md).

From the repository root, with Python 3.10 or later (tested on CPython
3.11.2; standard library only):

```sh
python3 probability/gaussian_prior_stationary_contacts/check.py
python3 -O probability/gaussian_prior_stationary_contacts/check.py
(cd probability/gaussian_prior_stationary_contacts && sha256sum -c SHA256SUMS)
```

The first two commands must reproduce [EXPECTED.json](EXPECTED.json),
with status `EXACT_CONTACT_CONTROLS_PASS` and four rejected corruptions.
The small checker derives Gaussian moments from independent increments,
checks the constants and the orientation of an analytic signed control.
That control is explicitly **not** a contraction/contact counterexample.
The checker does not verify the compactness/transversality proof, analytic
differentiation, or stochastic calculus. Those are written proof obligations.
No simulation, solver, external data, or large artifact is required.
