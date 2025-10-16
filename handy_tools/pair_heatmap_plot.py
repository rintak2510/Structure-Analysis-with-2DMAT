import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import platform
import os
import subprocess
import sys


# ====  データ読み込み ====
def load_data(file_path: str) -> pd.DataFrame:
    df = pd.read_csv(file_path, sep=r"\s+").round(5)
    return df


# ====  初期値処理 ====
def select_basis(df: pd.DataFrame, init_params: dict, target: str) -> dict:
    features = [col for col in df.columns if col != target]
    n = len(features)
    if len(init_params) != n:
        sys.exit("Error: the number of initial params must be same as features.")
    dist = np.sqrt(((df[features] - pd.Series(init_params))**2).sum(axis=1))
    idx_min = dist.idxmin()
    basis = df.loc[idx_min, features].to_dict()
    return basis


# ====  可視化関数 ====
def plot_rz_dependency(df: pd.DataFrame,
                       basis: dict,
                       target: str = "R",
                       output_path: str = "pairplot.png",
                       cmap: str = "Spectral") -> None:
    features = [col for col in df.columns if col != target]
    n = len(features)
    R_min = df[target].min()
    R_max = df[target].max()

    fig, axes = plt.subplots(nrows=n, ncols=n, figsize=(4 * n, 4 * n))
    heatmap_mappable = None

    for i, xi in enumerate(features):
        for j, xj in enumerate(features):
            ax = axes[i, j]
            mask = pd.Series(True, index=df.index)
            for fk, fv in basis.items():
                if (i == j and fk != xi) or (i != j and fk not in [xi, xj]):
                    mask &= (df[fk] == fv)
            df_plot = df[mask]

            if df_plot.empty:
                ax.set_visible(False)
                continue

            if i == j:
                # ==== 対角: 散布図 ====
                df_plot_sorted = df_plot.sort_values(by=xi)
                sns.scatterplot(df_plot_sorted, x=xi, y=target, ax=ax,
                                edgecolor="Red", color='None', s=50,
                                linewidth=2.0, marker="o")
                ax.set_ylim(R_min, 0.08)
                ax.set_title(f"{target} vs {xi} (others fixed)")
            else:
                # ==== 非対角: ヒートマップ ====
                pivot = df_plot.pivot_table(index=xi, columns=xj, values=target, aggfunc="mean")
                if pivot.isnull().all().all():
                    ax.set_visible(False)
                    continue
                hm = sns.heatmap(pivot, ax=ax, cmap=cmap, vmin=R_min, vmax=0.05, cbar=False)
                x_vals = pivot.columns.values
                y_vals = pivot.index.values
                x_ticks = np.linspace(0, len(x_vals)-1, 3)
                y_ticks = np.linspace(0, len(y_vals)-1, 3)
                ax.set_xticks(x_ticks)
                ax.set_xticklabels([f"{v:.3g}" for v in np.quantile(x_vals, [0, 0.5, 1])])
                ax.set_yticks(y_ticks)
                ax.set_yticklabels([f"{v:.3g}" for v in np.quantile(y_vals, [0, 0.5, 1])])
                ax.invert_yaxis()
                ax.set_title(f"{xi} × {xj} (others fixed)")

                if heatmap_mappable is None:
                    heatmap_mappable = hm.get_children()[0]

            # 軸ラベル整形
            if i == n - 1:
                ax.set_xlabel(xj, fontsize=14, fontname='Helvetica')
            else:
                ax.set_xlabel("")
            if j == 0:
                ax.set_ylabel(xi, fontsize=14, fontname='Helvetica')
            else:
                ax.set_ylabel("")

    if heatmap_mappable is not None:
        cbar_ax = fig.add_axes([0.92, 0.15, 0.02, 0.7])
        fig.colorbar(heatmap_mappable, cax=cbar_ax, label='R-factor')

    plt.savefig(output_path)
    plt.close(fig)

    open_img(output_path)


# ====  画像を開く関数 ====
def open_img(image_path: str):
    system = platform.system()
    if system == "Windows":
        os.startfile(image_path)
    elif system == "Darwin":
        subprocess.run(["open", image_path])
    elif "microsoft" in platform.release().lower():
        subprocess.run(["explorer.exe", image_path])
    else:
        subprocess.run(["xdg-open", image_path])


# ====  メイン呼び出し例 ====
if __name__ == "__main__":
    file_path = "rz_dependency.txt"
    init_params = {"r1": 0.8, "r2": 0.7, "z1": 2.8, "z2": 2.7}
    df = load_data(file_path)
    basis = select_basis(df, init_params, target="R")
    plot_rz_dependency(df, basis, target="R", output_path="pairplot.png")
