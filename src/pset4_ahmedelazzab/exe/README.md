# Automatic executables

This directory is a special place for executables - elements of your application which execution
can be invoked by a command line call. `python-pod` provides an automated mechanism that will
create executables for your package. [Dynamic setup.py script](/setup.py) produces them from all
Python modules (i.e., `.py` files) you have in this directory - except for the `__init__.py` ones,
which are intentionally ignored. Executables are created in following format:

```sh
pset4-ahmedelazzab-module-name
```

so the sample `hello_world.py` module will become a
`pset4-ahmedelazzab-hello-world` executable. Keep in
mind that all underscores (`_`) will be replaced with hyphens (`-`) as per standard industry
approach to naming. In order to run the executable, be sure to install the package first, and then
call it via command shown above. You can also learn more about particular executable via `--help`
flag (if author provided help message):

```sh
pset4-ahmedelazzab-module-name --help
```
