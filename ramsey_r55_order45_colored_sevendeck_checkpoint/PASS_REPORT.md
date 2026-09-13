# Pass 7 report: colored induced seven-deck trial

- Researcher: `general-researcher-4`
- Started: `2026-09-12T23:24:52Z`
- Closed: `2026-09-13T01:37:59Z`
- Outcome: **failed pass; no certified occurrence bound**
- Required next action: 2700-second cooldown, then approach change away
  from the unresolved order-seven LP and toward the `beta(22) <= 109` gate.

## Start-of-pass audit

- Frontier read in full:
  `/scratch/research-team-general-20260910/workspaces/general-orchestrator-1/r55-campaign/frontier-20260912.md`
  with SHA-256
  `c848da3dd1b3ef0a9312e66f8d3b6146c12080925ee3a3f2c669561a63e4f8a6`.
- Latest full principal report read in full:
  `/scratch/research-team-general-20260910/state/work/general-principal-1/reports/20260912T224126.355942Z.md`
  with SHA-256
  `0a9010ed2899829526623fd8cec8ff80da2a99ad170961721e33c282e205e8a5`.
- Exact height-3501 neighborhood-occurrence reduction reread:
  `bafkreicgpqb2vyw2qtelysclrfyt6f2rljwzybt3a6f2wgotwgobtb75oy`.
- Accepted height-3527 review/correction reread:
  `bafkreifxpqqpaifsozor24am6dnux7sczu2yhmrbmjqafjy5wakhob5qpu`.
- Incoming relations were queried; no new relevant accepted objection or
  correction was present at indexed height 4363 (node height 4364, frozen).
- The repository was fetched and fast-forwarded cleanly to `e8a1916` before
  this pass began.
- Imported catalogue boundary refreshed: the complete `(4,5,24)` catalogue
  has 352,366 graphs; its `e>=126` tail has 15,913 graphs represented by
  10,009 aggregate four-deck rows.  The aggregate tail file has SHA-256
  `66485ac032414af7972302e2bb12fbbe381724a40ec92732f6447e7b89f06111`.

## Work completed

1. Defined the complete symmetry-free colored induced-deck occurrence family
   through order seven at a degree-24 root.
2. Canonically enumerated 74,332 valid colored types through order seven.
3. Joined the pure-neighborhood four-deck to the exact convex hull of the
   complete dense order-24 catalogue tail.
4. Added exact one-vertex deletion marginals for both colors and the full
   order-20 complementary-nonneighborhood edge window.
5. Found that raw-count HiGHS scaling gives an untrustworthy infeasibility
   status.  Recast the same equations in probability form with coefficient
   range `1e-2..1`; normalized full runs timed out and produced neither a
   primal point nor a dual ray.
6. Verified positive controls: order six, individual order-seven color
   compositions, the central pair and triples, and the central four-slice
   system `a={2,3,4,5}` all remain feasible at the relaxed sum 232.
7. Exported the complete normalized system as a literal-rational LP with
   84,341 variables, 10,619 rows, and 574,669 nonzeros.
8. Built SoPlex 9.0.0 at pinned commit
   `7418b737e675b0f533e8743c2992763c318a911b` with Boost 1.74.0 and GMP
   6.2.1.  Rational-read/automatic-exact-check runs timed out after 68,290
   (Devex/bound-flipping) and 93,391 (Devex/Harris) iterations without a
   decision.

## Mathematical status

Every actual dense order-24 occurrence at a degree-24 root maps into the full
normalized LP.  Therefore an exact infeasibility certificate would imply
`beta(24) <= 125`, and with the imported `beta(20) <= 100` would close the
first order-45 gate.  No such certificate was obtained.  Nor was a complete
full-LP pseudomodel obtained.  Accordingly:

- no claim about `beta(24)` is made;
- no order-45 inequality is certified;
- no Ramsey bound is improved;
- no Discovery Net contribution is submitted for this failed pass.

The raw-count infeasibility messages are explicitly rejected because the
equivalent normalized primal/dual systems did not validate them.

## Approach decision

The contracted whole-inequality threshold was not met.  Continuing to tune
the same full seven-deck LP would not constitute the required approach
change.  After cooldown, begin a new pass at the symmetric order-22 gate
`beta(22) <= 109`, first refreshing its complete catalogue boundary and
deriving order-specific occurrence constraints.  Retain this package only as
an exact resumable checkpoint in case an external exact-LP improvement later
makes the seven-deck system decidable.
