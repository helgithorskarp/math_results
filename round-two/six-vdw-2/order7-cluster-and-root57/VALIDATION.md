# Author validation, 2026-10-01

Actual author: **six-vdw-2**, researcher. No external review or formalization
is claimed. CPU-heavy stages ran serially with all solver/BLAS/OpenMP threads1.

The separate literal-field audits traverse all380072 ordered nonconstant
seven-term APs in F617, discard4312 through zero, and compare all375760
retained APs and26488 signed supports with the producer's entire models.
The two representations are actual field cosets versus discrete-log/scaling.
Both normal Python and `-O` agree. QR field controls are positive.

New mathematical work: all84 spacing-five models refuted under the requested
50000-conflict cap (maximum1918 actual conflicts); native/conversion/dual
exact replay took258.624 seconds and68812 KiB peak child RSS. Four closest
pair cases, d4/d3 for both backgrounds, refuted; the following d2,b0 case
returned UNKNOWN requested50000/actual50003. That run stopped after41.725
seconds,71748 KiB peak child RSS. The complete earlier private root57
longest-run8..14 cover was newly audited using literal field definitions and
all seven cached positive proofs strict-replayed in normal and optimized
Python,17.900 seconds. Earlier inconclusive root57 cases below8 are not used.

A genuinely different d2,b0 model added the newly proved root57 necessary
color cut. Its complete definition audits passed normal/-O,4.372/4.272
seconds. It returned UNKNOWN at50000 conflicts,6.753 seconds, and stopped.
No identical negative retry or cap increase occurred. The other strengthened
d2/d1 branches were not proposed. These bounded failures remove no case.

Public-source validation regenerated all95 canonical models in a fresh
external work directory. Every CNF matched [EXPECTED.csv](EXPECTED.csv).
It re-audited every full model in normal/-O and strict-replayed matching
cached candidate LRAT proofs, without trusting the producer or previous
status flags. It did not repeat the95 native positive proposals. Result:
`EXACT_H7_TWO_NECESSARY_CONSTRAINTS`, 293281 additions,
3627680 hints, all proof bytes reproduced. This source check
took210.257 seconds, parent RSS29428 KiB,
child peak RSS68000 KiB. The default reader command
generates fresh native proofs instead; proofs with a different valid trace
remain acceptable after strict replay.

The independent packed audit checked322 rooted profiles,42 cyclic orbits
per background,1771 labeled phase words per background and3542 signed
normalizations, explicitly retaining period11/22 phases and44 color
orientations. Counter audits checked every local truth relation and172540
tiny threshold cells/4092 exact-six input assignments.

[guards.py](guards.py) rejected16 controlled corruptions, in
normal and optimized Python (16.810 seconds): omitted period11
phase orbit; changed canonical case index; omitted longest-run8 case; wrong
geometric stride; wrong exact-six unit; changed helper before import; an
empty proof step without hints; and a missing live proof hint.

The complete checked positive cover is7+84+4=95 refutations. The proved
geometry is minimum minority cyclic distance<=2 at K8 or36, with squared
majority-gap sum>=176. EndpointK8/K36 and general H7 remain unresolved. The
existing phase band8..36 and W(2,7) interval target are not improved here.

Primary Monroe Table1 (>3703 for two colors/seven terms), Table2 (617), and
the author repository were refreshed before publication. Bounded pertinent
peer reports/source and committed graph neighborhoods were refreshed; the
period618/620 XOR exclusions are complementary context and are not premises.
