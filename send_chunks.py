import openai
import os
from dotenv import load_dotenv
load_dotenv()
import time
import json
from prompts import chunks_send
from main_mod import *
def getAPIkey():
    return os.getenv('OPENAI_API_KEY')
def compare_str(string,comp):
    input([string,comp])
    ls = [[string[0]]]
    for k in range(0,len(string)):
        if string[k] in comp:
            if str(ls[-1])+string[k] in comp:
                ls[-1].append(string[k])
            else:
                ls[-1] = len(ls[-1])
                ls.append([string[k]])
    ls[-1] = len(ls[-1])
    ls.sort()
    return int(len(comp)/int(ls[-1]))    
def tokens(model):
    js = {"8192":['gpt-4', 'gpt-4-0314'],"32768":['gpt-4-32k', 'gpt-4-32k-0314'],"4097":['gpt-3.5-turbo', 'gpt-3.5-turbo-0301','text-davinci-003', 'text-davinci-002'],"8001":["code-davinci-002","code-davinci-001"],"2048 ":['code-cushman-002','code-cushman-001'],"2049":['davinci', 'curie', 'babbage', 'ada','text-curie-001','text-babbage-001','text-ada-001']}
    keys = list(js.keys())
    input(keys)
    for k in range(0,len(keys)):
        if model in js[keys[k]]:
            input(keys[k])
            return keys[k]
    return 2049
def endPoints(model,prompt):
    ends = {'/v1/chat/completions':{"prompt":[{"role": "user", "content": f'{json.loads(prompt)}'}],"model":"gpt-4, gpt-4-0314, gpt-4-32k, gpt-4-32k-0314, gpt-3.5-turbo, gpt-3.5-turbo-0301".split(',')},'/v1/completions':{"prompt":[{"role": "user", "content": f'{prompt}'}],"model":'text-davinci-003, text-davinci-002, text-curie-001, text-babbage-001, text-ada-001'.split(',')},'/v1/edits':{"prompt":[{"role": "user", "content": f'{prompt}'}],"model":['text-davinci-edit-001, code-davinci-edit-001'.split(',')],
                                                                                                                                                                                                                                                                                                                                                                                   '/v1/audio/transcriptions':{"prompt":[{"role": "user", "content": f'{prompt}'}],"model":['whisper-1']},
                                                                                                                                                                                                                                                                                                                                                                                           '/v1/audio/translations':['whisper-1']},
                                                                                                                                                                                                                                                                                                                                                                                   '/v1/fine-tunes':{"prompt":[{"role": "user", "content": f'{prompt}'}],"model":'davinci, curie, babbage, ada'.split(',')},
                                                                                                                                                                                                                                                                                                                                                                                   '/v1/embeddings':{"prompt":[{"role": "user", "content": f'{prompt}'}],"model":'text-embedding-ada-002, text-search-ada-doc-001'.split(',')},
                                                                                                                                                                                                                                                                                                                                                                            '/v1/moderations':{"prompt":[{"role": "user", "content": f'{prompt}'}],"model":'text-moderation-stable, text-moderation-latest'.split(',')}}
    keys= list(ends.keys())
    for k in range(0,len(keys)):
        for j in range(0,len(ends[keys[k]]["model"])):
              if ends[keys[k]]["model"][j] == model:
                  return keys[k],ends[keys[k]]["model"][j],ends[keys[k]]["prompt"]
    return keys[k],ends[keys[k]]["model"][j],ends[keys[k]]["prompt"]
def get_all(model,prompt):
    endpoint,model,prompt = endPoints(model,prompt)
    max_tokens = tokens(model)
    return prompt,model,max_tokens,endpoint
def parameters(jsN):
    js = {"top_p": 1,"temperature": 2,"frequency_penalty": 0,"presence_penalty": 0}
    keys = list(js.keys())
    for k in range(0,len(keys)):
        jsN[keys[k]] = js[keys[k]]
    return jsN
def headers():
    return {'Content-Type': 'application/json','Authorization': 'Bearer  '+getAPIkey()}
def urls(end_point):
    return 'https://api.openai.com'+end_point
def datas(js):
    return json.dumps(parameters(js))
def send_prompt_to_openai(prompt, model='gpt-4', max_tokens=4046, endpoint='/v1/chat/completions'):
    response = requests.post(urls(endpoint), json=datas({"model": model,"messages": prompt,"max_tokens": 4046}),headers=headers())
    input(response)
    if response.status_code == 200:
        return json.loads(json.dumps(response.json()))
    else:
        raise Exception("Request failed with status code: {}".format(response.status_code))
def send_chunks_to_chatgpt(file_path,model):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    content = reader(file_path)
    k = 0
    max_tokens = int(tokens(model))
    notation = ''
    chunks = [content[i:i + max_tokens] for i in range(0, len(content), max_tokens)]
    for chunk in chunks:
        prompt,model,max_tokens,endpoint = get_all(model,chunks_send(k,chunks,chunk,'the following is a conversation regartding a potential react project with the goal of graphic user interface to allow the user to view the objects within a folder as buttons on a canvas to be [pressed for a littany of objectives, first and foremost being to create a visualization of which files it interacts with; i would like for the entirety of this project to be installed and developed with a bash script or series of bash scripts that do all propigation of files, folders, edits, modificatioins etc via running the bash script. so far as desired responses, i would like for the response to be stricky a single json response that houses the bash scriptas a valye of a "script" key. if at some point the bash script has to be truncated withough just cause, i would like for the next response to accompany another bash script that will mend the broken bash scripts when in the same folder. i will be sending this script in pieces.',"Include any important notes for better contextual understanding of the  subsequent parts. Update this section as needed."))
        response = send_prompt_to_openai(prompt,model,max_tokens,endpoint)
        notation = response["notation"]
        responses.append(response["choices"][0]["message"]["content"])
        input(notation)
        pen(responses,'response{k}.json')
        time.sleep(1)  # Add delay to avoid rate limits
        k +=1
    return "".join(responses)

