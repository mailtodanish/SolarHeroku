from flask import render_template, flash, redirect, url_for, send_file, request
from app import app
from app.forms import SimForm
from app.api_calls import *
import time

@app.route('/')
@app.route('/dashboard', methods=['GET', 'POST'])
def form():
	form = SimForm()
	if form.validate_on_submit():
		# date_ = form.date.data
		# location_ = form.location.data
		# time_span_ = form.time_span.data
		flash(f'Building graph for {form.time_span.data} days...') #success, add css
		return redirect(url_for('about'))
	return render_template('form.html', title='Check Yo Place!', form=form)

@app.route('/about', methods=['GET', 'POST'])
def about():
	return render_template('about.html', title='About')

@app.route('/results', methods=['GET', 'POST'])
def handle_data():
	projectpath = request.form
	output, sunrise, sunset = loop_data_collect(int(request.form['time_span']), request.form['location'], request.form['date'])
	day_dict = process(output, int(request.form['time_span'], sunrise, sunset)
	return render_template('results.html', title=' sunny day(s)')


# @app.route('/images/<plot>')
# def images(plot):
#     return render_template("images.html", title=plot)

# @app.route('/fig/<plot>')
# def fig(plot):
#     images_dict = plot(day_dict, projectpath.time_span.data)
#     img = StringIO()
#     fig.savefig(img)
#     img.seek(0)
#     return send_file(img, mimetype='image/png')
# showing a matplotlib image
# import io
# import random
# from flask import Response
# from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
# from matplotlib.figure import Figure

# @app.route('/plot.png')
# def plot_png():
#     fig = create_figure()
#     output = io.BytesIO()
#     FigureCanvas(fig).print_png(output)
#     return Response(output.getvalue(), mimetype='image/png')

# def create_figure():
#     fig = Figure()
#     axis = fig.add_subplot(1, 1, 1)
#     xs = range(100)
#     ys = [random.randint(1, 50) for x in xs]
#     axis.plot(xs, ys)
#     return fig


# plot 
# <img src="/plot.png" alt="my plot">