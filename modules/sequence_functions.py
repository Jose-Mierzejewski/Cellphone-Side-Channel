import numpy as np
from scipy import signal
import csv
import os
import pylab

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

def generate_data_from_parent_folder(path_to_parent_folder):
    """
    Returns a numpy array of requested data, as well as an array of labels for each data point.
    :param buttons_pressed: the buttons that were pressed, corresponding to the folders that will be read.
    :param path_to_parent_folder: path to the parent folder of the folders that will be read.
    """
    X = []
    y = []

    for filename in os.listdir(path_to_parent_folder):
      full_path = os.path.join(path_to_parent_folder, filename)

      if os.path.isdir(full_path):
        button_pressed = filename
      
        data = _load_data_from_folder(full_path)
        X = X + data
        y = y + [button_pressed] * len(data)

    X = np.array(X, dtype='float')
    y = np.array(y)

    return X, y

def thresholding_algo(y, lag, threshold, influence):
    """
    This code is modified from https://stackoverflow.com/questions/22583391/peak-signal-detection-in-realtime-timeseries-data/56451135#56451135
    """
    signals = np.zeros(len(y))
    filteredY = np.array(y)
    avgFilter = [0]*len(y)
    stdFilter = [0]*len(y)
    avgFilter[lag - 1] = np.mean(y[0:lag])
    stdFilter[lag - 1] = np.std(y[0:lag])
    for i in range(lag, len(y)):
        # Absolute value removed from the next line, because I only want positive peaks, not negative peaks.
        # Original line included abs(y[i] - avgFilter[i-1])
        # I have not explored how these "negative peaks" could impact the filteredY mean or std by not passing through the influence parameters
        if y[i] - avgFilter[i-1] > threshold * stdFilter [i-1]:
            if y[i] > avgFilter[i-1]:
                signals[i] = 1
            else:
                signals[i] = -1

            filteredY[i] = influence * y[i] + (1 - influence) * filteredY[i-1]
            avgFilter[i] = np.mean(filteredY[(i-lag+1):i+1])
            stdFilter[i] = np.std(filteredY[(i-lag+1):i+1])
        else:
            signals[i] = 0
            filteredY[i] = y[i]
            avgFilter[i] = np.mean(filteredY[(i-lag+1):i+1])
            stdFilter[i] = np.std(filteredY[(i-lag+1):i+1])

    return dict(signals = np.asarray(signals),
                avgFilter = np.asarray(avgFilter),
                stdFilter = np.asarray(stdFilter))
