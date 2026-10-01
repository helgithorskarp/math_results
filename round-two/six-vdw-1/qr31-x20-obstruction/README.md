# QR31-by20 construction obstruction

six-vdw-1, researcher. Every binary template
`q_e(x mod31) XOR g(x mod20)` has a monochromatic nonconstant seven-AP
in the first2296 positions, for both colors of q_e(0) and every20-bit g.
Its cyclic affine images fail by2480. These are restricted construction
families; no improved W(2,7) bound or unrestricted exclusion follows.
See [PROOF.md](PROOF.md) for definitions, complete coverage and prior art.

Python3.11.2 and its standard library suffice. No solver, compiler, network,
earlier corpus or private input is needed. From this directory:

```sh
python3 -B reproduce.py --work /tmp/qr31-x20-proof
```

The generator reconstructs a2048-record AP cover. The separate checker
directly visits all2097152 parameter pairs and checks one actual AP for
each. Normal and optimized Python agree; four damaged covers reject in
both modes. Expected hashes are compared in addition to the substantive
checks, and do not replace them. Every child has a35-second wall deadline;
an incomplete replay exits nonzero and proves nothing.

Generated certificates, control files and full outputs remain in the chosen
work directory. They are regenerated from compact source rather than uploaded.
This is same-author algorithm independence, without formalization or an
external peer-review verdict. Generic cyclic/zipper methods are prior art;
historical novelty of this exact finite family obstruction is unestablished.
