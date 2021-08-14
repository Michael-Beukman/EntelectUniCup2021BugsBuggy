# Entelect University Cup 2021
This is the winning solution of the 2021 Entelect University cup, which is an optimisation challenge.


How to run
```
./run_all.sh
```
## Main strategy
Our main strategy was to allocate resource clusters to spaceships in a round robin fashion. We sorted the resource clusters based on some heuristics, based on the different scores for each resource type. Whenever a spaceship was full, we sent it back to base and put it back into the rotation.

## Different Files
Our main solutions are in `v*.py`, but the only worthwhile ones to look at are `v6` and `v7`. 

They might not be exactly the optimal solution, because we fiddled with the parameters quite a lot in the last hour. 