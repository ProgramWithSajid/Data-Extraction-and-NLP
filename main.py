import requests
from bs4 import BeautifulSoup
import pandas as pd
import string
from nltk.tokenize import word_tokenize,sent_tokenize
from nltk.corpus import stopwords

df = pd.read_excel('D:\Sajit\Python Practice\input.xlsx', engine='openpyxl')

#empty data frame for storing the result
result_df = pd.DataFrame(columns=['URL_ID','URL','TITLE','POSITIVE SCORE','NEGATIVE SCORE','POLARITY SCORE','SUBJECTIVITY SCORE','AVG SENTENCE LENGTH', 'AVG NUMBER OF WORDS PER SENTENCE','WORD COUNT','SYLLABLE PER WORD'])


for index, row in df.iterrows():
    url_id = row['URL_ID']
    url = row['URL']
    
    

    if pd.notna(url):  #if row id not null 
#        print(f"row id {url_id}")
        try:
            # Send an HTTP GET request to the URL
            response = requests.get(url)
            
            # Check if the request was successful (status code 200)
            if response.status_code == 200:

            
                soup = BeautifulSoup(response.content,'html.parser')
                # print(soup.find_all('title'))
                title = soup.title.string
            #    print(title)
                para = soup.find(attrs={'class':'td-post-content tagdiv-type'}).get_text()


                #sent_tokenize creating tokenize sentence from para
                total_sentences = sent_tokenize(para,"english")
                #print(len(total_sentences))



                #for remove punctuations
                text = para.lower()
                clean_text = text.translate(str.maketrans('','',string.punctuation))
             #   print("Total number of words: ", len(clean_text))

                #word_tokenize creating tokenize word from para
                tokenize_word = word_tokenize(clean_text,"english")
             #   print("Word count: ", len(tokenize_word))




                #remove stopword in our content
                final_words = []
                for word in tokenize_word:
                    if word not in stopwords.words("english"):
                        final_words.append(word)

             #   print("clean words: ", len(final_words))

                #positive word count
                POSITIVE_WORD = []
                with open('MasterDictionary/positive-words.txt', 'r') as file:
                    for line in file:
                        clear_line = line.replace('\n','')         #for no blank lines
                        var = clear_line
                        if var in final_words:
                            POSITIVE_WORD.append(var)

                POSITIVE_SCORE = len(POSITIVE_WORD)
             #   print("Positive score: ", POSITIVE_SCORE)


                #negative word count
                NEGATIVE_WORD = []
                with open('MasterDictionary/negative-words.txt', 'r') as file:
                    for line in file:
                        clear_line = line.replace('\n','')       #for no blank line
                        var = clear_line
                        if var in final_words:
                            NEGATIVE_WORD.append(var)

                NEGATIVE_SCORE = len(NEGATIVE_WORD)
             #   print("Negative score: ",NEGATIVE_SCORE)

                # Measuring polarity score 
                POLARITY_SCORE = (POSITIVE_SCORE - NEGATIVE_SCORE)/((POSITIVE_SCORE + NEGATIVE_SCORE) + 0.000001)
             #   print("Polarity score: ", round(POLARITY_SCORE, 4))

                #Measuring subjectivity score
                clean_words = len(final_words)
                SUBJECTIVITY_SCORE = (POSITIVE_SCORE + NEGATIVE_SCORE)/ ((clean_words) + 0.000001)
             #   print("Subjective score: ", round(SUBJECTIVITY_SCORE, 4))

                #Measuring Average Sentence Length
                AVG_SENTENCE_LENGTH = len(final_words) / len(total_sentences)
             #   print("Average Sentence Length: ", round(AVG_SENTENCE_LENGTH))


                #AVG NUMBER OF WORDS PER SENTENCE
                AVG_NUMBER_OF_WORDS_PER_SENTENCE = len(tokenize_word)  / len(total_sentences)
             #   print("AVG NUMBER OF WORDS PER SENTENCE: ", round(AVG_NUMBER_OF_WORDS_PER_SENTENCE))

                #Syllable Count Per Word
                count_vowels = ""
                for x in tokenize_word:
                    for i in x:
                        if i.lower() in 'aeiou':
                            count_vowels += i

             #   print("SYLLABLE PER WORD: ", len(count_vowels))
                
                #data = [[url_id,url,title,POSITIVE_SCORE,NEGATIVE_SCORE,POLARITY_SCORE,SUBJECTIVITY_SCORE,round(AVG_SENTENCE_LENGTH),round(AVG_NUMBER_OF_WORDS_PER_SENTENCE),len(tokenize_word),len(count_vowels)]]
                result_data = {'URL_ID': url_id,
                               'URL':url,
                               'POSITIVE SCORE':POSITIVE_SCORE,
                               'NEGATIVE SCORE':NEGATIVE_SCORE,
                               'POLARITY SCORE':POLARITY_SCORE,
                               'SUBJECTIVITY SCORE':SUBJECTIVITY_SCORE,
                               'AVG SENTENCE LENGTH':AVG_SENTENCE_LENGTH,
                               'AVG NUMBER OF WORDS PER SENTENCE':AVG_SENTENCE_LENGTH,
                               'WORD COUNT':len(tokenize_word),
                               'SYLLABLE PER WORD':len(count_vowels)
                               }
                result_df = result_df.append(result_data,ignore_index = True) #appending the result data in the data frame
                

                
                print(f"Successfully processed URL {index + 1}: {url}")
            else:
                print(f"Failed to fetch URL {index + 1}: {url}, Status Code: {response.status_code}")
        except Exception as e:
            print(f"Error processing URL {index + 1}: {url}, Error: {str(e)}")



print("----for loop end ----")

result_df.to_csv('output_data_structure.csv')

