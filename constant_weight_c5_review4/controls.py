#!/usr/bin/env python3
"""Reject corruptions of the actual public tree/domain bridges and lower witness."""
from copy import deepcopy
import json

from audit import TARGET, all_links, check_certificate, model, witness


def rejected(function, expected):
    try:
        function()
    except ValueError as error:
        if expected not in str(error):
            raise ValueError("unexpected rejection: " + str(error)) from error
        return str(error)
    raise ValueError("invalid mathematical input accepted")


def main():
    context = model()
    _, links = all_links(context, 17)
    original = json.loads((TARGET / "certificate.json").read_text())
    _, adjacency = check_certificate(context, original, links)
    reports = {}

    def check(name, altered, fragment):
        reports[name] = rejected(lambda: check_certificate(context, altered, links), fragment)

    altered = deepcopy(original)
    altered["representative"][0] += 1
    check("wrong_representative", altered, "representative bridge")
    altered = deepcopy(original)
    altered["residual"].pop()
    check("missing_residual_orbit", altered, "residual domain")
    altered = deepcopy(original)
    altered["target"] = 9
    check("wrong_target", altered, "certificate target")
    altered = deepcopy(original)
    altered["tree"]["children"].pop()
    check("missing_inclusion_branch", altered, "branch coverage")
    altered = deepcopy(original)
    altered["tree"]["colors"][0].pop()
    check("missing_color_vertex", altered, "color partition")
    altered = deepcopy(original)
    altered["tree"]["colors"][0].append(altered["tree"]["colors"][0][0])
    check("repeated_color_vertex", altered, "repeated vertex")
    altered = deepcopy(original)
    altered["tree"]["colors"][0].append(len(adjacency))
    check("extra_color_vertex", altered, "vertex range")
    altered = deepcopy(original)
    first, second = next((i, j) for i, mask in enumerate(adjacency)
                         for j in range(i + 1, len(adjacency)) if mask & (1 << j))
    classes = altered["tree"]["colors"]
    for color in classes:
        if second in color:
            color.remove(second)
    classes[:] = [color for color in classes if color]
    next(color for color in classes if first in color).append(second)
    check("compatible_vertices_in_one_color", altered, "color contains")
    altered = deepcopy(original)
    altered["tree"] = {"small": True}
    check("false_cardinality_leaf", altered, "false cardinality")

    rows = [line.strip() for line in (TARGET / "witness68.txt").read_text().splitlines()
            if line.strip()]
    witness(rows)
    altered = rows[:]
    altered[0] = altered[1]
    reports["duplicate_lower_word"] = rejected(lambda: witness(altered), "distinctness")
    altered = rows[:]
    old = int(altered[0][::-1], 2)
    used = next(i for i in range(18) if old & (1 << i))
    # The classical fixture omits 17. This one-word exchange preserves rank;
    # check that a packing with broken C5 symmetry is not a symmetric witness.
    replacement = (old ^ (1 << used)) | (1 << 17)
    altered[0] = format(replacement, "018b")[::-1]
    reports["broken_lower_symmetry"] = rejected(lambda: witness(altered), "symmetry")
    print(json.dumps({"rejected_controls": reports, "control_count": len(reports)},
                     indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
