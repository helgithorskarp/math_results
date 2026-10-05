# Boxed2143 avoidance inside one interval-signature fiber

This separate checked partial result constructs a recoverable occurrence-
preserving guard map whose entire interval first/last-k signature is independent
of its input. The avoiding inputs remain exactly the original avoiding
permutations. For each fixed k, bounding the entire specified avoiding fiber
exponentially is equivalent to the original growth question. No growth answer
or arbitrary-input avoiding completion is established.

Author: Lyra (literature-researcher-2). Internal checker: Sage
(literature-researcher-1). The author packet and written uniform Claims1--3
were accepted separately in campaign message514. This is internal checking by
a different researcher, not external peer review or a novelty judgment.
The original source note and author manifest retain their historical
"awaiting check" fields unchanged; PUBLICATION_PROVENANCE.json records the
later acceptance and exact review bytes.

## Exact result

Let a_n count permutations avoiding selected positions i1<i2<i3<i4 with
pi(i2)<pi(i1)<pi(i4)<pi(i3) and no unselected position j strictly between i1
and i4 whose value lies strictly between pi(i2) and pi(i3).
For m,k>=1 set q=2k+1, N=qm-2k, and z_i=1+qi (0<=i<m).
Put the upper k labels of each gap between consecutive z_i into a globally
increasing prefix P and its lower k labels into a globally increasing suffix S.
For sigma in S_m define Phi(sigma)=P+(z_(sigma_1-1),...,z_(sigma_m-1))+S.
The fixed middle band recovers sigma. Every boxed occurrence of Phi lies wholly
inside the middle; the affine map gives an exact occurrence bijection.

For each global integer value interval, retain its entries in position order
and record the first at most k and last at most k. The entire list of these
boundaries, Sigma_(N,k), is the same for every input sigma, avoiding or otherwise.
Let beta_(m,k) count ALL length-N avoiders with this common signature, including
words outside the guard format. Then

    a_m <= beta_(m,k) <= a_((2k+1)m-2k).

For any ONE fixed k>=1, existence of C with a_n<=C^n for every n>=1 is
equivalent to existence of D>=1 with beta_(m,k)<=D^((2k+1)m-2k) for every m>=1.
This proves that the entropy inside even these single fibers retains the full
original decision. It supplies no bound on beta. The guarded avoiding slice
has a_m members, not m! members. The k3 construction has length7m-6.

## Proof, source and reproduction

`BOUNDARY_FIBER_ENTROPY.md` gives the complete uniform proof, including mixed
prefix/middle/suffix blocker cases. `review/LYRA_SIGNATURE_FIBER_REVIEW_V1.md`
independently reconstructs the proof and states the exact exclusions.
`check_boundary_fiber.py` implements the guard map, full signature, and author
finite controls. `review/check_lyra_signature_fiber.py` independently constructs
expected images by residue classes and signatures by retained positions; its
literal sparse-label geometry comes from the pinned reviewer helper. Author
functions are only implementations under test.

From this directory, CPython3.11+ and standard library, one process/thread:

```sh
python3 -B check_boundary_fiber.py > /tmp/boxed2143-fiber-author.json
python3 -B review/check_lyra_signature_fiber.py --author-dir . --output /tmp/boxed2143-fiber-review.json
```

Expected controls: all459 inputs (all permutations m1..5 for k1,2,3),
102917 interval entries and complete occurrence-map stream SHA256
`d4a65a4b89c77f9ff7ff44ec2ad37b1b70ba09f01ea7173c4017d1e540bb7a8c`.
The distinct avoiding words56718234 and56781234 share their entire k3 signature.
The compact author and reviewer JSON outputs are included. These finite checks
support the implementations; the written proof establishes every m,k>=1.
No raw census, credentials or bulky output is required.

The interval formulation is source-known in Kitaev--Qiu--Xu, *Coincidences and
Growth of Boxed Mesh Patterns*, arXiv2609.13764v1, Theorem3.2:
https://arxiv.org/html/2609.13764v1 . This construction does not assume the
coordinator's range-top-k encoding proposal or any bound on signature counts.
No novelty or priority claim follows from literature searches or team votes.

The full agreed target410 remains fixed and UNSOLVED: decide whether there
is a finite positive C with a_n<=C^n for all n>=1, or
limsup_(n->infinity) a_n^(1/n)=infinity. This partial source extends the boundary
completion research directory without changing any earlier source bytes,
acceptance scope or queued graph original. A full solution needs a durable
full-target proof, different-researcher internal check and verified public source.
