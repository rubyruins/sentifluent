import streamlit as st
import pandas as pd
import plotly.express as px

st.title('sentifluent.') 
st.markdown('A dashboard for viewing story stats and character targeted sentiment analysis.')
st.sidebar.title('Select a story to get started.')
story = st.sidebar.selectbox('Story', ['Crown of Glass', 'Queen of Death'])

@st.cache(persist = True)
def load_data():
	cog = pd.read_csv("Data/cog.csv", keep_default_na = False)
	qod = pd.read_csv("Data/qod.csv", keep_default_na = False)
	cog.pop('Unnamed: 0')
	qod.pop('Unnamed: 0')
	return cog, qod

cog, qod = load_data()

# story = 'Queen of Death'
if story == 'Crown of Glass':
	data = cog
else: 
	data = qod

st.subheader("Stats over all chapters.")
option = st.radio("Type", ['Comments', 'Reads', 'Votes'], key = 1)
temp = data[['Comments', 'Reads', 'Votes', 'Chapter Name']].drop_duplicates()
st.plotly_chart(px.bar(temp, x = 'Chapter Name', y = option))
a, b = list(temp[option]), list(temp['Chapter Name'])
option = option.lower()
st.write(f"Each of the chapters has an average of around {round(sum(a) / len(a))} {option}! {b[a.index(max(a))]} performed the best with around {max(a)} {option}, while {b[a.index(min(a))]} achieved only {min(a)} {option}.")

st.subheader("Stats over all parts.")
option = st.radio("Type", ['Comments', 'Reads', 'Votes'], key = 2)
temp = data[['Comments', 'Reads', 'Votes', 'Part']].drop_duplicates().groupby(by=["Part"])[option].sum().reset_index()
st.plotly_chart(px.pie(temp, names = 'Part', values = option).update_layout(width=350, height=350))
a, b = list(temp[option].index), list(temp[option].values)
st.write(f"Part {a[(b).index(max(b))]} of {story} seems to be the most popular with a total of over {max(b)} {option.lower()}.")

st.subheader("Comments over all time.")
temp = dict()
for i in data.Date:
    temp[i] = temp.get(i, 0) + 1
temp = pd.DataFrame(list(temp.items()),columns = ['Date','Comments']).sort_values(by = 'Date')
st.plotly_chart(px.line(temp, x = 'Date', y = 'Comments').update_layout(
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
    )
))
temp = temp[temp['Comments']==temp['Comments'].max()]
st.write(f"{story} reached max popularity on {temp.Date.values[0]} with {temp.Comments.values[0]} comments on a single day!")