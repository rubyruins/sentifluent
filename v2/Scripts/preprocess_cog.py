import pandas as pd
import re
import datetime
import ftfy
import emoji
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')

df1 = pd.DataFrame(columns = ['Chapter Name', 'Username', 'Date', 'Original', 'Text', 'Negative', 'Neutral', 'Positive', 'Compound'])
sid = SentimentIntensityAnalyzer()
months = ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

for line in open("..\Data\commentdata_cog.csv", mode='r', encoding='utf-8'):
	fields = line.split(",")
	chaptername = fields[0]
	if 'SCENE' in fields[1]:
		chaptername = fields[0] + fields[1]
		fields.pop(1)
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
	print(line)
	sentiments = dict(sid.polarity_scores(comment))
	comment = comment.lower()
	row = pd.Series(list([chaptername, username, date, original, comment, sentiments['neg'], sentiments['neu'], sentiments['pos'], sentiments['compound']]), index=df1.columns)
	df1 = df1.append(row, ignore_index=True)   

df2 = pd.DataFrame(columns = ['Comments', 'Scraped Comments', 'Reads', 'Votes', 'Chapter Name', 'Chapter', 'Part'])

def K_to_int(s):
	if 'K' in s:
		return int(float(s.replace('K', '')) * 1000)
	else: 
		return int(s)

def roman_to_int(s):
	if 'V' not in s:
		return s.count('I')
	else:
		if s == 'IV':
			return 4
		else:
			return (5 * s.count('V')) + (1 * s.count('I'))

for line in open("..\Data\chapterdata_cog.csv", mode='r'):
	fields = line.strip().split(',')
	total_comments = K_to_int(fields[0])
	scraped_comments = K_to_int(fields[1])
	total_reads = K_to_int(fields[2])
	total_votes = K_to_int(fields[3])
	if 'SCENE' in fields[5]:
		chapter_name = fields[4] + fields[5]
		chapter = fields[4].split('|')[0].strip()
		part = fields[4].split('|')[1].split()[1]
		part = roman_to_int(part)
	else:
		chapter_name = fields[4]
		chapter = fields[4]
		if 'ACT ' in fields[4]:
			part = fields[4].split('|')[0].split()[1]
			part = roman_to_int(part)
		else:
			part = 'NA'
	row = pd.Series(list([total_comments, scraped_comments, total_reads, total_votes, chapter_name, chapter, part]), index=df2.columns)
	df2 = df2.append(row, ignore_index=True) 

cog = df2.merge(df1, on='Chapter Name').to_csv("..\Data\cog.csv")