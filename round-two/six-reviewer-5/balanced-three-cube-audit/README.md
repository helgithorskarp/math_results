# Balanced private-triangle cap: independent review

Actual agent **six-reviewer-5**, independent mathematical reviewer. Confirms
the balanced three-point-cube family for integer \(h\ge2\), with every
original vertex retained, capped greatest lower rank and a proved larger
rational repair. Read [REVIEW.md](REVIEW.md) and [PROOF.md](PROOF.md).
Written proof exposed; **NOT BLIND**. No producer program or certificate is
needed or was used. This is an ordinary proof with exact computational
polynomial signs, not a proof-assistant formalization.

Use CPython 3.10+ and a local environment with the pinned requirements
(observed CPython 3.12.14, SymPy 1.14.0, mpmath 1.3.0):

```sh
python3 -m venv work/venv
work/venv/bin/python -m pip install -r requirements.txt
work/venv/bin/python -B reproduce.py --check primary.json
work/venv/bin/python -B -O reproduce.py --check primary.json
```

Each invocation runs three serial exact phases, each with an unchanged
45-second guard and all six native thread variables set to one. The two
whole mathematical streams must agree with **every byte** of `primary.json`,
not just a hash, count or sample. Expected output reports 95,727 bytes and
SHA256 `2dd0bdc97e284f74b1928618ab85fd385763f0267cbc850aefb9d58b8e0ee357`,
18 signs and the two literal controls \(h=2,3\). Local runs used the unchanged
1CPU/2GiB scope; no failure/timeout is a mathematical premise.

`symbolic.py` builds primitive original-row dot products, full representative
forms and exact permutation determinants over \(\mathbb Q(h)\).
`original.py` uses standard-library `Fraction` on all original vertices.
`bind.py` checks the entire physical basis against those all-parameter forms.
Finite controls support the implementation; the full decomposition and signs
in the proof establish the unbounded theorem. The sealed data contain all
sign polynomials and complete rational control records with reproducible
whole-matrix fingerprints; bulky raw matrix tables and private scratch are
not required. [VALIDATION.json](VALIDATION.json) gives the cold replay and
private-copy semantic-fault checks.

Target [author proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-1/balanced-triangle-cube-three/PROOF.md),
source commit `960058d192b80040f9e81385e0ca34e8b51f4f20`, committed lemma
`bafkreidggu6uyrsapjotothqt6o3tebqosvluyi2nwewvvuehh2tdkll5m`.
Primary literature [Ellis–Filmus–Friedgut v1](https://arxiv.org/abs/2609.28404),
Section 4. No general H/I, different profile or literature-priority verdict.
