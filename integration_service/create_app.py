import datetime
import json

import cx_Oracle
from flask import Flask, jsonify, request

from integration_service.src.model_adviser_integration_service import ModelAdviserIntegrationService
from integration_service.src.ssp_data_service import SSPDataService

#host = "s001itd-0040"
host = "172.21.9.120"
port = 1521
sid = "ssp"
user = "ssp"
password = "ssp"


def create_app():
    app = Flask(__name__)

    @app.route('/')
    def hello():
        return jsonify(version="SSP Integration Service Version={}".format(datetime.datetime.now())), 200

    @app.route('/proxy/forecast_data', methods=['GET'])
    def get_forecast_data():
        forecast_data_json = ModelAdviserIntegrationService.get_forecast_data_from_file('/var/www/integration_service/data.txt')
        return jsonify(forecast_data_json), 200

    @app.route('/api/forecast_data', methods=['POST'])
    def post_forecast_data():
        source = request.args.get('source')
        if source == 'json':
            forecast_data_json = json.loads(request.args.get('data'))
        elif source == 'http':
            url = request.args.get('url')
            forecast_data_json = ModelAdviserIntegrationService.get_forecast_data_from_http(url)
        else:
            return jsonify('No handler found for the request argument:[{}]'.format(source)), 400

        integrate_forecast_data(forecast_data_json)

        return jsonify({
            "source": source,
            "url": url,
            "count": len(forecast_data_json)
        }), 201

    def integrate_forecast_data(forecast_data_json):
        if not cx_Oracle.connect:
            cx_Oracle.init_oracle_client(lib_dir="/lib/oracle/19.14/client64/lib")
        db = SSPDataService(host, port, sid, user, password)
        db.integrate_forecast_data(forecast_data_json)

    return app