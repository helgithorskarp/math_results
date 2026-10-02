# A fixed first surround determines its prototype

six-heesch-1, researcher. Author-checked finite lemma; unformalized and
independently unreviewed. No new Heesch value, construction or priority claim.

The seven-copy first surround of a scale-two version of the known P192
polyomino admits **one** prototype in a 105-cell domain with 35 fixed interior
cells. All 70 editable cell choices are forced: the prototype is the original
68-cell shape. This excludes all 2^70 masks in that domain except the parent,
without assuming an area, topology or balanced number of edits. New motions,
a larger cell domain or altered interior cells remain outside the result.

[proof.md](proof.md) states the literal template and the exact implication.
[input.json](input.json) contains the attributed seventeen-cell seed and seven
pose records. [membership.rup](membership.rup) is the
384-byte certificate; [expected.json](expected.json) records the rebuilt evidence.

Run from the repository root with Python 3.11 or later, standard library only:

```sh
python3 round-two/six-heesch-1/p192-template-rigidity/verify.py
python3 -O round-two/six-heesch-1/p192-template-rigidity/verify.py
```

Both commands verify 105 variables, 987 clauses and 70 RUP units, recheck the
unchanged disc first corona (1/7 copies, 68/476 cells), and reject three damaged
certificates. Output bytes agree. [verify.py](verify.py) uses two byte-pinned
public reader dependencies listed in [dependencies.json](dependencies.json):
[the integer geometry module](../p192-exact-three/upper.py) and
[the RUP checker](../finite-contact-types/rup.py). No SAT solver is required.

The literal seed is entry 192 (zero-based) of
[Kaplan's primary data](https://cs.uwaterloo.ca/~csk/heesch/omino/17omino_2up.txt).
Its published [P192 certificate](../p192-exact-three/proof.md), source
37e77d6c9e113673356b0c3a96cae5021a7811a2, supplies the original corona template.
Scaling is only a calibration. This result closes a specific prototype-edit
route; it does not rule out other polyominoes with finite Heesch number five.
