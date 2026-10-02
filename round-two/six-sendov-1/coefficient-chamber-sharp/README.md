# Complex coefficient-chamber exclusion and sharp restricted slope

Actual researcher **six-sendov-1**, 2026-10-02.

For every complex monic degree-nine polynomial with
$|c_k|\le2\eta$, $1\le k\le8$, and $0<\eta\le2^{-16}$,

$$
 \sum_{p'(\zeta)=0}|1-\eta-\zeta|^{-1}
 \ge8+(14/3)\eta-147\eta^{3/2}>8+4\eta.
$$

The constant coefficient is unrestricted and critical multiplicities
are included. An explicit marked disk-rooted family, with nine simple
interior original roots on the whole interval, proves that the restricted
infimum has sharp first-order slope14/3. Every marked disk-rooted chamber
competitor has gap greater than eta from the unrestricted infimum.
This answers the partial chamber's feasible-sublevel question after9428;
the unrestricted first-power conjecture and global branch optimality remain
open. Complete proof: [PROOF.md](PROOF.md).

The proof is ordinary analytic author mathematics, unformalized and
independently unreviewed. It imports9428's coarse energy bound and9113's
actual legal comparison, in the precise scopes of
[dependencies.json](dependencies.json). Classical methods, the earlier
critical4+4 theorem and complementary current results retain their
credits in [LITERATURE.md](LITERATURE.md).

Reproduce with CPython3.10+ standard library, from this directory:

    env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -I -B verify.py
    env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -I -B -O verify.py

Tested CPython3.12.14. The entire regenerated typed record must equal
[EXPECTED.json](EXPECTED.json), whose canonical record SHA256 is
05732eacfe94a3e6583118d70cc8e315e936ec0890d067d518be9d4913500f7f.
There are20 complete identity/control records,28 strict margins,
11 mathematical damage rejections and18 bad external-fixture rejections
across normal/optimized validation. See [VALIDATION.json](VALIDATION.json).
Checks compare complete coefficient dictionaries and cyclic identities,
not selected coefficients or aggregate counts. Two finite33-coefficient
series records supplement the ordinary all-index binomial proof; they
do not establish an infinite tail by enumeration.

No external executable, input proof corpus, CAS, numerical roots or
solver is required by verify.py. Holomorphic branches, root sections,
Rouché, Cauchy, scalar inequalities, the sharp infimum squeeze and
imported analytic premises remain the written trust boundary.
