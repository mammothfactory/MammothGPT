from langchain import HuggingFacePipeline
from langchain import PromptTemplate,  LLMChain
from transformers import AutoTokenizer, AutoModelForCausalLM
import transformers
import os
import torch
import gradio as gr

# https://github.com/nicknochnack/Falcon40B/blob/main/Falcon.ipynb


###Build the Pipeline
# Define Model ID
model_id = "tiiuae/falcon-40b-instruct"  #TODO Pin version to avoid more downloads model_name = "username/repo-name:model-version"
# Load Tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_id)
# Load Model 
model = AutoModelForCausalLM.from_pretrained(model_id, cache_dir='./workspace/', 
    torch_dtype=torch.float32, trust_remote_code=True, device_map="auto", offload_folder="offload")  # Use torch.float32 instead of torch.bfloat16 for Apple Silicon
# Set PT model to inference mode
model.eval()
# Build HF Transformers pipeline 
pipeline = transformers.pipeline(
    "text-generation", 
    model=model,
    tokenizer=tokenizer,
    device_map="auto",
    max_length=400,
    do_sample=True,
    top_k=10,
    num_return_sequences=1,
    eos_token_id=tokenizer.eos_token_id
)
pipeline('who is kim kardashian?')

# Setup prompt template
template = PromptTemplate(input_variables=['input'], template='{input}') 
# Pass hugging face pipeline to langchain class
llm = HuggingFacePipeline(pipeline=pipeline) 
# Build stacked LLM chain i.e. prompt-formatting + LLM
chain = LLMChain(llm=llm, prompt=template)

response = chain.run('who is kim kardashian?')

def generate(prompt): 
    # The prompt will get passed to the LLM Chain!
    return chain.run(prompt)
    # And will return responses 
    
title = '🦣 Mammoth GPT'
description = f'Explore the {model_id.upper()} LLM'

def generate(prompt):
    return "Testing this prompt"
     
gr.Interface(fn=generate, inputs=["text"], outputs=["text"],
             title=title, description=description,
             theme='gstaff/xkcd'
             
            ).launch(server_port=6969, share=True)    