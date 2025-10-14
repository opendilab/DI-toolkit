import glob
import os
import re
from contextlib import contextmanager
from typing import Optional
from unittest.mock import patch

try:
    import torch
    import torch.distributed as dist
except (ImportError, ModuleNotFoundError):
    torch = None
    dist = None

from hbutils.system import TemporaryDirectory
from natsort import natsorted


class DistDataSaver:
    def __init__(self, tmpdir: Optional[str] = None):
        if tmpdir is not None:
            self.tmp = None
            self.tmpdir = tmpdir
        else:
            self.tmp = TemporaryDirectory()
            self.tmpdir = self.tmp.name

    def __enter__(self):
        yield self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.tmp is not None:
            self.tmp.cleanup()

    def dist(self):
        return DistDataSaver(tmpdir=self.tmpdir)

    def _get_rank_file(self, rank: int):
        return os.path.join(self.tmpdir, f'rank-{rank}.pt')

    def _save_data(self, rank: int, data: dict):
        torch.save(data, self._get_rank_file(rank))

    def _load_data(self, rank: int):
        return torch.load(self._get_rank_file(rank), map_location='cpu')

    def save_data(self, rank: int, data):
        self._save_data(rank, data)

    def load_data(self, rank: int):
        return self._load_data(rank)

    def update_data(self, rank: int, extra: dict):
        data = self._load_data(rank)
        data.update(extra)
        self._save_data(rank, data)

    def load_all(self):
        d_data = {}
        for file in natsorted(glob.glob(os.path.join(self.tmpdir, f'rank-*.pt'))):
            matching = re.fullmatch(r'^rank-(?P<rank>\d+)\.pt$', os.path.basename(file))
            rank = int(matching.group('rank'))
            d_data[rank] = self._load_data(rank)
        return d_data


@contextmanager
def spawn_worker_context(rank, world_size, port):
    with patch.dict(os.environ, {'MASTER_ADDR': '127.0.0.1', 'MASTER_PORT': str(port)}):
        dist.init_process_group("gloo", rank=rank, world_size=world_size)
        try:
            yield
        finally:
            dist.destroy_process_group()
