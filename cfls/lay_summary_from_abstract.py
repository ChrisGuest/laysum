import argparse
import datetime
import json
import os
import random
import time

import openai


class ChatGPTSession:
    model = ''
    def __init__(self, model="gpt-3.5-turbo"):
        self.model = model
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def get_completion(self, content):
        return openai.ChatCompletion.create(
            model=self.model,
            messages=[{"role": "user", "content": content}])

    def feed(self):
        pass


class CorporaForLayAbstraction(ChatGPTSession):
    """
    Data format:
        'id', 'year', 'title', 'sections', 'headings', 'abstract', 'summary', 'keywords'
    """
    data = []
    path = ''
    def __init__(self, path, output_path_summary, verbose=True, model="gpt-3.5-turbo"):
        self.path = path
        self.model = model
        self.output_path_summary = output_path_summary
        self.verbose = verbose
        with open(self.path) as f:
            self.data = json.load(f)

    def process(self, i, article):
        try:
            abstract = '\n'.join(article['abstract'])
            request = f"""Rewrite the following abstract for a lay audience:\n{abstract}"""
            if self.verbose:
                print(i, article['title'])
            completion = self.get_completion(request)
            lay_abstract = completion.choices[0].message.content
            results = dict(id=article['id'], abstract=abstract, lay_abstract=lay_abstract)
            time.sleep(1)
        except Exception as error:
            print(f"Exception at {i} {article['id']}: {error}")
            results = dict(id=article['id'], abstract=article, error=str(error))
        return results

    def feed(self):
        if os.path.exists(self.output_path_summary):
            with open(self.output_path_summary) as f:
                results_summary = json.load(f)
        else:
            results_summary = []

        for i, article in enumerate(self.data):
            if i < len(results_summary):
                if 'error' in results_summary[i]:
                    results_summary[i] = self.process(i, article)
                else:
                    continue
            results_summary.append(self.process(i, article))

            if i%50==49:
                print(i, end=' ')
                with open(self.output_path_summary, "w") as f:
                    json.dump(results_summary, f)

        else:
            print(i)

        with open(self.output_path_summary, "w") as f:
            json.dump(results_summary, f)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    parser.add_argument('output_path_summary')
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-m', '--model', default='gpt-3.5-turbo')
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    cfls = CorporaForLayAbstraction(args.path, args.output_path_summary, args.verbose, args.model)
    cfls.feed()
