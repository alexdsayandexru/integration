import datetime
from abc import ABC

import cx_Oracle
from sqlalchemy import MetaData, Table, Column, Integer, String, insert, Float
from sqlalchemy import create_engine, Date


class SSPDataService:
    def __init__(self, host, port, sid, user, password):
        self.host = host
        self.port = port
        self.sid = sid
        self.user = user
        self.password = password

    def integrate_forecast_data(self, forecast_data_json):
        self.__clear_forecast_data('clear_bcg_model')
        self.__insert_forecast_data(forecast_data_json)
        self.__accept_forecast_data('map_bcg_model')

    def __clear_forecast_data(self, store_procedure_name):
        query = CallStoreProcedureQuery(self.host, self.port, self.sid, self.user, self.password, store_procedure_name)
        query.execute()

    def __insert_forecast_data(self, forecast_data_json):
        query = InsertForecastDataQuery(self.host, self.port, self.sid, self.user, self.password, forecast_data_json)
        query.execute()

    def __accept_forecast_data(self, store_procedure_name):
        query = CallStoreProcedureQuery(self.host, self.port, self.sid, self.user, self.password, store_procedure_name)
        query.execute()


class BasicQuery(ABC):
    def __init__(self, host, port, sid, user, password):
        sid = cx_Oracle.makedsn(host, port, sid=sid)
        connection_string = 'oracle://{user}:{password}@{sid}'.format(user=user, password=password, sid=sid)
        self.engine = create_engine(connection_string)

    def execute(self):
        pass


class CallStoreProcedureQuery(BasicQuery):
    def __init__(self, host, port, sid, user, password, proc_name):
        self.proc_name = proc_name
        super(CallStoreProcedureQuery, self).__init__(host, port, sid, user, password)

    def execute(self):
        connection = self.engine.connect()
        cursor = connection.connection.cursor()
        try:
            cursor.callproc(self.proc_name)
        finally:
            cursor.close()
            connection.close()


class InsertForecastDataQuery(BasicQuery):
    def __init__(self, host, port, sid, user, password, forecast_data_json):
        super(InsertForecastDataQuery, self).__init__(host, port, sid, user, password)
        self.forecast_data_json = forecast_data_json

    def execute(self):
        connection = self.engine.connect()
        table = self.get_bcg_model_table()
        connection.execute(insert(table), self.forecast_data_json)
        connection.close()

    @staticmethod
    def get_bcg_model_table():
        return Table('bcg_model', MetaData(),
                     Column('ID', Integer(), primary_key=True),
                     Column('PERIOD', String(200), nullable=True),
                     Column('PRODUCT_NAME', String(200), nullable=True),
                     Column('BRAND_CODE_ASV', String(200), nullable=True),
                     Column('BRAND_NAME_ASV', String(200), nullable=True),
                     Column('BRAND_CODE_DPO', String(200), nullable=True),
                     Column('BRAND_NAME_DPO', String(200), nullable=True),
                     Column('MANAGER_NAME', String(200), nullable=True),
                     Column('CUSTOMER_NAME', String(200), nullable=True),
                     Column('CUSTOMER_CODE_ASV', String(200), nullable=True),
                     Column('CUSTOMER_NAME_ASV', String(200), nullable=True),
                     Column('CUSTOMER_CODE_DPO', String(200), nullable=True),
                     Column('CUSTOMER_NAME_DPO', String(200), nullable=True),
                     Column('CONTRACT_NAME', String(200), nullable=True),
                     Column('DEPARTMENT_NAME', String(200), nullable=True),
                     Column('REGION_CODE', String(200), nullable=True),
                     Column('REGION_NAME', String(200), nullable=True),
                     Column('REGION_FACT', String(200), nullable=True),
                     Column('MODEL', String(200), nullable=True),
                     Column('MODEL_FLAG', String(200), nullable=True),
                     Column('COUNTRY_ISO3', String(200), nullable=True),
                     Column('BCG_FORECAST_MIN', Float(), nullable=True),
                     Column('BCG_FORECAST_MAX', Float(), nullable=True),
                     Column('BCG_FORECAST', Float(), nullable=True),
                     Column('COUNTRY', String(200), nullable=True),
                     Column('CREATED_AT', Date, onupdate=datetime.datetime.now().date, nullable=True)
                     )