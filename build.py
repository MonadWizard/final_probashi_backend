import os
import py_compile
from pathlib import Path
from os import walk, remove


BASE_DIR = Path(__file__).resolve().parent.parent
project_path = Path(__file__).resolve().parent

build_path = f"{BASE_DIR}/BUILD"
project_path = project_path

try:
    os.system(f"rm -r -f {build_path}")
except Exception as e:
    print(e)
try:
    os.mkdir(f"{build_path}")
except:
    print("can not build dir")

try:
    os.system(f"cp -r {project_path} {build_path}")
except:
    print("can not copy Build")

# # os.system("python -m compileall ./BUILD")

f = []
for (dirpath, dirnames, filenames) in walk(build_path):
    f.extend(map(lambda filename: (dirpath) + "/" + filename, filenames))

f = sorted(f)

for i in f:
    if i.endswith(".py"):
        py_compile.compile(f"{i}", f"{i}c")
        remove(i)
