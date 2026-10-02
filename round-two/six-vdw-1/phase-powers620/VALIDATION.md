# Completed checks and their limits

Author: **six-vdw-1, researcher**. Python3.12.14/Linux, one serial child and
one numerical thread. These are author checks, without an external review or
formalization claim.

The full checker completed in normal and optimized Python, respectively
5.578 and 5.855 seconds, with peak child 15,912 and 19,312 KiB. Entire JSON
objects matched: 1,024 local inputs, 580 admissible rows, seven disjoint
phase orbits, 92,800 raw parameter pairs, 1,120 representative/map profiles,
1,120 directly checked integer bad progressions, 1,856,000 phase-conjugacy
identities and 672,000 regular word entries. The 468 closed profiles give
280,800 actual H3 regular identities and 8,704,800 diagonal CRT/color
identities. The 652 nonclosed profiles each fail actual H3 invariance.

Controls in both modes returned identical full objects. They examine all
68 parameter pairs in three tiny physical examples, including nonclosed
canonical profiles: 66 regular-AP-free positives and two actual negatives,
3,232 actual regular APs, and 800 conditional subgroup identities. The
q5/phase2/length3 instance has both cross-field positives and negatives.
Another 80 truth inputs cover every phase and all four arbitrary first-field
color pairs for the actual step310 antipodal necessity.

All 14 catalogue mutations reject in each mode: missing/duplicated coverage,
wrong base or unit, boolean-domain errors, invalid status, pole/zero/out-of-
range progression data, wrong color, a fake CORE and incorrect closure flags.
Damage checks explicitly omit expensive production bridges. Both full
production runs include those bridges. Rejection is an implementation control,
not a mathematical exclusion beyond the proved parameter family.

The source runner resolves the intended control checker explicitly even in
isolated Python, verifies all ten non-pin files before launching source,
regenerates the entire catalogue and compares every field of each expected
result in normal and optimized modes. Runtime receipts are written only into
the fresh selected output directory. No solver proposal, seed witness,
private proof corpus or cached native result is required.

The certificate does not rely on a complete search for positives in the
nonclosed family: every claimed negative has a checked actual progression.
The complete 9,600-cross-AP cover and order-three invariance require the
explicit closed-transport condition. No timeout, UNKNOWN, incomplete job or
native status is used as nonexistence evidence. The broad 3704 target and
arbitrary regular/H3-invariant construction families remain open here.
