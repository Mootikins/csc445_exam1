# NFA to DFA and DFA Minimizer

### Requirements

- Python version 3.7 or greater -- uses `__future__`'s annotations for a forward
  reference in the `FiniteAutomata` class
- `networkx` with all optional packages (may need to install with `pip install
  networkx[all]` in BASH specifically -- will error out in ZSH)
- `pygraphviz` which specifically requires you to have the system package for
  graphviz, which is usually named identically in repositories

These are listed in the `requirements.txt` file, so you should be able to
install as follows:

```sh
# enter virtual environment if desired
$ pip install -r requirements.txt 
```

### Running

This takes two or three arguments. Shown below is the help text:

```
usage: main.py action input_file [options]

Convert an NFA to a DFA, minimize a DFA, or both in sequence. Writes the
output .dot file to 'grid.dot' and a PDF rendering to 'grid.dot.pdf'

positional arguments:
  {convert,minimize,both}
                        convert an NFA to DFA, minimize a DFA, or both
  input_file            Input filename in graphviz .gv format

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT_FILE, --output_file OUTPUT_FILE
                        Output filename for intermediate .dot file and the
                        PDF. Defaults to 'grid.dot' and 'grid.dot.pdf'
```

### Notes

While I had done the NFA -> DFA mostly successfully (there is one error in the
test case), my method made it so I could not get the original final states from
the graphviz/networkx instance, which makes the DFA minimization impossible.
With how much architecting I did to get the NFA -> DFA to work without tons of
edge case checks, I'm not terribly keen on rewriting it all to use networkx just
so I can preserve the final states and do the DFA minimization.
