# Introduction to MkDocs

> **Note:** This documentation serves as an example and has to be adjusted to reflect project structure.
Below is a simpified explanation of templated docs structure.

By default `python-pod` template creates main module with `hello_world` submodule located in
`ds-cf-pset4-ahmedelazzab/src/pset4_ahmedelazzab/hello_world/`
and `exe` package located in
`ds-cf-pset4-ahmedelazzab/src/pset4_ahmedelazzab/exe/`.
Names of all mentioned `.md` files are conventional and can be anything - as long as they match with
**nav** section of [mkdocs.yml](../mkdocs.yml).

After executing `mkdocs build`:

* Documentaton for `hello_world` package is generated exclusively from source code/docstrings located
  in modules of said package. It's done via
  [pset4_ahmedelazzab.helloworld.md](modules/pset4_ahmedelazzab.helloworld.md)
  file where below line triggers the generation:

```text
::: pset4_ahmedelazzab.helloworld
```

* Documentaton for `exe` package is generated according to:

  * [getting_started.md](modules/pset4_ahmedelazzab.exe/getting_started.md):
  static markdown document, built and maintained manually by developers - for content
  not suitable to be placed in docstrings
  * [source_code.md](modules/pset4_ahmedelazzab.exe/source_code.md):
  this one dynamically generates from source code (same way as for `hello_world` package)

To include your module/package in documentation, include it in the **nav** section of [mkdocs.yml](../mkdocs.yml).
