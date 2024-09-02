"""Example notebook in the form of a python script.

Decorator '# %%' is used to separate notebook cells.
To add new cell simpy add `# %%`, that will indicate the start of new cell
For notebook to work jupyter notebook and ipykernel are required (check README.md)
To run a cell press control+enter or shift+enter.
NOTE: This type of notebook can only be executed from VS Code environment.
If you're using different IDE or jupyter-notebook to execute notebooks,
please write them in a classic .ipynb format.
"""

# %%
from pset4_ahmedelazzab.helloworld import hello_world

# %%
hello_world(remote=False)
