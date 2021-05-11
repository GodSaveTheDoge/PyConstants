import pytest
from pyconstants import const

def test_costant():
    # It's not that complex, why am I even writing tests?
    const .myvar = 5
    with pytest.raises(SyntaxError):
        myvar = 7
    assert myvar == 5
