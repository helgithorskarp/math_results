# Boolean617 core classification and exact constant-phase cap

six-vdw-3, researcher. Arbitrary Boolean rules of at most three affine quadratic
characters modulo617, with every original root occurrence independently free,
constant phase and no extra edited nonroot column, cannot color [1,3704] without
a monochromatic seven-term AP. The known Rabung length3703 coloring belongs to
this family, so its exact maximum is3703. This is a restricted construction
result; the numerical lower bound for W(2,7) is unchanged.

[PROOF.md](PROOF.md) specifies every quantifier and the field/interval bridge.
[VALIDATION.md](VALIDATION.md) records algorithms, domains and trust boundaries.
[expected.json](expected.json) is the compact exact result; full generated
records are deliberately local outputs.

```sh
python3 round-two/six-vdw-3/boolean617-core-filter/reproduce.py --work /tmp/boolean617-fresh
```

CPython3.11.2, standard library only, new empty output directory. Run from the
repository root. The program uses serial children, one numerical thread and a
20s child guard. An incomplete child is saved as incomplete and stops the replay.
Typical complete runtime is about six minutes on the research machine, with
small memory use; [VALIDATION.md](VALIDATION.md) gives measured runs.

The producer and checker pairs are [generate.py](generate.py)/[check.py](check.py)
for complete regular-core scans, [cover.py](cover.py)/[check_cover.py](check_cover.py)
for affine field coverage and literal raw witnesses, and
[complete_roots.py](complete_roots.py)/[check_roots.py](check_roots.py) for physical
interval unit contradictions. [seed.py](seed.py) reconstructs and checks the
known3703 seed. [merge.py](merge.py) verifies exact finite coverage;
[damage.py](damage.py) tests rejected witnesses/domains. The algorithmic
independence is within one author, not an independent reviewer verdict.
