# No regular18 or regular24 good43 graph: an exact overlap certificate

**There is no 18-regular or 24-regular graph on 43 vertices with neither K5
nor independent5.** Thus any regular good43 must have degree 20 or 22.
The proof decides these complete classes without an automorphism, packing
or fixed neighborhood assumption. It does not exclude irregular graphs.

Regularity and the published extremum U(18)=85 force every neighborhood in
the 24-regular color into a complete list of 1,027 (4,5;24) graphs with at
least 128 edges. Two adjacent vertices' neighborhoods must overlap on the
same actual graph. Two exact overlap inequalities exclude every possible
pair, even after deliberately admitting extra matches between common graphs
that merely share a degree sequence. All 24,648 rooted neighborhoods enter
the certificate: 39 degree-sequence bins, 527 profiles, 6,669 pair decisions,
zero survivors. See [PROOF.md](PROOF.md).

The full published catalog is an external 16,913,568-byte input and is not
included in this source package. Download it outside the repository:

```sh
curl -fL https://users.cecs.anu.edu.au/~bdm/data/r45_24.g6 -o /tmp/r45_24.g6
python3 -B ramsey_r55_regular18_overlap_exclusion/reproduce.py --catalog /tmp/r45_24.g6
```

Run the second command from the repository root using CPython 3.11 or later
and its standard library. It runs normal and assertion-disabled producer,
independent checker, physical identity controls and malformed-input controls.
Expected status: `REPRODUCED_COMPLETE_REGULAR18_AND24_EXCLUSION`.
The catalog's SHA256 is
`83ca4028f206b2fa4315ef219b8c2c57c7835209673dd8183d8fb4353bd4fdd0`.
The exact retained records and certificate are compact public artifacts.
Catalog completeness, U(18)=85, R(3,5)=14 and R(4,5)=25 remain explicit
imported inputs; the independent checker does not re-create their historical
proofs. No SAT solver, external graph library or floating point is used.

[HANDOFF.md](HANDOFF.md) describes the precise use in physical search. The
regular18/24 strata are excluded in every h3887 task, including the teammate's
frozen q10 formulas at those degrees. This is a mathematical decision of
their specified graph classes, not a certification of the old formulas or
partial proof streams. All 2,189,178 whole h3887 tasks remain undecided.
Degrees 20/22 and irregular completions remain open. No good43 was found and
no Ramsey lower bound is improved.

An indexed prior statement at kenan.works claims the same conclusion; its
page could not be retrieved for proof comparison. No historical novelty or
external review of this certificate is claimed. The failed aggregate
regular-degree gate remains closed; this proof instead uses all actual
neighborhood types and the impossibility of their physical overlaps.
