# Validation and trust boundary

`derive.py` exhausts every integer signature population
`n_0+n_1+n_2+n_3=39` satisfying `n_3<=16` and
`n_1+2n_2+3n_3>=4(d-3)`. For each `d=18,...,24`, it independently recovers
the sharp projected maximum `n_0=53-2d` and records every extremal row.

`controls.py` checks all 36 assignments in the primitive equivalence truth
tables. A direct unit propagator verifies all seven contact strata:
one excess noncontact conflicts, while equality forces every remaining
outside vertex to contact the block. It also checks both boundaries of the
18--24 degree window and all four directions needed from a 43-input global
degree guard. These checks run no search solver.

`audit.py` imports no producer module. It verifies the hash-locked h3899
clause prefix, independently reconstructs every degree-counter, degree-window,
global-guard and contact-stratum literal, rejects out-of-range, repeated and
tautological clauses, and checks the exact header, width, byte size, and hash.
Normal and optimized audits must agree with [FORMULA_AUDIT.json](FORMULA_AUDIT.json).
`integration.py` also instantiates the generic suffix in one representative of
each of the 18 h3887 macro classes and checks the added dimensions exactly.

The exact per-block projection in [SIGNAL.json](SIGNAL.json) compares binary
contact patterns only. Different block projections share physical edges, so
their counts must not be multiplied or described as physical graph counts.
The three-earlier unconditional conflict and the guarded higher-degree
boundaries are exact propagation signals; no wall-time conclusion is made.

Logical trust consists of the established `R(4,5)=25` degree window, the
displayed unformalized signature argument, and the existing h3887/h3899
physical-family premises. Computational trust consists of the pinned source,
CPython integer and file semantics, SHA-256, and ordinary hardware. The h3657
argument was independently accepted at h3667. This new interface has not
received an external review. h3909 is accepted at h3917 and both source and
review are pinned as the newer global context, but it is not a premise: its
contact consequence is weaker than the local inequality used here.

Generated CNFs and caches are omitted from Git. A claimed target still
requires a compact independently checkable edge list and verifier. This
package supplies neither a model nor an UNSAT certificate and decides no
physical task.
