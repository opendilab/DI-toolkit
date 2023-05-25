import os

import pytest
from hbutils.testing import isolated_directory

from ditk.doc.annotated import generate_annotated_doc


@pytest.mark.unittest
def test_generate():
    with isolated_directory({'ppo.py': os.path.join('ditk', 'doc', 'annotated', 'ppo.py')}):
        generate_annotated_doc('ppo.py', 'ppo.html', 'This is the title')
        assert os.path.exists('ppo.html')
