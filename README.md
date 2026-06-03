# Reproducing Netflix EDA: From R to Python

> Reproducible Research Project — Jan Kozubowski, 2026

## Overview

This project **reproduces** the Exploratory Data Analysis conducted by
Evan Kanigara in R ([Netflix-Movies-and-TV-Show-EDA](https://github.com/evankanigara/Netflix-Movies-and-TV-Show-EDA)),
translating the entire analysis into Python and extending it with additional insights.

We use the same source dataset:
[Netflix Movies and TV Shows](https://www.kaggle.com/datasets/shivamb/netflix-shows)
(Shivam Bansal, Kaggle), covering content added to Netflix up to 2021.

---

## Original Study

| | |
|---|---|
| **Author** | Evan Kanigara |
| **Language** | R |
| **Source** | https://github.com/evankanigara/Netflix-Movies-and-TV-Show-EDA |
| **Dataset** | Netflix Movies and TV Shows (Kaggle, Shivam Bansal) |
| **Key analyses** | Content type distribution, yearly additions, top countries, genre analysis, duration trends |

---

## What We Did

1. **Translated** all R code to Python using a class-based package structure
2. **Reproduced** the original findings (content type split, country rankings, genre frequencies)
3. **Identified** differences between R and Python outputs (e.g. missing value handling, date parsing)
4. **Extended** the analysis with rating distribution, movie duration trends,
   content portfolio analysis, and simple growth forecasting

---

## Research Questions

1. How has the volume of content added to Netflix changed annually?
2. Is Netflix shifting its focus from Movies to TV Shows?
3. Which countries contribute the most titles?
4. What genres dominate, and how do they differ by content type?
5. Has the average duration of movies changed over time? *(extension)*
6. How diversified is Netflix's content portfolio by country and genre? *(extension)*
7. What does a simple trend forecast suggest about future content additions? *(extension)*

---

## Quickstart (Docker — recommended)

```bash
git clone https://github.com/ywen2-dot/the-project-of-reproducible-research.git
cd the-project-of-reproducible-research
docker pull yuhan023/netflix-analysis:latest
docker run --rm \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/output:/app/output \
  yuhan023/netflix-analysis:latest
```

The generated figures are saved in `output/figures`.

```bash
open output/figures
```

## Quickstart (Local)

```bash
git clone https://github.com/ywen2-dot/the-project-of-reproducible-research.git
cd the-project-of-reproducible-research
make install
# Dataset is included in data/netflix_titles.csv
make run
```

## Render the Report

The final report is written in Quarto:

```bash
PYTHONPATH="$PWD" quarto render report/report.qmd --to html --execute-dir "$PWD"
open report/report.html
```

`--execute-dir "$PWD"` makes Quarto run the report from the project root, so
the report can find `data/netflix_titles.csv`, the `netflix_analysis` package,
and the generated figures in `output/figures`.

---

## Project Structure

```
.
├── netflix_analysis/          # Python package
│   ├── data/
│   │   ├── loader.py          # NetflixDataLoader
│   │   └── cleaner.py         # NetflixDataCleaner
│   ├── analysis/
│   │   ├── explorer.py        # NetflixExplorer
│   │   ├── portfolio.py       # Content portfolio extension
│   │   └── forecaster.py      # Growth forecasting extension
│   └── visualization/
│       └── plotter.py         # NetflixPlotter
├── notebooks/
│   └── exploration.ipynb      # Dev experimentation
├── report/
│   └── report.qmd             # Quarto report (reproduction + discussion)
├── docs/                      # Sphinx documentation
├── Dockerfile
├── docker-compose.yml
├── .pre-commit-config.yaml
├── pyproject.toml
└── Makefile
```

---

## Make Commands

| Command | Description |
|---|---|
| `make install` | Install package + dev deps + pre-commit hooks |
| `make run` | Run the full analysis pipeline |
| `make lint` | Run ruff linter |
| `make docs` | Build Sphinx HTML documentation |
| `make docker-build` | Build the Docker image |
| `make docker-push` | Push image to DockerHub |
| `make clean` | Remove generated files |

---

## Team Contributions

| Member | Responsibilities |
|---|---|
|Yuhan Wen| Data loading & cleaning (`data/`) |
| Linh Tran | Analysis logic and notebook-based EDA (`analysis/`, `notebooks/`) |
| Yuezhang Chen | Visualization, report writing, and extension discussion |

---

## AI Disclosure

Parts of this project were scaffolded with Claude Sonnet 4.6 (Anthropic, 2026).
AI was used for: initial code structure, docstring generation, and Dockerfile setup.
All reproduction decisions, analysis validation, and report writing were done by the team.
