Actual author: **six-covering-1, researcher**. See [proof.md](proof.md).

Every selection of at most one phase at each of the24 original labels
m|720,m>=8 misses at least104 residues. Its holes cannot all lie inside
one18-coset plus one8-coset, for ANY pair of target phases. This excludes
the stated construction route, including a later tail on only the actual
proper8-coset holes. The global L_min(8) bounds are unchanged.

Python standard library only, author replay with CPython3.11.2. From this
directory:

```sh
python3 check.py --expected expected.json
python3 audit.py --expected expected.json
python3 controls.py
python3 -O check.py --expected expected.json
python3 -O audit.py --expected expected.json
python3 -O controls.py
```

Expected:144 target pairs excluded by56 hole-mass,80 singleton and8 pair
comparisons. The final eight demands440 exceed their exact group capacity437.
Both implementations replay280752 actual original phase combinations;
the separate physical-set audit also checks2046 anchor phase pairs and72
translations. Twelve semantic damages reject in both implementations.
No SAT status, large proof corpus, external input or exhaustive full-stage
phase enumeration is a premise. The written bridge is unformalized and
same-author independence is not a reviewer verdict.

certificate.json is the compact full target table. expected.json is the
frozen complete replay summary. manifest.json records source/evidence
hashes and bounded actual runs; SHA256SUMS covers every other source file.
All threads were one and one intensive job ran at a time under the
existing1CPU/2GiB scope. No additional resources are required.
