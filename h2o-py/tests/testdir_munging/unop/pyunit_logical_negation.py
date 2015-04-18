import sys
sys.path.insert(1, "../../../")
import h2o
import numpy as np
import random

def logical_negation(ip,port):
    # Connect to h2o
    h2o.init(ip,port)

    h2o_data = h2o.import_frame(path=h2o.locate("smalldata/logreg/prostate.csv"))
    rows, cols = h2o_data.dim()
    np_data = np.loadtxt(h2o.locate("smalldata/logreg/prostate.csv"), delimiter=',', skiprows=1)

    # frame type input
    new_h2o_data = h2o.logical_negation(h2o_data)
    new_np_data = np.logical_not(np_data)

    #   dimension check
    new_rows, new_cols = new_h2o_data.dim()
    assert new_rows == rows and new_cols == cols, \
        "failed dim check! new_rows:{0} rows:{1} new_cols:{2} cols:{3}".format(new_rows, rows, new_cols, cols)

    #   value check
    for i in range(10):
        r = random.randint(0,rows-1)
        c = random.randint(0,cols-1)
        h2o_val = h2o.as_list(new_h2o_data[r,c])[0][0]
        num_val = new_np_data[r,c]
        assert h2o_val == num_val, "failed value check! h2o computed {0} and numpy computed {1}".format(h2o_val,num_val)

    #   side effect check
    #63,0,76,1,2,1,9.5,14.4,7
    #80,1,66,1,1,1,25.7,39.1,9
    now1 = h2o.as_list(h2o_data[62,2])[0][0]
    now2 = h2o.as_list(h2o_data[79,6])[0][0]
    assert now1 == 76, "failed side effect check! original:76 and now:{0}".format(now1)
    assert now2 == 25.7, "failed side effect check! original:25.7 and now:{0}".format(now2)

    # vec type input
    new_h2o_data = h2o.logical_negation(h2o_data["CAPSULE"])
    new_np_data = np.logical_not(np_data[:,1])

    #   dimension check
    new_rows = len(new_h2o_data)
    assert new_rows == rows, "failed dim check! new_rows:{0} rows:{1}".format(new_rows, rows)

    #   value check
    for i in range(10):
        r = random.randint(0,rows-1)
        h2o_val = h2o.as_list(new_h2o_data[r,0])
        num_val = new_np_data[r]
        assert h2o_val == num_val, "failed value check! h2o computed {0} and numpy computed {1}".format(h2o_val,num_val)

    #   side effect check
    #63,0,76,1,2,1,9.5,14.4,7
    #80,1,66,1,1,1,25.7,39.1,9
    now1 = h2o.as_list(h2o_data[62,1])[0][0]
    now2 = h2o.as_list(h2o_data[79,1])[0][0]
    assert now1 == 0, "failed side effect check! original:0 and now:{0}".format(now1)
    assert now2 == 1, "failed side effect check! original:1 and now:{0}".format(now2)


    # expr type input
    new_h2o_data = h2o.logical_negation(h2o_data * 2)
    new_np_data = np.logical_not(np_data * 2)

    #   dimension check
    new_rows, new_cols = new_h2o_data.dim()
    assert new_rows == rows and new_cols == cols, \
        "failed dim check! new_rows:{0} rows:{1} new_cols:{2} cols:{3}".format(new_rows, rows, new_cols, cols)

    #   value check
    for i in range(10):
        r = random.randint(0,rows-1)
        c = random.randint(0,cols-1)
        h2o_val = h2o.as_list(new_h2o_data[r,c])[0][0]
        num_val = new_np_data[r,c]
        assert h2o_val == num_val, "failed value check! h2o computed {0} and numpy computed {1}".format(h2o_val,num_val)

    #   side effect check
    #63,0,76,1,2,1,9.5,14.4,7
    #80,1,66,1,1,1,25.7,39.1,9
    now1 = h2o.as_list(h2o_data[62,6])[0][0]
    now2 = h2o.as_list(h2o_data[79,7])[0][0]
    assert now1 == 9.5, "failed side effect check! original:76 and now:{0}".format(now1)
    assert now2 == 39.1, "failed side effect check! original:25.7 and now:{0}".format(now2)

if __name__ == "__main__":
    h2o.run_test(sys.argv, logical_negation)
