# Period-10080 base repair obstructions

Actual author: **six-covering-1**, role **researcher**. Complete author checks;
independent review is not claimed.

The saved 65-class assignment has minimum exactly eight, actual LCM 10080,
and 87 uncovered residues. These integer certificates show that no tail
completion can cover if at most one of its 30 non-7 base phases changes.
At least four residues remain uncovered, with all 35 tail phases fully free.
If modulus 80 takes phase 32 or 72 and at most one other base phase changes,
at least six residues remain uncovered. The ten vectors also give necessary
linear inequalities for any distinct covering with minimum at least eight
and LCM dividing 10080.

Unrestricted period 10080 remains open. These conditional bounds do not
improve the global interval or establish an exact conditional optimum.

Read [proof.md](proof.md) for the quantified statements and weighted counting
argument. [weights.json](weights.json) contains ten sparse integer vectors;
[near_cover.tsv](near_cover.tsv) contains the labeled fixture. The definition
checker [check.py](check.py) uses every physical residue and ordinary phase,
without LP, SAT, CRT updater or search dependencies.

```bash
python3 -B check.py near_cover.tsv weights.json
python3 -B check_controls.py
```

Python 3.11+ and its standard library suffice. The principal check reports:

* Single base trades: all 4863 excluded, partition 4791 original weight /
  63 residual indicators / 9 new weights; hole floor four.
* Modulus-80 anchors 32/72 plus one other trade: all 9568 excluded,
  partition 9546 weights / 22 residual indicators; hole floor six.
* Complete toy controls: 14,784 phase/omission assignments, 24 covers,
  4396 positive obstructions; eight malformed certificates rejected.

The certificate hash is
`c0134943cc348054059f099e1b72cffd63f94e08b6e152f04d8937bf53fe25c8`.
The deterministic physical-check event hash is
`019ed2f33466ef5ff713f6ed964dd13c50a314b92910f5c8d9c5d0df913b2667`.

The original fixed-base vector and its 41-hole bound are reproduced from
[the preceding certificate](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_10080_fixed_base_weights/proof.md),
source `482870cd5dbb8ca17eb39590d65b9ecd49fb22cc`, committed graph lemma
7588. The nine new vectors close its remaining single-base repair options.
Raw discovery LPs, heuristic walks, binaries and private checkpoints are
unnecessary for verification and are not publication artifacts.
