# R(B4,B7): ordinary forcing completes the broader cross-shell obstruction

Actual author **six-books-1**, role **researcher**, 2026-10-02, pass20.

Under the complete explicit normalized cross-shell hypotheses in
[PROOF.md](PROOF.md), all five initially free SY/T-to-X rows are forced to
the four terminal cores of lemma9685. Ordinary T2 lemma9795 and the new
remaining-row argument give the forcing; ordinary completion lemma9685
then excludes every completion with E<=108. Both actual r labels are
covered. No global degree bound outside N[u] is assumed.

This replaces the remaining finite forcing step inside the cross part of
the already computer-assisted specified-leaf exclusion9631. It excludes
no additional host class and establishes no new Ramsey endpoint. The
new ordinary proof is complete as an author argument, unformalized and
independently unreviewed. Review9753 concerns the older prescribed-core
completion theorem9685; fresh review9820 concerns the earlier T2 lemma9795.
Neither verdict transfers to this new remaining-row argument.

## Mechanism and execution boundary

Cut equality makes the eleven-point outside graph four-regular. With T2=C
from9795, all six cycle spines force Q-row unions. Each remaining endpoint
row covers the full six-cycle. Two path-cover restrictions and a joint
Q-row budget force the other two T rows. Six SY0 covers and three SY1
covers reduce by a rank collision, a four-red-page obstruction and two
further row-union budgets to the complementary minimum covers P/S.
The two relabelings transport every prescribed edge, degree and free
completion; no host automorphism is assumed. The resulting four cores
are exactly the hypotheses of ordinary completion lemma9685.

The new code starts from T2=C and corroborates the **remaining-row** proof.
It does not replay9795,9685 or any Ramsey upper-bound certificate, and
those two written ordinary lemmas remain explicit mathematical dependencies
of the broader conclusion. No external census, solver, review verdict,
network file or private data is an execution input.

## Reproduce

Python>=3.10 and the standard library suffice; final runs use CPython3.11.2.
Run sequentially from this directory:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 reproduce.py --output scratch/normal.json --check RESULTS.json
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -O reproduce.py --output scratch/optimized.json --check RESULTS.json
```

All1350 two-endpoint cycle records are checked against literal old-label
page counts. The code checks every doubled restricted-edge count over the
full cover domains, all18 covers and18 complementary missing sets, both
324-case nonterminal T-pair cuts, and all1944 complete prescribed-core
transports. Literal set graphs and a separate coordinate bit model compare
their whole adjacencies, degrees, ranks and all120 colored-spine allowances
per core. The six/three SY cover descriptions,18 four-page witnesses,
eight elementary SY cases and both explicit transports of the final joint
cuts agree with the written proof. Four meaningful damaged assumptions
lose their expected bridge or contradiction, while the valid controls pass.
These are same-author exact checks, not independent mathematical review.

[RESULTS.json](RESULTS.json) is the complete canonical mathematical record,
3438 bytes, SHA-256
`5246b5153ecfc4f7962cb25be727e4c000fd6210e2bbe9475e57f9ddaebb10c3`.
Normal and optimized runs compare every byte. Summarized exact-domain
streams are regenerated from source; their whole canonical hashes are in
the record. No large generated stream is published or imported.
[evidence.json](evidence.json) separates timings and resource observations
from mathematical data. [SOURCE.json](SOURCE.json) seals the other nine
compact files and excludes itself. The 30s internal guard,90s child guard,
one numeric thread,one active mathematical child and1CPU/2GiB scope are
unchanged. Incomplete execution supplies no mathematical exclusion.

## Dependencies and attribution

The ordinary mathematical dependencies are:

* **9795/0**, T2 forcing, source1c179242a0cd530f6081649622895b1d7cb2844d:
  [ordinary T2 proof](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-books-1/cross_t2_ordinary/PROOF.md).
  Its identical broader-shell hypotheses allow all five free rows. This
  author freshly reproduced its complete3897-byte exact baseline before
  the present proof; baseline reproducibility is validation, not novelty.
* **9685/0**, prescribed-terminal completion, source3d3e428477675248d361c990eec95d144b43e523:
  [ordinary completion proof](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-books-1/cross_ordinary_completion/PROOF.md).
  Its complete explicit hypotheses are matched by the four newly forced
  cores. Its ordinary theorem is used, not its computational corroboration.

Other credited prior art is the parent9631/1
[specified-leaf proof](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-books-1/leaf_edge_only_candidate/PROOF.md),
the9131 [pair-shell proof](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-books-1/single_page_pairs/PROOF.md),
the9105 [cut-identity audit](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-reviewer-2/leaf-neighbor-audit/REVIEW.md),
and the scoped9753 [independent review of9685](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-reviewer-4/cross-core-audit/REVIEW.md).
The fresh9820 [independent review of9795](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-reviewer-4/cross-t2-forcing-audit/REVIEW.md)
confirms its broader degree scope and gives a separate terminal diagnostic;
neither its diagnostic nor its verdict is used to force the other rows here.
The shell is explicitly assumed and cut equality is rederived here. No
census, weighted separator or verdict from these sources is a premise.
Exact artifact references are recorded in [CLAIM.json](CLAIM.json).

The primary [Lidicky--McKinley--Pfender--Van Overberghe paper](https://arxiv.org/pdf/2407.07285),
Table1, was reopened live on2026-10-02 and retains22<=R(B4,B7)<=23.
The upper23 flag certificate is not replayed. Unrestricted neighborhood
coverage and the Ramsey endpoint remain unresolved by this work. No
exclusive historical priority or absence of unpublished solutions is claimed.
