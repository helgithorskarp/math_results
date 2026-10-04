# An original capped H matrix beyond the closed sparse repair face

Author: **six-downset-3, researcher**. Exact ordinary author proof;
the PSD/lift/completeness arguments are unformalized. This contribution
has no independent reviewer verdict. All workers share a signing identity;
the author name identifies who performed this work.

For the triangle-majority downset with 16 outside elements and any eight
deleted `bcx` triples, this directory gives an explicit rational weighted
Hoffman matrix on **all 232 members, including the actual empty vertex**.
It satisfies Conjecture H and the additional cap `M <= I`. Its two
endpoint matrices have their greatest possible ordinary ranks231; the
unit eigenvalue is simple. This is one precisely specified finite carrier,
up to relabeling, not an assertion for other `q,k` or all downsets.

The new matrix is outside the previously excluded five-parameter sparse
repair face. More strongly, it supports a full **20103-dimensional** real
box of independent original edge/anchored-trade repairs, each coefficient
of magnitude at most `1/10292736`. These repairs can be noninvariant.
The center has a certified proper-core margin `1/128`; the box retains
margin `1/256`. See [PROOF.md](PROOF.md) for precise hypotheses and bounds.

`CERTIFICATE.json` contains 143 original orbit entries, each an integer
over1024, and six small dyadic factors. The factor residuals are checked
using integers. Six further scalar sectors are checked directly. The
verifier reconstructs all 53,361 original proper entries, all 53,824 actual-
empty lift entries, and **106722** original action positions: both full
endpoint matrices on a complete231-column basis. Positive fixed-space
quotients alone are not the evidence used here.

From the repository root, reproduce the complete proof record with:

```sh
python3 -I -B round-two/six-downset-3/full-star-capped-q16/check.py
python3 -I -B -O round-two/six-downset-3/full-star-capped-q16/check.py
```

Standard-library CPython 3.12.14 was used for exact checking. No CAS,
NumPy, optimization solver, prior author table, parent sector decoder,
external generated corpus or network is needed to verify the certificate.
The manifest checks all defining source bytes before mathematical input
is parsed. `EXPECTED.json` is compared byte-for-byte with the proof record.
Use `--out /some/scratch/path.json` to save that record outside this directory.

Discovery used one homemade phase-I logdet Newton proposal on the complete
143-parameter invariant repair space, including all nonfixed sectors,
with NumPy 1.24.2 on CPython 3.11.2. Numerical eigenvalues and the optimizer
are not proof inputs. The search took 1.088 seconds; dyadic recovery took
2.520 seconds. All six native thread controls were 1; each child had a
fixed 60-second guard under the standing1 CPU/2 GiB process limit. The exact
original verifier takes under one second here. This compact source and
certificate reproduce the mathematics without replaying discovery.

The [primary problem](https://arxiv.org/html/2609.28404v1#S4) is Conjecture H
of Ellis--Filmus--Friedgut. Their September 2026 preprint remains v1 in the
live 2026-10-04 source check. Its spectral conjectures remain conjectural.
The earlier [five-repair obstruction](../fifth-repair-obstruction/PROOF.md)
has a narrower repair domain and is not contradicted. Prior reviews of
earlier results do not supply a verdict for this certificate.
