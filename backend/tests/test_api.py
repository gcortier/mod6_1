import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/.."))
from main import load_predict_sample_fromparquet_test
import pandas as pd
import pytest


def test_load_predict_sample_fromparquet_test():
    result = load_predict_sample_fromparquet_test()
    assert isinstance(result, pd.DataFrame)
    assert not result.empty
    assert "feature1" in result.columns
    assert "feature2" in result.columns
