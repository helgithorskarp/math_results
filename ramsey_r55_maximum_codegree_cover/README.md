# R(5,5): maximum-codegree cover and first physical decision attempt

The complete four-frame physical attempt ended **UNKNOWN after 1200.5295
seconds**. The first whole-physical-class milestone is **not met**: no
physical subset was closed and no good43 was found. The 3039092736-byte DRAT
file is an unfinished trace, not a certificate. All 431 normalization cases
remain unresolved. This is R2 pass 37, separate from the parked
maximal-packing carrier. The published frontier remains 43 <= R(5,5) <= 46.

The exact normalized cover has 431 common-neighborhood cases in four major
branches, maximum monochromatic edge codegree 10,11,12,13. The first declared
physical subset is the union of four frames in the codegree-13 branch.
`PROOF.md` gives the cover, its trust boundary, and the exact four-way join.
No physical case has been closed by the compact controls in this package.

The full mixed-clique incidence method is insufficient on all four frames:
integer-checked rational feasible controls retain the required mass 27.
All four frames also occur in published good42 examples. A separate
degree-24/codegree-10 catalogue test retains 243 of 352366 neighborhoods;
it does not close that secondary declared subset. These are failed-method
findings, not new lower bounds, constructions, or global exclusions.

## Reproduction

The compact checks need Python 3.11 or later and its standard library:

    python3 -B ramsey_r55_maximum_codegree_cover/check.py

Expected output includes catalogue counts 313,105,12,1, four exact feasible
capacity controls, four verified published order-42 controls, and
431 unresolved physical cases. `CHECK.json` records the executed check.

To regenerate the complete four-frame physical input outside the repository:

    python3 -B ramsey_r55_maximum_codegree_cover/physical.py BULK_DIRECTORY
    python3 -B ramsey_r55_maximum_codegree_cover/audit_physical.py BULK_DIRECTORY/four_frames.cnf
    python3 -B ramsey_r55_maximum_codegree_cover/run_physical.py BULK_DIRECTORY --solver /path/to/cadical

The input has 785 variables, 1147284 clauses, and 50181326 bytes, SHA-256
`1ae0ddca878c96a3350ed2c51b70d5b0d6c3ded74603092abf31224e3bdf7049`.
The physical attempt uses CaDiCaL 1.9.5 with an ASCII DRAT output, a 1200-second
wall limit, a 4-GiB proof-file limit, and an 8-GiB address-space limit. Its
terminal status and artifact hashes belong in `RUN.json`; an incomplete trace
is never accepted as a proof. Bulk inputs and traces remain outside Git.

The optional floating discovery program requires NumPy 2.4.6 and SciPy
1.17.1: `discover_capacity.py --outdir BULK_DIRECTORY`. Re-running it is
unnecessary for the exact rational-certificate check. The separate catalogue
filter can be replayed with `catalogue24_filter.py /path/to/r45_24.g6` after
downloading the complete 17-MB primary input outside this repository.

## Primary inputs and inherited facts

* [McKay's Ramsey catalogue page](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html)
  explicitly lists all Ramsey(3,5) graphs of orders 10--13 and all 352366
  Ramsey(4,5;24) graphs. The small (3,5) inputs and their hashes are included.
  Catalogue membership is checked here; completeness remains the external
  published-enumeration premise. The page's old R(5,5) upper-bound prose is
  not used as the current frontier.
* [McKay and Radziszowski's R(4,5)=25 paper](https://users.cecs.anu.edu.au/~bdm/papers/r45.pdf)
  is primary context for the neighborhood method and small Ramsey inputs.
  Its original list of 350904 order-24 graphs was completed in 2016; the
  updated 352366-member catalogue is used for the secondary test.
* [Angeltveit and McKay, R(5,5)<=46](https://arxiv.org/abs/2409.15709)
  supplies the published upper frontier. That theorem is not a clause in
  the physical decision input.

The C13 transversal fact is inherited from committed Discovery Net result
`bafkreigzy3u3l43njmdksypj5r75j7nyew2vm6fs2mhs3v3ctkbnmikljq` and is reproduced,
not claimed as new. Earlier conditional c13 results and aggregate
counterexamples were inspected; none is silently imported as a global
exclusion. In particular no old order-5 automorphism premise is used.

No old pending graph transaction is resubmitted. No historical carrier input,
queue, proof, or computation is modified or restarted. No Discovery Net
mathematical claim is warranted merely by this cover or an unfinished run.

## Boundary decision

One of the three granted mathematical passes has been used, with zero earned
terminal milestones. The complete normalization, exact input interface,
rational barriers and unfinished trace are preserved. A mathematical change
is required before another decision attempt. Increasing the cap, restarting
this input, or reporting selected child certificates would not supply the
required terminal coverage. The next gate still requires repeated terminal
coverage across every major normalization branch or a complete branch closure
with its global join. No finishable whole-class residual has been established.
