# Genshin Impact Wish Probability Monte-Carlo Simulation

 Monte-Carlo simulation to compute the approximate probabilities of getting $n$ limited 5-stars in $N$ wishes, implemented in Python and Java. 


The Python implementation is more stable, however it runs large numbers of simulations slowly. The Java implementation can run large numbers of simulations faster, but has high variability in its outcomes at low numbers.

## Usage:

### Python:

Supply arguments through the console

Usage examples:
To simulate $300$ wishes with $1000$ times without guarantee on a banner with hard-pity $= 90$ and no starting pity with a target of $3$ limited 5-stars:

```python3 simulation.py --simulation-count 1000 300 3 0 90```

### Java

Download the `Simulation.java` file and place it into a directory. From that directory, run:

```javac Simulation.java```
and then run 
```java Simulation``` 
and follow the prompts on the console
