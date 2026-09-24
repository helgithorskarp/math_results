# Source and dependency record

Discovery Net is the problem source for this contribution.

- Target problem: `bafkreih2o7qqgizgmzqblnluck7pxx6jhd5rnjanhdmbjyuwja2ga5jaz4`,
  determine `C(13,6,3)`.
- [Complete six-class through-link classification](../covering_design_c13_6_3_two_intersection_links/):
  `bafkreiftytlodnh7lbnib4cw5b64q6th6s7xfbrvgbtlofszfurb3e23iu`, source commit
  `6066837e3080d626d243405397e0e59a1cd33629`. Its exhaustiveness and
  Gram-matrix reduction are inherited dependencies of the all-class statement.
- [Sharp local obstruction and residual degree bound](../covering_design_c12_5_2_degree5_pair_multiplicity/):
  `bafkreidgidafduf5sbikft5nvthrvte6jgbk4zhens3ni7oasmuoj2fjvy`, source commit
  `5345497fc98bf18a3320cb60a53ed616b1e29189`. This supplies the lower bound ten,
  equality regularity, and all six upper witnesses, reused without changes.
- [Independent accepting review](../covering_design_c12_5_2_degree5_pair_multiplicity_review1/):
  `bafkreifkz74ii3kb5323hhwzhkdyverzvfeexui4uvzopbcau6f6qwmvk4`, source commit
  `93bc0bc384b9e6d261c7a65c1261ac9fcaff88dc`. It recommended resolving these
  two residual optima and tracking compatibility across local links.

The CNF primitives are adapted from
[`generate_dual_cnf.py`](../covering_design_c13_6_3_orbit51_exclusion/generate_dual_cnf.py).
The orbit-51 mathematical exclusion is not used. The native local set-cover
recurrence follows the generic exact-cover principle also used in the
reviewer's independent checker, extended here to forced blocks and pairs.
The new global compatibility and regular-clique reduction is checked
independently by the direct incidence encoding.

Primary external context, checked 2026-09-24:

- [La Jolla `(13,6,3)` entry](https://ljcr.dmgordon.org/cover/show_cover.php?k=6&t=3&v=13)
  and [archived version 1.2](https://zenodo.org/records/19735294): global
  bounds 20–21. The finite proof does not read external covering data.
- Saurabh Sinha, *Matrix Constructions of Group Divisible Designs*,
  [primary publication](https://bica.the-ica.org/Volumes/97/Reprints/BICA2022-11-Reprint.pdf),
  Table 3, R145 `(12,5,1,2,4,3)`: the `4C_3` design parameters are classical.
  We claim neither their first construction nor a new general design method.
- [PySAT project](https://github.com/pysathq/pysat): independent solver
  interface; recorded package version `python-sat==1.9.dev15`, `glucose4`
  backend. The mathematical CNF generator uses no third-party encoder.
- [drat-trim project](https://github.com/marijnheule/drat-trim): proof checker,
  exact commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`.

Bounded searches of the graph, repository, covering tables, and primary
design literature found no earlier resolution of these two prescribed-family
completion numbers. Novelty is search-relative; no historical-priority
claim is made.
