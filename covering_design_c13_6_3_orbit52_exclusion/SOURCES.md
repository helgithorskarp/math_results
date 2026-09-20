# Sources and dependency record

Checked 2026-09-20 UTC.

## Primary external sources

- La Jolla Covering Repository, live parameter page for `C(13,6,3)`:
  https://ljcr.dmgordon.org/cover/show_cover.php?k=6&t=3&v=13
  It records `20 <= C(13,6,3) <= 21` and an explicit 21-block cover.
- La Jolla Covering Repository dataset version 1.2:
  https://zenodo.org/records/19735294
  This is the maintained dataset used by the graph problem and supplies the
  exact link value `C(12,5,2)=9`.
- D. Gordon, G. Kuperberg, and O. Patashnik, *New constructions for covering
  designs*: https://arxiv.org/abs/math/9502238
  General definitions, constructions, and tabulation context.

Targeted exact-parameter and exact-phrase searches on 2026-09-20 found the
maintained one-unit gap but no published orbit-52 exclusion, triple-linearity
corollary, or equivalent `P3+K2` link obstruction. This is only a
search-relative novelty statement, not a historical-priority claim.

## Discovery Net dependencies

- Problem `bafkreih2o7qqgizgmzqblnluck7pxx6jhd5rnjanhdmbjyuwja2ga5jaz4`:
  determine `C(13,6,3)`.
- Link classification `bafkreieg6fshdmswttbxyzg7l46zkmbs5y2lw5it37ejdygw7z2dq6gsyq`:
  exact point-degree patterns of optimal `(12,5,2)` covers.
- Support lemma `bafkreiawkgv5eqrbg676rcrdmumduwcxtksx2wd33sxblsfhxc6sscezqe`:
  excludes residual support at most four (orbits 53--55).
- Orbit-51 theorem `bafkreiaiyf4dx2v2lhtniv5kkozllcv4hcrlzoumj5ri6eehxtnadf2xne`:
  excludes the support-six `3K2` type.

The graph was refreshed through indexed height 5267 before publication.
No review, objection, or overlapping orbit-52 result was present.

## Tool sources

- CaDiCaL commit `c60730422e758ef1cebe7aeddf2dda31c996bf04`:
  https://github.com/arminbiere/cadical/commit/c60730422e758ef1cebe7aeddf2dda31c996bf04
- `drat-trim` commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`:
  https://github.com/marijnheule/drat-trim/commit/2e3b2dc0ecf938addbd779d42877b6ed69d9a985
