import sys
import openai
import json
from pathlib import Path

debug = False

project_folder = Path.cwd() #Path('/Users/adityajoshi/git_repos/job_app_assistant')
if debug: print(project_folder)

example_dir = project_folder / Path('data/letter_examples')
jobs_dir = project_folder / Path('data/jobs')
output_dir = project_folder / Path('output')

config_file = project_folder / '.config.json'
with open(config_file) as f:
    config = json.load(f)

job_description = config['job_description']

# Set up the OpenAI API client
openai.api_key = config['openai_key']
model_engine = "gpt-4"

def load_examples(example_dir=example_dir):
    ### load example cover letters from example_dir

    if debug: print(example_dir)

    all_examples = ''

    for file_path in example_dir.iterdir():
        if file_path.suffix == '.txt':
            with open(file_path, 'r') as f:
                if debug: print("opening file: " + file_path)
                file_text = f.read().strip()
                all_examples += file_text + '\n'
        else:
            break

    return all_examples

def load_jd(job_description_fn=job_description, jobs_dir=jobs_dir):

        file_path = jobs_dir / job_description_fn
        if file_path.suffix == '.txt':
            with open(file_path, 'r') as f:
                if debug: print("opening file: " + file_path)
                job_description = f.read().strip()
                return job_description
        else:
            "need a txt"
            return



#### pull in text and output response from chatgpt

base_prompt = """
you are a hiring manager for the following job listing
{job_description}

I am an applicant writing a cover letter. some example cover letters I have written in the past are the following
{examples}
"""

def generate_coverletter(jd=None, examples=None, save_fn=None):
    ### the main function to write a cover letter. this requires a job description but does not require cover letter examples.
    ### the cover letters are better and more tailored with past examples

    if debug: print("passing jd: \n" + jd)
    if debug: print("using examples: \n" + examples)

    if jd is None:
        print("error: no job description provided")
        return

    if examples is None:
        print("example: no example cover letters to work off")
        return

    completion = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {
          "role": "system",
          "content": base_prompt.format(job_description=jd, examples=examples)
        },
        {
          "role": "user",
          "content": "write a cover letter that is similar to my previous example cover letters that would work perfectly for the job you are hiring for. try not to change too much regarding my cover letter examples and make sure the new one follows the same style of writing. please keep it short"
        }
      ],
    temperature=1,
    max_tokens=2500,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    coverletter = completion.choices[0].message.content

    if save_fn is None:
        save_fn = 'coverletter_' + job_description

    save_path = output_dir / save_fn
    file = open(save_path, "a+")
    file.write(coverletter)
    file.close()
    return coverletter

def save_coverletter(save_path, coverletter):
    ### save to file
    file = open(save_path, "a+")
    file.write(coverletter)
    file.close()


