# Parts159: three arbitrary rotations

For the archived Parts `v159e646` support A, every union uA union vA union wA
with |u|=|v|=|w|=1 is four-colourable, including all strict unit edges and
point coincidences. There are at most 475 points. This is a restricted
construction theorem, not a record improvement or global lower bound.

Read [the proof](PROOF.md) and [reproduction instructions](REPRODUCE.md).
The 45 KB positive certificate has 62 extension rows and 360 three-copy
rows sharing 226 component words. Independent-author review is outstanding.

From the repository root:

```sh
python3 -B hadwiger_nelson_parts159_three_rotations/verify.py --check-expected
python3 -B hadwiger_nelson_parts159_three_rotations/controls.py
```

No SAT solver is required to verify the theorem. Reflections, different
anchors, different gadgets, and four-copy unions are outside its scope.
