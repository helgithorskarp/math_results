# Pinned public dependencies

All links below are reader-facing publication-repository paths. Four
published JSON files are read as input data. Their mathematical proofs
are imported with the scope and source credit in [PROOF.md](PROOF.md);
reading their hashes is not a substitute for those proofs.

| Public input | SHA256 |
|---|---|
| [Native fixture](../../six-sorting-2/native24-kernel-cover/fixture.json) | `93b7cda51cc14fa8f53c0ed89c7c1c2150b8ab6b58f823fc69b41ec7035022e6` |
| [Canonical45-kernel certificate](../../six-sorting-2/native24-kernel-cover/certificate.json) | `21981cab47d3b795b85d9b7c3ab8dbb5a086aba8e059d54154770ec59edcac06` |
| [Unique-root/paired-touch certificate](../../six-sorting-2/native24-kernel-cover/touch-certificate.json) | `04bcf3e1617c3ae2ce026149d1c76f620c8acf6e38bdc448719e26fa3ecd2455` |
| [Fourteen-target normalization certificate](../../six-sorting-2/native24-kernel-cover/normalize-certificate.json) | `99bcad813962ff1495a7f9f217b5ec4a8b94b83e71020754ff5eacf6f7abe490` |

These bytes were freshly consumed from source
`264872c896d9ca292a448a42f45804909952d9c1`; the unchanged earlier inputs
have their original source provenance in the corresponding parent proofs.
The original native fixture ultimately comes from six-sorting-1's
projection/deletion packet, source
`b92f5b0bcafc7fffabf245d806bb01ae94b69d61`.

The producer additionally imports only these two pinned public code files:

| Producer code | SHA256 | Original source |
|---|---|---|
| [Exact original-domain Boolean columns](../../six-sorting-2/semantic-pruning/profile.py) | `dca9c8d6331c3fc548c514ca8f5f1cd170f4a0bb39a3c05250876247d0362719` | `97bd126fa1aa3756008e6dc7c1e04a4f9542bffe` |
| [Dyadic semantic anchors](../../six-sorting-2/semantic-pruning/anchors.py) | `0b95573e7e3c446d0b7ca5352f6b5f4b8d92b91d6f3c72e7b4f783cd99d89902` | `b49096c7b4af0920e93e78c489d69bd7105363cb` |

The standalone verifier imports no such implementation. Its numeric
clamping, pruning and heap-Huffman primitives are credited and reused
directly from [six-sorting-2's touch_verify.py](../../six-sorting-2/native24-kernel-cover/touch_verify.py),
source `e260dd848eb8616697a952840c0027965e5851c3`. They are included
directly so the new verifier has no sibling-code import. The new two-touch
word census and fourteen-case application were written by six-sorting-1.

Original conditional input cubes, both current marker masks and retained
carrier routing are preserved throughout. Only after reconstructing each
original inner record are current classes grouped by maxima. The two
semantic anchor bounds use the classical lower bounds S(5)>=9,S(6)>=12;
the included S(7)>=16 floor is weaker than all selected inner bounds.

No credentials, signing keys, ledger, binary, large private corpus,
heuristic-search output or resource-setting dependency is present.
