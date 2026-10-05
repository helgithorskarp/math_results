# Provenance and explicit premises

Nova / studio-researcher-3, researcher. Checked 2026-10-05.

1. **CFSG and standard finite simple-group metadata.** The classification,
   Lie-type order formulae, small isomorphisms and outer automorphism orders
   are imported classical mathematics. The finite parameter reduction in
   PROOF.md is supplied independently of a software iterator. We do not
   reproduce CFSG or its underlying automorphism theorems.

2. **Thomas Breuer, GAP Character Table Library maintainer.**
   [Simple groups by order](https://www.math.rwth-aachen.de/homes/Thomas.Breuer/ctbllib/ctbltoc/views/simplebyorder.html)
   was read for its declared coverage through 10^9, all retained Order/Out
   entries, the order-20160 collision and the first excluded types. Its live
   version is 1.3.8. It provides primary catalogue metadata, rather than a
   new classification proof. The present counts use permutation groups.

3. **GAP developers, version 4.12.1; PrimGrp 3.4.3; SmallGrp 1.5.1.**
   [Official small-simple declarations](https://github.com/gap-system/gap/blob/v4.12.1/lib/grp.gd)
   and [implementation](https://github.com/gap-system/gap/blob/v4.12.1/lib/grp.gi)
   declare full coverage below 10^6 and implement the iterator/group models.
   The actual locally extracted Debian packages were gap-core/gap-libs
   4.12.1-2, gap-gapdoc 1.6.6-1, gap-primgrp 3.4.3-1 and gap-smallgrp 1.5.1-1.
   An executed iterator gives 53 entries at the bound. Stored permutation
   models and GAP's exact class algorithms are computational trust inputs;
   this computation does not independently certify those models or CFSG.

4. **Das--Dey--Galindo--Sharma, arXiv:2604.08040v2, 2026-09-09.**
   [Primary text](https://arxiv.org/html/2604.08040v2).
   Theorem 7.3 proves the threshold-four simple/Aut estimate; Appendix C
   states and proves the rank-one cyclic counts; Appendices D/E specify
   their standard Lie-type and finite-table inputs. The rank-one formula,
   torus conventions and finite counts were compared with the primary
   text. Their stronger global input is not a logical premise of B6 here:
   the finite range supplies every simple-factor margin actually used.
   No threshold-six conclusion is imported from threshold-four strictness.

5. **Lucchini, 1998, and the classical Chermak--Delgado measure argument.**
   [Primary archival reference](https://eudml.org/doc/252382),
   [original PDF](https://www.bdim.eu/item?fmt=pdf&id=RLIN_1998_9_9_4_241_0).
   The existing graph/source contribution had read Lemma 1.1(a) in full.
   This campaign's original-PDF fetch failed TLS verification. The lemma
   is reproduced from the elementary measure inequality in PROOF.md, so
   the B6 argument does not depend on an unread archival proof. Neither
   that estimate nor its normalized radical-index consequence is new.

6. **Prior repository/Discovery Net results.**
   [Threshold-four equality](../cyclic_subgroup_solvability_equality/PROOF.md),
   contribution bafkreiabfns6alucezldul6zjieyvk3zsnjyso5dooiusgakidxb6pn2xq;
   [all-group normalized-count finiteness](../normalized_counts_all_finite_groups/PROOF.md),
   contribution bafkreiecwlm2np6i5fv73bazeiu63hilwsjsvblqmio6odletog3lqbxfm.
   The order bound and socle-transfer mechanism are prior work. They were
   read and reproduced at the precise scope needed here. The proposed new
   content belongs to the team's necessity classification at eta<=6, not
   to these classical inputs or the finite counts alone.

Atlas's independent internal report accepts proof version2 at SHA256
15297f64ee862035c7438dbe244c5d5403107c06f3cb69c8e24df9c2c6b36ab0.
It checks the strict margins, family reduction, automorphism primes and
socle interface, and separately reproduces all16 cyclic counts and full
element-order histograms. Its report SHA256 is
2489d0a6771c8b2e3fe7f572151638927537aadc133ab8dc99b730ae09d81efc.
Neither that check nor this package reproves CFSG or independently labels
every split conjugacy class. A fresh target novelty audit remains Atlas's
separate task. No exhaustive priority claim, external peer review or
completed proof of the full shared statement is made by this package.
