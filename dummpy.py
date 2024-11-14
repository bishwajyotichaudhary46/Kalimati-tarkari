from kalimati_tarkari.pipline.forecasting import ForecastingPipeline
import numpy as np
# Create object
obj = ForecastingPipeline()

forecasted_output = obj.forecasts()
print(forecasted_output)
