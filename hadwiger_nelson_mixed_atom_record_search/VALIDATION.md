# Completed validation, 2026-09-13 UTC

- The packaged portable driver rebuilt the E-phase inventory, all 106 sources,
  all 99,080 retained contact quadratics, and all 6,738 fixed-field phases in a
  fresh output directory. `summarize.py` reported PASS against EXPECTED.json;
  zero UNSAT and zero UNKNOWN occurred.
- The two compact construction recipes regenerated the archived exact labelled
  seeds. A mistaken early identification of density-ranked source0 as 3M was
  caught by the seed edge-count gate. Source0 is the recorded overlapping
  Golomb/conjugate-Golomb source. Its recipe was corrected and matches the
  archived coordinates, phase, colour word, and edge count exactly. No search
  graph or mathematical result was changed by this provenance repair.
- Both solver-free fixture replays passed with Python `-O` and native
  undefined-behaviour sanitization. Runtime was 140.757 seconds for the
  847-point fixture and 102.549 seconds for the 518-point fixture while other
  search processes were running. Neither replay called SAT.
- Each replay checks every seed and augmented-support pair using both the
  complex-field norm formula and a separately derived real-coordinate metric.
  Together these are 731,794 unordered pair instances, evaluated twice.
  Both complete edge lists and both physical point streams matched their
  pinned hashes. Distinctness is exact tuple equality in a nonsquare extension.
- For each fixture, 60 deterministic real-extension square-root controls
  checked exact squared identities. Malformed and constant colour words were
  rejected. The checks use explicit exceptions and remain active under `-O`.
- Compiler: g++ 12.2.0. Python: CPython 3.11.2. Search solver:
  python-sat 1.8.dev24 / CaDiCaL195. All arithmetic input was rational; no
  floating-point geometry, numerical tolerance, or probabilistic geometry
  hash selected edges. Native overflow guards were satisfied and no sanitizer
  diagnostic occurred.

The positive words make SAT a discovery tool rather than a proof dependency
for the two published physical fixtures. The broader census still trusts its
exact event-enumeration reduction and ordinary Python/PySAT execution; it was
not given a second all-pairs replay for every retained quadratic. The local
colouring filters are accepted, unformalized mathematics from the pinned
preceding work. This is author validation, not external peer review or a
formal proof-assistant result. No five-chromatic witness or global bound is
asserted. There is no surviving candidate, timeout, or unfinished mathematical
computation at publication.
