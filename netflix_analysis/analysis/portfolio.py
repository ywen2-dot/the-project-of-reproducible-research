"""Content portfolio analysis for the Netflix catalogue.

This extension treats Netflix titles as a content portfolio. Countries and
genres are interpreted as allocation categories, and concentration is measured
with the Herfindahl-Hirschman Index.
"""

import pandas as pd


class ContentPortfolioAnalyser:
    """Analyse country and genre allocation in the Netflix catalogue."""

    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df

    def country_allocation(self, top_n: int = 6) -> pd.DataFrame:
        """Compute yearly content allocation by top contributing countries."""
        exploded = self.df.copy()
        exploded["country"] = exploded["country"].str.split(", ")
        exploded = exploded.explode("country").copy()
        exploded["country"] = exploded["country"].str.strip()
        exploded = exploded[exploded["country"] != "Unknown"]

        top_countries = exploded["country"].value_counts().head(top_n).index.tolist()
        exploded = exploded[exploded["country"].isin(top_countries)]

        pivot = exploded.groupby(["year_added", "country"]).size().unstack(fill_value=0)
        return pivot.div(pivot.sum(axis=1), axis=0).mul(100).dropna()

    def genre_allocation(self, top_n: int = 6) -> pd.DataFrame:
        """Compute yearly content allocation by top genres."""
        exploded = self.df.copy()
        exploded["genre"] = exploded["listed_in"].str.split(", ")
        exploded = exploded.explode("genre").copy()
        exploded["genre"] = exploded["genre"].str.strip()

        top_genres = exploded["genre"].value_counts().head(top_n).index.tolist()
        exploded = exploded[exploded["genre"].isin(top_genres)]

        pivot = exploded.groupby(["year_added", "genre"]).size().unstack(fill_value=0)
        return pivot.div(pivot.sum(axis=1), axis=0).mul(100).dropna()

    def herfindahl_index(self) -> pd.DataFrame:
        """Compute country concentration using the Herfindahl-Hirschman Index."""
        exploded = self.df.copy()
        exploded["country"] = exploded["country"].str.split(", ")
        exploded = exploded.explode("country").copy()
        exploded["country"] = exploded["country"].str.strip()
        exploded = exploded[exploded["country"] != "Unknown"]

        yearly = exploded.groupby(["year_added", "country"]).size().reset_index(name="count")
        yearly["share"] = (
            yearly["count"] / yearly.groupby("year_added")["count"].transform("sum") * 100
        )
        hhi = (
            yearly.groupby("year_added")
            .apply(lambda x: (x["share"] ** 2).sum(), include_groups=False)
            .reset_index(name="hhi")
        )
        return hhi[hhi["year_added"] >= 2015]

    def us_dependency(self) -> pd.DataFrame:
        """Track the share of US-produced content over time."""
        exploded = self.df.copy()
        exploded["country"] = exploded["country"].str.split(", ")
        exploded = exploded.explode("country").copy()
        exploded["country"] = exploded["country"].str.strip()
        exploded = exploded[exploded["country"] != "Unknown"]

        yearly_total = exploded.groupby("year_added").size().reset_index(name="total")
        us_only = (
            exploded[exploded["country"] == "United States"]
            .groupby("year_added")
            .size()
            .reset_index(name="us_count")
        )
        result = yearly_total.merge(us_only, on="year_added", how="left").fillna(0)
        result["us_share"] = result["us_count"] / result["total"] * 100
        return result[result["year_added"] >= 2015]
