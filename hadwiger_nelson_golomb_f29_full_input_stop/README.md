# A fixed nonseparable Golomb–F29 interaction preserves every full input colouring

The exact interaction below has **32 distinct plane points and 86 complete
unit edges**. Its graph has no bridge or articulation vertex, and three unit
edges join vertices private to different inputs. Nevertheless **every proper
four-colouring of its complete ten-vertex Golomb input extends**. The graph
is exactly four-chromatic. This freezes a failed compact-coupler selector;
it is not a five-chromatic construction or a record improvement.

The result illustrates a stronger negative control than the earlier pendant
attachment: nonseparability and private contacts together still need a direct
complete-input extension test. No different frame, second copy, receiver test
or subsequent completion layer is included or licensed by this result.

## One exact physical interaction

Write a coefficient row `(a,b,c,d)` at denominator `D` for

```text
(a + b sqrt(33) + i(c sqrt(3) + d sqrt(11)))/D.
```

Let `rho=(1+i sqrt(3))/2`, `w=rho^2`, and `q=(1+i sqrt(11))/6`.
The ordered Golomb input is

```text
G = (0, 1, rho, rho^2, rho^3, rho^4, rho^5, q, w*q, w^2*q).
```

The 29 rows in [f29.tsv](f29.tsv), at denominator 12, are the previously
certified F29 frozen-centre source. Its centre is vertex 0. The triangle
`(F0,F28,F25)` has coordinates `(0,1,rho)`. Use the single
orientation-preserving isometry

```text
T(z) = G7 + (G8-G7)*z.
```

It maps that triangle onto the inner Golomb triangle `(G7,G8,G9)`.
The multiplier is

```text
(-3-sqrt(33) + i(sqrt(3)-3sqrt(11)))/12,
```

and has squared norm exactly one. Form `G union T(F29)`, preserving Golomb
labels 0 through 9 and appending new points in increasing F29 label order.
The complete F29-to-union map is

```text
7,10,11,12,13,14,15,16,17,18,19,20,21,22,23,1,
24,25,26,27,2,28,29,30,0,9,31,3,8.
```

Seven points are shared: Golomb labels `0,1,2,3,7,8,9`. All merged coordinates
have denominator 144 in the displayed basis. The inputs have 18 and 75 unit
edges, with ten edges shared. Reconstruction of **all 496 unordered pairs**
finds exactly three additional edges:

```text
(4,17), (6,20), (6,21).
```

Each joins a Golomb vertex outside the F29 copy to an F29 vertex outside
Golomb. Thus the edge count is `18+75-10+3=86`. Connectivity is checked after
every single vertex deletion and every single edge deletion; none disconnects
the graph. This is a claim about the frozen complete graph, not a general
criterion that nonseparable graphs have chromatic amplification.

## Complete source-extension proof

Normalize colours on the unit triangle `(G0,G1,G2)` to `(0,1,2)`.
An exhaustive definition-level check of all `4^7=16,384` assignments to the
other seven vertices finds exactly **95 complete Golomb four-colourings**.
The certificate contains one checked full 32-vertex extension for each,
ordered by its complete ten-vertex prefix. There are no missing or duplicate
prefixes. Consequently every labelled Golomb four-colouring extends, not
just a terminal projection or selected sample. There are 2,280 labelled input
words, since each normalized word has 24 distinct global colour relabellings.

All `3^7` normalized assignments fail on Golomb. A literal proper four-word
for the complete union is

```text
01212120232103212313010312222110.
```

These give chromatic number exactly four. The certificate also checks the
proper five-word obtained by changing its first colour to 4; having such a
word does not make the graph five-chromatic. No ordinary non-four statement
or claim about the full F29 projection is made.

The exact arithmetic test uses

```text
D^2 |z|^2 = a^2+33b^2+3c^2+11d^2 + 2(ab+cd)sqrt(33).
```

A unit pair therefore requires the two integer coefficients to be `(D^2,0)`.
Collision equality is coefficientwise: irrationality of `sqrt(33)` separates
the real coefficients, and irrationality of `sqrt(11/3)` separates the
imaginary coefficients. No numerical incidence threshold is used.

## Budget and role-map limit

The Golomb input embeds in the published native Parts parent with labels

```text
0,153,150,169,166,161,158,53,65,59.
```

[parent_roles.tsv](parent_roles.tsv) is a compact literal extraction from the
pinned exact parent table. All ten roles belong to the retained Parts373
host. The small interaction adds at most 22 points relative to those roles,
so the elementary host-union upper bound would be `373+22=395`. This is only
a role map and point bound: the full receiving frame, its additional contacts
and its boundary relation were **not** tested. Universal extension of Golomb
does not prove universal extension of a larger host with additional contacts.

The source gate already fails, so neither Parts receiver earns continuation.
No receiver pattern is claimed eliminated, no cap-preserving route to an
empty residual is supplied, and no amplifier or receiver sweep follows.
The scoped stopping theorem does not exclude arbitrary Golomb–F29 placements,
other component interfaces, or arbitrary replacements in the same field.

## Reproduction and provenance

Python 3.11 or later and the standard library suffice. From the repository
root:

```sh
python3 -B hadwiger_nelson_golomb_f29_full_input_stop/verify.py --check-expected
python3 -O -B hadwiger_nelson_golomb_f29_full_input_stop/verify.py --check-expected
python3 -B hadwiger_nelson_golomb_f29_full_input_stop/controls.py
python3 -B hadwiger_nelson_golomb_f29_full_input_stop/produce.py --output /tmp/golomb-f29-certificate.json
cmp /tmp/golomb-f29-certificate.json hadwiger_nelson_golomb_f29_full_input_stop/certificate.json
(cd hadwiger_nelson_golomb_f29_full_input_stop && sha256sum -c SHA256SUMS)
```

The producer uses complex rotations in separate Cartesian radical vectors
and DSATUR. The verifier uses a direct integer transformation, a two-term
norm identity, exhaustive input assignments and literal extension checks.
They agree entrywise on coordinates, edges and the complete small
certificate. Controls first accept the valid certificate and then reject a
missing source word, improper extension, displaced point and omitted private
edge. [VALIDATION.json](VALIDATION.json) records the runs and a development
correction caught before publication. These are author-side checks, not an
independent-author review or a claim of formal proof.

[PROVENANCE.json](PROVENANCE.json) pins both input files and records remote
byte verification. The prior
[F29 source](https://github.com/helgithorskarp/math_results/blob/ef05942eeebba29628dc02f37a5792ac7d4122b8/hadwiger_nelson_frozen_centre_transfer/README.md)
provides the demonstrated palette force that motivated this interaction;
the new universal-extension theorem depends only on the displayed physical
points and checked words. No novelty claim is made for Golomb, F29 or the
extension-certificate principle.

The live primary-source check still supports the 509-point unrestricted
record of [Parts](https://arxiv.org/abs/2010.12665), also explicitly identified
as current in [Haugland v4](https://arxiv.org/html/2608.04542v4). Restricted
spindle-free constructions and non-strict edge minimization do not change
this vertex target. No Discovery submission is made for this scoped stop.
