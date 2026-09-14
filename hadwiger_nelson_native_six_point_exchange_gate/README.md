# Native six-point insertion and old-point exchange gate

**Every graph obtained by adding at most six points of the native 3,919-point
host to its fixed 503-point record base is four-colourable.** Consequently,
adding six such points and deleting one old base point cannot produce a
five-chromatic graph on 508 vertices. This closes the bounded successor gate
left open by the [five-point repair result](../hadwiger_nelson_native_five_point_repair_closure).

This is an exact computer-assisted exclusion of a specified physical
construction family. It produces no smaller five-chromatic graph and no
global vertex lower bound. A smaller five-chromatic subset of the host using
more than six points outside the base remains possible. The previous
[certified 1,090-point construction](../hadwiger_nelson_native_contact_repair)
is unaffected. The next construction step must change the fixed-base design;
this package does not propose a sequence of larger insertion allowances.

Let A be the archived Parts `v159e646` realization, D its 30 oriented unit
steps, L = A union (A+D), rho = (7+i sqrt(15))/8, and H = L union rho L.
The complete strict unit-distance graph of H has 3,919 distinct plane points
and 29,125 edges. B is the pinned 503-point intersection with the displayed
Parts509 realization, missing original zero-based indices
25, 74, 106, 107, 298, 336. See [the proof](PROOF.md) for all quantifiers.

The current published benchmark is Parts's
[509-point construction](https://arxiv.org/abs/2010.12665), also identified as
the unrestricted record in
[Haugland's August 2026 manuscript](https://arxiv.org/html/2608.04542v1).
A live source check on 2026-09-14 found no smaller published plane witness.

## Reproduce

From the repository root, with Python 3.11 and a C++17 compiler:

```sh
python3 -B hadwiger_nelson_native_six_point_exchange_gate/verify.py --work /tmp/hn-native-six
python3 -B hadwiger_nelson_native_six_point_exchange_gate/controls.py --work /tmp/hn-native-six-controls --sanitize
python3 -B hadwiger_nelson_native_six_point_exchange_gate/rotation_pilot.py
```

`verify.py --compare-esu` also runs the distinct connected-six enumeration
used during discovery. After verification, `compare_small_esu.py --work` with
the same work path independently regenerates and compares every smaller
component entry. `--sanitize` enables C++ undefined-behaviour checks.
No SAT, MILP, CAS, network access or nonstandard Python package is needed for
verification. CPython 3.11.2 and Debian g++ 12.2.0 were used. The full normal
replay including both connected-six enumerations took 155.6 seconds on the
shared research host. Generated enumeration files, binaries and logs stay in
the requested work directory; the proof input is compact source plus words.

## Evidence

The 126 previous partial four-colourings are pinned as a source dependency.
[certificate.json](certificate.json) adds 40 checked words from the already
saved six-point discovery probe. Each word has length 3,919; a dot omits a
point and `0` through `3` are colours. Every word retains all of B. No
infeasibility answer from the earlier MILP or SAT master is trusted.

- Independent connected-set and spanning-tree enumerations cover the
  21,289,412 degree-qualified connected six-point sets.
- The connected triple, quadruple and quintuple lists have respectively
  18,965, 175,654 and 1,856,054 entries. The independent lists agree entrywise.
- All 5+1, 4+2 (including 4+1+1), and 3+3 component cases are covered.
- A triple with smaller components leaves 13 residual physical 509-point
  candidates under the original 126 words. All have explicit four-colourings
  in [positive_cases.json](positive_cases.json), checked on every actual unit edge.
- The singleton/pair remainder has 1,823 atoms. Two exact algorithms exclude
  a weight-at-most-six cover of all 166 omission sets: weighted recursion and
  a split according to zero, one, two or three pair atoms.
- Twenty small graph cases compare full entries against brute force, with
  398 positive uncovered sets. Ninety weighted-cover cases include 74
  feasible cases and exercise bit widths through 256. Four malformed words
  are rejected. These controls also pass with undefined-behaviour sanitization.

This is author-run validation with different algorithms, not an
independent-author review or a proof-assistant formalization. Exact coordinate
transcription, program execution and the completeness arguments in PROOF.md
remain explicit trust boundaries. [VALIDATION.json](VALIDATION.json) records
commands and observed results; [SOURCE_PINS.json](SOURCE_PINS.json) pins inputs.

## A concrete geometry pivot also tested

The failed exchange gate motivated one different quadratic direction,
rho' = (7+i sqrt(51))/10. It couples equal points on the radius-squared 5/3
shell, where L has 36 points, and uses a new sqrt(17) extension.
The exact host L union rho' L has 3,919 distinct points and 29,096 unit edges.
It too is four-colourable. [rotation_pilot.py](rotation_pilot.py) rebuilds it
using generic Cartesian radical multiplication and checks the complete
positive word in [rotation_four_word.txt](rotation_four_word.txt). This closes
that particular alternative host without changing the insertion budget.
It says nothing about other rotations, additional point sets or other bases.

The durable next proposal is a construction assembled from three small
A159 images, with total size at most 475 when they share the origin, testing
joint colour constraints without retaining B. No such construction is
claimed by this package. It is distinct from the paired-Golomb and fixed
Heule/Parts partner lanes. A new pass must inspect fresh directions before
pursuing it.
