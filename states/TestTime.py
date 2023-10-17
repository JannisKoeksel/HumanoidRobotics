import numpy as np
time1 = np.datetime64('now')
diff = 0
while (diff < 5):
    time2 = np.datetime64('now')
    diff = (np.datetime64(time2)-np.datetime64(time1))/(np.timedelta64(1,'s'))
    print(diff)