from flask import Flask, send_from_directory
from config import Config
from flask_bootstrap import Bootstrap
import os

app = Flask(__name__, instance_path = 'C://Users//Mark//Documents//DataSci//Module 5//FLASK//flask_dashboard//solar_dashboard//app//protected')
app.config.from_object(Config)
bootstrap = Bootstrap(app)



from app import routes, errors

# ...

from logging.handlers import RotatingFileHandler

# ...

if not app.debug:
    # ...

    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/solsim.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.WARNING)
    app.logger.info('Sol Sim startup')


# protected files
# def special_requirement(f):
#     @wraps(f)
#     def wrap(*args, **kwargs):
#         try:
#             if 'Ehler' == session['username']:
#                 return f(*args, **kwargs)
#             else:
#                 flash('Don\'t forget the magic word.')
#                 return redirect(url_for('home'))
#         except:
#             return redirect(url_for('home'))
#     return wrap



# @app.route('/protected/<path:filename>')
# @special_requirement
# def protected(filename):
#     try:
#         return send_from_directory(os.path.join(app.instance_path,''), filename)

#     except Exception as e:
#             return redirect(url_for('home'))