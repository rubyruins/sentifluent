import streamlit as st
import pandas as pd
import plotly.express as px
import random

st.title('sentifluent.') 
st.markdown('A dashboard for viewing story stats and character targeted sentiment analysis.')
st.sidebar.title('Select a story to get started.')
story = st.sidebar.selectbox('Story', ['Crown of Glass', 'Queen of Death'])

@st.cache(persist = True)
def load_data():
	cog = pd.read_csv("Data/cog.csv")
	qod = pd.read_csv("Data/qod.csv")
	cog.pop('Unnamed: 0')
	qod.pop('Unnamed: 0')
	return cog, qod

def sentiments_to_chapter(df):
	pos = df[(df.Compound > 0)].groupby('Chapter Name').count().reindex(data['Chapter Name'].unique()).reset_index().fillna(0).Positive
	neu = df[(df.Compound == 0)].groupby('Chapter Name').count().reindex(data['Chapter Name'].unique()).reset_index().fillna(0).Neutral
	neg = df[(df.Compound < 0)].groupby('Chapter Name').count().reindex(data['Chapter Name'].unique()).reset_index().fillna(0).Negative
	df = pd.DataFrame(columns = ['Positive', 'Neutral', 'Negative', 'Chapter Name'])
	df['Chapter Name'] = data['Chapter Name'].unique()
	df['Positive'] = pos
	df['Negative'] = neg
	df['Neutral'] = neu
	return df

def sentiments_to_time(df, choice):
	mydict = dict()
	df = df.reset_index()
	if choice == 'Positive':
		for i in range(len(df)):
			if df.loc[i, 'Compound'] > 0:
				mydict[df.loc[i, 'Date']] = mydict.get(df.loc[i, 'Date'], 0) + 1
		mydict = pd.DataFrame(list(mydict.items()),columns = ['Date','Positive Comments']).sort_values(by = 'Date')
	if choice == 'Neutral':
		for i in range(len(df)):
			if df.loc[i, 'Compound'] == 0:
				mydict[df.loc[i, 'Date']] = mydict.get(df.loc[i, 'Date'], 0) + 1
		mydict = pd.DataFrame(list(mydict.items()),columns = ['Date','Neutral Comments']).sort_values(by = 'Date')
	if choice == 'Negative':
		for i in range(len(df)):
			if df.loc[i, 'Compound'] < 0:
				mydict[df.loc[i, 'Date']] = mydict.get(df.loc[i, 'Date'], 0) + 1
		mydict = pd.DataFrame(list(mydict.items()),columns = ['Date','Negative Comments']).sort_values(by = 'Date')
	return mydict

def load_random(df):
	while True:
		i = random.randint(0, len(data) - 1)
		if 'This comment may be offensive.' in data.loc[i]['Original'] or len(data.loc[i]['Original']) < 100:
			# st.write(data.loc[i]['Original'])
			continue
		else:
			st.sidebar.markdown(f"**@{data.loc[i]['Username']}** commented on {data.loc[i]['Chapter Name']}:")
			st.sidebar.markdown(f"{data.loc[i]['Original']}")
			break

cog, qod = load_data()

if story == 'Crown of Glass':
	data = cog
	names = ['Edwina', 'Tristan', 'Eric', 'Amphitrite', 'Drusilla', 'Aidon', 'Celestina', 'Deimos', 'Cosmo', 'Emerick', 'Thanatos', 'Ambrosine', 'Apollo', 'Titania', 'Favian', 'Helios', 'Eros', 'Vivian', 'Miriel', 'Elodie', 'Lucius']
else: 
	data = qod
	names = ['Persephone', 'Hades', 'Demeter', 'Zeus', 'Hecate', 'Athena', 'Artemis', 'Thanatos', 'Poseidon', 'Charon', 'Cerberus']

load_random(data)

st.subheader("Stats over all chapters.")
option = st.radio("Type", ['Comments', 'Reads', 'Votes'], key = 1)
temp = data[['Comments', 'Reads', 'Votes', 'Chapter Name']].drop_duplicates()
st.plotly_chart(px.line(temp, x = 'Chapter Name', y = option))
a, b = list(temp[option]), list(temp['Chapter Name'])
option = option.lower()
st.write(f"Each of the chapters has an average of around {round(sum(a) / len(a))} {option}! {b[a.index(max(a))]} performed the best with around {max(a)} {option}, while {b[a.index(min(a))]} achieved only {min(a)} {option}.")

