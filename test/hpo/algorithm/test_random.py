import pytest

from ditk.hpo import uniform, quniform, choice, R
from .base import get_hpo_func, EPS


@pytest.mark.unittest
class TestHpoAlgorithmRandom:
    def test_random_single(self):
        visited, func = get_hpo_func()
        func.random().max_steps(1000).spaces({
            'x': uniform(-2, 8),
            'y': 2.5,
        }).run()

        assert len(visited) == 1000
        for item in visited:
            assert -2 <= item['x'] <= 8
            assert item['y'] == pytest.approx(2.5)

    def test_random_all(self):
        visited, func = get_hpo_func()
        func.random().max_steps(1000).spaces({
            'x': uniform(-2, 8),
            'y': quniform(-1.6, 7.8, 0.2),
            'z': choice(['a', 'b', 'c'])
        }).run()

        assert len(visited) == 1000
        for item in visited:
            assert -2 <= item['x'] <= 8
            assert -1.6 - EPS <= item['y'] <= 7.8 + EPS
            index = (item['y'] - (-1.6)) / 0.2
            assert abs(round(index) - index) == pytest.approx(0.0)
            assert item['z'] in {'a', 'b', 'c'}

    def test_random_stop_when(self):
        visited, func = get_hpo_func()
        cfg, res = func.random().stop_when(R['result'].abs() <= 0.5).spaces({
            'x': uniform(-2, 8),
            'y': quniform(-1.6, 7.8, 0.2),
        }).run()

        assert pytest.approx(res['result']) == pytest.approx(cfg['x'] * cfg['y'])
        assert abs(res['result']) <= 0.5

    def test_random_stop_when_or(self):
        visited, func = get_hpo_func()
        cfg, res = func.random() \
            .stop_when(R['result'].abs() <= 0.5) \
            .stop_when(R['result'] >= 56.25) \
            .spaces({
            'x': uniform(-2, 8),
            'y': quniform(-1.6, 7.8, 0.2),
        }).run()

        assert pytest.approx(res['result']) == pytest.approx(cfg['x'] * cfg['y'])
        assert (abs(res['result']) <= 0.5) or (res['result'] >= 56.25)

    def test_random_maximize(self):
        visited, func = get_hpo_func()
        cfg, res = func.random() \
            .max_steps(1000) \
            .maximize(R['result']) \
            .spaces({
            'x': uniform(-2, 8),
            'y': quniform(-1.6, 7.8, 0.2),
        }).run()

        assert pytest.approx(res['result']) == pytest.approx(cfg['x'] * cfg['y'])
        assert res['result'] >= 58

    def test_random_minimize(self):
        visited, func = get_hpo_func()
        cfg, res = func.random() \
            .max_steps(1000) \
            .minimize(R['result']) \
            .spaces({
            'x': uniform(-2, 8),
            'y': quniform(-1.6, 7.8, 0.2),
        }).run()

        assert pytest.approx(res['result']) == pytest.approx(cfg['x'] * cfg['y'])
        assert res['result'] <= -12
