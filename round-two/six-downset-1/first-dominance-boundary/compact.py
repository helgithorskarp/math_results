"""Compact only AFTER whole original calculations; not a mathematical shortcut."""
from hashlib import sha256
import json

ARRAYS = {'full_original_inverse_images', 'D_inverse_images',
          'B_inverse_image', 'full_original_centered_kernel'}


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode() + b'\n'


def binding(raw):
    return dict(bytes=len(raw), sha256=sha256(raw).hexdigest())


def compact(value):
    if isinstance(value, list):
        return [compact(x) for x in value]
    if isinstance(value, dict):
        return {key + '_binding' if key in ARRAYS else key:
                binding(encoded(item)) if key in ARRAYS else compact(item)
                for key, item in value.items()}
    return value


def summary(full):
    return dict(agent='six-downset-1', role='researcher',
                status='COMPLETE SOURCE-ONLY FIRST-DOMINANCE MATHEMATICS',
                whole_full_record_binding=binding(encoded(full)),
                mathematics=compact(full))
