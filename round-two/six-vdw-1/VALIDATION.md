# Validation record

Actual agent: **six-vdw-1**, role **researcher**, 2026-10-01. All native,
solver, BLAS and OpenMP jobs used one thread; substantive jobs ran serially.

## Exact proof computation

Python3.11.2, standard library only. The complete reproduction checks:

- all2187 local ternary vectors,139968 multiplicity entries, five profiles
  and the exact period-three characterization of the four-constraint case;
- all756 skeletons for the general balance boundary cases `m=3,6`;
- all21114 projected seven-point supports, each appearing twice, and exact
  carry-defect totals28152 for six explicit207-column skeletons;
- complete weighted edge dictionaries for six skeletons, comparing the
  carry decomposition with direct literal `Z621` AP enumeration;
- direct cyclic counts versus twice the static weighted cost for six words;
- the independently reconstructed3703-point QR617 incumbent;
- eleven malformed/invalid-input rejections, including a step-two AP,
  plus a valid short-word control.

The six dictionary sizes are161619,165628,165661,160655,168357,161619 in
the order listed in `expected.json`. Static weight is190026 in every case.
The final normal run took35.795931 seconds and143164KiB peak process RSS.
The optimized Python run also passed every check and compared the compact
expected outputs. These are finite regression audits; all-skeleton scope of
the reduction and numerical floor is established by the proof in PROOF.md.

## Optional construction experiments

Python-SAT1.8.dev24, CaDiCaL1.9.5,207 orientation variables, and the complete
audited signed constraints, normalized by `u(0)=0`:

| skeleton | conflict cap | result | elapsed seconds | peak RSS KiB |
| --- | ---: | --- | ---: | ---: |
| constant | 5000 | UNKNOWN | 5.965762 | 173252 |
| digit9 | 5000 | UNKNOWN | 12.993556 | 171492 |

No family exclusion follows. Generated instances, traces and interpreter
environments are omitted. The optional search code independently audits its
constraint dictionary before invoking the solver and independently checks
any SAT witness. An UNSAT proposal would require further certificate checking.

The six-state C++ search was built with Debian GCC12.2.0,
`-std=c++17 -O2 -Wall -Wextra -Wconversion -pedantic`, without warnings.
Two bounded10000-move runs produced a20000-move local checkpoint. The best
word has **3142 ordered monochromatic cyclic windows**,1571 after pairing
reversals, independently counted from its621 literal bits. It is **invalid**.
Its file SHA256, including a newline, is
`74e4b2add9a9e584200c29bb8e5fcabe2e72d499fa99e3d91f2cbb78d3fab3a5`.
This is operational progress for a construction heuristic, not a mathematical
claim about absence, optimality or closeness to a valid coloring. The checkpoint
and invalid candidate stay in scratch and are not proof inputs.

## Search correctness checks

`validate_search.py` ran250 deterministic moves in a release build,
100+150 moves with an exact restart, and250 moves with AddressSanitizer
and UndefinedBehaviorSanitizer (`-O1 -g -fsanitize=address,undefined
-fno-omit-frame-pointer`). The complete final checkpoints, RNG state, active
bad-edge order, tabu memory and best words agree byte for byte. Cache scores
and costs also agree with full recomputation. Three malformed/truncated/
extra-content checkpoints were rejected. A direct cyclic count confirmed
the common best half-count1789 and ordered count3578.

Expected best-word SHA256:
`e41932b077761d380de13b87da7572768279c7147d12975c6df649bb613de0f9`.
Expected checkpoint SHA256:
`2bd28d4d481079a2cea4f4dbe4c4331f2e7e4a64e8fbe27ced2e864f776f9b99`.
The complete compile/check sequence took11.105677 seconds and242032KiB
peak child RSS, including the sanitizer compiler. This validates the search
implementation; it does not add an exclusion or improve a W bound.

Only source, this compact record and expected summaries are published.
No solver trace, binary, checkpoint, private graph data or credential is
included. The theorem trust boundary comprises the written elementary proof,
the complete finite local/support audits and Python integer execution.
The optional solver and heuristic searches are outside that proof boundary.
