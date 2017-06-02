import pymongo
import matplotlib.pyplot as plt
from constants import *
import numpy as np 
from matplotlib.ticker import FuncFormatter
from scipy.stats import mode

conn = pymongo.MongoClient(DB_URL)
db = conn[DB]
plt.style.use('ggplot')

subjects = db.collection_names(True)

for subject in subjects:
	marks = [x["marks"] for x in db[subject].find()]
	
	marks_t = sorted(list(set(marks)))
	y = len(marks)
	cum = [len(marks_t) - x for x in xrange(1, len(marks_t) + 1)]
	cum = map(lambda x: 1 - float(x)/y, cum)
	
	fig = plt.figure()
	p = fig.add_subplot(1,1,1)
	p.set_title(subject.upper())
	plt.plot(marks_t, cum)
	plt.savefig("%s_cum.png" % (subject,))