# Reproduction notes

The compact verification uses only CPython's standard library:

```bash
cd math_results
python3 -B hadwiger_nelson_weighted_mixed_orbit_gap/verify.py --check-expected
python3 -O -B hadwiger_nelson_weighted_mixed_orbit_gap/verify.py --check-expected
python3 -B hadwiger_nelson_weighted_mixed_orbit_gap/independent_check.py
python3 -O -B hadwiger_nelson_weighted_mixed_orbit_gap/independent_check.py
sha256sum -c hadwiger_nelson_weighted_mixed_orbit_gap/SHA256SUMS
```

The recorded environment used CPython 3.11.2. The checker reconstructs both
finite graphs, decides all 41,616 physical point pairs by exact arithmetic,
checks every positive colouring symbol against every edge, and regenerates
the five-colour quotient CNF byte for byte.

The auxiliary lower bound used Kissat 4.0.4 at commit
`8af8e56f174b778aef3aa45af9f739b2a5f492c2` and `drat-trim` at commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`:

```bash
python3 -B hadwiger_nelson_weighted_mixed_orbit_gap/verify.py \
  --emit-cnf /scratch/weighted-mixed-quotient-5.cnf
kissat --no-binary /scratch/weighted-mixed-quotient-5.cnf \
  /scratch/weighted-mixed-quotient-5.drat
drat-trim /scratch/weighted-mixed-quotient-5.cnf \
  /scratch/weighted-mixed-quotient-5.drat
```

Recorded hashes:

```text
CNF   c5b0faf45916cef4f2e65b025c93d16f4b27bef696da814df56e23b09f3b8525
DRAT  8f084faba331c1654e09b656989af6cd5497b68a965510d7de59d42688dba150
```

Large solver traces remain outside the repository. The DRAT bytes are not
needed to verify the physical graph's exact chromatic number three.
