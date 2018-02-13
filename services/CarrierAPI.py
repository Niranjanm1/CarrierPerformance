from flask_restplus import Resource
import pandas as pd
from services import App
from services import settings
from services import GeneralFunctions

with open(GeneralFunctions.get_json_file(), "r") as f:
    data = pd.read_json(f)

carrierAPI,CarrierApp = App()
ns = carrierAPI.namespace('Rating', description='Carrier Rating')

@ns.route('/carrier/<input>')
class CarrierRating(Resource):

    def get(self,input):
        plan_val = settings.PLANNING + input.upper()
        exec_val = settings.EXECUTION + input.upper()
        settings.PLANINPUTVALUE = plan_val
        settings.EXECINPUTVALUE = exec_val
        settings.INPUT = input

        if data[plan_val].dtype == object:
            if "AM" in data.iloc[0][plan_val] or "PM" in data.iloc[0][plan_val]:
                data[settings.DIFF] = (pd.to_datetime(data[exec_val]) - pd.to_datetime(data[plan_val])).dt.total_seconds()
        else:
            data[settings.DIFF] = data[exec_val] - data[plan_val]

        data_srt = data.sort_values(by=settings.PLANLOAD)
        loads = data_srt.groupby(settings.PLANLOAD)

        sorted_loads = GeneralFunctions.get_sorted_dict_from_data(loads)
        rankings = GeneralFunctions.create_json_object_from_dict(sorted_loads)

        return {'CarrierRatingRanking': rankings}

@ns.route('/carrier/<load_id>/<input>')
class CarrierRatingByLoadID(Resource):

    def get(self,load_id,input):
        plan_val = settings.PLANNING + input.upper()
        exec_val = settings.EXECUTION + input.upper()
        settings.PLANINPUTVALUE = plan_val
        settings.EXECINPUTVALUE = exec_val
        settings.INPUT = input
        settings.LOADID = str(load_id).upper()

        if data[plan_val].dtype == object:
            if "AM" in data.iloc[0][plan_val] or "PM" in data.iloc[0][plan_val]:
                data[settings.DIFF] = (pd.to_datetime(data[exec_val]) - pd.to_datetime(data[plan_val])).dt.total_seconds()
        else:
            data[settings.DIFF] = data[exec_val] - data[plan_val]

        specific_load = data[data[settings.PLANLOAD]==settings.LOADID]

        sorted_loads = GeneralFunctions.get_sorted_dict_from_specific_load_data(specific_load)
        rankings = GeneralFunctions.create_json_object_from_dict(sorted_loads)

        return {'CarrierRatingRanking': rankings}

if __name__ == '__main__':
    CarrierApp.run(debug=True)
