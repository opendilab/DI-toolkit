import pytest
import os
import time
from ditk.annonated import generate_annonated_doc
from .ppo import ppo_policy_error


@pytest.mark.unittest
def test_generate():
    os.popen('rm -rf ppo.html')
    time.sleep(0.2)
    assert not os.path.exists('ppo.html')
    generate_annonated_doc('ppo.py', 'ppo.html')
    assert os.path.exists('ppo.html')
    os.popen('rm -rf ppo.html')
