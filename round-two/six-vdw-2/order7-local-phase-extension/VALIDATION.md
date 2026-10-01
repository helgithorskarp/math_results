# Exact validation

The public runner regenerates the deterministic positive certificate and
compares independent normal and optimized literal-field audit results with
the entire compact semantic fixture. This includes complete support and
union coverage and every requested phase assignment, rather than sample
colorings. The generator and auditor use different field-support, rotation,
coverage, and coloring representations.

The separate auditor reconstructs H and every signed H-coset by modular
multiplication and enumerates all 380072 ordered field (a,d) pairs. The
4312 APs meeting zero are removed by checking their actual points. Literal
quadratic-residue positive controls and 61888 exhaustive small-word scalar
rotation/color-exchange controls also pass.

The twelve adversarial checks run both normal and optimized Python for six
controls: wrong field, missing phase witness, boolean masquerading as a
color word, constant coloring with the correct zero phase, omitted union
representative that is not an original AP support, and changed pinned helper.
The last control mutates an isolated helper copy; it is rejected before
import or certificate generation. The other guards distinguish structural
coverage, phase-domain validity, and actual monochromatic field APs.

Certificate SHA256:
`93cbc629bb455f991b4ba6acf8ecf7b0ac136604dbae893f4635e07f36be4938`.
464 records and 51696 positive witnesses cover every set of at most seven
J-cosets through the proved union reduction. Generated certificates remain
in scratch; only source, documentation, pins, hashes, and concise expected
results are published. No external solver or negative enumeration certificate
is trusted. The trust boundary is Python integer/set semantics and the
correctness of the explicit checker and mathematical reduction. This is
same-author implementation independence, not an independent peer review or
proof-assistant formalization. Full H7 existence and the 3704 target remain open.

Fresh source replay on Python3.11.2: generation3.954s, normal audit6.041s,
optimized audit5.975s, complete16.291s. Peak child RSS29276KiB and parent
RSS16112KiB. All twelve adversarial controls passed, including removal of
the nonbasis union mask33603905. These timings are observations, not limits
or mathematical inputs. The fixed subprocess deadline is55s per stage;
no native solver, thread-count increase, or resource-limit change occurred.
