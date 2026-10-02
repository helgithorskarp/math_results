# Actual four-coset seven-tail: 82-point construction, 110-point bound

Actual author: **six-covering-1, researcher**, 2026-10-02.

For K subset{0mod4,not6mod9} modulo720, allow one phase per DISTINCT
ORIGINAL modulus7d, d|720,d>=2. A tail covering all seven copies of K
requires |K|<=110. positive-tail.json explicitly completes one82-point
K. See [proof.md](proof.md) for the complete finite reduction and scope.

The particular82-point tail has no compatible owned first720 stage at
fixed8:5/9:6: the complete distinct-resource pair budget is427<448.
These are conditional results. They supply neither a compatible
first720 stage nor a full15120/minimum-eight covering. Global L_min(8)
bounds remain unchanged. Checks are same-author independent algorithms,
not an independent reviewer verdict or formalization.

From this directory, with Python>=3.10 and g++ supporting C++17:

    python3 -B verify.py --scratch /tmp/four-coset-tail-overlap-replay

Six sequential normal/optimized replays check complete integer profiles,
separate literal C++ progressions, and the positive82-point fixture.
Ten semantic certificate damages reject in both engines/modes; four
positive-fixture damages reject in both modes. Each child has a20-second
guard and one numerical thread. Guard exhaustion proves nothing.

Individual replays:

    python3 -B check.py --output /tmp/four-overlap-check.json
    python3 -B audit.py --scratch /tmp/four-overlap-build --output /tmp/four-overlap-audit.json
    python3 -B controls.py --output /tmp/four-overlap-positive.json

Only compact source, fixed-domain certificate, frozen counters and the
29-class positive fixture are published. Builds, logs and generated
state remain in scratch. [manifest.json](manifest.json) records the
author replay and hashes; inequalities and literal classes prove the claim.
