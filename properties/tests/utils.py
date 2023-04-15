import json
import os


def get_test_resource(resource_name):
    """
    Mock calling the API by fetching dummy data from files.
    """
    data_path = os.path.join(os.path.dirname(__file__), 'data')

    if resource_name == 'properties':
        file = os.path.join(data_path, 'test_properties.json')
    else:
        return None

    with open(file) as f:
        data = json.load(f)
    return data
