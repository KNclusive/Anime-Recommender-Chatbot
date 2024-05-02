#!/usr/bin/env python
# coding: utf-8

# In[1]:


from openai import OpenAI
import json
import os
import pandas as pd
import numpy as np


# In[2]:


from openai import OpenAI

client = OpenAI(api_key='YOUR_API_KEY')


def intent_detection(user_input):
    generated_text = {}
    
    for x in ["genre", "episodes", "score", "title"]:
        text=""
        stream = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": f"In query -{user_input}- what is {x} number or type or name, answer in 1 word, answer in list format of type [genre1, genre2, ...], say null if {x} is not present in the query."}],
                stream=True,
            )
        for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    text += chunk.choices[0].delta.content
        generated_text[x] = text
    
    if generated_text["episodes"].lower()!="null" and generated_text["episodes"].isdigit():
        generated_text["episodes"] = int(generated_text["episodes"])
    
    if generated_text["score"].lower()!="null" and generated_text["score"].replace('.','',1).isdigit():
        generated_text["score"] = float(generated_text["score"])

    if generated_text["genre"].lower()!="null":
        generated_text["genre"] = generated_text["genre"][1:-1].split(', ')
    
    for key, value in generated_text.copy().items():
        if isinstance(value, str):
            if value.lower()=="null":
                del generated_text[key]
    print(generated_text)
    
    return generated_text

def response_text(prompt, filter_animes, found):
    generated_text = ""
    
    
    animes=[]
    genre=[]
    desc=[]
    rating=[]
    
    for anime in filter_animes:
        
        animes.append(filter_animes["title"])
        genre.append(filter_animes['genre'])
        desc.append(filter_animes['synopsis'])
        rating.append(filter_animes['score'])
    
    print('found', found)
    
    if found == 1:
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "assistant", "content": f"Structure a recomendations of length {len(filter_animes)} from this query {prompt} to provide output from these list of animes {animes} with a small decription of each as {desc} also the anime ratings {rating} and anime genre as {genre}"}],
            stream=True,
        )
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                generated_text += chunk.choices[0].delta.content
    elif found == 2:
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "assistant", "content": f"Structure a recomendations of length {len(filter_animes)} to provide output from these list of animes {animes} with a small decription of each as {desc} also the anime ratings {rating} and anime genre as {genre},but start similar to - Here are the most popular anime that I found, end without summarizing"}],
            stream=True,
        )
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                generated_text += chunk.choices[0].delta.content
    elif found == 3:
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "assistant", "content": f"Structure a recomendations of length {len(filter_animes)} from this query {prompt} to provide output from these list of animes {animes} with a small decription of each as {desc} also the anime ratings {rating} and anime genre as {genre},but start similar to - I could'nt find what you requested but here are some popular anime that I found, end without summarizing"}],
            stream=True,
        )
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                generated_text += chunk.choices[0].delta.content
    else:
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "assistant", "content": f"Structure a recomendations of length {len(filter_animes)} from this query {prompt} to provide output from these list of animes {animes} with a small decription of each as {desc} also the anime ratings {rating} and anime genre as {genre},but start with - Unfortunately could not find what you asked in the query, but here are some similar results you may like."}],
            stream=True,
        )
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                generated_text += chunk.choices[0].delta.content
                
    generated_text = generated_text.replace("\n", "<br>").replace("**", "")
    return generated_text


# In[ ]:





# In[ ]:




