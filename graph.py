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

	fig = plt.figure()
	p = fig.add_subplot(1,1,1)

	std_dev = np.std(marks)
	mean = np.mean(marks)
	mod = mode(marks)
	median = np.median(marks)

	h,_,_ = p.hist(marks, bins=30, histtype='bar')
	p.set_title("sub: %s std: %f mean: %f median: %f" % (subject.upper(), std_dev, mean, median), y=1.05)
	p.yaxis.set_major_formatter(FuncFormatter(lambda y, _: "{:.2f}".format((float(y*100)/np.sum(h))) + '%'))
	fig.savefig("%s.png" % (subject,))