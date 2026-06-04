# -*- coding: utf-8 -*-
from abaqus import mdb
import os

model = mdb.Model(name="API_Probe")
names = dir(model)
out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
if not os.path.isdir(out_dir):
    os.makedirs(out_dir)
out = os.path.join(out_dir, "abaqus_api_probe.txt")
with open(out, "w") as f:
    f.write("COUPLING_NAMES=" + ",".join([n for n in names if "Coupl" in n or "coupl" in n]) + "\n")
    f.write("TRACTION_NAMES=" + ",".join([n for n in names if "Traction" in n or "Force" in n or "Pressure" in n]) + "\n")
