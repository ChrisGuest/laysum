

The `lay_summary_from_abstract` module uses the OpenGPT API to create lay summaries for a corpus of academic articles.


Installation

```
pip install openai
export OPENAI_API_KEY=<your open ai key>
```

Usage:

```
usage: lay_summary_from_abstract.py [-h] [-v] [-m MODEL] path output_path_summary

positional arguments:
  path
  output_path_summary

options:
  -h, --help            show this help message and exit
  -v, --verbose
  -m MODEL, --model MODEL
 ```

For example to create a JSON object containing abstracts and their lay summaries from the article set `elife/test.json`, run the following.

`python cfls/lay_summary_from_abstract.py elife/test.json elife/test_lay_abstract.json`

