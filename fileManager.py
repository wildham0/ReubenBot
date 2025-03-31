import json

def read_config_file():
    return read_file("configs")

def read_weekly_file():
    return read_file("weekly")

def read_results_file():
    return read_file("weeklyresults")

def write_results_file(results_data):
    write_file("weeklyresults", results_data)

def write_weekly_file(weekly_data):
    write_file("weekly", weekly_data)

def read_file(filename):
    try:
        file = open(filename + ".json", "r")
    except FileNotFoundError:
        file = None

    if file is not None:
        file_data = file.read()
        if len(file_data) > 0:
            json_data = json.loads(file_data)
            file.close()
        else:
            print("No " + filename + " data to load.")
            file.close()
            return None
        print(filename + " data loaded.")
        return json_data
    else:
        print("No " + filename + " file.")
        return None
def write_file(filename, json_data):
    try:
        file = open(filename + ".json", "w")
    except FileNotFoundError:
        print("Results file not found.")
        return

    file_data = json.dumps(json_data)
    file.write(file_data)
    file.close()

