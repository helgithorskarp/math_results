# Reproduction

From the repository root, using CPython 3.11.2 (standard library only):

```sh
python3 -B hadwiger_nelson_homogeneous_three_power_pencils/verify.py --check-expected
python3 -O -B hadwiger_nelson_homogeneous_three_power_pencils/controls.py
```

Expected: PASS, 32 normalized sign cases, 161 exact polynomial identities, 20 equal-radius cases, 12 exceptional-radius cases, 1,152 lifts, 41,472 unit-gauge checks, 384 unit cases with zero survivors, and 36 A5 pencils / 4,608 lifts excluded physically. Verification takes a few seconds on the tested host. The certificate SHA256 is
`0f925652b9a0ab4c2e325cdcbc2a8036f528b560963fcd49f1ae268f6d981ed1`.

The checker first verifies every supplied consequence G as an explicit rational linear combination of the four defining quadratics. It then checks exact zero remainders for the radius identities. It never needs a Groebner-basis oracle. Ordinary and optimized replay agree. The controls retain two nonempty free-vector configurations and reject five corruptions, including an attempted false equal-radius-only strengthening.

To regenerate the certificate:

```sh
python3 -m venv /tmp/hn-three-power-cas
/tmp/hn-three-power-cas/bin/pip install sympy==1.14.0 python-flint==0.8.0
/tmp/hn-three-power-cas/bin/python -B hadwiger_nelson_homogeneous_three_power_pencils/produce.py --out /tmp/hn-three-power-regenerated.json
cmp /tmp/hn-three-power-regenerated.json hadwiger_nelson_homogeneous_three_power_pencils/certificate.json
```

The exact generator uses lexically sorted monomials and reduced row echelon form over Q to express each discovered consequence in the original defining ideal. It increases the Macaulay degree only to a fixed cap and fails if any identity is unavailable. All cases succeed at degree at most four; the replay does not trust the discovery procedure. No random choices, floating precision, or SAT solver are used. Fresh generation is byte-identical.

The optional finite result has a separate CAS trust boundary:

```sh
/tmp/hn-three-power-cas/bin/python -B hadwiger_nelson_homogeneous_three_power_pencils/finite_a5.py --method resultant --check-expected
/tmp/hn-three-power-cas/bin/python -B hadwiger_nelson_homogeneous_three_power_pencils/finite_a5.py --method groebner --check-expected
```

Both routes give the same complete canonical transcript for 96 anchor pairs and 180 algebraic components, proving complex-affine nonconcurrence of the 3,072 lifts in the selected 24 pencils. They import the existing h4105/C0 source interfaces in this repository. They do not filter out nonreal components. Unsupported fibers fail loudly. No bulky root transcript is committed.

To reproduce historical residual membership, regenerate the h4195 residual following `hadwiger_nelson_radix_pair_exclusion_propagation/REPRODUCE.md`, then run:

```sh
python3 -B hadwiger_nelson_homogeneous_three_power_pencils/a5_interface.py --residual /tmp/hn-three-power-residual.json --check-expected
```

This checks the pinned residual canonical hash `42132ed90f7696d9cf7c17e7b47588ca717bb71b633141e29412a1b55b55e97d` and every selected index/signature. The main physical theorem requires no historical residual file. `A5_INTERFACE.json` records all 36 applicable A5 pencils and the 24 literal residual entries, without recomputing any conditional global allowance.
