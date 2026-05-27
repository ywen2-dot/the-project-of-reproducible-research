"""Growth trend forecasting for Netflix content additions."""

import numpy as np
import pandas as pd


class ContentGrowthForecaster:
    """Forecast Netflix content growth using simple trend methods."""

    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df
        self._yearly: pd.DataFrame | None = None

    def _get_yearly_counts(self) -> pd.DataFrame:
        """Return yearly content additions for the main Netflix growth period."""
        if self._yearly is None:
            self._yearly = self.df.groupby("year_added").size().reset_index(name="count")
            self._yearly = self._yearly[
                (self._yearly["year_added"] >= 2015) & (self._yearly["year_added"] <= 2021)
            ]
        return self._yearly

    def moving_average(self, window: int = 3) -> pd.DataFrame:
        """Compute a simple moving average of yearly content additions."""
        yearly = self._get_yearly_counts().copy()
        yearly["ma"] = yearly["count"].rolling(window=window, min_periods=1).mean()
        return yearly

    def linear_forecast(self, forecast_years: int = 3) -> pd.DataFrame:
        """Forecast future yearly additions with a simple linear trend."""
        yearly = self._get_yearly_counts().copy()
        x = yearly["year_added"].values
        y = yearly["count"].values

        x_mean, y_mean = x.mean(), y.mean()
        slope = np.sum((x - x_mean) * (y - y_mean)) / np.sum((x - x_mean) ** 2)
        intercept = y_mean - slope * x_mean

        yearly["fitted"] = intercept + slope * yearly["year_added"]
        yearly["is_forecast"] = False

        future_years = list(range(int(x.max()) + 1, int(x.max()) + forecast_years + 1))
        future_df = pd.DataFrame(
            {
                "year_added": future_years,
                "count": np.nan,
                "fitted": np.nan,
                "is_forecast": True,
            }
        )
        future_df["forecast"] = intercept + slope * future_df["year_added"]

        result = pd.concat([yearly, future_df], ignore_index=True)
        result["forecast"] = result["forecast"].combine_first(result["fitted"])
        return result

    def r_squared(self) -> float:
        """Compute the R-squared of the linear trend fit."""
        yearly = self._get_yearly_counts()
        x = yearly["year_added"].values
        y = yearly["count"].values
        x_mean, y_mean = x.mean(), y.mean()
        slope = np.sum((x - x_mean) * (y - y_mean)) / np.sum((x - x_mean) ** 2)
        intercept = y_mean - slope * x_mean
        y_pred = intercept + slope * x
        return float(1 - np.sum((y - y_pred) ** 2) / np.sum((y - y_mean) ** 2))

    def growth_rate(self) -> pd.DataFrame:
        """Compute year-over-year growth rates of content additions."""
        yearly = self._get_yearly_counts().copy()
        yearly["yoy_growth_pct"] = yearly["count"].pct_change() * 100
        return yearly.dropna()
