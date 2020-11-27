import pandas as pd
import re
import datetime
import ftfy
import emoji
from word2number import w2n
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')

df1 = pd.DataFrame(columns = ['Chapter Name', 'Username', 'Date', 'Original', 'Text', 'Negative', 'Neutral', 'Positive', 'Compound'])
sid = SentimentIntensityAnalyzer()
months = ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

for line in open("..\Data\commentdata_qod.csv", mode='r', encoding='utf-8'):
	fields = line.split(",")
	chaptername = fields[0]
	username = fields[1]
	try:
		if fields[3].strip() in ['2020', '2019', '2018', '2017', '2016']:
			date = fields[2] + fields[3]
			comment = fields[4:]
		else:
			if 'ago' in fields[2]:
				s = fields[2]
				if s[0] == 'a':
					date = "Nov 21 2020"
				else:
					parsed_s = [s.split()[:2]]
					time_dict = dict((fmt,float(amount)) for amount,fmt in parsed_s)
					dt = datetime.timedelta(**time_dict)
					past_time = datetime.datetime.now() - dt
					past_time = str(past_time).split()[0].split('-')
					date = f"{months[int(past_time[1])]} {past_time[2]} 2020"
				comment = fields[3:]
			else:
				date = fields[2] + " 2020"
				comment = fields[3:]
	except: 
		pass
	try:
		date = date.replace('-', ' ')
		date = date.split()
		date = f"{date[2]}-{str(months.index(date[0])).zfill(2)}-{str(date[1]).zfill(2)}"
	except:
		date = f"{date[1][2:]}-{str(months.index(date[0])).zfill(2)}-{str(date[1][:2]).zfill(2)}"
	comment = " ".join(comment)
	original = comment
	comment = ftfy.fix_text(comment)
	comment = emoji.demojize(comment)
	comment = re.sub("[:,_]", " ", comment)
	if "This comment may be offensive." in comment:
		comment = comment.replace('This comment may be offensive.', '').strip()
	comment = comment.replace(",", '')
	comment = comment.replace('\n', ' ')
	sentiments = dict(sid.polarity_scores(comment))
	comment = comment.lower()
	row = pd.Series(list([chaptername, username, date, original, comment, sentiments['neg'], sentiments['neu'], sentiments['pos'], sentiments['compound']]), index = df1.columns)
	df1 = df1.append(row, ignore_index = True)   

df2 = pd.DataFrame(columns = ['Comments', 'Scraped Comments', 'Reads', 'Votes', 'Chapter Name', 'Chapter', 'Part'])

def K_to_int(s):
	if 'K' in s:
		return int(float(s.replace('K', '')) * 1000)
	else: 
		return int(s)

for line in open("..\Data\chapterdata_qod.csv", mode='r'):
	fields = line.strip().split(',')
	total_comments = K_to_int(fields[0])
	scraped_comments = K_to_int(fields[1])
	total_reads = K_to_int(fields[2])
	total_votes = K_to_int(fields[3])
	chapter_name = fields[4]
	if fields[4] not in ['QUEEN OF DEATH', 'PRELUDE', 'PROLOGUE', 'EPILOGUE', 'POSTLUDE', 'FINAL NOTE']:
		if 'PART' in fields[4]:
			part = w2n.word_to_num(fields[4].replace('PART',''))
			chapter = fields[4]
		else:
			chapter = w2n.word_to_num(fields[4])
			if chapter in [1, 14]:
				part = 1
			if chapter in [15, 40]:
				part = 2
			if chapter in [41, 52]:
				part = 3
	else:
		chapter = fields[4]
		part = 'NA'
	row = pd.Series(list([total_comments, scraped_comments, total_reads, total_votes, chapter_name, chapter, part]), index=df2.columns)
	df2 = df2.append(row, ignore_index=True)  

qod = df2.merge(df1, on='Chapter Name').to_csv("..\Data\qod.csv")