**Sentiment Analysis:**
- Used Selenium to scrape user comments on all chapters of my book at https://www.wattpad.com/361651023-crown-of-glass. 
- My aim was to analyse user sentiment towards **different characters** or **specific terms** in the story. 
- I cleaned and preprocessed the data using regex and did sentiment analysis using the vader lexicon from nltk. 
- Finally, I plotted the results using matplotlib to visualise positive, neutral and negative emotions towards each of the different characters by number and percentage of mentions.

!["Sentiments by character."](screenshots/1.png "Sentiments by character.")
!["Sentiments by family name."](screenshots/2.png "Sentiments by family name.")
!["Sentiments by number of mentions of character."](screenshots/3.png "Sentiments by number of mentions of character.")