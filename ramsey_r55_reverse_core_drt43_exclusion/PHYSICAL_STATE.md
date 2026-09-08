# Shared R(5,5) physical-decision state at this boundary

No certified good43 graph is known, so `R(5,5) >= 44` is not established.

Durable inputs incorporated here:

* h3931, independently accepted at h3935: every 26-set in a good43 contains
  an induced `P5` or complement-`P5`.
* h3947, independently accepted at h3957: no good graph properly contains the
  induced `C5[C5]` equality core. The unique equality branch is closed.
* h3951 and its h3963 generalization are preserved: punctures of Cayley graphs
  of order 44, and then of all vertex-transitive graphs of order 44, are
  excluded. These do not force or classify arbitrary good43 graphs.
* h3959 is now independently accepted at h3965: no regular good43 has degree
  18 or 24. Regular degrees 20 and 22 and every irregular case survive.
* The q10 regular route remains `BOUNDED UNKNOWN`; its partial proof streams
  certify no additional branch.

This package adds one complete physical decision. For the explicit regular
21-vertex tournament core and a reverse copy across a root, all `2^441`
initial cross orientations reduce to 352,716 possible first rows, then to two
exact commuting sign matrices, then to zero DRT completions. The result does
not decide any surviving regular degree or irregular good43 class.

Do not continue with neighboring cores or an adjacent DRT/Cayley/symmetry
ladder. A future use of this mechanism should first broaden the algebraic
coverage materially, for example by covering a complete class of core pairs,
or switch to a distinct candidate source. Global counting remains with
team-r55-3.
