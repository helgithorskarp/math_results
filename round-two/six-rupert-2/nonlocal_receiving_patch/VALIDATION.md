# Completed exact validation

**six-rupert-2, researcher; 2026-10-01.** CPython3.11.2, standard library
only. One CPU job at a time; all numerical-library thread variables set
to one; unchanged1CPU/2GiB scope. No solver is a checker dependency.

The complete expected output was generated and frozen first. That
generation had no pre-existing fixture to compare and is not reported
as validation. Two later production commands then read the already
existing frozen record, compared every field, left it unchanged and
produced byte-identical complete stdout:

| Mode | Result | Wall seconds | Peak child RSS, KiB |
| --- | --- | ---: | ---: |
| `python3 -B check.py` | Complete frozen record matches | 3.839415 | 17772 |
| `python3 -O -B check.py` | Complete frozen record matches; identical to normal | 4.112761 | 20028 |

Wall times depend on the shared host. Each run used a55-second external
guard. Neither run timed out or had a resource failure. Explicit
exception guards remain active under Python optimization.

Frozen new expected SHA256:
`8e77162c285797be18865c3581ec4c0addf82efc805521121b61621cb0d8038a`.
New literal certificate SHA256:
`6496645f44c7e981b21f3a2856885d94be12de8ed9833afc8cba9b7eaf1740ea`.
Parent expected SHA256:
`5015eb1607328e522501c3e728c0514a483398e917e391c98ad1c8c581f58f4b`.
Parent certificate SHA256:
`a2427bb6e1fdaece00a960bdaf755b4f6a456935600dfdfd0eecb7d1d99fdbca`.

Each production command checks all six [pinned inputs](DEPENDENCIES.json)
and replays the **complete** published parent finite record, including
the parent's four damaged controls, before checking the patch.
New exact gates include4320 original receiver support comparisons at
four box corners,4176 strict nonincident-original comparisons,1152
strict listed-corner comparisons, the actual unit edges, physical norm
and translation-chart bounds, and240 full-body symmetry vertex matches.
The uniform matrix/weight gates give inverse bound12, normalized
weights>1/60 and Cayley contraction243/640. All six quadratic
projective-separation bounds remain positive after a rigorous transverse
loss budget. The explicit off-arc example is compared against the
entire projective parent arc by an exact squared-cosine inequality.

At each of the four box corners, an independent exact linear solve of
the stated five-weight correction checks its entry bound, normalization
and all six spatial force/torque components, for24 exact component
identities. These are formula-consistency checks. They do not prove
balance at intermediate receivers by sampling: the continuum result
uses the uniform inverse and weight estimates in [PROOF.md](PROOF.md).

All five new damaged controls reject:

- Replacing the transverse vector by the old tangent fails independence.
- Widening the raw transverse radius to1/1000 fails the positivity budget.
- Cropping an actual horizon corner fails an original support inequality.
- Advertising a weight lower bound1/50 fails the normalized-weight budget.
- Enlarging the relative source Cayley radius to1/4000 fails contraction.

This validation certifies finite hypotheses and reproducibility of the
written unformalized proof. It is not independent review, a proof-assistant
formalization, an exhaustive motion search, or a global J74 resolution.
Unpublished floating ray searches are neither required nor used to check
the theorem. No private data, ledger or large proof corpus is needed.
