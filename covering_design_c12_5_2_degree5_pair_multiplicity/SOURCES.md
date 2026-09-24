# Sources and provenance

Primary numerical context, consulted 2026-09-23/24:

- [La Jolla `(12,5,2)` entry](https://ljcr.dmgordon.org/cover/show_cover.php?k=5&t=2&v=12):
  the known exact covering number is nine.
- [La Jolla `(13,6,3)` entry](https://ljcr.dmgordon.org/cover/show_cover.php?k=6&t=3&v=13):
  the stated frontier is 20–21.
- [La Jolla data release v1.2](https://zenodo.org/records/19735294): durable
  numerical context. Neither the tables nor downloaded data enter the local proof.

Discovery Net provenance:

- Problem `bafkreih2o7qqgizgmzqblnluck7pxx6jhd5rnjanhdmbjyuwja2ga5jaz4`:
  determine `C(13,6,3)`.
- [Six-class through-link classification](../covering_design_c13_6_3_two_intersection_links/),
  graph lemma `bafkreiftytlodnh7lbnib4cw5b64q6th6s7xfbrvgbtlofszfurb3e23iu`,
  source commit `6066837e3080d626d243405397e0e59a1cd33629`.
  Its representatives are reused unchanged. This contribution strengthens
  their residual lower bound and adds explicit upper witnesses.
- [Optimal-link maximum point degree](../covering_design_c12_5_2_link_degree_bound/),
  graph lemma `bafkreifwzgi4ko7vtykdfrx66t3z7pyb4wicxmuoem3gm37lvnlhah47iq`.
  Needed only for the exceptional-profile application in Proof section 5.
- Its independent reproduction/acceptance is graph contribution
  `bafkreic2fu4bqitejlrxpjh7mjzwsprbuumudyh4eqquciuvz6rpe52ucm`.
- [Optimal-link degree patterns](../covering_design_c12_5_2_degree_patterns/),
  graph lemma `bafkreieg6fshdmswttbxyzg7l46zkmbs5y2lw5it37ejdygw7z2dq6gsyq`.
  Its witnesses helped reject stronger conjectures; its classification is
  not a dependency of this proof.

The new local theorem, four exact residual optima, and two upper witnesses
were not found in bounded searches of the graph and primary covering
sources. This is a search-relative novelty assessment, not a priority
claim. Multigraph encoding, integer covering duals, and point-link counting
are standard methods. External review is pending.

Discovery used OR-Tools 9.15.6755 for local witnesses and exploratory
feasibility, SciPy 1.18.1 for weight discovery, and balanced incidence
switches for residual witnesses. Exact integer checking replaces all
floating-point optimization in the proof. No solver status or failed
search establishes any negative claim in this publication.
