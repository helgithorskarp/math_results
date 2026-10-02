# Original twelve differs from eight modulo four

Actual author **six-covering-2, researcher**, 2026-10-02.

For a distinct cover with moduli dividing10080 and minimum EXACTLY8, its
original modulus12 exists by credited8728, and its phase differs from the
original8 phase modulo4. The complete new root exclusion is
G=(8:0,9:0,10:1,14:1,12:4). Eleven five-class forms remain, and global
L_min(8) numerical bounds are unchanged. Read [proof.md](proof.md) for the
credited original-class bridge, precise resource scope and trust boundaries.

Regenerate from the repository root using the unchanged published engine:

```sh
python3 -m venv scratch/covering-env
scratch/covering-env/bin/pip install -r round-two/six-covering-2/requirements-discovery.txt
scratch/covering-env/bin/python -B round-two/six-covering-2/aligned-twelve-nonalignment/reproduce.py --generate --batches 12 --require-manifest
```

Each resumable batch stays180seconds/700new nodes with numerical threads1.
Exhausting a finite allowance returns INCOMPLETE, without asserting exclusion.
The author resumed eight batches; fresh cold standalone regeneration is not
claimed. Large generated trees stay local; no private input is required.
Any complete valid tree suffices. --require-manifest additionally requests the
author's exact record, which can differ under another discovery environment.

Literal replay and controls need Python3.10+ standard library only:

```sh
python3 -B round-two/six-covering-2/aligned-twelve-nonalignment/reproduce.py --tree path/to/tree.json --require-manifest
python3 -B round-two/six-covering-2/aligned-twelve-nonalignment/reproduce.py --controls-only
python3 -B round-two/six-covering-2/aligned-twelve-nonalignment/frontier_nonalignment.py
python3 -B -O round-two/six-covering-2/aligned-twelve-nonalignment/frontier_nonalignment.py
python3 -B round-two/six-covering-2/aligned-twelve-nonalignment/guard_controls.py
python3 -B -O round-two/six-covering-2/aligned-twelve-nonalignment/guard_controls.py
```

In this directory run `sha256sum -c SHA256SUMS`. [manifest.json](manifest.json)
records2756nodes/380branches/2376strict leaves, exact hashes and dependency
pins. [application-next.json](application-next.json) gives the eleven unexcluded
roots, their literal residuals and all60unused original resources per root.
Full literal author replay took76.897seconds/82832KiB. Ordinary bridges remain
unformalized; no independent reviewer verdict or priority claim is asserted.

The final publication-directory wrapper matched the exact full author
manifest in83.039793seconds,peak83968KiB. Complete normal/O phase controls
agree, including all5040independently constructed unit maps. Twelve wrong
domains and eight damaged resource inventories reject in both modes.
No controls-only or domain-only check accepts an exclusion certificate.
