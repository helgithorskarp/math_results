# Tammes-15: two completions and a 26-near-contact reduction

Actual author **six-tammes-2**, role **researcher**. Author-checked conditional
lemma; independent review pending. Read [PROOF.md](PROOF.md) for hypotheses
and the unformalized geometric reduction.

Fixing the known asymmetric incumbent except label14 leaves exactly two unit
completions: the asymmetric and cyclic incumbents. This is a complete
arbitrary-last-point classification, not a new packing construction.
For avoidance inequalities relaxed by delta<=1/1000, the arbitrary last
point is within1000delta of one of the two completions.

As a consequence, 26 near-contacts on fourteen labels, within e<=10^-13,
force all fifteen packing points within2100000000e of one of those incumbents
and |t-tau|<=30000e. At e<=10^-16, a strict improvement could only enter the
cyclic neighborhood. Cyclic local exclusion and unrestricted motif occurrence
remain open dependencies. Global numerical bounds are unchanged.

The proof computation enumerates all364 active-plane triples of a bounded
three-dimensional avoidance polytope. Its24 distinct vertices are22 short
vertices with squared norm<3/4 and two unit vertices with squared separation
>1/25. No floating-point decisions, solver or search timeout enters the proof.

Python >=3.11, standard library, one thread and one mathematical job:

```bash
python3 -B round-two/six-tammes-2/fourteen-point-completion/check.py
python3 -B round-two/six-tammes-2/fourteen-point-completion/audit.py
python3 -B round-two/six-tammes-2/fourteen-point-completion/controls.py
python3 -O -B round-two/six-tammes-2/fourteen-point-completion/check.py
```

Full prior arithmetic replay in a complete repository checkout:

```bash
python3 -B round-two/six-tammes-2/fourteen-point-completion/check.py --replay-prerequisites
```

In this researcher's sparse checkout, extracted old prerequisites are in
scratch, while the previous near-contact package is in its normal location:

```bash
python3 -B round-two/six-tammes-2/fourteen-point-completion/check.py --replay-prerequisites --prerequisite-root scratch
```

Expected outputs are in EXPECTED.json, AUDIT_EXPECTED.json and
CONTROLS_EXPECTED.json. The full prior replay adds
`"prior_exact_bounds_replayed": true` to the ordinary output.
The complete enumeration status digest is
`f2fa0f1a9af88af7ab192a6c5d8a142a65acb70a3f908155598e313f4f4f10e7`.

The audit uses a separate ordinary-polynomial representation, row cross
products and centered Taylor intervals. It checks arithmetic and enumeration
for the new completion lemma; it does not independently prove the inherited
core perturbation or local-stress theorems. Exact Gram identification is
checked by the primary program. This is not proof-assistant formalization.
certificate.json contains compact construction data and prior-source hashes;
SHA256SUMS inventories the public files. No raw vertex corpus is needed.

Validated on CPython3.11.2, sequential jobs with numerical-library threads1:
full prior replay14.734s; optimized full replay15.036s; audit5.825s;
six controls8.420s. Peak child RSS25984KiB. Normal and optimized outputs
are identical, and the separate arithmetic audit has the same complete
enumeration digest. Certificate SHA256:
`19c5ee11031d7fb1906a4ac3ec8c501da2efd9e62cf150a296829cd0c35b6524`.
