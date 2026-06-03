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
        """Initialize the plotter and create the output directory."""
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

    def plot_country_allocation(self, pivot: pd.DataFrame) -> None:
        """Stacked area chart of yearly country allocation."""
        fig, ax = plt.subplots(figsize=(12, 6))
        pivot.plot(kind="area", ax=ax, alpha=0.85)
        ax.set_title("Country Allocation in the Netflix Catalogue", fontweight="bold")
        ax.set_xlabel("Year Added")
        ax.set_ylabel("Share of Titles (%)")
        ax.legend(title="Country", bbox_to_anchor=(1.02, 1), loc="upper left")
        self._save("country_allocation.png")

    def plot_genre_allocation(self, pivot: pd.DataFrame) -> None:
        """Stacked area chart of yearly genre allocation."""
        fig, ax = plt.subplots(figsize=(12, 6))
        pivot.plot(kind="area", ax=ax, alpha=0.85)
        ax.set_title("Genre Allocation in the Netflix Catalogue", fontweight="bold")
        ax.set_xlabel("Year Added")
        ax.set_ylabel("Share of Titles (%)")
        ax.legend(title="Genre", bbox_to_anchor=(1.02, 1), loc="upper left")
        self._save("genre_allocation.png")

    def plot_hhi(self, hhi_df: pd.DataFrame) -> None:
        """Line chart of country concentration measured by HHI."""
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(hhi_df["year_added"], hhi_df["hhi"], marker="o", color=NETFLIX_RED)
        ax.set_title("Country Concentration: Herfindahl-Hirschman Index", fontweight="bold")
        ax.set_xlabel("Year Added")
        ax.set_ylabel("HHI")
        self._save("country_hhi.png")

    def plot_us_dependency(self, dep_df: pd.DataFrame) -> None:
        """Line chart of US content share over time."""
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(dep_df["year_added"], dep_df["us_share"], marker="o", color="#221F1F")
        ax.set_title("US Content Share Over Time", fontweight="bold")
        ax.set_xlabel("Year Added")
        ax.set_ylabel("US Share (%)")
        self._save("us_dependency.png")

    def plot_growth_forecast(self, forecast_df: pd.DataFrame, r2: float) -> None:
        """Line chart of historical additions and simple linear forecast."""
        fig, ax = plt.subplots(figsize=(11, 5))
        history = forecast_df[~forecast_df["is_forecast"]]
        forecast = forecast_df[forecast_df["is_forecast"]]
        ax.plot(history["year_added"], history["count"], marker="o", label="Actual")
        ax.plot(forecast_df["year_added"], forecast_df["forecast"], linestyle="--", label="Trend")
        ax.scatter(
            forecast["year_added"],
            forecast["forecast"],
            color=NETFLIX_RED,
            label="Forecast",
        )
        ax.set_title(f"Simple Linear Forecast of Content Additions (R² = {r2:.2f})")
        ax.set_xlabel("Year")
        ax.set_ylabel("Number of Titles Added")
        ax.legend()
        self._save("growth_forecast.png")

    def plot_moving_average(self, ma_df: pd.DataFrame) -> None:
        """Line chart comparing yearly additions with a moving average."""
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(ma_df["year_added"], ma_df["count"], marker="o", label="Actual")
        ax.plot(ma_df["year_added"], ma_df["ma"], marker="o", label="3-year moving average")
        ax.set_title("Moving Average of Netflix Content Additions", fontweight="bold")
        ax.set_xlabel("Year")
        ax.set_ylabel("Number of Titles Added")
        ax.legend()
        self._save("moving_average.png")

    def plot_yoy_growth(self, growth_df: pd.DataFrame) -> None:
        """Bar chart of year-over-year growth in content additions."""
        fig, ax = plt.subplots(figsize=(10, 5))
        colors = [NETFLIX_RED if value < 0 else "#221F1F" for value in growth_df["yoy_growth_pct"]]
        ax.bar(growth_df["year_added"], growth_df["yoy_growth_pct"], color=colors)
        ax.axhline(0, color="black", linewidth=0.8)
        ax.set_title("Year-over-Year Growth in Content Additions", fontweight="bold")
        ax.set_xlabel("Year")
        ax.set_ylabel("Growth (%)")
        self._save("yoy_growth.png")
