import pytest
import os
import time
from ditk.annonated import generate_annonated_doc
from ditk.annonated.ppo import ppo_policy_error


@pytest.mark.unittest
def test_generate():
    os.popen('rm -rf ppo.html')
    time.sleep(0.2)
    assert not os.path.exists('ppo.html')
    test_file_path = os.path.join(os.path.dirname(__file__), '../../ditk/annonated/ppo.py')
    generate_annonated_doc(test_file_path, 'ppo.html')
    assert os.path.exists('ppo.html')
    os.popen('rm -rf ppo.html')
