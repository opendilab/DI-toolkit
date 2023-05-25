import pytest
import os
import time
from ditk.doc.annonated import generate_annotated_doc


@pytest.mark.unittest
def test_generate():
    os.popen('rm -rf ppo.html')
    time.sleep(0.2)
    assert not os.path.exists('ppo.html')
    test_file_path = os.path.join(os.path.dirname(__file__), '../../ditk/doc/annonated/ppo.py')
    generate_annotated_doc(test_file_path, 'ppo.html')
    assert os.path.exists('ppo.html')
    os.popen('rm -rf ppo.html')
