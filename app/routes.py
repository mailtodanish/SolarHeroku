from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import SimForm

# posts = [
#     {
#         'author': 'Corey Schafer',
#         'title': 'Blog Post 1',
#         'content': 'First post content',
#         'date_posted': 'April 20, 2018'
#     },
#     {
#         'author': 'Jane Doe',
#         'title': 'Blog Post 2',
#         'content': 'Second post content',
#         'date_posted': 'April 21, 2018'
#     }
# ]

@app.route('/')
@app.route('/dashboard', methods=['GET', 'POST'])
def form():
	form = SimForm()
	if form.validate_on_submit():
		flash(f'Building graph for {form.time_span.data} days...') #success, add css
		return redirect(url_for('results'))
	return render_template('form.html', title='Check Yo Place!', form=form)


@app.route('/about')
def about():
	return render_template('about.html', title='About')

@app.route('/results')
def results():
	# returned = ReturnResults()
	# if statement
	return render_template('results.html', title=f'{form.time_span.data} sunny day(s)')

# API path route data rendered inside this route then call this route when running API 
# hidden folders start with a . and can be used to store api keys
# possibly a route to stored csv file from web scrape



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


# send files from a dir

# from flask import send_from_directory
# @app.route('/js/<path:path>')
# def send_js(path):
#     return send_from_directory('js', path)