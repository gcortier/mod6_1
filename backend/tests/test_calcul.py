import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/.."))
from modules.calcul import calcul_carre

import pytest


def test_calcul_carre():
    assert calcul_carre(2) == 4
    assert calcul_carre(-3) == 9
    assert calcul_carre(0) == 0
