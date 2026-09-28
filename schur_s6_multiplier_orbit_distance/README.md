# A 50-edit obstruction across the modular orbit of an S(6) colouring

## Statement

Use the classical convention: `S(6)` is the largest `N` admitting a
six-colouring of `[1,N]` with no monochromatic `x+y=z`, **including `x=y`**.
The file `baseline.txt` is the Fredricksen–Sweet colouring of `[1,536]`
([EJC 7 (2000), R32](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v7i1r32)).
For each unit `m` modulo 537, define a 536-entry colouring

```text
B_m(x) = B(m^{-1} x mod 537),    1 <= x <= 536.
```

The checker verifies directly that every `B_m` is a valid classical
six-colouring of `[1,536]`. There are `phi(537)=356` units. **If a valid
six-colouring of `[1,537]` exists, its first 536 entries differ from each
`B_m` at no fewer than 50 positions**, for every labelling of the six colours.
This is a local obstruction across a specified finite family. It neither
constructs a 537-colouring nor proves one impossible; the published lower
bound remains `S(6) >= 536`.

## Certificate argument

For a transformed baseline `B_m`, let `P_c` consist of the disjoint pairs
`(x,537-x)`, `1<=x<=268`, whose two entries both have colour `c`. If the new
integer 537 has colour `c`, every pair of `P_c` needs at least one edited
entry. Their counts, in colour order, are always `64,43,55,38,32,35`.

For selected pairs, the certificate provides ten triples: one for each
endpoint and each of its five alternative colours. The other entries of a
triple have that alternative baseline colour. Thus editing either endpoint
forces an additional edit in the union of these supporting entries. For each
`m,c`, the selected pairs have disjoint supports; the supports avoid all
`P_c` endpoints. The checker verifies every triple, baseline colour,
disjointness condition, and 536-entry colouring directly. It does not
import the heuristic generator.

The certificate has at least `8,13,17,16` selected pairs for colours
`2,4,5,6`, respectively. Hence the lower bounds are at least
`64,51,55,51,49,51`. For 354 multipliers, colour 5 has at least 18 selected
pairs, raising its bound to 50. Only multipliers 83 and 454 have 17.

For either exceptional multiplier, assume an extension at distance at most
49 with 537 in colour 5. Its 32 complement pairs and 17 selected supports
form 49 disjoint mandatory edit groups. Every group then has **exactly one**
edit, and every entry outside the groups retains its baseline colour. The
checker generates the exact Boolean constraints for these facts and for
every Schur triple through 537. It substitutes all fixed colours and obtains
an empty clause by ordinary unit propagation, with no SAT solver or search
branching. This excludes 49 edits and establishes the uniform 50-edit claim.

## Reproduction

CPython 3.11 or later and the standard library suffice. From this directory:

```sh
sha256sum -c SHA256SUMS
python3 check.py
```

Expected output:

```text
PASS units=356 minimum_distance=50 unit_refutations=2
multiplier=83 colour=5 clauses=144100 unit_rounds=2 assigned=875 UNSAT
multiplier=454 colour=5 clauses=139012 unit_rounds=2 assigned=867 UNSAT
```

The 470,664-byte `certificates.json.xz` contains only selected pair indices
and witness coordinates. Each entry `[x, [a,b,...]]` represents the pair
`(x,537-x)` and ten witnesses `(a,b,a+b)`, ordered by pair endpoint and then
alternative colour. The compact representation is fully decoded and checked
by `check.py`; its compression is only for source size. Its SHA-256 is
`3456e87ca38346e9e9f7d40a12ffad9f7798f4816a614e1b3d8f2c63d80e8d35`.
The baseline SHA-256 is
`2fdf85110de782426dd5deccfa7244f182441fda9870db64ba8e4eea7e3d600d`.

To regenerate the certificate using the deterministic randomized search:

```sh
python3 generate.py --workers 16 --output /tmp/schur-orbit-regenerated.json.xz
sha256sum /tmp/schur-orbit-regenerated.json.xz
```

The output digest should equal the certificate digest above. The generator
tries 100, then 500, then 3,000 shuffles where needed; its output is not
trusted by the checker. On 16 workers, regeneration takes several minutes.
It uses no external package, network call, or unpublished input.
