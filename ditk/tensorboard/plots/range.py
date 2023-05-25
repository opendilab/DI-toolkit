import os
import warnings
from typing import Optional, Mapping

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from hbutils.string import plural_word
from scipy import interpolate
from sklearn.cluster import KMeans

from ..log import tb_extract_recursive_logs


def _tb_rplot_single_group(dfs, xname, yname, label, ax, n_samples: Optional[int] = None,
                           lower_bound: Optional[float] = None, upper_bound: Optional[float] = None):
    datas = []
    for d in dfs:
        df = d[[xname, yname]]
        df = df[~df[yname].isna()]
        func = interpolate.UnivariateSpline(df[xname], df[yname], s=0)
        datas.append((df[xname], df[yname], func))

    if lower_bound is None:
        lower_bound = np.max([x.min() for x, _, _ in datas])
    if upper_bound is None:
        upper_bound = np.min([x.max() for x, _, _ in datas])

    all_xs = np.concatenate([x[(x <= upper_bound) & (x >= lower_bound)] for x, _, _ in datas])
    if n_samples is None:
        n_samples = all_xs.shape[0]
    if n_samples > all_xs.shape[0]:
        warnings.warn(f'{plural_word(all_xs.shape[0], "sample")} found in total, '
                      f'n_samples ignored due to the unavailableness of {plural_word(n_samples, "sample")}.')
        n_samples = all_xs.shape[0]

    clu_algo = KMeans(n_samples, n_init='auto')
    clu_algo.fit(all_xs[..., None])
    px = np.sort(clu_algo.cluster_centers_.squeeze(-1))

    fx = []
    fy = []
    for _, _, func in datas:
        fx.append(px)
        fy.append([func(x) for x in px])
    fx = np.concatenate(fx)
    fy = np.concatenate(fy)

    sns.lineplot(x=fx, y=fy, label=label, ax=ax)


def tb_create_range_plots(logdir, xname, yname,
                          label_map: Optional[Mapping[str, str]] = None, n_samples: Optional[int] = None,
                          lower_bound: Optional[float] = 0.0, upper_bound: Optional[float] = None,
                          ax=None):
    label_map = dict(label_map or {})
    log_data = tb_extract_recursive_logs(logdir)
    log_groups = {}
    for key, data in log_data.items():
        first_seg = key.split(os.path.sep)[0]
        if first_seg not in log_groups:
            log_groups[first_seg] = []
        log_groups[first_seg].append(data)

    if ax is None:
        ax = plt.gca()

    for group_name, dfs in log_groups.items():
        _tb_rplot_single_group(
            dfs, xname, yname,
            label=label_map.get(group_name, group_name),
            n_samples=n_samples,
            lower_bound=lower_bound,
            upper_bound=upper_bound,
            ax=ax,
        )
