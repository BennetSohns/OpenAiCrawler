import os
import openai
import nltk
from csv import writer
import time
from wallet import apikey

openai.api_key = apikey


def new_line(esg_input):
    with open('EsgDataNegative1.csv', 'a+', newline='') as f_object:
        # Pass this file object to csv.writer()
        # and get a writer object
        writer_object = writer(f_object)

        # Pass the list as an argument into
        # the writerow()
        writer_object.writerow(esg_input)

        # Close the file object
        f_object.close()


# Main loop
while True:

    # Try statement to avoid network error from OpenAi
    try:
        # Send request via OpenAi SDK
        response = openai.Completion.create(
          model="text-davinci-003",
          prompt="generate 50 random negative sentences about ESG and don´t use the word 'A'",
          temperature=0.6,
          max_tokens=150,
          top_p=1,
          frequency_penalty=1,
          presence_penalty=1
        )

        # Filter response by the text
        text = response["choices"][0]["text"]

        # Divide the outcome into sentences with NLTK
        tokenizedText = nltk.sent_tokenize(text)

        # Remove the first item and take every second item (to remove "1.", "2." ...)
        for each in tokenizedText[1:][0::2]:

            print(each)

            # Select only sentences which end with a dot or are which have a length > 60 to improve data quality
            if each[len(each)-1] == "." and len(each) > 40:
                new_line([each])
    except:
        print("error")

    # Relax for 60 seconds to avoid API overload
    time.sleep(60)
