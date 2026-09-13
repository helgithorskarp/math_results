# Reproduction

Run from the repository root. The tested environment is CPython 3.11.2, SymPy 1.14.0, python-flint 0.8.0. The checker does not need a SAT package. Producer regeneration additionally uses python-sat 1.8.dev17 and its CaDiCaL153 backend.

```sh
python3 -m venv /tmp/hn-c0-check
/tmp/hn-c0-check/bin/pip install sympy==1.14.0 python-flint==0.8.0
/tmp/hn-c0-check/bin/python -B hadwiger_nelson_radix_c0_physical_star/verify.py --check-expected
/tmp/hn-c0-check/bin/python -O -B hadwiger_nelson_radix_c0_physical_star/controls.py
```

Expected: `status: PASS`, 76 pairs, 77 components, 251 distinct real parameters, all chromatic numbers 3. The certificate file SHA256 is
`01454e3a32b5aa7d0b0b268de8b41c5a6a7926c6b8fad1f7184824861f866cea`.
No large historical residual export is needed for this standalone finite theorem: `pairs.json` is its explicit definition, and the h4105 architecture source in the same repository regenerates the event polynomials.

To regenerate all root decompositions and positive color witnesses:

```sh
/tmp/hn-c0-check/bin/pip install python-sat==1.8.dev17
/tmp/hn-c0-check/bin/python -B hadwiger_nelson_radix_c0_physical_star/produce.py --out /tmp/hn-c0-regenerated.json
cmp /tmp/hn-c0-regenerated.json hadwiger_nelson_radix_c0_physical_star/certificate.json
```

The producer took about 48 seconds and the full direct-distance verifier about three minutes on the authorized host in the initial run; timing is hardware dependent. Rational coefficient sizes, rather than graph size, dominate physical-distance replay. Runs are sequential and deterministic, with no random seed or floating precision setting. A failed or interrupted run is not a completed certificate.

For historical provenance, optionally regenerate the h4195 residual by following
`hadwiger_nelson_radix_pair_exclusion_propagation/REPRODUCE.md`, then supply its path:

```sh
/tmp/hn-c0-check/bin/python -B hadwiger_nelson_radix_c0_physical_star/verify.py --residual /tmp/hn-c0-residual.json --check-expected
```

This verifies its full canonical JSON SHA256 and checks `pairs.json` against the selected rows **entry by entry**. The pinned residual canonical hash is `42132ed90f7696d9cf7c17e7b47588ca717bb71b633141e29412a1b55b55e97d`; its file hash is `734286535020a4fc4ccbaac44a8a24c4b775d89854de6515c25b45353b93dc4b`. Our first complete verifier run used that input; the standalone optimized replay uses the committed pair list.

`controls.py` checks rational vertical fibers, nonrational linear fibers, nonreal projected factors, spurious resultant factors, all three collapsed component records, rejection of corrupted physical color words, and the C0/unit-circle identity. The verifier and controls use explicit exceptions rather than Python assertions and are also run with `-O`.

The publication contains source, a compact exact certificate and summaries. Generated historical exports, exploratory decompositions, local environments, and execution logs are excluded. The two algebraic algorithms share SymPy for rational polynomial factorization and real-root counting; they are different coverage algorithms, not independent software trust bases. External independent review remains outstanding.
