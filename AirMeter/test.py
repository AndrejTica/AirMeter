from PAS_CO2_LIB import *

_,_,status, meas_status, result = Measure(1019)
print(status)
print(meas_status)
print(result)