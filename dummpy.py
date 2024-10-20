from kalimati_tarkari.pipline.forecasting import ForecastingPipeline
import numpy as np
# Create object
obj = ForecastingPipeline()

# Normalize data
test_data_scaled, train_data_scaled, scaler = obj.normalize_data()

# Prepare test data
X_test, y_test = obj.test_splitting(train_data_scaled, test_data_scaled)

# Forecast
forecasted_output = obj.forecasts(X_test)

# Inverse scale the forecasted data
forecasted_output = np.array(forecasted_output).reshape(-1, 1)
original_scale_forecast = scaler.inverse_transform(forecasted_output)
