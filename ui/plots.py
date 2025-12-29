import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.colors as mcolors

def basic_plot(f, e, b, s, line_color="#4cc9f0", bg_color="#0b132b", grid_color="#1c2541",font_family="sans-serif",
        title="Basic Metrics",  xlabel="Time (s)", ylabel=""):
    plt.rcParams.update({
        "font.family": font_family,
        "font.size": 12,
        "axes.titlesize": 16,
        "axes.labelsize": 13
    })

    fig, ax = plt.subplots(figsize=(9, 4))
    fig.patch.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)

    ax.plot(f, color="#c91a1a", linewidth=2.8, label="Fatigue Cost")
    ax.plot(e, color="#9ad412", linewidth=2, label="Energy")
    ax.plot(s, color="#ffbb00", linewidth=2, label="Spectrum Changes")
    ax.legend()

    ax.set_title(title, color="white", pad=12, fontweight="bold")
    ax.set_xlabel(xlabel, color="white")

    ax.tick_params(colors="white")

    ax.grid(True, color=grid_color, linestyle="--", linewidth=0.6, alpha=0.6)

    for spine in ax.spines.values():
        spine.set_visible(False)

    plt.tight_layout()

    return fig

def risk_curve_plot(y, line_color="#4cc9f0", bg_color="#0b132b", grid_color="#1c2541",font_family="sans-serif",
        title="Listener Engagement curve",  xlabel="Time (s)", ylabel="Disengagement Score"):
    plt.rcParams.update({
        "font.family": font_family,
        "font.size": 12,
        "axes.titlesize": 16,
        "axes.labelsize": 13
    })

    fig, ax = plt.subplots(figsize=(9, 4))
    fig.patch.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)

    ax.plot(y, color=line_color, linewidth=2.8)

    ax.set_title(title, color="white", pad=12, fontweight="bold")
    ax.set_xlabel(xlabel, color="white")
    ax.set_ylabel(ylabel, color="white")

    ax.tick_params(colors="white")

    ax.grid(True, color=grid_color, linestyle="--", linewidth=0.6, alpha=0.6)

    for spine in ax.spines.values():
        spine.set_visible(False)

    plt.tight_layout()

    return fig

def engagement_heatmap(df, song_id):
    df = df[df["id"] == song_id].copy()

    norm = mcolors.Normalize(vmin=df["risk_score"].min(), vmax=df["risk_score"].max())

    risk_cmap = mcolors.LinearSegmentedColormap.from_list("risk", ["#ffd166", "#ef476f"])

    fig, ax = plt.subplots(figsize=(12, 2))

    fig.patch.set_facecolor("#0b132b")
    ax.set_facecolor("#0b132b")

    for _, row in df.iterrows():
        start = row["start"]
        width = row["end"] - row["start"]

        # color logic
        if row["state"] == 1:
            color = "#2ec4b6" 
        else:
            color = risk_cmap(norm(row["risk_score"]))

        rect = patches.Rectangle((start, 0), width, 1, linewidth=0, facecolor=color)
        ax.add_patch(rect)

    ax.set_xlim(df["start"].min(), df["end"].max())
    ax.set_ylim(0, 1)
    ax.set_yticks([])
    ax.set_xlabel("Time (seconds)", color="white")
    ax.tick_params(colors="white")

    for spine in ax.spines.values():
        spine.set_visible(False)

    plt.title("Zone Risks", color="white", fontsize=14, fontweight="bold", pad=10)
    plt.tight_layout()

    return fig
