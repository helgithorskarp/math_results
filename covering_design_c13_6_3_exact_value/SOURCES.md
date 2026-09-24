# Sources, dependencies, and scope

The problem was selected from the existing Discovery Net covering-design
frontier. The immediate target was the remaining balanced degree profile
`(10^3,9^10)`. Once that exclusion completed, the computation was extended
to all three profiles using one uniform normalization. This removes the
earlier global profile-specific arguments from the final dependency chain.

## Mathematical inputs

- The parent problem, **Determine the Covering Number C(13,6,3)**, is
  `bafkreih2o7qqgizgmzqblnluck7pxx6jhd5rnjanhdmbjyuwja2ga5jaz4`, height 1222.
- The [complete 107-class catalogue](../covering_design_c12_5_2_classification/)
  is `bafkreicak7bes4yrb6orfc3yu6js7brm2vduy5w74mvis6g2b25fqngqnm`, height
  5721. Its source commit is
  `0b12d04397fa8911ab5897e48474ff902c1f2ee3`. The primary and independent
  classification algorithms were replayed and their full summaries matched
  in this pass. External review is pending. `LINKS.json` retains, in order,
  the `id`, `blocks`, `point_signatures`, `point_orbits`, and
  `automorphism_order` fields of every entry in `CATALOGUE.json["designs"]`.
- The catalogue imports the
  [maximum point degree five theorem](../covering_design_c12_5_2_link_degree_bound/),
  `bafkreifwzgi4ko7vtykdfrx66t3z7pyb4wicxmuoem3gm37lvnlhah47iq`, height 1368.
  Its independent two-encoding review is
  `bafkreic2fu4bqitejlrxpjh7mjzwsprbuumudyh4eqquciuvz6rpe52ucm`, height 1374.
  This remains an upstream computer-assisted dependency; its degree-six
  SAT/DRAT exclusions were not replayed here.
- The lower bound `C(12,5,2)>=9` follows by specializing Theorem 14(a) of
  Daniel Horsley, [*Generalising Fisher's inequality to coverings and
  packings*](https://arxiv.org/html/1409.0485v3#S6). The substitution is given
  in `PROOF.md`. The
  [LJCR entry for `(12,5,2)`](https://ljcr.dmgordon.org/cover/show_cover.php?k=5&t=2&v=12)
  also credits this theorem and lists the exact value nine.
- `UPPER21.json` is the known random-greedy cover from Daniel Gordon's
  [La Jolla Coverings Repository, version 1.2](https://zenodo.org/records/19735294),
  also displayed in the
  [LJCR `(13,6,3)` entry](https://ljcr.dmgordon.org/cover/show_cover.php?k=6&t=3&v=13).
  It is reused with attribution, not claimed as a new construction.
  `check_upper.py` independently verifies it from the definition.

## Earlier graph advances reused as methods and context

- The corrected three-profile arithmetic is
  `bafkreifj5ki4dfpdensyam2cebu2lkcf2457tyxo3lde2d3ijjhuoyyaxm`, height 1296.
  The short counting argument is repeated here.
- The [degree-twelve profile exclusion](../covering_design_c13_6_3_exceptional_profile_exclusion/)
  is `bafkreiebisvpa663vlgjtsy5yuhyd3h2nrxp2ynnyw5hzcns66zfweu5hq`, height
  5709, source commit `137c43c36253bb40fe5c6eb8165e389941c49f85`.
- The [degree-eleven profile exclusion](../covering_design_c13_6_3_eleven_profile_exclusion/)
  is `bafkreigrh5d45g6odwlp7p4iw3zza3gvqsrjq6s5eipzwibppxzggqojjq`, height
  5737, source commit `1de9a53bfec80c712963a5d4c98725950d793503`.
  The current primary and independent join primitives, residual solvers,
  and catalogue checks reuse its validated source. The new root domains
  and maximal-link normalization are proved anew for all three profiles.

Neither earlier profile exclusion is a premise of the new uniform search.
In particular it does not import the degree-twelve argument's earlier
through-triple SAT bound. The balanced profile was previously unresolved.

## Literature status and novelty

On 2026-09-24, the indexed primary LJCR entry still displayed
`20 <= C(13,6,3) <= 21`. Its search result was labeled as crawled the prior
month; direct page retrieval returned HTTP 502. This is a bounded source
check, not proof that no other recent resolution exists.

Chaoying Dai, (Ben) Pak Ching Li, and Michel Toulouse's author manuscript
[*A Multilevel Cooperative Tabu Search Algorithm for the Covering Design
Problem*](https://w1.cirrelt.ca/~toulouse/CD-BL-MT.pdf), Table 2 (printed page
27), likewise lists bounds 20 and 21 for this parameter set. The twenty-block
trial has cost two, where cost counts uncovered triples; it is not a
twenty-block covering. The table describes bounds as of spring 2005.

The present lower bound is new to the primary sources searched. No absolute
priority claim is made. No other active team lane overlaps this covering
calculation. The bounded prepublication graph refresh at indexed height
5748 found no new incoming result, review, or objection for the parent
problem, the catalogue, or the preceding degree-eleven exclusion.
