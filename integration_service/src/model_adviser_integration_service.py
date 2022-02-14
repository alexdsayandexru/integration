import requests


def string_to_float(s_value):
    if s_value is None:
        return None
    return float(s_value.replace(',', '.'))


def create_json_obj(cells):
    obj = {
                "PERIOD": cells[1],
                "PRODUCT_NAME": cells[2],
                "BRAND_NAME": cells[3],
                "BRAND_CODE_ASV": cells[15],
                "BRAND_NAME_ASV": cells[16],
                "BRAND_CODE_DPO": cells[17],
                "BRAND_NAME_DPO": cells[18],
                "MANAGER_NAME": cells[4],
                "CUSTOMER_NAME": cells[5],
                "CUSTOMER_CODE_ASV": cells[19],
                "CUSTOMER_NAME_ASV": cells[20],
                "CUSTOMER_CODE_DPO": cells[21],
                "CUSTOMER_NAME_DPO": cells[22],
                "CONTRACT_NAME": cells[6],
                "DEPARTMENT_NAME": cells[7],
                "REGION_CODE": cells[23],
                "REGION_NAME": cells[9],
                "REGION_FACT": cells[10],
                "MODEL": cells[25],
                "MODEL_FLAG": cells[26],
                "BCG_FORECAST_MIN": string_to_float(cells[11]),
                "BCG_FORECAST_MAX": string_to_float(cells[12]),
                "BCG_FORECAST": string_to_float(cells[13]),
                "COUNTRY": cells[8],
                "COUNTRY_ISO3": cells[27].replace('\n', '')
            }
    return obj


class ModelAdviserIntegrationService:
    @staticmethod
    def get_forecast_data_from_file(file_name):
        i = 0
        results = []
        with open(file_name, encoding='utf-16') as f:
            for line in f:
                if i == 0:
                    i += 1
                    continue

                obj = create_json_obj(line.split('\t'))
                results.append(obj)
                i += 1
                if i > 200000:
                    return results

        return results

    @staticmethod
    def get_forecast_data_from_http(url):
        response = requests.get(url, proxies={'http': None, 'https': None})
        return response.json()
