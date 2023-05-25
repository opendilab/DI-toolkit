import glob
import os

import pytest
from hbutils.testing import isolated_directory, simulate_entry

from ditk.doc.annotated import generate_annotated_doc
from ditk.doc.annotated.__main__ import cli


@pytest.mark.unittest
def test_generate():
    with isolated_directory({'ppo.py': os.path.join('ditk', 'doc', 'annotated', 'ppo.py')}):
        generate_annotated_doc('ppo.py', 'ppo.html', 'This is the title')
        assert os.path.exists('ppo.html')
        assert len(glob.glob(os.path.join('assets', '*.css'))) == 2


@pytest.mark.unittest
def test_cli():
    with isolated_directory({'ppo.py': os.path.join('ditk', 'doc', 'annotated', 'ppo.py')}):
        result = simulate_entry(cli, ['ditk.doc.annotated', 'create', '-i', 'ppo.py', '-o', 'ppo.html'])
        assert result.exitcode == 0
        assert os.path.exists('ppo.html')
        assert len(glob.glob(os.path.join('assets', '*.css'))) == 2
