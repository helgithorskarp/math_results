# Validation record

Actual agent: six-reviewer-3. Role: independent mathematical reviewer.
Date2026-10-01; CPython3.11.2 standard library, one mathematical process
at a time and all BLAS/OpenMP thread counts one. No solver or CAS.

Final independent normal and `-O` runs exit0 and agree on every receipt
field, SHA256 `7fb10b7945f9884e789540285c48eaa55bff9b3672516386b251087764a7fb02`.
Elapsed times11.539s/13.189s; cumulative child peak-RSS upper bounds
26064/26436KiB. These are observations, not runtime guarantees.

Coverage:

- Complete33 symbolic records:15 leading determinants and18 weighted
  Gershgorin fractions, checking all357 author coefficients, exact
  polynomial/rational identities, denominators, entry signs and kernels.
- Independent Newton reconstruction with proved entry degree<=9,
  size-k minor degree<=9k and weighted-margin numerator degree<=12;
  constant-direction and2s-mode identities checked coefficientwise.
- Literal q2..7 matrices, orders23,32,42,53,65,78: downset/support,
  row sums, full and core lower/upper PSD and ranks, forced kernels.
  q2/3/4 numerator hashes and denominators match original author records.
- At q4/5/6,65/79/94 overcomplete projector-column actions, with full
  span ranks41/52/64;238 columns total. Edge projector identities,
  PSD/rank and incident row sums are checked.
- Complete compatible-triple extension of every intersecting pair
  subfamily at q2..7:76,192,456,1045,2344,5186 cases,9299 total;
  exactly four maxima each, with the singleton case handled by stars.
- Full rational eigenvector identities and projected full upper-gap PSD
  checks at q4..7, and rational strengthened U-gap PSD checks there.
  Spectral scalar records at q4,5,6,7,24,25,32,100,1000; complete finite
  q4..24 threshold test plus positive shifted cubic for all q>=25.
- Five product forced-Gram checks: (2,2),(2,3),(4,4),(2,3,2),(3,5,3).
  Their full product matrices and spectra are not computed. Exact product
  endpoint, equality and upper-gap statements are proved in REVIEW.md.
- Twelve rejected controls for invalid domains, inexact/incomplete/
  duplicate boundary inputs, changed certificate coefficients, indefinite
  matrices, negative polynomial coefficients and an excessive gap.

Independent arithmetic uses hash-pinned reviewer8682 Bareiss routines,
not author code. Author boundary weights are untrusted supplied rational
inputs, fully checked for the two boundary instances. Author sign and
result files are comparisons. In particular author C/U characteristic-
polynomial hash fields are not recomputed by this independent checker.

Separately replaying the entire pinned13-file author package normally and
with `-O` passes in3.753s/4.256s (cumulative child peak-RSS upper bounds
19068/20912KiB). Both reproduce the author's mathematical-record hash
`96e033843bd8c31faf2bd3518d292bec5137a5580bc96f1fea5579f40cdad383`,
33 sign records,41 original action-basis columns,26 damaged controls and
four positive controls. These are author replays, not extra independent
methods or a replacement for this audit.

No assertion is a proof obligation. Python exact arithmetic, this code,
its pinned toolkit and the written ordinary mathematical bridges remain
the trust boundary. Finite literal checks do not extend to untested
parameters without those bridges. Nothing is formalized in a proof assistant.
