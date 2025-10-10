import pytest

from ditk.distribution import is_main_process, get_rank, get_world_size, is_distributed


@pytest.mark.unittest
class TestDistributionEnv:
    def test_on_local(self):
        assert not is_distributed()
        assert get_world_size() == 1
        assert get_rank() == 0
        assert is_main_process()
