import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import itertools

file_path = "rz_dependency.txt"
init_params = {"r1":0.6, "r2":0.5, "z1":3.0, "z2":2.7}

# データ読み込み
df_res = pd.read_csv(file_path, sep=r"\s+").round(5)
target = "R"
features = [col for col in df_res.columns if col != target]
R_min = df_res[target].min()
R_max = df_res[target].max()

# 使用点の探索 (init_paramsから最も近いの探索)


n = len(features)
fig, axes = plt.subplots(nrows=n, ncols=n, figsize=(4 * n, 4 * n))

# ==== メインループ ====
for i, xi in enumerate(features):
    for j, xj in enumerate(features):
        ax = axes[i, j]

        # ====== 共通マスク（固定変数を除いてフィルタリング）======
        mask = pd.Series(True, index=df_res.index)
        for fk, fv in init_params.items():
            if (i == j and fk != xi) or (i != j and fk not in [xi, xj]):
                mask &= (df_res[fk] == fv)
        df_plot = df_res[mask]

        if df_plot.empty:
            ax.set_visible(False)
            print(f"⚠️ Skip {xi}, {xj} — no data after filtering")
            continue

        # ====== 対角: R vs xi の lineplot ======
        if i == j:
            try:
                df_plot_sorted = df_plot.sort_values(by=xi)
                sns.scatterplot(
                    df_plot_sorted,
                    x=xi,
                    y=target,
                    ax=ax,
                    edgecolor="Red",
                    color='None',
                    s=50,
                    linewidth=2.0,
                    marker="o")
                ax.set_title(f"{target} vs {xi} (others fixed)")
            except Exception as e:
                ax.set_visible(False)
                print(f"❌ Error in diag {xi}: {e}")

        # ====== 非対角: heatmap（xi × xj） ======
        else:
            try:
                pivot = df_plot.pivot_table(index=xi, columns=xj, values=target, aggfunc="mean")
                if pivot.isnull().all().all():
                    ax.set_visible(False)
                    continue
                sns.heatmap(
                    pivot, 
                    ax=ax, 
                    cmap="Spectral", 
                    vmin=R_min, 
                    vmax=R_max,
                    cbar=False)
                ax.set_title(f"{xi} × {xj} (others fixed)")
            except Exception as e:
                ax.set_visible(False)
                print(f"❌ Error in off-diag {xi}, {xj}: {e}")

        # 軸ラベル整形
        if i == n - 1:
            ax.set_xlabel(xj)
        else:
            ax.set_xlabel("")

        if j == 0:
            ax.set_ylabel(xi)
        else:
            ax.set_ylabel("")
plt.tight_layout()
plt.savefig('pairplot.png')
