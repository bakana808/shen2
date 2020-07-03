
Shen 2
======

A ladder tournament ranking system for competitive games

* * *

## Usage

#### CLI

`shen read <file>`: attempts to read matches from a file

### Module

#### Usage

```python
import shen

# initialize a shen sesssion
# --------------------------

shn = shen.init()

# create users
# ------------

a = shn.create_user()
b = shn.create_user()
c = shn.create_user()

# create matches
# --------------

# begins a match between players A and B
# this match is marked as "in progress"
match = shn.start_match([a, b], best_of=3)

# report that the first round was won by player A
match.report_win(a)

# report that the second round was won by player B
match.report_win(b)

rnd = match.report_win(a)

# additionally, you can add metadata to each round
rnd.meta["stage"] = "dream_land_64"
rnd.user_meta[a]["character"] = "kirby"
```

#### Ranking

Rankings can be generated from a list of matches.

```python
from shen.ranker import EloRankingAlgo

# rank the players using the Elo rating system
ranker = EloRankingAlgo()

# generates rankings from the matches in shn
rankings = ranker.start(shn)

print(rankings)
```

