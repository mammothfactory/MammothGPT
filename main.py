#from transformers import AutoTokenizer, AutoModelForCausalLM
#from optimum.bettertransformer import BetterTransformer
#from transformers import TrainingArguments
#import transformers
#import torch

# Offical python library with pre-defined set of classes (e.i  openai.Edit.create()) for API resources  
# https://github.com/openai/openai-python
import openai

import gradio as gr

MAX_CREATIVITY = 1
COLLEGE_LEVEL_CREATIVITY = 0.8
HIGH_SCHOOL_LEVEL_CREATIVITY = 0.6
ELEMENTARY_SCHOOL_LEVEL_CREATIVITY = 0.4
MIN_CREATIVITY = 0

ENTITY_TYPES = ["Investor", "Speculator", "Land Syndicate", "Recreational Land"]

model_id = "tiiuae/falcon-40b-instruct" #"tiiuae/falcon-180B"
title = '🦣 Mammoth GPT'
description = f'Explore the {model_id.upper()} LLM with Real Estate fine-tuning'

def generate(prompt, operation):
    if operation == ENTITY_TYPES[0]:
        return call(prompt, "You are a land investors buying undeveloped land with the expectation that its value will appreciate over time. ")
    elif operation == ENTITY_TYPES[1]:
        return call(prompt, "You are a speculators what doesn't plan to make significant improvements to the property. ")
    elif operation == ENTITY_TYPES[2]:
        return call(prompt, "You are in a group of investors that pooled their resources to purchase land collectively, thus spreading the risk. ")
    elif operation == ENTITY_TYPES[2]:
        return call(prompt, "You are looking for land for recreational purposes, such as hunting, fishing, camping, or outdoor activities. ")
    else: 
        return call(prompt, "You are a Real Estate agent ")

def call(prompt, systemRole):
    openai.api_key = "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"
    
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "system", "content": systemRole + prompt}])
    text_field = completion.choices[0].message.content
    
    if "AI language model" in text_field:
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "system", "content": systemRole + "Don't use the words 'As an AI language model'. " + prompt}])
        text_field = completion.choices[0].message.content

    return text_field
     
gr.Interface(fn=generate, 
             title=title, description=description,
             theme='gstaff/xkcd',
             inputs=[
                gr.inputs.Textbox(label="Input Question"),
                gr.inputs.Dropdown(choices=ENTITY_TYPES, label="Select the type of real estate entity behavior to use:")
                ],
             outputs=gr.outputs.Textbox(label="AI Output")).launch(server_port=6969, share=False) 
