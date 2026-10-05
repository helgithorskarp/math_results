# Global sixth boundary minimum and the exact fifth skew endpoint

Actual six-sendov-3 / researcher, 2026-10-05. Ordinary author proof,
unformalized and independently unreviewed.

For every actual monic complex degree-nine polynomial with all nine roots
in the closed unit disk and marked root a=1-eta>0, count all eight critical
slots with multiplicity. Let F be the sum of positive reciprocal distances
from a, and lambda_eta=eta^-2 sum(Im zeta)^3; a zero denominator means
infinity. On an existential boundary collar, the actual global minimum is
M5+J6 eta^6+O(eta^7), where M5 is the credited fifth truncation and

J6 = 147514579224189087883/29386561536
   + 1385519724994877353691 c/58773123072
   - 301426096066413242953 c^2/9795520512, c=cos(pi/9).

Exact rational signs give -65097<J6<-65096. At the exact fifth endpoint
F=M5, both equality-level and upper-cap maximal absolute skew have the
sharp law sqrt(-H J6/kappa) eta^(3/2) [1+O(eta)]. For every fixed finite
D>=0, uniformly for all Delta in [0,D], each exact level
F=M5+Delta eta^5 and its upper cap have maximal skew
eta sqrt(H(Delta-J6 eta)/kappa) [1+O_D(eta)]. Each is nonempty on the
common collar. Fixed sixth bands strictly above J6 have the corresponding
sharp eta^(3/2) law; fixed v<J6 is eventually empty. The exact next
endpoint v=J6 remains open in this source.

[PROOF.md](PROOF.md) gives the quantified statements, two analytic inverse
maps, stationary mean correction, full twelve-direction/four-slack cost,
and physical matching lower construction. [THEOREM.json](THEOREM.json)
fixes the scope declarations; declaration equality is not a proof.
[DEPENDENCIES.json](DEPENDENCIES.json) and [LITERATURE.md](LITERATURE.md)
credit all premises. This does not claim global interior FIRST, an
effective collar, a formal proof, or an exact finite-radius optimizer.

The independently unreviewed fifth-minimum premise has published source
025381de3c987c9879993e4510f8bfc507f0afbc. Its original graph packet is
accepted but uncommitted at this source's preparation; neither it nor
this source inherits a new-child verdict from earlier reviews.

## Reproduction and verification boundary

The producer uses only Python standard-library exact rational arithmetic
in Q[w]/(w^6+w^3+1)[mu]. It reads seven mathematical source files, never
EXPECTED.json or generated mathematical inputs. The five kernel modules
are unchanged whole files from source71b6298e4b9e3159294d95c87dc4d439b2a1f8fd.
The unchanged producer's initial PRIVATE docstring records its development
stage; the source is published here. CPython 3.12.14 was used by the author.

From this directory, with an external scratch output directory:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python -B verify.py --output ../sixth-record.json
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python -B validate.py ../sixth-validation-output
```

Each producer has the unchanged 45-second guard; validation runs children
serially with native thread counts one. Use a fresh external validation
directory. Timeout or resource interruption supplies no mathematical
conclusion. EXPECTED.json is a single complete 215430-byte fixture,
compared in whole after each fresh result. It is not a proof certificate
for the analytic arguments. All 707 finite identities are compared in
whole before hashing, and 12 signs use rational root isolation and Horner
intervals. Every original root, moment, primitive coefficient and positive
FIRST coefficient is retained. Digests alone do not establish these facts.

VALIDATION.json distinguishes the four prior exact-producer replays and
seven mathematical damage controls from two new publication-interface
replays, actual whole-record rejections, scope consistency controls and
preimport source/fixture controls. Mathematics is unchanged across both
runs; old post-generation sensitivity probes are described as sensitivity,
not as end-to-end checker rejection. SOURCE.json seals those same seven
mathematical files and the entire fixture. Its supporting hashes record
provenance, not an independent proof.

Global entry, analytic normal and mean inverse maps, stationary
differentiation, uniform error estimates and physical sharpness remain
ordinary written bridges outside the finite computation. This source
contains no independent review or Lean formalization of those bridges.
