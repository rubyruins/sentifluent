
sentifluent 📉📊
============

[![](https://img.shields.io/badge/Made_with-Python3-blue?style=for-the-badge&logo=python)]()
[![](https://img.shields.io/badge/Made_with-pandas-blue?style=for-the-badge&logo=pandas)]()
[![](https://img.shields.io/badge/Made_with-selenium-blue?style=for-the-badge&logo=selenium)]()
[![](https://img.shields.io/badge/Made_with-nltk-blue?style=for-the-badge&logo=nltk)]()
[![](https://img.shields.io/badge/Made_with-plotly-blue?style=for-the-badge&logo=plotly)]()
[![](https://img.shields.io/badge/Made_with-streamlit-blue?style=for-the-badge&logo=streamlit)]()
[![](https://img.shields.io/badge/deployed_on-heroku-blue?style=for-the-badge&logo=heroku)]()

A dashboard for viewing character targeted sentiment analysis and story stats.

It uses Selenium and BeautifulSoup for scraping comments + Pandas and NLTK for data preprocessing and sentiment analysis +  Streamlit and Plotly Express for the dashboard and visulization. You can find the deployed website [here!](https://sentifluent.herokuapp.com/) 

---

## Features:

- The `scrape.py` files use Selenium and BeautifulSoup for scraping around 35k comments from over 100 chapters of my work on Wattpad, [here](https://www.wattpad.com/user/rubyruins).
- The `preprocess.py` files clean, preprocess and split the comments into sentiment scores using NLTK's VADER lexicon. VADER relies on a dictionary that maps lexical features to emotion intensities known as sentiment scores. 
- Most computations are performed on the Compound sentiment score. The sentiment score of a text can be obtained by summing up the intensity of each word in the text.
- The `sentiment.py` file creates the dashboard which visualises stats and inferences.

---

## Screenshots:

<p float="left">
  <img src="https://user-images.githubusercontent.com/50259869/100525910-07eccd80-31ea-11eb-8c5c-138c80920abf.png" width="400" />
  <img src="https://user-images.githubusercontent.com/50259869/100525926-205ce800-31ea-11eb-8260-b72ba77cf053.png" width="400" /> 
</p>

---

## Tech stack:

- `selenium` and `beautifulsoup:` data mining.
- `pandas:` formatting and cleaning the data.
- `nltk:` sentiment analysis using VADER.
- `plotly express:` visualisations.
- `streamlit:` web framework.

---

## Deployment:

The live project is deployed on https://sentifluent.herokuapp.com/. 

---

## Local installation:

**You must have Python 3.6 or higher to run the file.**

- Create a new virtual environment for running the application. You can follow the instructions [here.](https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/26/python-virtual-env/)
- Navigate to the virtual environment and activate it.
- Install the dependancies using `pip install -r requirements.txt`
- Run the `sentiment.py` file with `streamlit run sentiment.py`

**Note:** to run the scraping and preprocessing scripts locally, you must have a version of `chromedriver.exe` that matches the one installed on your device. 
