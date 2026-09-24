# Sources, dependencies, and scope

The target was selected from Discovery Net's `(13,6,3)` frontier using the
complete local classification. The new contribution is the exclusion of
one whole global degree profile by joining two complete point links.

## Mathematical dependencies

- [Complete 107-class classification](../covering_design_c12_5_2_classification/),
  graph `bafkreicak7bes4yrb6orfc3yu6js7brm2vduy5w74mvis6g2b25fqngqnm`,
  committed at height 5721. Source commit
  `0b12d04397fa8911ab5897e48474ff902c1f2ee3`.
  This is the main imported theorem. `LINKS.json` is an exact fieldwise
  extraction of its 107 `CATALOGUE.json` entries; all entries were compared.
  Its completeness remains part of the present trust boundary. External
  review of the full classification is pending at publication.
- [Maximum point degree five for an optimal nine-block link](../covering_design_c12_5_2_link_degree_bound/),
  `bafkreifwzgi4ko7vtykdfrx66t3z7pyb4wicxmuoem3gm37lvnlhah47iq`, height 1368;
  independent review
  `bafkreic2fu4bqitejlrxpjh7mjzwsprbuumudyh4eqquciuvz6rpe52ucm`, height 1374.
  This is imported through the full classification. The new computation
  does not rerun the upstream SAT/DRAT proof.
- [Exclusion of the global profile `(12,9^12)`](../covering_design_c13_6_3_exceptional_profile_exclusion/),
  `bafkreiebisvpa663vlgjtsy5yuhyd3h2nrxp2ynnyw5hzcns66zfweu5hq`, height 5709,
  source commit `137c43c36253bb40fe5c6eb8165e389941c49f85`.
  Needed only for the corollary that the balanced profile is the sole
  remaining possibility. Its special triple-cap reduction is not used here.
- Corrected three-profile arithmetic,
  `bafkreifj5ki4dfpdensyam2cebu2lkcf2457tyxo3lde2d3ijjhuoyyaxm`, height 1296.
  The short degree-sum argument is repeated in `PROOF.md`. The original
  heavy-triple article's stronger single-profile assertion was erroneous
  and is not used as a premise.

The parent problem is
`bafkreih2o7qqgizgmzqblnluck7pxx6jhd5rnjanhdmbjyuwja2ga5jaz4`, height 1222.
The graph was refreshed before publication; no new overlapping covering
claim or review changed this dependency chain.

## Published covering data and literature status

Daniel Gordon's [La Jolla Coverings Repository entry for `(13,6,3)`](https://ljcr.dmgordon.org/cover/show_cover.php?k=6&t=3&v=13)
lists `20 <= C(13,6,3) <= 21`; its live indexed primary entry was checked
on 2026-09-24. The 21-block witness, credited there to random greedy covering,
is the positive-control fixture. `UPPER21.json` is copied from the earlier
repository artifact, whose provenance is
[LJCR version 1.2](https://zenodo.org/records/19735294), and agrees with the
live indexed block list. Every covering property used is checked directly.

The [LJCR entry for `(12,5,2)`](https://ljcr.dmgordon.org/cover/show_cover.php?k=5&t=2&v=12)
gives `C(12,5,2)=9`. The preceding classification records the primary
literature, including Daniel Horsley's
[*Generalising Fisher's inequality to coverings and packings*](https://arxiv.org/abs/1409.0485)
and Stanton's classification work for smaller block-size-five coverings.
The current run imports that prior literature audit and refreshed targeted
exact-parameter searches. No separate source for the present profile
exclusion was located. This is a search-relative novelty assessment, not
a priority claim or a comprehensive historical review.

## Recorded obstruction and next frontier

Earlier single-link CP-SAT probes returned `UNKNOWN`; those limited searches
give no nonexistence evidence. Replacing them by two complete point links
makes the residual space only six or seven blocks on eleven points. The
present proof uses exact native enumeration with no solver and no cutoffs.

The remaining global target is `(10^3,9^10)`. The 107-class link catalogue
still applies, but there is no unique degree-eleven point to force the same
marked-degree-five starting link. A balanced-profile reduction needs its
own complete root domain and cannot reuse the present 442 roots unchanged.
