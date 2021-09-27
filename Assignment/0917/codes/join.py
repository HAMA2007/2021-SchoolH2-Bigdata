import MapReduce
import sys

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line
import copy

def mapper(record):
    # print('MAPPER: ', record)
    mr.emit_intermediate(record[1], record)
    # TODO: implement this class

def reducer(key, list_of_values):
    # print('REDUCER: ', key, list_of_values)
    for data_idx in range (1, len(list_of_values)):
        data = copy.deepcopy(list_of_values[0])
        data.extend(list_of_values[data_idx])
        mr.emit(data)
    # TODO: implement this class

# Do not modify below this line
# =============================
if __name__ == '__main__':
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)
