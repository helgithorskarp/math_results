# Receiver contract and stopping point

Replay the package first. `interface.py` accepts 19 distinct physical
labels in [0,42]: root, four labels of M0, four of M1, four of M2, three
of M3, three of M4. Color 1 means red; color 0 means blue. It returns the
147-literal physical clause, canonical DIMACS clause, source premises and
19-step canonical RUP proof. `verify.py` independently checks this output.
An embedding is supplied by the receiver; this package does not search for
embeddings or evaluate the receiver's candidate pool.

To translate into a compact formula, pass `--map PATH` where JSON has an
`edges` array covering every physical unordered pair exactly once. Entries
have either form:

```
[u, v, "var", positive_DIMACS_variable]
[u, v, "fixed", red_bit]
```

Require 0<=u<v<43, injective variable numbers, and red_bit in {0,1}.
A positive variable must mean that physical edge is RED. The adapter rejects
missing pairs and reused variable IDs. Normalize polarity externally if
the receiving encoding differs. Canonical variables 1..903 must never be
assumed to match the receiver's numbering.

Receiver statuses:

- `CLAUSE`: the returned disjunction is valid for this physical embedding
  after substitution of the supplied fixed edges.
- `TAUTOLOGY`: a fixed edge prevents this template; this instance adds no cut.
- `CONFLICT`: all cut literals are fixed false. The whole completion family
  of that partial graph is excluded. If every edge is fixed, a literal
  monochromatic five-set is also returned; verify its ten pairs directly.

The adapter returns the substituted cut and the original canonical proof.
It does not claim to append a proof to an arbitrary owner's DRAT stream.
For proof-logging integration, the owner must supply or derive the listed
Ramsey premises in its encoding and transport the proof through its own
preprocessing. Semantically the cut is valid in any correct good43 encoding.
One can audit the canonical proof without trusting the adapter or solver.

The controls use eight generated complete graphs in the counted family,
each satisfying the edge window and chosen-root degree 21. Each rejection
returns a separately checked monochromatic five-set. These deliberately
bad fixtures are not search candidates. Remapped IDs, partial fixed edges,
both colors, three random relabellings, and corrupt inputs are checked.

The coherent milestone ends with this complete-family exclusion, exact
count, physical proof, receiver interface and durable publication. No
broader template sweep, smaller-module variant, additional cycle-cover
lemma, or adjacent local sharpening belongs to this milestone. Application
to team-r55-1's 161 q10 survivors remains its decision and ownership; this
handoff asserts neither delivery acknowledgement nor a survivor decision.

Preserve h4009/h4017 and h4015/h4019 as the accepted global base. Preserve
h4001's 518 excluded and 122 UNKNOWN q7-r5 tasks, the 2,188,660 remaining
whole h3887 tasks, and h3987's 99 closed/161 UNKNOWN q10 children with the
existing forced edge in 29 residualF22 children. None of these counts is
combined with the complete-assignment count here.