st.subheader("Stats over all parts.")
option = st.radio("Type", ['Comments', 'Reads', 'Votes'], key = 2)
temp = data[['Comments', 'Reads', 'Votes', 'Part']].drop_duplicates().groupby(by=["Part"])[option].sum().reset_index()
st.plotly_chart(px.pie(temp, names = 'Part', values = option, hole=0.5).update_layout(width=400, height=400))
# a, b = list(temp[option].index), list(temp[option].values)
# st.write(f"Part {a[(b).index(max(b))]} of {story} seems to be the most popular with a total of over {max(b)} {option.lower()}.")

st.subheader("Comments over all time.")
temp = dict()
for i in data.Date:
	temp[i] = temp.get(i, 0) + 1
temp = pd.DataFrame(list(temp.items()),columns = ['Date','Comments']).sort_values(by = 'Date')
st.plotly_chart(px.histogram(temp, x = 'Date', y = 'Comments', histfunc='sum').update_traces(xbins_size="M1").update_layout(bargap=0.35,
	xaxis=dict(
		rangeselector=dict(
			buttons=list([
				dict(count=1,
					 label="1m",
					 step="month",
					 stepmode="backward"),
				dict(count=6,
					 label="6m",
					 step="month",
					 stepmode="backward"),
				dict(count=1,
					 label="YTD",
					 step="year",
					 stepmode="todate"),
				dict(count=1,
					 label="1y",
					 step="year",
					 stepmode="backward"),
				dict(step="all")
			])
		),
		rangeslider=dict(
			visible=True
		),
		type="date"
	)))
temp = temp[temp['Comments']==temp['Comments'].max()]
st.write(f"{story} reached max popularity on {temp.Date.values[0]} with {temp.Comments.values[0]} comments on a single day!")

st.subheader("General sentiment over all chapters.")
option = st.radio("Type", ['All', 'Positive', 'Neutral', 'Negative'], key = 3)
temp = data[['Chapter Name', 'Positive', 'Neutral', 'Negative', 'Compound']]
temp = sentiments_to_chapter(temp)
if option == 'All':
	st.plotly_chart(px.line(temp, x = 'Chapter Name', y = ['Positive', 'Negative', 'Neutral']))
else:
	c = ['', '#636EFA', '#00CC96', '#EF553B'][['All', 'Positive', 'Neutral', 'Negative'].index(option)]
	st.plotly_chart(px.line(temp, x = 'Chapter Name', y = option).update_traces(line_color=c))

st.subheader("General sentiment over all time.")
option = st.radio("Type", ['Positive', 'Neutral', 'Negative'], key = 4)
temp = sentiments_to_time(data, option)
c = ['', '#636EFA', '#00CC96', '#EF553B'][['All', 'Positive', 'Neutral', 'Negative'].index(option)]
st.plotly_chart(px.histogram(temp, x = 'Date', y = f'{option} Comments', histfunc='sum').update_traces(xbins_size="M1", marker_color=c).update_layout(bargap=0.35))

st.header("Let's see how the readers feel about particular characters.")
st.subheader("Get started by naming a character from the story. ")
st.markdown("💡 Pro tip: Check out the sidebar for a full list of awesome characters appearing in the story!")
person = st.selectbox('Select', names)
# option = st.radio("Type", ['Positive', 'Neutral', 'Negative'], key = 5)

temp = data[data['Text'].str.contains(person.lower())]
temp = sentiments_to_chapter(temp)
# c = ['', '#636EFA', '#00CC96', '#EF553B'][['All', 'Positive', 'Neutral', 'Negative'].index(option)]
# st.plotly_chart(px.line(temp, x = 'Chapter Name', y = option).update_traces(line_color=c))
temp = temp.sum(axis = 0).reset_index()[:3]
temp.rename(columns ={'index': 'Sentiment', 0: 'Comments'}, inplace = True)
n = list(temp.Sentiment.values)
v = list(temp.Comments.values)
c = ['#636EFA', '#00CC96','#EF553B']
v, n, c = [list(i) for i in zip(*sorted(zip(v, n, c)))]
v.reverse()
n.reverse()
c.reverse()
st.plotly_chart(px.pie(values = v, names = n, color_discrete_sequence = c, hole=0.5).update_layout(width=400, height=350))
st.write(f"Most reader sentiment towards {person} is {n[v.index(max(v))].lower()}.")