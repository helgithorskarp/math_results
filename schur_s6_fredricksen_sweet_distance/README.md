# A 51-edit obstruction around the Fredricksen–Sweet S(6) colouring

## Claim and convention

Write `S(6)` for the largest `N` such that `[1,N]` has a six-colouring with no
monochromatic `x+y=z`, including `x=y`. The 536-digit file `baseline.txt` gives
the colour of each integer `1,...,536` in order. A direct check shows it is a
valid colouring. It is the symmetric construction printed by Fredricksen and
Sweet, [*Symmetric Sum-Free Partitions and Lower Bounds for Schur Numbers*,
EJC 7 (2000), R32](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v7i1r32/pdf),
page 6. Their exceptional symmetric pair is `179,358`, with different colours.
The colour-class sizes are `129,86,110,77,64,70`.

**Proved local obstruction.** If a valid six-colouring of `[1,537]` exists,
its restriction to `[1,536]` differs from `baseline.txt` in at least **51**
positions. This holds for every labelling of its six colours. The claim is a
distance bound around one specified baseline. It does not prove that 537 is
uncolourable or improve the published lower bound `S(6) >= 536`.

## Certificate argument

Let `B(i)` be the baseline colour of `i`. For each colour `c`, let

```text
P_c = {(x,537-x): 1 <= x <= 268 and B(x)=B(537-x)=c}.
```

The pairs within and across these six sets are disjoint. If 537 has colour `c`,
at least one endpoint of every pair in `P_c` must change colour. The six values
`|P_c|`, in colour order, are `64,43,55,38,32,35`.

The certificate selects some pairs from `P_c`. For each selected pair, for each
endpoint `v`, and for each alternative colour `d != c`, it supplies a Schur
triple containing `v` whose other entries have baseline colour `d`. The union
of these other entries is the pair's *support*. The supports of selected pairs
of the same colour are disjoint. All support entries have baseline colour
different from `c`, so none belongs to a pair in `P_c`.

For a selected pair, whichever endpoint changes must take some colour `d != c`.
Its supplied `d`-triple then forces at least one support entry to change too.
Disjoint supports force one *additional* change per selected pair. The
certificate supplies `0,8,0,13,19,16` selected pairs for colours 1 through 6,
giving respective lower bounds `64,51,55,51,51,51`. Their minimum is 51.

As a small example, `(9,528)` is one of the colour-5 pairs. If 9 changes to
colour 1, `(1,8,9)` forces another edit; if 528 changes to colour 1,
`(1,528,529)` does. `certificate.json` gives analogous triples for all five
alternative colours at both endpoints of every selected pair.

## Reproduction

The theorem needs only CPython 3.11 or later and the standard library:

```sh
cd schur_s6_fredricksen_sweet_distance
python3 check.py
```

Expected output:

```text
PASS triples=71824 pair_counts=64,43,55,38,32,35 selected_counts=0,8,0,13,19,16 witnesses=560 distance_at_least=51
```

The checker enumerates all `71,824` unordered Schur triples on `[1,536]`,
checks the baseline directly, and verifies every certificate pair, triple,
colour, and support-disjointness condition. It does not import the generator.
The compact certificate is 31,621 bytes. SHA-256:

```text
baseline.txt    2fdf85110de782426dd5deccfa7244f182441fda9870db64ba8e4eea7e3d600d
certificate.json b9c28cde217a6b4d06f672d0f389c1c9fa9e7544897cf4eb392fad3985edaa4f
```

The witness search is deterministic but heuristic; its success is not needed
for the proof. To regenerate the committed certificate:

```sh
python3 search.py --trials 1000 --output /tmp/schur-s6-certificate.json
sha256sum /tmp/schur-s6-certificate.json
```

The second command should print the `certificate.json` hash above. The search
enumerates baseline-colour blocker triples, then greedily packs pairs whose
supports can be chosen disjointly. It uses `random.Random(20260928+c)` for
colour `c`; each trial shuffles candidate pair order. No floating point is
used in either program.

`sat_probe.py` is a separate exploratory CNF generator. It uses one-hot colour
variables, one negative clause per colour and unordered Schur triple, and an
optional palindrome constraint `colour(i)=colour(N+1-i)`. Install
`python-sat==1.9.dev15` and run, for example:

```sh
python3 sat_probe.py --n 537 --colors 6 --symmetry --conflicts 100000
```

`SAT` output includes a definition-level checked colouring. `UNKNOWN` means
the conflict budget was exhausted. A solver `UNSAT` result would concern only
the encoded class; this script emits no independently checked UNSAT proof.
The certificate theorem does not use PySAT or the SAT probe.

## Scope and trust boundary

The distance theorem follows from the displayed pair-and-support argument and
the finite data checked by `check.py`. The remaining trust boundary is the
checker and standard Python integer/file operations; the proof uses no solver
soundness assumption. Certificate generation is untrusted. The baseline is
also verified as a valid 536-colouring regardless of its source attribution.
No conclusion is drawn about the existence of a six-colouring at 537 or about
all 536-colourings.
