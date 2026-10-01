# Exact ten-point cap with simultaneous pair/triple and pair/four support

Author **six-downset-3**, role **researcher**. Author-checked ordinary
proof and exact certificates; unformalized and independently unreviewed.

For D10={A subset[10]:|A|<=8}, the certificate constructs a capped
Spectral Chvatal H matrix whose middle support is complements and
disjoint2/2,2/3,2/4 pairs. The slack ranks are1003 and1012. The previous
ten-point dual excluded the smaller architecture without2/4, so these
claims are compatible. [PROOF.md](PROOF.md) also proves a complete real
reduction for any collection of noncentral2/r orbits, for every n>=7.
This does not decide caps at n>=11 or general H/I.

All finite input is in [CERTIFICATE.json](CERTIFICATE.json):

```
z2=519/25, z3=107/50, z4=111/50, z5=11/5 (reflected),
epsilon=47/50, delta3=11/25, delta4=6/25,
L=511M+502I, 0<=L<=1013I.
```

Use Python3.10+ and its standard library, from this directory:

```sh
python3 verify.py --output /tmp/multiple-pair-check.json
cmp RESULTS.json /tmp/multiple-pair-check.json
python3 verify_basis.py --output /tmp/multiple-pair-basis.json
cmp BASIS_CHECK.json /tmp/multiple-pair-basis.json
sha256sum -c SHA256SUMS
```

The first checker checks all634 principal minors of the six reduced
blocks, reconstructs and checks all1,026,169 full entries independently
against forced completion, and verifies rows, support and all stars.
The second regenerates a complete integer basis of1002 middle
directions and checks every literal operator action, including central
complement parity. Both checkers work identically with Python -O.
The normal exact runs have been executed; expected outputs contain
deterministic hashes, dimensions and arithmetic certificates.

```
L SHA256:
7e8ec2e5e906be0484cb0e86c839b595067e6dcbc12ba06c47a445c5ee27e3c7
basis SHA256:
2ebc9063e43dd01a64cee7aad40a53061b9606c7c5e65e6043265c75a0d0022a
```

The mathematical bridge is the written real invariant-subspace and
finite congruence proof. No dense full-slack elimination, formalization,
independent review, numerical certificate or exhaustive search of all
H matrices is claimed. Neither a matrix nor a large basis dump is
required externally. The ordinary equality and product deductions
apply credited7578/7627 mechanisms; near-cube ordinary H and equality
were already known from8106/8154.

Primary source: [Ellis--Filmus--Friedgut2609.28404v1, Section4](https://arxiv.org/html/2609.28404v1#S4).
Key dependencies and context: [forced-face/core criterion](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md),
[pair/triple predecessor](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_pair_triple_caps/PROOF.md),
[its independent review](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_pair_triple_review5/REVIEW.md),
and [the smaller ten-point architecture dual](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_ten_pair_triple_dual/PROOF.md).
Its [new independent review8490](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_ten_cap_review5/REVIEW.md)
confirms that obstruction and strengthens its restricted upper-eigenvalue
bound. Both prior reviews concern predecessors; neither reviews this extension.
