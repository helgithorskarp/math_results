# Sharp common-neighbor threshold for toroidal thrackles

Two vertices of a graph thrackled on the orientable torus have at most
**four common neighbors**, and four is attainable. The matching example
is an explicit cyclic thrackle of $K_{2,4}$ with twelve crossings.
Its planarization has $(V,E,F)=(18,32,14)$.

The upper bound follows from the known nonzero mod-two homology of
thrackled four-cycles. This package supplies the attaining construction,
a hand-checkable proof, and an exact small certificate. It makes no
historical-priority claim.

- [PROOF.md](PROOF.md): complete theorem, crossing orders, rotations,
  four face orbits, realization argument, and homological equality case.
- [certificate.json](certificate.json): full finite construction, 2.4 kB.
- [build.py](build.py): deterministic constructor from the cyclic rule.
- [verify.py](verify.py): independent certificate consumer and checks.
- [expected.json](expected.json): exact expected verification output.
- [SOURCES.md](SOURCES.md): primary literature and scope of the audit.

From this directory, using Python 3.11 or later and no third-party packages:

    python3 build.py > /tmp/torus-thrackle-certificate.json
    cmp certificate.json /tmp/torus-thrackle-certificate.json
    python3 verify.py --self-test > /tmp/torus-thrackle-verification.json
    cmp expected.json /tmp/torus-thrackle-verification.json

Both comparisons must succeed. Verification checks all edge-pair meetings,
proper crossings, the 14 faces, connectedness, and cellular homology over
two fields. Four deliberately damaged certificates must be rejected.
The computation is instantaneous at this scale; the proof does not depend
on the exploratory search that suggested the construction.

Scope: finite simple graphs, simple edge arcs, proper pairwise crossings,
and the orientable torus. The planar Conway conjecture and large-$n$
thrackle-genus estimates remain outside this result.
