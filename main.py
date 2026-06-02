"""Main entry point for the Netflix EDA reproduction pipeline."""

import argparse
from pathlib import Path

from netflix_analysis.data import NetflixDataLoader, NetflixDataCleaner
from netflix_analysis.analysis import (
    ContentGrowthForecaster,
    ContentPortfolioAnalyser,
    NetflixExplorer,
)
from netflix_analysis.visualization import NetflixPlotter


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Netflix EDA Reproduction Pipeline")
    parser.add_argument("--data", type=Path, default=Path("data/netflix_titles.csv"))
    parser.add_argument("--output", type=Path, default=Path("output/figures"))
    return parser.parse_args()


def run_pipeline(data_path: Path, output_dir: Path) -> None:
    """Execute the full reproduction pipeline."""
    print("=" * 50)
    print("Netflix EDA — Reproduction of Kanigara (2021)")
    print("=" * 50)

    print("\n[1/5] Loading data...")
    loader = NetflixDataLoader(data_path)
    raw_df = loader.load()

    print("\n[2/5] Cleaning data...")
    cleaner = NetflixDataCleaner(raw_df)
    clean_df = cleaner.clean()
    print(f"Clean dataset: {len(clean_df):,} rows")

    print("\n[3/5] Running EDA analysis...")
    explorer = NetflixExplorer(clean_df)
    type_dist = explorer.content_type_distribution()
    yearly = explorer.yearly_additions()
    countries = explorer.top_countries()
    genres = explorer.top_genres()
    duration = explorer.movie_duration_trend()
    ratings = explorer.rating_distribution()

    print("\n[4/5] Generating EDA figures...")
    plotter = NetflixPlotter(output_dir)
    plotter.plot_type_distribution(type_dist)
    plotter.plot_yearly_additions(yearly)
    plotter.plot_top_countries(countries)
    plotter.plot_top_genres(genres)
    plotter.plot_movie_duration_trend(duration)
    plotter.plot_rating_distribution(ratings)

    print("\n[5/5] Running portfolio and forecasting extensions...")
    portfolio = ContentPortfolioAnalyser(clean_df)
    plotter.plot_country_allocation(portfolio.country_allocation())
    plotter.plot_genre_allocation(portfolio.genre_allocation())
    plotter.plot_hhi(portfolio.herfindahl_index())
    plotter.plot_us_dependency(portfolio.us_dependency())

    forecaster = ContentGrowthForecaster(clean_df)
    plotter.plot_growth_forecast(
        forecaster.linear_forecast(forecast_years=3),
        forecaster.r_squared(),
    )
    plotter.plot_moving_average(forecaster.moving_average())
    plotter.plot_yoy_growth(forecaster.growth_rate())

    print(f"\nDone! All figures saved to: {output_dir}")


if __name__ == "__main__":
    args = parse_args()
    run_pipeline(args.data, args.output)
