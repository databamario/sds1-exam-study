"""Generate the figures used by the graph-reading questions.

The figures are drawn here rather than cropped from the lecture PDFs so they
stay sharp at any size, carry no course material, and are reproducible with a
single command:

    python tools/figures.py

Every figure is deterministic (fixed seed, no randomness unless the figure is
about sampling), and is written to data/images/<name>.png at 2x resolution.

The types mirror the ones the exam actually asks about:

    bar_stacked        grouped bars, compare counts across two groups
    boxplots_h         horizontal box plots, infer which has most variance
    hist_skewed        right-skewed histogram, infer mean vs median
    ci_dotplot         estimates with 95% CI, infer significance
    normal_shaded      normal curve with shaded regions, write P(...)
    scatter_trend      scatter plot, describe direction and strength
    density_overlay    two overlapping densities, compare groups
    corr_heatmap       correlation matrix, find the strongest pair
    hist_symmetric     symmetric histogram, compare sd and variance
    freq_bars          frequency table as bars, proportions and marginals
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "images"

INK = "#1f2933"
MUTED = "#7b8794"
GRID = "#e4e7eb"
BAR_A = "#2f6f9f"
BAR_B = "#e08a3c"
BAR_C = "#5b8c5a"
SHADE_1 = "#bcd9ef"
SHADE_2 = "#f6d99a"
SHADE_3 = "#e8a5a5"

DPI = 200

# ---------------------------------------------------------------- figure data
#
# The numbers each figure draws live here, at module level, rather than inside
# the drawing functions. That is what lets ``verify_numbers.py`` import them and
# check that the G-* questions' answers and options actually agree with what is
# plotted. While the data was buried in the functions, every number in a figure
# question was unchecked - which is how G-MC-008 came to claim that group A's
# interval spans 7.6 units and group B's 3.8 when both span 7.6.

FIG_DATA = {
    "bar_stacked": {
        "categories": ["Never", "Rarely", "Sometimes", "Often"],
        "men": [18, 22, 34, 26],
        "women": [36, 22, 14, 13],
    },
    "boxplots_h": {
        #            low    q1    med   q3    high
        "A": [10, 22, 30, 38, 50],
        "B": [5, 20, 30, 40, 55],
        "C": [28, 29, 30, 31, 32],
    },
    "hist_skewed": {
        "seed": 7, "shape": 2.0, "scale": 2.0, "n": 4000, "bins": 28,
    },
    # Paired figures. Four questions were written about two plots side by side
    # while only one was ever drawn, so the pair is now what gets drawn.
    "hist_skewed_pair": {
        "seed": 7, "shape": 2.0, "scale": 2.0, "n": 4000, "bins": 28,
        "sym_seed": 8, "sym_mean": 4.0, "sym_sd": 2.0, "sym_n": 4000,
    },
    "hist_symmetric_pair": {
        "seed": 21, "mean": 15.0, "narrow_sd": 2.0, "wide_sd": 7.0,
        "n": 4000, "bins": 30,
    },
    "hist_counts_pair": {
        "seed": 33, "mean": 50.0, "sd": 10.0,
        "small_n": 30, "large_n": 80, "bins": 15,
    },
    "ci_dotplot": {
        "names": ["A", "B"],
        "means": [52.4, 45.1],
        "lo": [45.0, 41.3],
        "hi": [59.8, 48.9],
        "ref": 44.0,
    },
    "normal_shaded": {
        "edges": [5.0, 6.2, 7.4],
        "labels": ["a", "b", "c"],
    },
    "scatter_trend": {
        "x_mean": 50, "x_sd": 10, "slope": 0.8, "intercept": 20,
        "noise_sd": 14, "n": 120, "seed": 3,
    },
    "density_overlay": {
        "A_mean": 30, "A_sd": 5, "B_mean": 38, "B_sd": 9, "n": 3000,
        "seed": 11,
    },
    "corr_heatmap": {
        "labels": ["Hours", "Sleep", "Screen", "Stress", "Caff"],
        "matrix": [
            [1.00, -0.28, 0.62, 0.41, 0.35],
            [-0.28, 1.00, 0.18, -0.33, -0.15],
            [0.62, 0.18, 1.00, 0.55, 0.29],
            [0.41, -0.33, 0.55, 1.00, 0.47],
            [0.35, -0.15, 0.29, 0.47, 1.00],
        ],
    },
    "freq_bars": {
        "labels": ["0-9", "10-19", "20-29", "30-39", "40-49"],
        "counts": [2, 5, 11, 9, 3],
    },
}


def _style(ax) -> None:
    """Shared look: no top/right spines, soft horizontal grid only."""
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(GRID)
    ax.tick_params(colors=MUTED, labelsize=9)
    ax.yaxis.label.set_color(INK)
    ax.xaxis.label.set_color(INK)


def _save(fig, name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"{name}.png"
    fig.savefig(path, dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("  wrote %s" % path.relative_to(ROOT))


# --------------------------------------------------------------------- types

def bar_stacked() -> None:
    """Two groups across four categories; drives the 'describe the plot' item."""
    categories = FIG_DATA["bar_stacked"]["categories"]
    men = np.array(FIG_DATA["bar_stacked"]["men"])
    women = np.array(FIG_DATA["bar_stacked"]["women"])

    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    x = np.arange(len(categories))
    w = 0.38
    ax.bar(x - w / 2, men, w, label="Men", color=BAR_A)
    ax.bar(x + w / 2, women, w, label="Women", color=BAR_B)
    ax.set_xticks(x, categories)
    ax.set_xlabel("How often do you read a book?")
    ax.set_ylabel("Number of respondents")
    ax.legend(frameon=False, fontsize=9)
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    _style(ax)
    _save(fig, "bar_stacked")


def boxplots_h() -> None:
    """Three boxes with clearly different spread; the 'highest variance' item."""
    fig, ax = plt.subplots(figsize=(6.4, 3.2))
    labels = ["A", "B", "C"]
    stats = [tuple(FIG_DATA["boxplots_h"][k]) for k in ("A", "B", "C")]
    for i, (lo, q1, med, q3, hi) in enumerate(stats):
        ax.plot([i, i], [lo, hi], color=MUTED, linewidth=1.4)
        ax.plot([i - 0.12, i + 0.12], [lo, lo], color=MUTED, linewidth=1.4)
        ax.plot([i - 0.12, i + 0.12], [hi, hi], color=MUTED, linewidth=1.4)
        ax.add_patch(plt.Rectangle((i - 0.18, q1), 0.36, q3 - q1,
                                   facecolor=BAR_A, edgecolor="none", alpha=0.75))
        ax.plot([i - 0.18, i + 0.18], [med, med], color=INK, linewidth=2.2)
    ax.set_xticks(range(len(labels)), labels)
    ax.set_xlabel("Group")
    ax.set_ylabel("Response value")
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    _style(ax)
    _save(fig, "boxplots_h")


def hist_skewed() -> None:
    """Right-skewed: pulls mean above median. Drives the mean-vs-median item."""
    d = FIG_DATA["hist_skewed"]
    rng = np.random.default_rng(d["seed"])
    sample = rng.gamma(shape=d["shape"], scale=d["scale"], size=d["n"])
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    ax.hist(sample, bins=d["bins"], color=BAR_A, edgecolor="white", linewidth=0.6)
    ax.set_xlabel("Response value")
    ax.set_ylabel("Frequency")
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    _style(ax)
    _save(fig, "hist_skewed")


def ci_dotplot() -> None:
    """Estimates with 95% CI. Group A's CI clears the reference line, B's does not.

    A's interval is drawn roughly twice as wide as B's on purpose: it lets the
    margin-of-error item have a real answer, and it makes the point that the
    estimate furthest from the reference is not the sharpest one.
    """
    names = FIG_DATA["ci_dotplot"]["names"]
    means = FIG_DATA["ci_dotplot"]["means"]
    lo = FIG_DATA["ci_dotplot"]["lo"]
    hi = FIG_DATA["ci_dotplot"]["hi"]
    ref = FIG_DATA["ci_dotplot"]["ref"]

    fig, ax = plt.subplots(figsize=(6.4, 3.0))
    y = np.array([1, 0])  # A on top, B below, reading order
    ax.errorbar(means, y, xerr=[np.array(means) - np.array(lo),
                                np.array(hi) - np.array(means)],
                fmt="o", color=BAR_A, markersize=9, capsize=6, linewidth=2)
    ax.axvline(ref, color=BAR_B, linestyle="--", linewidth=1.8)
    ax.annotate(f"reference = {ref}", xy=(ref, 0.62), xytext=(ref, 0.68),
                color=BAR_B, fontsize=9, ha="center", va="bottom")
    ax.set_yticks(y, names)
    ax.set_ylim(-0.55, 1.6)
    ax.set_xlabel("Mean response with 95% confidence interval")
    ax.grid(axis="x", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    _style(ax)
    _save(fig, "ci_dotplot")


def normal_shaded() -> None:
    """Normal curve with three shaded regions, like the P(...) exercise."""
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    x = np.linspace(2, 8, 800)
    y = 3.2 * np.exp(-0.5 * ((x - 5) / 1.2) ** 2)

    ax.fill_between(x, 0, y, where=(x >= 5) & (x <= 6.2),
                    color=SHADE_1, alpha=0.9)
    ax.fill_between(x, 0, y, where=(x >= 6.2) & (x <= 7.4),
                    color=SHADE_2, alpha=0.9)
    ax.fill_between(x, 0, y, where=(x >= 7.4),
                    color=SHADE_3, alpha=0.9)
    ax.plot(x, y, color=INK, linewidth=1.8)

    for xv, label in zip(FIG_DATA["normal_shaded"]["edges"],
                        FIG_DATA["normal_shaded"]["labels"]):
        ax.axvline(xv, color=MUTED, linewidth=1.0, linestyle=":")
        ax.text(xv, 3.45, f" {label}", color=MUTED, fontsize=9)

    ax.set_xlabel("Value of X")
    ax.set_ylabel("Density")
    ax.set_ylim(0, 3.8)
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    _style(ax)
    _save(fig, "normal_shaded")


def scatter_trend() -> None:
    """Positive but moderate association; drives direction and strength items."""
    d = FIG_DATA["scatter_trend"]
    rng = np.random.default_rng(d["seed"])
    x = rng.normal(d["x_mean"], d["x_sd"], d["n"])
    y = d["slope"] * x + d["intercept"] + rng.normal(0, d["noise_sd"], d["n"])
    fig, ax = plt.subplots(figsize=(5.6, 3.6))
    ax.scatter(x, y, s=34, color=BAR_A, alpha=0.75, edgecolor="none")
    ax.set_xlabel("Study hours per week")
    ax.set_ylabel("Final score")
    ax.grid(color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    _style(ax)
    _save(fig, "scatter_trend")


def density_overlay() -> None:
    """Two groups with different centres and different spreads."""
    d = FIG_DATA["density_overlay"]
    rng = np.random.default_rng(d["seed"])
    a = rng.normal(d["A_mean"], d["A_sd"], d["n"])
    b = rng.normal(d["B_mean"], d["B_sd"], d["n"])
    grid = np.linspace(8, 58, 500)

    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    ax.plot(grid, 3.2 * np.exp(-0.5 * ((grid - 30) / 5) ** 2) / 5,
            color=BAR_A, linewidth=2, label="Group A")
    ax.plot(grid, 3.2 * np.exp(-0.5 * ((grid - 38) / 9) ** 2) / 9,
            color=BAR_B, linewidth=2, label="Group B")
    ax.fill_between(grid, 0, 3.2 * np.exp(-0.5 * ((grid - 30) / 5) ** 2) / 5,
                    color=BAR_A, alpha=0.15)
    ax.fill_between(grid, 0, 3.2 * np.exp(-0.5 * ((grid - 38) / 9) ** 2) / 9,
                    color=BAR_B, alpha=0.15)
    ax.set_xlabel("Response value")
    ax.set_ylabel("Density")
    ax.legend(frameon=False, fontsize=9)
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    _style(ax)
    _save(fig, "density_overlay")


def hist_skewed_pair() -> None:
    """A skewed histogram beside a symmetric one, for the 'which is skewed?' item."""
    d = FIG_DATA["hist_skewed_pair"]
    skew = np.random.default_rng(d["seed"]).gamma(
        shape=d["shape"], scale=d["scale"], size=d["n"])
    sym = np.random.default_rng(d["sym_seed"]).normal(
        d["sym_mean"], d["sym_sd"], d["sym_n"])

    fig, axes = plt.subplots(1, 2, figsize=(8.2, 3.2), sharey=True, sharex=True)
    for ax, data, title in ((axes[0], skew, "Left"), (axes[1], sym, "Right")):
        ax.hist(data, bins=d["bins"], color=BAR_A, edgecolor="white", linewidth=0.6)
        ax.set_title(title, color=INK, fontsize=10)
        ax.set_xlabel("Response value")
        ax.grid(axis="y", color=GRID, linewidth=0.8)
        ax.set_axisbelow(True)
        _style(ax)
    # One x range for both panels: the item asks which shape has the long tail,
    # and a panel that is merely drawn wider would answer it wrongly.
    lo = min(skew.min(), sym.min())
    hi = max(skew.max(), sym.max())
    axes[0].set_xlim(lo, hi)
    axes[0].set_ylabel("Frequency")
    _save(fig, "hist_skewed_pair")


def hist_symmetric_pair() -> None:
    """Same shape, same centre, two spreads: the 'which is more spread out?' item."""
    d = FIG_DATA["hist_symmetric_pair"]
    rng = np.random.default_rng(d["seed"])
    narrow = rng.normal(d["mean"], d["narrow_sd"], d["n"])
    wide = rng.normal(d["mean"], d["wide_sd"], d["n"])

    fig, axes = plt.subplots(1, 2, figsize=(8.2, 3.2), sharey=True, sharex=True)
    for ax, data, title in ((axes[0], narrow, "Left"), (axes[1], wide, "Right")):
        ax.hist(data, bins=d["bins"], color=BAR_A, edgecolor="white", linewidth=0.6)
        ax.set_title(title, color=INK, fontsize=10)
        ax.set_xlabel("Response value")
        ax.grid(axis="y", color=GRID, linewidth=0.8)
        ax.set_axisbelow(True)
        _style(ax)
    # Shared range again, so the only thing that differs is the width of the
    # bars. If each panel were scaled to its own data the narrow one would look
    # the same width as the wide one and the item would stop working.
    axes[0].set_xlim(min(narrow.min(), wide.min()), max(narrow.max(), wide.max()))
    axes[0].set_ylabel("Frequency")
    _save(fig, "hist_symmetric_pair")


def hist_counts_pair() -> None:
    """Two groups from the same process, different sample sizes.

    The point is that a histogram's area is a count, so the taller total means
    more observations - the thing a density curve cannot show, since it is
    normalised to area 1 whatever the sample size.
    """
    d = FIG_DATA["hist_counts_pair"]
    rng = np.random.default_rng(d["seed"])
    small = rng.normal(d["mean"], d["sd"], d["small_n"])
    large = rng.normal(d["mean"], d["sd"], d["large_n"])

    fig, axes = plt.subplots(1, 2, figsize=(8.2, 3.2), sharey=True)
    for ax, data, title in ((axes[0], small, "Small group"),
                            (axes[1], large, "Large group")):
        ax.hist(data, bins=d["bins"], color=BAR_A, edgecolor="white", linewidth=0.6)
        ax.set_title(title, color=INK, fontsize=10)
        ax.set_xlabel("Response value")
        ax.grid(axis="y", color=GRID, linewidth=0.8)
        ax.set_axisbelow(True)
        _style(ax)
    axes[0].set_ylabel("Frequency")
    axes[0].set_xlim(min(small.min(), large.min()) - 5,
                     max(small.max(), large.max()) + 5)
    # A shared frequency scale is what makes the item answerable: with each
    # panel scaled to itself the total area would look the same in both, and
    # "the area is bigger" would not be something the picture shows.
    _save(fig, "hist_counts_pair")


def corr_heatmap() -> None:
    """Correlation matrix; the student must find the strongest pair."""
    labels = FIG_DATA["corr_heatmap"]["labels"]
    matrix = np.array(FIG_DATA["corr_heatmap"]["matrix"])

    fig, ax = plt.subplots(figsize=(5.2, 4.4))
    im = ax.imshow(matrix, cmap="RdBu_r", vmin=-1, vmax=1)
    ax.set_xticks(range(len(labels)), labels, rotation=30, ha="right")
    ax.set_yticks(range(len(labels)), labels)
    for i in range(len(labels)):
        for j in range(len(labels)):
            ax.text(j, i, f"{matrix[i, j]:.2f}", ha="center", va="center",
                    fontsize=9, color=INK)
    ax.grid(color="white", linewidth=1.6)
    ax.set_title("Correlation between study variables", color=INK,
                 fontsize=11, pad=12)
    _style(ax)
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    _save(fig, "corr_heatmap")


def freq_bars() -> None:
    """Frequency table as bars; drives proportion and marginal questions."""
    labels = FIG_DATA["freq_bars"]["labels"]
    counts = np.array(FIG_DATA["freq_bars"]["counts"])

    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    bars = ax.bar(labels, counts, color=BAR_A, width=0.62)
    for rect, value in zip(bars, counts):
        ax.text(rect.get_x() + rect.get_width() / 2, value + 0.25,
                str(value), ha="center", color=INK, fontsize=9)
    ax.set_xlabel("Number of books read last year")
    ax.set_ylabel("Number of students")
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    _style(ax)
    _save(fig, "freq_bars")


FIGURES = {
    "bar_stacked": bar_stacked,
    "boxplots_h": boxplots_h,
    "hist_skewed": hist_skewed,
    "hist_skewed_pair": hist_skewed_pair,
    "hist_symmetric_pair": hist_symmetric_pair,
    "hist_counts_pair": hist_counts_pair,
    "ci_dotplot": ci_dotplot,
    "normal_shaded": normal_shaded,
    "scatter_trend": scatter_trend,
    "density_overlay": density_overlay,
    "corr_heatmap": corr_heatmap,
    "freq_bars": freq_bars,
}


def main() -> int:
    print("Generating figures -> %s" % OUT.relative_to(ROOT))
    print("-" * 58)
    for name in sorted(FIGURES):
        FIGURES[name]()
    print()
    print("%d figures written." % len(FIGURES))
    return 0


if __name__ == "__main__":
    sys.exit(main())