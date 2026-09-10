# Reproduction from public source

The new producer and checker use CPython 3.11.2 and the standard library.
Regenerating the older h4191/h4193 input interfaces additionally imports
python-flint 0.8.0 through their existing geometry helpers. No CAS factorization
or solver result is used by this new propagation proof.

All output paths below must be fresh. Run from the repository root.

## Pinned historical inputs

```sh
python3 -B hadwiger_nelson_radix_five_active_orbits/produce.py \
  --out /tmp/hn-propagation-orbits.json \
  --export-interface /tmp/hn-propagation-orbit-interface.json
python3 -B hadwiger_nelson_radix_incidence_geometry/verify.py \
  --export-interface /tmp/hn-propagation-incidence.json
python3 -B hadwiger_nelson_radix_first_step_anchor/frontier.py \
  --interface /tmp/hn-propagation-orbit-interface.json \
  --incidence /tmp/hn-propagation-incidence.json \
  --export-interface /tmp/hn-propagation-anchor.json --check-expected
python3 -B hadwiger_nelson_radix_reflection_pair_stratum/frontier.py \
  --frontier /tmp/hn-propagation-anchor.json \
  --export-interface /tmp/hn-propagation-reflection.json --check-expected
python3 -B hadwiger_nelson_radix_rotation_pair_stratum/frontier.py \
  --frontier /tmp/hn-propagation-reflection.json \
  --export-interface /tmp/hn-propagation-input.json --check-expected
```

The two new-program inputs are bound by canonical SHA-256:

- frontier: `9da6cb1a32bbb5004b72bf2ac934dc05a44b5e2bf7705e7ec55498c3e7caabf9`;
- incidence: `c9cb33688915d282b9d410898eeeb22d4bd33e242b3d28b7703ca4fe2111c477`.

These commands regenerate historical interfaces, not new candidate searches.
Their proofs and trust boundaries remain in the respective source packages.

## New certificate, independent verification, and exact residual

```sh
python3 -B hadwiger_nelson_radix_pair_exclusion_propagation/produce.py \
  --frontier /tmp/hn-propagation-input.json \
  --incidence /tmp/hn-propagation-incidence.json \
  --out /tmp/hn-propagation-certificate.json \
  --export-interface /tmp/hn-propagation-result.json
cmp /tmp/hn-propagation-certificate.json \
  hadwiger_nelson_radix_pair_exclusion_propagation/certificate.json
python3 -B hadwiger_nelson_radix_pair_exclusion_propagation/verify.py \
  --frontier /tmp/hn-propagation-input.json \
  --incidence /tmp/hn-propagation-incidence.json \
  --export-interface /tmp/hn-propagation-independent-result.json --check-expected
cmp /tmp/hn-propagation-result.json /tmp/hn-propagation-independent-result.json
python3 -O -B hadwiger_nelson_radix_pair_exclusion_propagation/verify.py \
  --frontier /tmp/hn-propagation-input.json \
  --incidence /tmp/hn-propagation-incidence.json --check-expected
python3 -O -B hadwiger_nelson_radix_pair_exclusion_propagation/controls.py \
  --frontier /tmp/hn-propagation-input.json \
  --incidence /tmp/hn-propagation-incidence.json
```

The measured fresh producer used about 43 seconds and 202 MiB peak resident
memory; the independent optimized checker used about 14 seconds and 119 MiB.
These are observed resource costs, not time caps. Each run is deterministic
and single-threaded; independent validation processes were run concurrently.
The complete count remains small enough for Python, so no C++ rewrite or
fixed-width arithmetic was introduced.
