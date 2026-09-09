# All first-step anchor members of A5(z) are three-chromatic

Let `T={0,1,omega}`, `omega=(1+i sqrt(3))/2`, and
`A5(z)=T+zT+z^2T+z^3T+z^4T`. For **every** complex parameter satisfying
`|1+epsilon*z|=1` for any of the six Eisenstein units `epsilon`, the strict
physical unit-distance graph on A5(z) has chromatic number **three**.
These are six offset circles, not the previously closed radial circle.
The theorem covers all incidences on these loci, without an active-count cap.

Two representatives have 2,760 distinct nonzero primitive restricted norm
polynomials. A 163,330-byte certificate factors them into 2,536 blocks, of
which 1,907 have real roots. There are 2,865 distinct finite real event
parameters per representative. Five blocks have explicit collision witnesses
and use accepted h4119. Every other real block has an actual-edge-checked
three-colour word. Generic parameters and the endpoints are also covered.
See [PROOF.md](PROOF.md).

The physical fixtures `z=+/-(-1+i sqrt(7))/4` each have **243 distinct points,
603 unit edges, eight active curves, and chromatic number three**. Their exact
coordinates occupy 8,652 bytes. Every one of the 58,806 physical point pairs
across the two fixtures is checked using rational arithmetic.

The [frontier interface](HANDOFF.md) removes 424 whole global pair systems,
closes 216 additional five-active pencils and their 3,354,048 surviving lifts,
and moves 4,784 retained systems from exact-five to at-least-six mode.
The complete A5 architecture remains open. No sub-509 record is established.
These are author-side checks; independent reviewer-1 assessment of this new
result remains pending. The global pair/orbit accounting imports the explicit
h4117/h4175/h4177 trust boundary.

From the repository root, with standard-library CPython 3.11.2 or later:

```sh
python3 -B hadwiger_nelson_radix_first_step_anchor/verify.py
python3 -O -B hadwiger_nelson_radix_first_step_anchor/verify.py
python3 -B hadwiger_nelson_radix_first_step_anchor/physical.py --check-expected
python3 -O -B hadwiger_nelson_radix_first_step_anchor/controls.py
```

The main checker takes about 80 seconds in the tested environment. Its
1,817,371 degree-preserving modular coprimality checks use a different
implementation from the FLINT producer; all root counts use exact rational
Sturm sequences. It reconstructs the curve and actual-edge inventory using
reviewer-1's h4163 code and substitutes in the bivariate norm equations,
independently of the producer's direct Eisenstein coefficient norms.
[EXPECTED.json](EXPECTED.json), [PHYSICAL_EXPECTED.json](PHYSICAL_EXPECTED.json)
and [VALIDATION.json](VALIDATION.json) contain compact expected evidence.

Optional fresh generation needs python-flint 0.8.0 and SymPy 1.14.0:

```sh
python3 -B hadwiger_nelson_radix_first_step_anchor/produce.py --out /tmp/hn-anchor-certificate.json
cmp /tmp/hn-anchor-certificate.json hadwiger_nelson_radix_first_step_anchor/certificate.json
python3 -B hadwiger_nelson_radix_first_step_anchor/physical.py --produce /tmp/hn-anchor-physical.json
cmp /tmp/hn-anchor-physical.json hadwiger_nelson_radix_first_step_anchor/physical.json
```

Generation paths must not exist. The main certificate SHA-256 is
`15235c8e304f762422162f3cb7422e74b683b2f8e997e11037cc43f567cf9976`;
the physical fixture SHA-256 is
`845d08282f55e27461b413fa6d0a21b8610ccba8b1806e985b1005af7fdbf8d7`.
The large regenerable frontier interface remains outside the repository.
