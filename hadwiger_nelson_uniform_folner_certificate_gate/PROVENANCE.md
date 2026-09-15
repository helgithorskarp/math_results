Source intake and coefficient audit: 2026-09-15, general-researcher-1.

Primary mathematical sources:

- Dúcz--Varga, arXiv:2606.28157v1, Lemma 1 and the linked supplementary data.
- Matolcsi--Ruzsa--Varga--Zsámboki, arXiv:2311.10069v4, Theorem 1,
  especially its full shape-isometry generator set and equations (15)--(20).

The authors' landing page is https://users.renyi.hu/~akos/ep1070/ and links
to https://users.renyi.hu/~akos/ep1070/data/snail.zip. Both were fetched
directly during the pass. The archive is 45,637,428 bytes, SHA-256
`ff6c9fc9df606ee15be9b4e3d14e7144e3d829fbd7fbeca3bc21bdd50e43667c`.
It is deliberately not republished here.

The two inputs used, inside the `snail_reproduction/` archive directory, are:

| Member | Bytes | SHA-256 |
|---|---:|---|
| rational_dual.txt | 358067 | c30e2b3d3e7b50c01fe3bcdc17df80cf7053f0e73a756ec9965088c8dd50c106 |
| congruences.txt | 915422 | f6374e5f79cd4565c36c613656d3b75410c9258a010bf859a1c7cff526f87110 |

The dual has 16,859 congruence coefficients; together with its scalar value,
these are the paper's 16,860 dual variables. The value is transcribed from
the authors' `verify_data.py`, SHA-256
`abaf8e49b5e15e3721bd1f948d28ac30cfe8778f8aebcfcc2871816cb28ef9e3`.
That script was read, not executed. Its full symbolic and independent-set
verification was not rerun.

The proof uses only the claimed genuine congruences and dual inequality,
three distinct source points, and a source unit edge. The unit-edge fact
also follows directly from the first and seventh columns of the published
G27 table: their difference is omega_1*omega_3, a product of unit complex
numbers. It uses exact ordinary plane incidence bounds on a hypothetical
output support; no approximate geometry or generated edge list is involved.

Computational trust: the two text transcriptions pinned above, CPython
integer/rational arithmetic, standard-library ZIP/text parsing, the written
coefficient and counting arguments, and ordinary hardware. No SAT solver,
numerical optimizer, proof assistant or independent peer review is claimed.
Normal/optimized replay and small controls are recorded in VALIDATION.json.
