# Let's import dependences 
import pandas as pd
import nltk
import pandas as pd
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Collecting the news from finviz.com into tables

perdiod = 30

finviz_url = 'https://finviz.com/quote.ashx?t='

tickers = ['AAPL', 'GOOG', 'AMZN', 'FB']

for ticker in tickers:
    url = finviz_url + ticker

    req = Request(url=url, headers={'user-agent':'my-app'})
    response = urlopen(req)

    html = BeautifulSoup(response, 'html.parser')

    news_table = html.find(id='news-table')
    news_tables[ticker] = news_table
    
# Extract the important variables from the data collected

parsed_data = []

for ticker, news_table in news_tables.items():

    for row in news_table.findAll('tr'):

        title = row.a.get_text()

        if len(date_data) == 1:
            time = date_data[0]
        else:
            date = date_data[0]
            time = date_data[1]
        
        parsed_data.append([ticker, date, time, title])
        

# Store data as dataframe

df = pd.DataFrame(parsed_data, columns=['ticker', 'date', 'time', 'title'])
df.head()

# Carry put the sentiment analysis on the data

vader = SentimentIntensityAnalyzer()

condition = lambda title: vader.polarity_scores(title)['compound'] #using a lambda function to treat each row of the compound function
df['compound'] = df['title'].apply(condition) # Applying the condition on the compound feature
df['date'] = pd.to_datetime(df['date']).dt.date #Convert the data column to pandas datetime
df.head()

#Let's create a function that calculate positive and negative sentiment

mean_df = df.groupby(['ticker', 'date']).mean().unstack().xs('compound', axis = 'columns').transpose()
mean_df = mean_df.iloc[-period:]
mean_df.tail()

# Plot a bar chart to visualise sentiments

plt.figure(figsize=(15,8))

plt.bar(mean_df.index,mean_df.AAPL , label='AAPL') 
plt.bar(mean_df.index,mean_df.AMZN, label='AMZN')
plt.bar(mean_df.index,mean_df.FB, label='FB')
plt.bar(mean_df.index,mean_df.GOOG, label='GOOG')
plt.title('Sentiment Intensity Chart')
plt.xlabel('News days over the past 30 days period')
plt.ylabel('Sentiment Intensity')
plt.legend()

plt.show()
        
        
        
        
        
        
