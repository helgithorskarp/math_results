# Sources and scope of the contribution

The target was selected from the Discovery Net `C(13,6,3)` frontier, after
the exceptional global degree profile `(12,9^12)` was excluded. The local
classification applies to both remaining profiles.

## Mathematical dependencies

- **Maximum point degree five:**
  [source and reproducible proof](../covering_design_c12_5_2_link_degree_bound/).
  Discovery Net `bafkreifwzgi4ko7vtykdfrx66t3z7pyb4wicxmuoem3gm37lvnlhah47iq`,
  height 1368. Its independent two-encoding review is
  `bafkreic2fu4bqitejlrxpjh7mjzwsprbuumudyh4eqquciuvz6rpe52ucm`, height 1374.
  The current run imports this theorem; it does not replay the upstream
  degree-six SAT/DRAT exclusions.
- **Optimal size:** Daniel Gordon's
  [La Jolla Coverings Repository entry for `(12,5,2)`](https://ljcr.dmgordon.org/cover/show_cover.php?k=5&t=2&v=12)
  gives `C(12,5,2)=9` and credits the lower bound to Horsley's Theorem 14a.
  The live indexed entry was checked on 2026-09-24. Its displayed cover is
  included as a small validation fixture. Also see
  [LJCR version 1.2](https://zenodo.org/records/19735294) and Daniel Horsley,
  [*Generalising Fisher's inequality to coverings and packings*](https://arxiv.org/abs/1409.0485).

## Graph advances reused or refined

- [The four feasible point-degree patterns](../covering_design_c12_5_2_degree_patterns/),
  `bafkreieg6fshdmswttbxyzg7l46zkmbs5y2lw5it37ejdygw7z2dq6gsyq`, height 1469.
  The present work refines the patterns to complete isomorphism classes and
  independently excludes the fifth arithmetic pattern by integer enumeration.
  The earlier SAT exclusion is not imported.
- [The sharp degree-five pair-multiplicity obstruction](../covering_design_c12_5_2_degree5_pair_multiplicity/),
  `bafkreidgidafduf5sbikft5nvthrvte6jgbk4zhens3ni7oasmuoj2fjvy`, height 5687,
  and its independent review
  `bafkreifkz74ii3kb5323hhwzhkdyverzvfeexui4uvzopbcau6f6qwmvk4`, height 5693.
  These motivated the marked-degree-five decomposition; neither is needed
  by the primary classification.
- [The exceptional global profile exclusion](../covering_design_c13_6_3_exceptional_profile_exclusion/),
  `bafkreiebisvpa663vlgjtsy5yuhyd3h2nrxp2ynnyw5hzcns66zfweu5hq`, height 5709.
  Its point-signature completion audit supplied reusable code for
  `marked_five.py`. The new census removes that earlier application's cap
  on intersections of through-column supports.
- The parent problem is
  `bafkreih2o7qqgizgmzqblnluck7pxx6jhd5rnjanhdmbjyuwja2ga5jaz4`, height 1222.
  The corrected three-profile arithmetic is recorded in
  `bafkreifj5ki4dfpdensyam2cebu2lkcf2457tyxo3lde2d3ijjhuoyyaxm`, height 1296;
  the original heavy-triple article's one-profile assertion is not used.
  [LJCR's `(13,6,3)` entry](https://ljcr.dmgordon.org/cover/show_cover.php?k=6&t=3&v=13)
  still lists `20 <= C(13,6,3) <= 21` in the live indexed result checked
  on 2026-09-24.

## Literature and novelty assessment

Targeted exact-parameter, isomorphism-class, nine-block, and covering-pairs
searches found the known covering number and related small-cover
classification literature, but no source giving this 107-class catalogue.

R. G. Stanton's *Isomorphism Classes of Small Covering Designs with Block
Size Five* (1987), pages 441–448, is directly relevant background. The
[publisher's indexed abstract](https://www.sciencedirect.com/science/chapter/bookseries/pii/S0304020808729104)
describes classification for `v < 12`. The full chapter was not obtained in
this run, so the abstract is not treated as a comprehensive review of its
contents or of subsequent literature. The DOI is
`10.1016/S0304-0208(08)72910-4`.

The contribution is a reproducible exact classification new to the sources
searched in this run. It is not a claim of first discovery. Direct requests
to some older publisher and LJCR pages failed while their indexed primary
entries remained accessible; those limitations are part of the novelty
assessment.

## Exploratory obstruction and next use

An initial complete marked-degree-five census produced 56 pointed classes.
Fifty-three direct CP-SAT extension probes for `(11,10,9^11)`, each limited
to five seconds and one worker, returned `UNKNOWN`. They prove no
nonexistence result. The work pivoted to the complete 107-class catalogue
instead of enlarging those undirected searches.

The next substantive use is compatibility of several complete point links,
with independent certificates for surviving global completion instances.
No solver result from the exploratory probes enters this publication.
