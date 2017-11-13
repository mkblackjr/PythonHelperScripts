import numpy as np
import glob

data_identifiers = {
        
        'NUM_COLS':           12,
        'DATA_MULT_FACTOR':   13,
        'DATA_FORMAT':        14,
        'DATA_EXPL_START':    15,
        'DATA_EXPL_STOP':     23,
        'NUM_TIMING_COLS':    24,
        'TIMING_MULT_FACTOR': 25,
        'TIME_FORMAT':        26,
        'TIME_EXPL_START':    27,
        'TIME_EXPL_STOP':     39,
        'FIRST_HEADER':       41
        
        }

'''

How to access the data:
    The data from each file is stored in the all_data list in the form of a 
    list of dictionaries. The data contained in each dictionary may be accessed
    by invoking the name of the column as specified in the .txt file 
    (e.g. all_data[0][3]['Ozone Number Density (molecules / m**3)'], where the 
    first index corresponds to the file, in order listed, the second index
    corresponds to the test number within that file, and the identifier refers
    to the specific field withing that test within that file).
    
Dictionary:
    In addition to all of the data collected during the test, each
    part of which is stored under its title as specified in the .txt
    file, each dictionary entry contains the name of the file, the date, start
    time, end time, altitude, latitude, and longitude of the test (all named 
    accordingly e.g. all_data[0][2]['date'])
    
If you need to access the data in list/array format, you can call data fields
in the following way:
    
    Suppose you are looking for a field called "Time" in the first test of the 
    first file:
        
    time = all_data[0][0]['Time']
 
I have included two lines (69, 128) that would allow you to run this as a
function. Uncomment these lines to implement this behavior.
    
'''

def obtain_contents(filename):
    import csv

    with open(filename, newline='') as inputfile:
        r1 = list(filter(lambda a: a != '',csv.reader(inputfile,delimiter=' ')))
        results = [[x for x in y if x != ''] for y in r1]
        for j in range(len(results)):
            for i,x in enumerate(results[j]):
                try:
                    results[j][i] = float(x)
                    if len(results[j]) == 1:
                        results[j] = results[j][0]
                except ValueError:
                    pass
    return results


if __name__ == "__main__":
    
#def get_data(input_path):
    
    # SPECIFY THE FOLDER IN WHICH THE FILE RESIDES
    input_path = "/Users/mac/Documents/PythonScripts/*.txt"
    files = glob.glob('{}'.format(input_path),recursive=True)
    
    all_data = []
    
    for file in files:
        results = obtain_contents(file)
        
        num_cols_data = int(results[data_identifiers['NUM_COLS']-1]+1)
        mult_data = results[data_identifiers['DATA_MULT_FACTOR']-1]
        mult_data.insert(0,0)
        format_data = results[data_identifiers['DATA_FORMAT']-1]
        labels_data = [' '.join(x) for x in 
                      results[data_identifiers['DATA_EXPL_START']-1:
                      data_identifiers['DATA_EXPL_STOP']]]
            
        num_cols_timestamp = results[data_identifiers['NUM_TIMING_COLS']-1]
        mult_timestamp = results[data_identifiers['TIMING_MULT_FACTOR']-1]
        mult_timestamp.insert(0,0)
        format_time = results[data_identifiers['TIME_FORMAT']-1]
        labels_timestamp = [' '.join(x) for x in 
                      results[data_identifiers['TIME_EXPL_START']-1:
                      data_identifiers['TIME_EXPL_STOP']]]
        
        i = data_identifiers['FIRST_HEADER']
        temp_data = [{'filename':file}]
        while (i < len(results)):        
            num_entries = int(np.multiply(results[i][1],mult_timestamp[1]))
            date = int(str(int(np.multiply(results[i][2],mult_timestamp[2])))+
                   str("{0:0=2d}".format(int(np.multiply(results[i][3],mult_timestamp[3]))))+
                   str("{0:0=2d}".format(int(np.multiply(results[i][4],mult_timestamp[4])))))
            start = ':'.join([str(int(np.multiply(results[i][5],mult_timestamp[5]))),
                    str("{0:0=2d}".format(int(np.multiply(results[i][6],mult_timestamp[6]))))])
            end = ':'.join([str(int(results[i][7]*mult_timestamp[7])),
                  str("{0:0=2d}".format(int(results[i][8]*mult_timestamp[8])))])
            latitude = float(np.multiply(results[i][10],mult_timestamp[10]))
            longitude = float(np.multiply(results[i][11],mult_timestamp[11]))
            altitude = float(np.multiply(results[i][12],mult_timestamp[12]))
            dataset = np.zeros((num_entries,num_cols_data))
            i += 1
            for j in range(num_entries):
                dataset[j,:] = np.multiply(results[i],mult_data)
                i += 1
            new_set = np.matrix(dataset)
            new_entry = {'date':date,'start_time':start,'end_time':end, 'latitude':
                         latitude,'longitude':longitude,'altitude':altitude}
            for k in range(num_cols_data-1):
                a = new_set[:,k+1].tolist()
                a = [x[0] for x in a]
                new_entry.update({labels_data[k]:a})
            
            # # This is where the relevant data is stored # #
            temp_data.append(new_entry)
        
        all_data.append(temp_data)
        
#    return all_data
    
    
    