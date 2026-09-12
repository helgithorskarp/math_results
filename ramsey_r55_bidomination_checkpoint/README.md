# Complete good43 class with domination number four in both colors

The complete-class run ended **UNKNOWN after 900.474 seconds**. No good43 graph was found, no family was excluded, and no original task was retired. The first structural-feasibility milestone is **not met**. This directory preserves the failed proof attempt from researcher 1 pass 38; `RUN_RESULT.json` records the exact checkpoint. The 191874073-byte DRAT file is an unfinished trace, not an UNSAT certificate.

The question is whether every good43 graph (no clique or independent set of size five) has a dominating triple in at least one color. Its negation is exactly the class encoded here. The encoding has 903 physical edge variables, 988183 total variables and 4911724 clauses. It uses no catalog, prescribed automorphism, packing profile, edge count, or numerical Ramsey input. The sole label restriction places a red K4 first, which follows directly from the common-neighbor property of the tested class. See [METHOD.md](METHOD.md) for both directions of the reduction and the stopping gate.

## Reproduction

Python3.11.2, standard library only:

```sh
python3 check_controls.py
python3 bi_domination.py --n 43 --output /absolute/scratch/path/bi_domination43.cnf
/path/to/cadical -t 900 /absolute/scratch/path/bi_domination43.cnf /absolute/scratch/path/bi_domination43.drat > /absolute/scratch/path/bi_domination43.log
```

The generated CNF SHA256 must be `80d71dc1901166572cfe2864be91e48f026afc16e0eaedf83e92db3f07a9cb27`, with 137301312 bytes. Run in a fresh scratch directory; do not overwrite the retained checkpoint. The solver used was CaDiCaL 1.9.5, source commit 146207318796f094dcded87349a64f0c6927309e, executable SHA256 19dc7cc71b68d938e707eb0fab422470005616c68afddb0b9b52481e07efa049. A wall-clock cutoff is not a deterministic instruction budget, so a repeated run need not produce a byte-identical unfinished trace.

If SAT is reported, `python3 check_model.py /absolute/scratch/path/bi_domination43.log` checks the physical graph directly, independently of auxiliary witness variables. An UNSAT report must be followed by a complete DRAT check against the exact CNF; no theorem follows from an unchecked status or an incomplete proof. The archived DRAT-trim build is source 2e3b2dc0ecf938addbd779d42877b6ed69d9a985, binary SHA256 9c09fe813af0b52f58d923837a1bc3ca5e6017987c1e9530d62fa5b4f018412a.

## Controls

The explicit graphs of orders 29 and 37 satisfy all generated clauses. A graph of order 41 satisfies the domination condition but violates exactly 410 Ramsey clauses. C5[C5] satisfies the Ramsey conditions but violates exactly 1250 common-neighbor coverage clauses. Closed-neighborhood unions and generated clause evaluations agree; see `CONTROLS.json`. These are internal validation controls, not external peer review or a symmetry-family research claim.

The 137MB CNF, proof trace and verbose solver log remain in the researcher's scratch archive. Only source, hashes and compact summaries are published. No old pending Discovery Net transaction is resubmitted by this work.

Background: [Angeltveit–McKay, R(5,5)<=46](https://arxiv.org/abs/2409.15709), [McKay's Ramsey graph data](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html). No completeness of the known order 42 examples is assumed.

## Boundary decision

The complete domination-four class remains unresolved. The analytic link conditions did not produce a contradiction or a finite structural classification. Another raw solver run, a longer timeout, or proper-profile exclusions are not the next milestone. One pass remains in the renewed two-milestone trial; it must yield a direct complete-class consequence. If that cannot be demonstrated, the structural slot should be reassigned within R(5,5). No new mathematical Discovery Net claim is submitted for this attempt.
