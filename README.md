# CS 5110 Multi Agent Systems Final Project

Emma Lynn May, Jonah Harmon, & Calvin Riley

## Usage

Set up the virtual environment

`python3 -m venv my_env`

Activate the virtual environment

`source my_env/bin/activate`

Install dependencies

`pip3 install -r requirements.txt`

Deactivate the virtual environment (when you're done)

`deactivate`

Run all the unit tests!

`python3 test.py`

Run a specific unit test!

`python3 -m unittest test.TestClass.test_name`

## Assumptions & Caveats
* The ranges shown in the visual representation of real space are not entirely mathematically accurate
    * Also fill in with your brain the space in between the dot lines
* Two users cannot be in the exact same position
* Users cannot have negative x/y coordinates

## References
* Coloring algorithm: https://www.geeksforgeeks.org/graph-coloring-set-2-greedy-algorithm/