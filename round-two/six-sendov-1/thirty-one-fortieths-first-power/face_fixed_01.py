from pathlib import Path
import importlib.util
p=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('fixed_face_support',p/'face_fixed.py')
m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.run(1)
