"""Visualization class for Netflix EDA using matplotlib and seaborn.

Translates R/ggplot2 charts from Kanigara (2021) to Python/matplotlib.
Visual style differs (ggplot2 vs matplotlib) but data is equivalent.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

NETFLIX_RED = "#E50914"


class NetflixPlotter:
    """Generates and saves all visualizations for the Netflix analysis.

    Args:
        output_dir (str | Path): Directory where figures will be saved.

    Example:
        >>> plotter = NetflixPlotter("output/figures")
        >>> plotter.plot_type_distribution(type_series)
    """

    def __init__(self, output_dir: str | Path = "output/figures") -> None:
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        sns.set_theme(style="darkgrid")

    def _save(self, filename: str) -> None:
        """Save the current figure to the output directory.

        Args:
            filename (str): Output filename.
        """
        path = self.output_dir / filename
        plt.savefig(path, dpi=150, bbox_inches="tight")
        plt.close()
        print(f"Saved: {path}")

    def plot_type_distribution(self, series: pd.Series) -> None:
        """Bar chart of Movies vs TV Shows (RQ2).

        Args:
            series (pd.Series): Output of NetflixExplorer.content_type_distribution().
        """
        fig, ax = plt.subplots(figsize=(7, 5))
        series.plot(kind="bar", ax=ax, color=[NETFLIX_RED, "#221F1F"], edgecolor="white")
        ax.set_title("Movies vs TV Shows on Netflix", fontsize=14, fontweight="bold")
        ax.set_xlabel("Content Type")
        ax.set_ylabel("Number of Titles")
        ax.tick_params(axis="x", rotation=0)
        self._save("type_distribution.png")

    def plot_yearly_additions(self, pivot: pd.DataFrame) -> None:
        """Stacked area chart of yearly content additions (RQ1).

        Args:
            pivot (pd.DataFrame): Output of NetflixExplorer.yearly_additions().
        """
        fig, ax = plt.subplots(figsize=(12, 6))
        pivot.plot(kind="area", ax=ax, color=[NETFLIX_RED, "#221F1F"], alpha=0.8)
        ax.set_title("Content Added to Netflix per Year", fontsize=14, fontweight="bold")
        ax.set_xlabel("Year")
        ax.set_ylabel("Number of Titles Added")
        self._save("yearly_additions.png")

    def plot_top_countries(self, series: pd.Series) -> None:
        """Horizontal bar chart of top contributing countries (RQ3).

        Args:
            series (pd.Series): Output of NetflixExplorer.top_countries().
        """
        fig, ax = plt.subplots(figsize=(9, 6))
        series.sort_values().plot(kind="barh", ax=ax, color=NETFLIX_RED)
        ax.set_title("Top 10 Countries by Number of Titles", fontsize=14, fontweight="bold")
        ax.set_xlabel("Number of Titles")
        self._save("top_countries.png")

    def plot_top_genres(self, series: pd.Series) -> None:
        """Horizontal bar chart of top genres (RQ4).

        Args:
            series (pd.Series): Output of NetflixExplorer.top_genres().
        """
        fig, ax = plt.subplots(figsize=(9, 6))
        series.sort_values().plot(kind="barh", ax=ax, color="#564d4d")
        ax.set_title("Top 10 Genres on Netflix", fontsize=14, fontweight="bold")
        ax.set_xlabel("Number of Titles")
        self._save("top_genres.png")

    def plot_movie_duration_trend(self, df: pd.DataFrame) -> None:
        """Line chart of average movie duration over the years (RQ5 — extension).

        Args:
            df (pd.DataFrame): Output of NetflixExplorer.movie_duration_trend().
        """
        fig, ax = plt.subplots(figsize=(12, 5))
        ax.plot(df["release_year"], df["avg_duration"], color=NETFLIX_RED, linewidth=2)
        ax.fill_between(df["release_year"], df["avg_duration"], alpha=0.15, color=NETFLIX_RED)
        ax.set_title("Average Movie Duration Over Time", fontsize=14, fontweight="bold")
        ax.set_xlabel("Release Year")
        ax.set_ylabel("Average Duration (minutes)")
        self._save("movie_duration_trend.png")

    def plot_rating_distribution(self, series: pd.Series) -> None:
        """Pie chart of content rating distribution (RQ6 — extension).

        Args:
            series (pd.Series): Output of NetflixExplorer.rating_distribution().
        """
        fig, ax = plt.subplots(figsize=(8, 8))
        series.head(8).plot(
            kind="pie", ax=ax, autopct="%1.1f%%",
            colors=sns.color_palette("Reds_r", len(series)),
            startangle=90,
        )
        ax.set_ylabel("")
        ax.set_title("Content Rating Distribution", fontsize=14, fontweight="bold")
        self._save("rating_distribution.png")
