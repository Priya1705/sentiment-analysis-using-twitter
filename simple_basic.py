import numpy as np
import pandas as pd
from textblob import TextBlob

a="apples are fruits"
obj = TextBlob(a)
sentiment = obj.sentiment.polarity
print(sentiment)

if sentiment == 0:
	print("the text is neutral")
elif sentiment > 0:
	print("the text is positive")
else:
	print("the text is negative")