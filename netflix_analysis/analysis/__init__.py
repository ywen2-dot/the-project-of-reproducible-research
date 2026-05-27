"""Analysis subpackage for Netflix EDA."""

from netflix_analysis.analysis.explorer import NetflixExplorer
from netflix_analysis.analysis.forecaster import ContentGrowthForecaster
from netflix_analysis.analysis.portfolio import ContentPortfolioAnalyser

__all__ = ["NetflixExplorer", "ContentGrowthForecaster", "ContentPortfolioAnalyser"]
