import pytest
from .views import soma

def test_soma():
    a = 5
    b = 10
    resultado = soma(a, b)
    assert resultado == 15