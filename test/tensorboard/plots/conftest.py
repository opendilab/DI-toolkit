import matplotlib.pyplot as plt
import pytest


@pytest.fixture(scope='module', autouse=True)
def clear_previous_plot():
    plt.cla()
