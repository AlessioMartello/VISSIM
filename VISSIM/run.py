from methods.journey_times import get_journey_times
from methods.demand_dependencies import get_demand_dependencies
from methods.saturation_flow import get_saturation_flow

try:
    get_journey_times()
except:
    print(f"Journey time script did not run correctly")

try:
    get_demand_dependencies()
except:
    print(f"Demand dependancy script did not run correctly")

try:
    get_saturation_flow()
except:
    print(f"Saturation flow script did not run correctly")