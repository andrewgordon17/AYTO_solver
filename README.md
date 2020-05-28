# AYTO_solver

The television show Are You the One? is a reality dating show that operates in the following way:

  10 men and 10 women compete. Before the start of the show, the showrunners match the male and female contestants into couples. This matching is kept secret
  
  The contestants win by uncovering the matching. Each episode they can get a yes/no answer as to where a single couple is correct w/r/t the secret matching (this is called the Truth Booth, I'm told). The contestants then split entirely into couples and are infomred the number of correct matches, but not which ones are correct.
  
  The contestants have 10 episodes to get everything correct, in which case they win.
  
  My algorithm works by treating all possible 10 couple matchings as equally likely, making the guess that will provide the most information, in expectation, and then paring down the list of possible matchings according to the information received. It is probabilistic and not guaranteed, but empirically works more than 99 times out of 100
  
  Running the code will play an interactive version of the game where the user can choose a matching (https://www.random.org/sequences/?min=0&max=9&col=1&format=html&rnd=new) and the game will attempt to guess it. There is a function titled check accuracy that will run multiple trials and give statistics on success, though this can take a while.
