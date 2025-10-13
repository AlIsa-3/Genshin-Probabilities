# Genshin Impact Wish Probability Monte-Carlo Simulation

A Python script implementing a Monte-Carlo simulation to compute the approximate probabilities of getting $n$ limited 5-stars in $N$ wishes.


## Usage:

Supply arguments through the console

Usage examples:
To simulate $300$ wishes with $1000$ times without guarantee on a banner with hard-pity $= 90$ and no starting pity with a target of $3$ limited 5-stars:

```python3 simulation.py --simulation-count 1000 300 3 0 90```
