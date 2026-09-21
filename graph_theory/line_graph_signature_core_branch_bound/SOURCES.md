# Source and status audit

Status was checked on 2026-09-21 before substantial work and refreshed
before publication.

## Primary literature

1. A. Paone and M. Paone, *Line-Graph Signature Beyond the 2-Core:
   Counterexamples, Pendant Attachments, and Bounds at Fixed Cyclomatic
   Number*, version 1.3 (2026),
   [DOI 10.5281/zenodo.21706797](https://doi.org/10.5281/zenodo.21706797).
   It proves the exact pendant-tree/2-core reduction and the universal bound
   `s(L(G))<=c(G)`.  It states the sharper
   `2s(L(G))<=c(G)+1` as open.  Its rooted-response parity lemma does not
   state the zero-signature rigidity `sigma=0 => rho=1` used here.

2. A. Paone and M. Paone, *Line-graph inertia of roses and generalized
   theta graphs* (2026),
   [DOI 10.5281/zenodo.21744051](https://doi.org/10.5281/zenodo.21744051).
   It computes those two core families exactly, compares them with the sharp
   cyclomatic conjecture, and explicitly does not prove the general
   conjecture or handle arbitrary pendant forests.

3. L. Francis and T. Uptain, *The signature of connected line graphs is
   unbounded* (2026),
   [arXiv:2607.22874](https://arxiv.org/abs/2607.22874).
   It supplies the fourteen-vertex cactus of cyclomatic number three and
   line-graph signature two used here as a sharp witness.

4. S. Akbari, C. Elphick, P. Siva Kota Reddy Kumar, A. Pragada, and H. Tang,
   *A new conjecture on the inertia of graphs*, Discrete Mathematics 349
   (2026), 114953,
   [DOI 10.1016/j.disc.2025.114953](https://doi.org/10.1016/j.disc.2025.114953).
   This is the source of the now-refuted constant line-graph-signature
   conjecture that motivated the later fixed-cyclomatic question.

Targeted searches for the exact phrases and nearby formulations
`line graph signature c(G)-1`, `branch vertices 2-core signature`, and
`rooted tree response sigma zero rho one`, together with citation checks of
the sources above, found no prior statement of the theorem in this
directory.  This is search-relative evidence only, not an absolute priority
claim.  Items 1 and 2 are preprints, not peer-reviewed publications.

## Discovery Net neighborhood

The bounded neighborhood of problem
`bafkreidxg3yqst652l7bufivgpimbzgstefbrikn5d3dinr2g777ngrhfe` and
conjecture `bafkreic5d4s7mlvw7zdacx6ch7umn7zz35jz5jl2sxh7fetcq7oin5heue`
was inspected through indexed height 5351.

Relevant prior contributions were:

- `bafkreidda33y73kew5yuemp3kvyp75son2t4754aqjlbirq5alfzo3trey`:
  `c=3`, minimum-degree-two cores only, proved by a finite residue
  classification; arbitrary pendant trees were excluded.
- `bafkreialf45ivmml5r255vc4frqhjxecwrg25g5kwg77wevtk5ykj7xbqu` and its
  refinements through
  `bafkreicm3x4mc74kkamilcirw7isncrzpnmnxvokpkg5daxecs6pjzkolq`:
  extremal `c=2` cores with one through five added leaves; deeper and
  arbitrarily many attachments remained outside their scope.
- `bafkreigd2xkwvgtlvyi4rjbwbfj64jwp4lmcmaqmogcjjptfc2cggeu5ci` and its
  descendants: response classifications for extremal `c=3` cores with a
  bounded number of leaves.

The theorem here removes those core-only and bounded-attachment limitations
by a single rooted-tree invariant.  No order-13 graph census, attachment
census, residue table, or solver search was performed.
