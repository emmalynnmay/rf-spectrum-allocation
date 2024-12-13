# CS 5110 Multi Agent Systems Final Project

Emma Lynn May, Jonah Harmon, & Calvin Riley

## Usage

### Set Up

Set up the virtual environment

`python3 -m venv my_env`

Activate the virtual environment

`source my_env/bin/activate`

Install dependencies

`pip3 install -r requirements.txt`

Deactivate the virtual environment (when you're done)

`deactivate`

### Running the Simulation

To run the default simulation, run: `python3 main.py`

Input `no` when asked `Use CSV for setup?`.

Input `large` when asked `Choose dataset for hardcoded setup`.

Feel free to experiment with our other test cases by entering other options in the initial input dialog.

### Unit Tests

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
* Coloring algorithm basic implementation: https://www.geeksforgeeks.org/graph-coloring-set-2-greedy-algorithm/