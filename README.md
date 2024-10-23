# AI-8PuzzleProblem
The following is the code for Assignment-1 for a course in Artificial Intelligence. It involves the use of different search algorithms to find the solution to the classic 8-PuzzleProblem.

The programming language used is Python 3.10.6

The entire code base is divided into multiple python files 
each implementing a different search algorithm.


## Running The Program

To run the code type:

> python3 expense_8_puzzle.py start.txt goal.txt `<method>` `<dump_flag>`

`<start-file>` and `<goal-file>` are required.
`<method>` can be: 

    bfs - Breadth First Search

    ucs - Uniform Cost Search

    dfs - Depth First Search

    dls - Depth Limited Search (Note: Depth Limit will be obtained as a Console Input)

    ids - Iterative Deepening Search

    greedy - Greedy Seach

    star - A* Search (Note: if no <method> is given, this is considered to be the default option)


If `<dump-flag>`  is given as true, search trace is dumped for analysis. 
(Note: if `<dump-flag>` is not given, it is assumed to be false)