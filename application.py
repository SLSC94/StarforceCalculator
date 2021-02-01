from flask import Flask, redirect, url_for, render_template, request
import numpy as np
from StarforceCalculator import StarforceCalculator

application = Flask(__name__)
app = application

@app.route("/", methods = ["POST", "GET"])
def home():

	increase = np.minimum(np.array([100 - i*5 for i in range(20)]+ [1]*10) , 100)
	decrease = np.array([0]*10 + [10,10,15,15,20,20,25,25,30,30]+ [40]*5 + [45]*5)
	destroy = np.array([0]*10 + [5]*10 + [10]*5 + [15]*5)
	same = 100 - increase - decrease - destroy
	scroll = ['s'+str(i) for i in range(30)]
	ward = ['w'+str(i) for i in range(30)]
	lucky = ['l'+str(i) for i in range(30)]
	click = ['c'+str(i) for i in range(30)]

	if request.method == 'POST':
		calc = True
		response_lucky = []
		response_click = []
		response_ward = []
		response_scroll = []
		for i in range(0,30):
			response_lucky.append(request.form.get('l'+str(i)) != None)
			response_click.append(request.form.get('c'+str(i)) != None)
			response_ward.append(request.form.get('w'+str(i)) != None)
			response_scroll.append(request.form.get('s'+str(i)) != None)


		allscroll = request.form.get('allscroll') != None
		allward = request.form.get('allward') != None
		alllucky = request.form.get('alllucky') != None
		allclick = request.form.get('allclick') != None
		# try:
		Startforce = int(request.form.get('Startforce'))
		Endforce = int(request.form.get('Endforce'))
		# except:
		# 	Startforce = int(request.form.get('Startforce2'))
		# 	Endforce = int(request.form.get('Endforce2'))

		# the following is just a hack.
		response_click = response_click[:21] + [True]*9
		# for i in range(10,30):
		# 	response_ward.append(request.form.get('w'+str(i)) != None)
		# 	response_scroll.append(request.form.get('s'+str(i)) != None)
		# # insert code here ###########################################
		SFC = StarforceCalculator(start = Startforce, end = Endforce,
									ward = response_ward,
									scroll = response_scroll,
									lucky = response_lucky,
									click = response_click)
		SFC.create_table()
		SFC.transient()
		SFC.get_counts()
		SFC.get_state_counts()

		NV = list(SFC.table['Num Visits'])
		blanks = sum([abs(nv) < 1e-5 for nv in NV])



		n_visits = [' ']*(min(Startforce, 9)+blanks) + list(SFC.table['Num Visits'])[blanks:]
		n_destroyed = [' ']*(min(Startforce, 9)+blanks) + list(SFC.table['Num Destroyed'])[blanks:]
		totalcost = [' ']*(min(Startforce, 9)+blanks) + list(SFC.table['Total Cost(M)'])[blanks:]
		finalcost = round(sum(list(SFC.table['Total Cost(M)'])),2)
		finalvisits = round(sum(list(SFC.table['Num Visits'])[blanks:]),2)
		finaldestroys = round(sum(list(SFC.table['Num Destroyed'])[blanks:]),2)
		################################################################


		# n_visits = [0]*30
		# n_destroyed = [0]*30
		# totalcost = [0]*30
		print(response_ward)
		return render_template("index.html",
							   increase = list(np.round(increase,2)),
							   decrease = list(np.round(decrease,2)),
							   destroy = list(np.round(destroy,2)),
							   same = list(np.round(same,2)),
							   scroll = scroll,
							   ward = ward,
							   lucky = lucky,
							   click = click,
							   response_scroll = response_scroll,
							   response_ward = response_ward,
							   response_lucky = response_lucky,
							   response_click = response_click,
							   calc = calc,
							   n_visits = n_visits,
							   n_destroyed = n_destroyed,
							   totalcost = totalcost,
							   Startforce = Startforce,
							   Endforce = Endforce,
							   allscroll = allscroll,
							   allward = allward,
							   alllucky = alllucky,
							   allclick = allclick,
							   finalvisits = finalvisits,
							   finaldestroys = finaldestroys,
							   finalcost = finalcost)
	else:
		calc = False
		return render_template("index.html",
							   increase = list(np.round(increase,2)),
							   decrease = list(np.round(decrease,2)),
							   destroy = list(np.round(destroy,2)),
							   same = list(np.round(same,2)),
							   scroll = scroll,
							   ward = ward,
							   lucky = lucky,
							   click = click,
							   calc = calc)



if __name__ == '__main__':
	app.run(debug = True)