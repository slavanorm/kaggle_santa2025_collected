# Kaggle Santa 2025 Competition Data

Collected data from the [Kaggle Santa 2025](https://www.kaggle.com/competitions/santa-2025) competition.

## Data

### leaderboard.csv (2000 teams)
| Column | Description |
|--------|-------------|
| rank | Final ranking |
| team | Team name |
| score | Final score (lower is better) |
| date | Submission date |
| writeup_url | Link to solution writeup |
| notebook_path | Local path to downloaded notebook |
| usernames | Team member usernames (top 300 teams) |

### notebooks.csv (397 notebooks)
| Column | Description |
|--------|-------------|
| ref | username/notebook-slug |
| author | Display name |
| title | Notebook title |
| votes | Upvotes |
| language | python/r |
| has_gpu/has_tpu | Accelerator usage |
| approach_tags | SA, Sparrow, GA, Translation, Ensemble, Physics, RL, Greedy |
| import_tags | Libraries used |
| sloc | Source lines of code |
| is_fork | Whether forked |
| parent_ref | Forked from |
| has_optimizer | Uses scipy/optuna/etc |
| is_analysis | EDA/visualization notebook |
| is_solution | Contains solution code |
| is_ensemble | Combines multiple solutions |
| url | Kaggle URL |
| local_path | Local download path |
| top_score | Notebook's best score |
| team | Mapped LB team name |
| lb_rank | Team's LB rank |

### by_tag/
Notebooks split by approach:
- SA.csv (44) - Simulated Annealing
- Sparrow.csv (8) - Sparrow algorithm
- GA.csv (10) - Genetic Algorithm
- Translation.csv (105) - Translation-based methods
- Ensemble.csv (73) - Ensemble solutions
- Physics.csv (57) - Physics-based optimization
- RL.csv (4) - Reinforcement Learning
- Greedy.csv (41) - Greedy approaches

## Downloading notebooks

Notebooks are not included due to copyright. Re-download using:

```bash
while read ref; do
  kaggle kernels pull "$ref" -p downloaded/
done < <(cut -d, -f1 notebooks.csv | tail -n +2)
```

## Scripts

- `src/parse_notebooks.py` - Parse downloaded notebooks for metadata
- `src/scrape_scores.py` - Scrape notebook scores from Kaggle
- `src/scrape_teams.py` - Scrape team usernames from leaderboard
