"""Only the published defining residual is shared by the two arithmetic routes."""
from pathlib import Path
import sys
import source_gate

SOURCE_GATE = source_gate.verify()
SOURCE = source_gate.BASE / 'credited/effective-arithmetic-cutoff/credited/uniform-repair-face'
sys.path.insert(0, str(SOURCE))
import zero_generator


def defining_fields():
    raw = zero_generator.generated()
    return (raw['joint_residual_numerator'], raw['joint_residual_denominator'])
