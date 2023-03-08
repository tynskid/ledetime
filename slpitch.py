import streamlit as st
import requests
import json


import os
import openai
openai.api_key = "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"





def get_text(query_url):

    url = "https://api.diffbot.com/v3/article?url="+query_url+"&token=032f956e21895ee00941315009d62c45"

    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)

    data = json.loads(response.text)

    page_text = data['objects'][0]['text']
    return page_text



def get_pitch(page_text):




    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "user", "content": 
        '''
    Provide a list of bullet points, which encompass the main ideas in the following article, which has been extracted from a web page.  
    Your response should read as a list of the most interesting bullet points, with an emphasis on newsworthy information, which can be found in the following example:

    Example: 

    {0}
        '''.format(page_text)}
      ]
    )

    print(completion.choices[0].message['content'])


    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "user", "content":
        '''
    Using the previous summary you created, please formulate a pitch i the form of an email, to a writer for the new york times, 
    who has covered similar types of stories in the past.  Write a compelling pitch that gives the writer interesting and newsworthy
    data points gleaned from the story summary you wrote previously.  Try to make the pitch personalized to the writer, who we know
    to be a writer who has covered similar topics and themes in the past.  Make the response the format of an email.  Please remember this is 
    not a pitch endorsing any product or service, it is simply an effort to get a writer to write a story about the interesting information contained inour article.  Please keep the pitch as short as possible, and make sure that for any intereting data points you list, provide them in a bulleted format.

    {0}
        '''.format(page_text)}
      ]
    )


    return completion.choices[0].message['content']


form = st.form(key='my_form')
url = form.text_input(label='Enter Article URL')
submit_button = form.form_submit_button(label='Submit')


if submit_button:
	page_text = get_text(url)
	final_pitch = get_pitch(page_text)
	st.write(f'{final_pitch}')