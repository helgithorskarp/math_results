# Tammes fifteen: equality for a prescribed G22 core

Actual author **six-tammes-2**, researcher. Conditional author proof,
independently unreviewed and unformalized.

An actual fifteen-point unit packing at the incumbent cosine tau containing
the prescribed injective thirteen-point/22-contact core gains both omitted
contacts and is one of the known asymmetric/cyclic incumbents. The two added
points are arbitrary. Read [PROOF.md](PROOF.md) for the exact hypotheses,
the boundary extraction from the completed cap cover and credited prerequisites.
The unresolved occurrence bridge still prevents an unrestricted optimality claim.

From the repository root, Python3.11+ standard library:

```bash
python3 -B round-two/six-tammes-2/twenty-two-contact-equality/check.py
python3 -O -B round-two/six-tammes-2/twenty-two-contact-equality/check.py
python3 -B round-two/six-tammes-2/twenty-two-contact-equality/controls.py
python3 -B round-two/six-tammes-2/twenty-two-contact-equality/check_sources.py
```

Optional second arithmetic route, Python3.11+ with SymPy1.14.0:

```bash
python3 -B round-two/six-tammes-2/twenty-two-contact-equality/algebra.py
```

The native result has13 unit norms,24 contacts,54 strict noncontact gaps,
91 labelled Gram equalities and13 critical-point Gram equalities. Both routes
recover the two missing contacts with zero normal forms and give coordinate
SHA256 `368039f5ca2b773b0bd1eaa20e7792923ebf100fc304f07dd3d765e29be51514`.
Every sign uses exact rational enclosures; every inversion is checked.
All six damaged/invalid cases must reject, including under optimized Python.

`check_sources.py` identifies the compact public prerequisites by exact bytes;
it does not rerun their proofs. In particular the completed cover9515 is an
imported actual-execution premise. To reproduce it from scratch follow that
contribution's separate `reproduce.py` instructions. This equality checker
does not silently substitute a manifest for that complete execution.

The mathematical boundary argument and prior completion theorem are external
to the algebra programs. Output paths are optional `--receipt PATH` arguments;
keep generated outputs in scratch. The published source uses no private
ledger, keys, large proof-state input or rounded coordinate input. Each process
has a160-second guard and one native thread; a guard failure is incomplete evidence.
