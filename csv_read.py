import csv


def read_csv(path, filename):
    """Function to read csv files to a character array.

    Args:
        path: The path to the file to be read.
        filename: The name of the file to be read.

    Returns:
        The contents of the file in a character array format.
    """

    try:
        file = open(path + filename, "r")
        reader = csv.reader(file)
        x = []
        for r in reader:
            for s in r:
                x.append(s)
        file.close()
        return x
    except FileNotFoundError as err:
        print(err.args)
