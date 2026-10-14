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
    categories = ["Never", "Rarely", "Sometimes", "Often"]
    men = np.array([18, 22, 34, 26])
    women = np.array([29, 30, 27, 14])

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
    #            low    q1    med   q3    high
    stats = [(10, 22, 30, 38, 50),
             (5, 20, 30, 40, 55),
             (28, 29, 30, 31, 32)]
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
    rng = np.random.default_rng(7)
    sample = rng.gamma(shape=2.0, scale=2.0, size=4000)
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    ax.hist(sample, bins=28, color=BAR_A, edgecolor="white", linewidth=0.6)
    ax.set_xlabel("Response value")
    ax.set_ylabel("Frequency")
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    _style(ax)
    _save(fig, "hist_skewed")


def hist_symmetric() -> None:
    """Symmetric: mean sits in the middle, variance follows the spread."""
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    bins = np.arange(0, 28, 2)  # 14 edges for 13 bars
    counts = np.array([1, 2, 5, 11, 19, 24, 21, 14, 8, 4, 2, 1, 1])
    ax.bar(bins[:-1], counts, width=2.0, align="edge",
           color=BAR_A, edgecolor="white", linewidth=0.6)
    ax.set_xlabel("Response value")
    ax.set_ylabel("Frequency")
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    _style(ax)
    _save(fig, "hist_symmetric")


def ci_dotplot() -> None:
    """Estimates with 95% CI. Group A's CI clears the reference line, B's does not."""
    names = ["A", "B"]
    means = [52.4, 45.1]
    lo = [48.6, 41.3]
    hi = [56.2, 48.9]
    ref = 44.0

    fig, ax = plt.subplots(figsize=(6.4, 3.0))
    y = np.array([1, 0])  # A on top, B below, reading order
    names = ["A", "B"]
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

    for xv, label in ((5, "a"), (6.2, "b"), (7.4, "c")):
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
    rng = np.random.default_rng(3)
    x = rng.normal(50, 10, 120)
    y = 0.8 * x + 20 + rng.normal(0, 14, 120)
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
    rng = np.random.default_rng(11)
    a = rng.normal(30, 5, 3000)
    b = rng.normal(38, 9, 3000)
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


def corr_heatmap() -> None:
    """Correlation matrix; the student must find the strongest pair."""
    labels = ["Hours", "Sleep", "Screen", "Stress", "Caff"]
    matrix = np.array([
        [1.00, -0.28, 0.62, 0.41, 0.35],
        [-0.28, 1.00, 0.18, -0.33, -0.15],
        [0.62, 0.18, 1.00, 0.55, 0.29],
        [0.41, -0.33, 0.55, 1.00, 0.47],
        [0.35, -0.15, 0.29, 0.47, 1.00],
    ])

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
    labels = ["0-9", "10-19", "20-29", "30-39", "40-49"]
    counts = np.array([2, 5, 11, 9, 3])

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
    "hist_symmetric": hist_symmetric,
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