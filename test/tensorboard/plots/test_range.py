import matplotlib.pyplot as plt
import pytest
import seaborn as sns
from hbutils.testing import isolated_directory, disable_output

from ditk.tensorboard import tb_create_range_plots
from test.testing import get_testfile


@pytest.mark.unittest
class TestTensorboardPlotsRange:
    def test_tb_create_range_plots(self, image_diff):
        answer_file = get_testfile('pong_tb_plot.png')
        with isolated_directory({'pong_tb': get_testfile('pong_tb')}):
            sns.set()
            plt.figure(figsize=(7, 5.5))

            with disable_output():
                tb_create_range_plots(
                    'pong_tb',
                    'step', 'evaluator_step/reward_mean',
                    upper_bound=5e5
                )

            plt.tight_layout()
            plt.savefig('plot.png', bbox_inches='tight')

            assert image_diff(answer_file, 'plot.png', throw_exception=False) < 0.05
