# Original16 presence at the first open five-class root

Actual author **six-covering-2, researcher**, 2026-10-01.

For distinct covers of minimum EXACTLY8 and all moduli dividing10080,
the prescribed root8:0,9:0,10:1,14:0,12:4 requires an ORIGINAL even16
class whose phase is not0mod8. Covering existence at this root is equivalent
to existence at its16:2 or16:4 child. Both children remain OPEN; the
thirteen five-class forms and numerical L_min(8) bounds are unchanged.

Read [proof.md](proof.md) for the exact domain, original-class bridge,
new685-node exclusion, credited methods and limitations. The tree is
omitted; [manifest.json](manifest.json) fixes its exact literal replay and
six unchanged core source hashes. [application-next.json](application-next.json)
gives both open residual bitsets and all59 unused original resources,
including every phase of all four TOPs.

From the repository root, create a local discovery environment if needed:

```sh
python3 -m venv scratch/covering-env
scratch/covering-env/bin/pip install -r round-two/six-covering-2/requirements-discovery.txt
scratch/covering-env/bin/python -B round-two/six-covering-2/first-root-sixteen-presence/reproduce.py --generate --batches 12 --require-manifest
```

Each resumable batch remains180s/700new nodes, with all native threads one.
The voluntary allowance is finite; exhaustion returns INCOMPLETE and
asserts no exclusion. The author used an extracted completed subtree,
not a fresh cold standalone regeneration. Any complete valid tree proves
the conditional exclusion; --require-manifest additionally requires the
author hashes and may differ with a different numerical discovery environment.

Once a certificate is available, replay needs only Python3.10+ standard library:

```sh
python3 -B round-two/six-covering-2/first-root-sixteen-presence/reproduce.py --tree path/to/certificate.json --require-manifest
python3 -B round-two/six-covering-2/first-root-sixteen-presence/phase_controls.py
python3 -B -O round-two/six-covering-2/first-root-sixteen-presence/phase_controls.py
python3 -B round-two/six-covering-2/first-root-sixteen-presence/guard_controls.py
python3 -B -O round-two/six-covering-2/first-root-sixteen-presence/guard_controls.py
```

In this directory also run `sha256sum -c SHA256SUMS`. The final integrated
replay matched in22.870s with48324KiB peak child RSS. Complete phase controls
agree normally/optimized; ten wrong domains, eight wrong application
inventories and six invalid transports reject in both modes. These controls
supplement the literal proof; they do not replace it. The written bridge is
unformalized and no independent reviewer verdict is claimed.
