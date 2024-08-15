def read_csv(file_path, csv_has_metadata=True):
    """reads through an individual csv file and returns a list of the voltages
    Author: Forrest Dudley
    :param file_path: path to the csv file
    :param csv_has_metadata: this flag will trigger the first 22 rows of the csv to be skipped
    :return: list of voltages
    """

    result = []

    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)

        if csv_has_metadata:
            # Skip first 22 rows
            for _ in range(22):
                next(csv_reader)

        for row in csv_reader:
            result.append(round(float(row[2]), 8))

    return result

# Jose
def _load_data_from_folder(path):
    """
    Returns a list containing voltage data from all csv files in a folder.
    """
    data = []
    for filename in os.listdir(path):
        if filename.endswith('.csv'):
            data.append(read_csv(path + '/' + filename))

    return data

def generate_data_from_parent_folder(path_to_parent_folder, buttons_pressed:'list'):
    """
    Returns a numpy array of requested data, as well as an array of labels for each data point.
    :param buttons_pressed: the buttons that were pressed, corresponding to the folders that will be read.
    :param path_to_parent_folder: path to the parent folder of the folders that will be read.
    """
    X = []
    y = []

    for button_pressed in buttons_pressed:
        data = _load_data_from_folder(path_to_parent_folder + '/' + str(button_pressed))
        X = X + data
        y = y + [button_pressed] * len(data)

    X = np.array(X, dtype='float')
    y = np.array(y)

    return X, y
