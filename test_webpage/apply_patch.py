import patch
import os

pset = patch.fromfile(os.path.join(os.path.dirname(os.path.realpath(__file__)),"output.patch"))
pset.apply()