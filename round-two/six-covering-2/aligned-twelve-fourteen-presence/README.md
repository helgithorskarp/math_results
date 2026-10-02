# Aligned twelve forces original fourteen

Actual author **six-covering-2, researcher**, 2026-10-02.

For distinct covers whose moduli divide10080 and whose minimum is EXACTLY8,
if the original12 phase agrees with the original8 phase modulo4, then original14
is present and has opposite parity. The new complete exclusion is
F=(8:0,9:0,10:1,14:0,12:4). It removes one of thirteen five-class forms,
leaving twelve. Global L_min(8) numerical bounds are unchanged.

Read [proof.md](proof.md) for the original-class bridge, exact tree reduction,
credited premises and scope. [manifest.json](manifest.json) fixes the2625-node
author replay and all dependency hashes. [application-next.json](application-next.json)
supplies the twelve remaining literal residuals and all 60 free original moduli,
including every phase of all four TOP resources.

From the repository root, regenerate locally using the unchanged source:

```sh
python3 -m venv scratch/covering-env
scratch/covering-env/bin/pip install -r round-two/six-covering-2/requirements-discovery.txt
scratch/covering-env/bin/python -B round-two/six-covering-2/aligned-twelve-fourteen-presence/reproduce.py --generate --batches 12 --require-manifest
```

Each resumable batch remains180 seconds/700 new nodes with all numerical threads1.
Exhausting the finite allowance returns INCOMPLETE and asserts no exclusion.
The author resumed the five-class root across seven batches; a fresh cold
standalone regeneration is not claimed. Any complete valid tree proves the
conditional exclusion. --require-manifest additionally fixes the recorded
author replay, which may differ under another numerical discovery environment.
Large generated trees are intentionally omitted; no private input is needed
for the supplied regeneration command.

Once a certificate is available, replay uses Python 3.10+ standard library only:

```sh
python3 -B round-two/six-covering-2/aligned-twelve-fourteen-presence/reproduce.py --tree path/to/tree.json --require-manifest
python3 -B round-two/six-covering-2/aligned-twelve-fourteen-presence/reproduce.py --controls-only
python3 -B -O round-two/six-covering-2/aligned-twelve-fourteen-presence/frontier_fourteen.py
python3 -B round-two/six-covering-2/aligned-twelve-fourteen-presence/guard_controls.py
python3 -B -O round-two/six-covering-2/aligned-twelve-fourteen-presence/guard_controls.py
```

In this directory also run `sha256sum -c SHA256SUMS`. Controls-only mode
authenticates source/phase/inventory data and explicitly asserts no exclusion.
The direct literal author check took118.084 seconds/78120 KiB. The written
ordinary coverage, affine and original-class bridges remain unformalized.
No independent reviewer verdict is claimed.

The final publication-directory wrapper matched in77.561 seconds/79564KiB.
Complete phase controls agree normally and optimized, and12 wrong domains plus
eight damaged resource inventories reject in both modes.
