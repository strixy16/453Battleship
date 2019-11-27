# Run this file to see that our code works

import QL
import MC

print("Running Monte-Carlo learning algorithm for 1000 episodes...")
print("Please exit Monte-Carlo graph to continue")
MC.main(1000)

print("Running Q-learning learning algorithm for 1000 episodes...")
QL.main(1000)
