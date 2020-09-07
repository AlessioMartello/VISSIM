from VISSIM.methods.journey_times import get_journey_times
from VISSIM.methods.demand_dependencies import get_demand_dependencies

try:
    get_journey_times()
except:
    print(f"Journey time script did not run correctly")

try:
    get_demand_dependencies()
except:
    print(f"Demand dependancy script did not run correctly")