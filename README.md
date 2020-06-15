# Teach Machines To Check
This project is aimed at creating a bare-bones Checkers board game, and creating a machine learning algorithm to learn to play it.

## Files

### checkers_3.py
In case it wasn't obvious by the name, this was the third iteration in a series of attempts of trying to make a game of checkers that could:
* Be easily manipulated,
* Present the board data in a way the algorithm could effectively use, and
* Calculate all possible moves in a given turn.

That last one proved the most difficult to accomplish. It was hindered primarily by how I had my data structured. You can look to the two previous iterations to see how I structured the data previously, but in the end this is how I decided to store the board data:
```py
          [1]
        [1,1,1]
      [1,1,1,0,0]
    [1,1,1,0,0,2,2]
    [1,1,0,0,2,2,2]
      [0,0,2,2,2]
        [2,2,2]
          [2]
```
The beauty of this model is that it allowed data manipulation to be consistent, whether a piece was moving up, down, left or right or even jumping, something the previous models lacked.

### check_ai.py
All things considered, my version of a checkers AI is rather simple. Currently the method to update the weights of synapses is non-functional, so all the algorithm can do is output what it considers an optimal move given a particular board. Otherwise, the algorithm has a basic method to turn tensors into their sigmoidal values and calculate the slope of the sigmoid function at those values.

### training_ground.py
This is where the real "Learning" takes place, which in truth is just an illusion. The checkersAiDojo method creates an asortment of randing algorithms and pits them against one another. Those that perform the best remain, while the rest are replaced with more randomized algorithms. Over time, effective algorithms will pop up and be added to the dojo, but as it stands there is no way for the dojo to train its current inhabitants. In essence, this program doesn't so much "train" algorithms to become better but rather determines which algorithms are more or less functional. 

This is easily the biggest problem I have with this project. The way the dojo functions is adequate, but it would be made more effective were the synapse weight update function implemented in the CheckersAI class. Were that so, after pruning the bottom 15 as the dojo currently does, each of the top 5 would be copied and adjusted 3 times in slightly different ways, filling the roster back up to 20 with the original 5 still remaining. Sadly, I did not have enough time to implement this for the purposes of my project.

## Resources Used

### "Deep Learning A-Z" by Kirill Eremenko, Hadelin de Ponteves, the the SuperDataScience Team.
This was my primary resource in research machine learning and neural networks. I ended up doing a lengthy but shallow run of this course, taking away a lot of key concepts but skimping on the details. It is a course I fully intend to go back through more in-depth and well worth the time I put in.

### "A Neural Network in 11 Lines of Python" by imtrask (iamtrask.github.io)
This article was the most valuable resource in building this project. It was recommended as further reading in the "Deep Learning A-Z" course, and I'm glad it was. The article demonstrated how neural networks are in essence a series of zero, one and two dimensional tensors and beyond manipulated by various pieces of calculus. The research I had to put in to understand it gave me an more intuitive understanding of the inner workings of neural networks.
