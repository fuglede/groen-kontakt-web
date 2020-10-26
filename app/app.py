from flask import Flask, request

from .cache import get_forecast, get_current_generation_mix, get_model
from .model import best_period, overview_next_day
from . import push


app = Flask(__name__,
            static_url_path='',
            static_folder='static')


@app.route('/')
def root():
    return app.send_static_file('index.html')


@app.route('/api/v1/current-emission-intensity')
def current_emission_intensity():
    model = get_model()
    return model


@app.route('/api/v1/current-generation-mix')
def current_generation_mix():
    return get_current_generation_mix()


@app.route('/api/v1/greenest-period/<period>/<horizon>', methods=['GET'])
def greenest_period(period, horizon):
    try:
        period = int(period)
        horizon = int(horizon)
    except ValueError:
        return {'success': False, 'error': 'Given period or horizon was non-integral.'}
    if period < 0 or period > 6:
        return {'success': False, 'error': 'Period must be between 1 and 6.'}
    if horizon < 6 or horizon > 72:
        return {'success': False, 'error': 'Horizon must be between 1 and 72.'}
    forecast = get_forecast()
    return best_period(forecast, period, horizon)


@app.route('/api/v1/next-day')
def next_day():
    forecast = get_forecast()
    return overview_next_day(forecast)


@app.route('/api/v1/next-day-short')
def next_day_short():
    forecast = get_forecast()
    return overview_next_day(forecast, True)


@app.route('/api/v1/save-subscription', methods=['POST'])
def save_subscription():
    try:
        push.save_subscription(request.data.decode('ascii'))
        return {'success': True}
    except Exception as e:
        print(e)
        return {'success': False}


@app.route('/api/v1/remove-subscription', methods=['POST'])
def remove_subscription():
    try:
        push.remove_subscription(request.data.decode('ascii'))
        return {'success': True}
    except Exception as e:
        print(e)
        return {'success': False}
