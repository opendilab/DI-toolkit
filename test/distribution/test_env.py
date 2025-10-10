from unittest import skipUnless

import pytest
from hbutils.system import get_free_port
from hbutils.testing import vpip, OS

from ditk.distribution import is_main_process, get_rank, get_world_size, is_distributed
from .worker_context import DistDataSaver, spawn_worker_context

try:
    import torch
    import torch.multiprocessing as mp
except (ImportError, ModuleNotFoundError):
    torch = None
    mp = None


@pytest.fixture()
def free_port():
    return get_free_port()


def dist_default_worker(rank, world_size, port, saver: DistDataSaver):
    with spawn_worker_context(rank, world_size, port):
        jdata = {
            'is_main_process': is_main_process(),
            'get_rank': get_rank(),
            'get_world_size': get_world_size(),
            'is_distributed': is_distributed(),
        }
        saver.save_data(rank, jdata)


@pytest.mark.unittest
class TestDistributionEnv:
    def test_on_local(self):
        assert not is_distributed()
        assert get_world_size() == 1
        assert get_rank() == 0
        assert is_main_process()

    @skipUnless(vpip('torch'), 'Torch required')
    def test_on_torch_local(self):
        assert not is_distributed()
        assert get_world_size() == 1
        assert get_rank() == 0
        assert is_main_process()

    @skipUnless(not vpip('torch'), 'No torch required')
    def test_on_no_torch_local(self):
        assert not is_distributed()
        assert get_world_size() == 1
        assert get_rank() == 0
        assert is_main_process()

    @skipUnless(vpip('torch') and not OS.windows, 'Torch with dist required (non-windows only)')
    def test_on_dist_app(self, free_port):
        world_size = 4
        saver = DistDataSaver()
        mp.spawn(dist_default_worker, args=(world_size, free_port, saver), nprocs=world_size, join=True)

        retval = saver.load_all()
        assert len(retval) == world_size
        assert retval == {
            0: {'is_main_process': True, 'get_rank': 0, 'get_world_size': 4, 'is_distributed': True},
            1: {'is_main_process': False, 'get_rank': 1, 'get_world_size': 4, 'is_distributed': True},
            2: {'is_main_process': False, 'get_rank': 2, 'get_world_size': 4, 'is_distributed': True},
            3: {'is_main_process': False, 'get_rank': 3, 'get_world_size': 4, 'is_distributed': True},
        }
