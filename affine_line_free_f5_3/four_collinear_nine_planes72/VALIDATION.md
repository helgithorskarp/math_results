# Validation record

Author checks on 2026-09-26; independent review of this contribution is
pending. The earlier nine-plane frame received a separate accepting
[independent review](../nine_plane_frame72_review2/README.md), which is
not a review of the present result or of the later no-eight theorem.

The full new replay passed with Python 3.11.2 and GCC 12.2. Normal and
Python optimized modes gave byte-identical output. The two complete runs
together took 10.96 seconds; peak child memory, including compilation,
was 96.2 MiB in the observed environment. These are measurements, not
runtime guarantees.

Checks completed:

* all 33,554,432 labelled planar subsets, reproducing the 70-spectrum input;
* the 72-row, 463-column integer Farkas certificate, with minimum column
  slack zero and right-side scalar product -181596;
* an integral control satisfying the original 61 equations and every
  one of the 45 full quadratic plane-pair identities;
* every one of the 11,935 pairs of affine planes, occurring exactly once
  among 31 parallel classes and 775 line pencils;
* projective-plane incidences, the arithmetic in the twelve-point
  argument, and the known 70-point construction;
* the six explicit affine normalization maps and all 625 offset tuples:
  25 fourfold-concurrent, 400 triple-concurrent, 200 with no triple;
* both integer quotient controls, including all thirty line weights and
  four B profiles in each;
* rejection of a damaged Farkas vector and a damaged incidence control.

The optional corollary follows by intersecting the new lower bound
twelve with the teammate's proved upper bound twelve in both higher
moment ranks. Its moment classification is imported, not re-proved by
the new checker. Likewise, the prior mixed-plane and two-eight-plane
DRAT exclusions remain imported dependencies with their own replay
commands. No claim of a new full UNSAT result, a 72-point construction,
or a proof-assistant formalization is made.
