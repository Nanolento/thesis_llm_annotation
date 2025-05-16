Annotation on reader's perception elements using LLMs
=====================================================

For my bachelor's thesis, I am doing research on the effect of reader's perception
elements on persuasion. For this, we need to annotate a large dataset of Reddit
r/ChangeMyView comments. We have annotated ~600 comments manually and will use
this code to annotate the full dataset (or at least a large part of it).

This GitHub repository contains the code used to get the annotations from the LLMs and
further processing of the annotations.

Description of files
--------------------

- `main.py`
    - contains the code that interfaces with the LLM, the system prompt, does the annotations
      and saves those annotations to a file.
- `validate_annotations.py`
    - validates the annotations and outputs how many annotations were properly made.
- `evaluation.py`
    - validates the LLM annotation file created by `main.py` against a golden standard file

Usage
-----

Annotate data into a JSON format. The program expects the body of the comment (the title of a post should be
merged into this body), the 'name' of the comment and the classes.

### Classes

- `story_class`: Either 'Story' or 'Not Story', depending if there is a story in the comment or not.
- `suspense`: Likert scale rating from 1 to 5.
- `curiosity`: Likert scale rating from 1 to 5.
- `surprise`: Likert scale rating from 1 to 5.

### Ollama

Download and install [Ollama](https://ollama.com). You do not have to install it system-wide but make sure
it is in your `$PATH` environment variable.

Run it with the model you want to use (in our research we used `llama3.2`):

    $ ollama run llama3.2

It will download the model and allow you to chat with the model. Just close the prompt with Ctrl+D.
Start the Ollama server:

    $ ollama serve

Then, in another terminal (tmux is recommended, since you can create multiple windows), you can run `main.py` to do the annotations:

    $ python3 main.py <input file> <method> <output file>

Here, the input file is the file you want the model to annotate, the method is either 'zeroshot' or 'fewshot' and the output file
is where you want the program to save the LLM's annotations.

You can then validate the annotations with `validate_annotations.py`:

    $ python3 validate_annotations.py <input file>

Where the input file is the file containing the LLM's annotations. If it looks good, you can evaluate the model performance:

    $ python3 evaluation.py <annotation file> <golden standard file>

Where you provide the LLM's annotations and the golden standard test set. Make sure when evaluating, you let the model annotate
that golden standard file first, before evaluating against it!
