# A strict-source and four-colour stop for one L10,1 edge-star closure

This package closes one exact, predeclared bottom-up Hadwiger--Nelson
architecture. It does **not** improve the 509-vertex record.

The intended source was the ten-vertex `L_{10,1}` incidence drawing in Figure
2 of Voronov--Neopryatnaya--Dergachev (2022). Exactification in
`Q(sqrt(3),sqrt(11))` retains all 17 displayed unit edges but complete
all-pairs reconstruction finds two omitted physical contacts, `BF` and `DH`.
Those contacts cannot be discarded in a strict unit-distance graph. They make
the seven points `ABFGHIJ` an exact Moser spindle: `ABFG` and `FIJH` are its
two diamonds and `GH` is the joining edge. Thus the strict source fails the
campaign's source-new admission gate.

For completeness, the already-frozen whole operation was still decided. For
every directed physical source unit edge `(u,v)`, it places a directly
oriented source copy by

```text
z -> u + (v-u) z.
```

With 19 complete source edges, its raw point bound is
`10+2*19*8=314<=508`. Exact collision merging gives **188 points**. Testing
all 17,578 physical pairs gives **765 unit edges**. The graph is connected,
has no articulation or bridge, and has a 184-vertex degree-four core.

The complete graph has chromatic number exactly four. The certificate contains
a checked proper four-colour word. Its Moser-spindle subgraph supplies the
matching lower bound. Hence there is no ordinary non-four signal, no proper
five-colour obligation, and no record candidate.

## Exact coordinates

Write `a=sqrt(3)`, `b=sqrt(11)`, and `c=ab=sqrt(33)`. The ten frozen points
are

```text
A=(0,0)                     B=(1,0)
C=(c/6,a/6)                 D=(1+c/6,a/6)
E=(1/2+c/6,2a/3)            F=(1/2,a/2)
G=(1/2,-a/2)                H=(1/2+c/6,-a/3)
I=((11+c)/12,(a+b)/12)      J=((1+c)/12,(a-b)/12).
```

Every coordinate in `certificate.json` is serialized coefficientwise in the
basis `[1,a,b,c]`. Equality, collision merging, and unit-distance decisions
use rational arithmetic only.

## Replay

Python 3.11 or later and only the standard library are required.

```sh
python3 -B produce.py --output /tmp/l101-edge-star.json
cmp /tmp/l101-edge-star.json certificate.json
python3 -B verify.py
python3 -B controls.py
```

`verify.py` reconstructs the source, incidental contacts, all 38 directed
placements, collision quotient, and all physical unit edges from the formulas;
checks the Moser subgraph and four-word; and recomputes connectivity, cuts,
degrees, core size, and fingerprints. `controls.py` requires rejection of a
bad colour word, a missing edge, and a moved point.

## Scope

This result concerns only the displayed exact ten-point support and its full
orientation-preserving directed-edge-star closure. It is not a theorem about
every realization of the abstract `L_{10,1}` graph, other small rigid graphs,
reflected closures, edge subsets, alternate anchors, or further layers. No
such variant was tested after this stop.
