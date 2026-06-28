import numpy as np
import pandas as pd
from abc import ABC, abstractmethod
from typing import Union, Dict, Any
import json


from sklearn.base import BaseEstimator
from sklearn.linear_model import LinearRegression
from sklearn.metrics import root_mean_squared_error,mean_absolute_error,mean_squared_error,r2_score

import logging 
import logging.config
import yaml

# Initialize logging system
with open("logging.yaml", "r") as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

# Get the specific loggers
root_logger = logging.getLogger(__name__)
pred_logger = logging.getLogger("prediction_logger")

class Base(ABC):
    "Base from which every other custom model inherits"
    def __init__(self,model_name : str):
        self.model_name = model_name # Accepting model name from the user
        self.model: Union[BaseEstimator, None] = None  # Basicaly we are specifying that either the model variable will hold a sklearn_object or None ; instantiated as None
        self.is_trained: bool = False # A simple flag so user can peek and see whether the model is already trained or not

    @abstractmethod
    # By specifying : col_types we are just expecting user to insert the the variable with the specified type.
    # For more specific validation have a whole other library - pydantic.
    def fit(self, X : np.ndarray , y : np.ndarray ) -> None:
        " Function to fit the passed params : X and y"
        pass
    @abstractmethod
    def predict( self , X : np.ndarray ):
        " Predicts the output of a test column X passed if the model is trained"
        pass
    @abstractmethod
    def evaluate_metrics(self,y_test : np.ndarray , y_pred : np.ndarray ) -> dict:
        "Evaluates the passed metric based on the params passed : y_test and y_pred "
        pass
    def get_info(self) -> str:
        """Return the general info of the model"""
        status = "Trained" if self.is_trained else "Untrained"
        return f"Model Architecture: {self.model_name} | Status: {status}"
    

# Now the customModel will inherit and be forced to follow the method name from the Base class while inheriting
class CustomRegressor(Base):
    """
    A custom Regressor standardizing scikit-learn model flows.
    All tracking uses structured log entries instead of console print statements.
    """

    # Constants
    REG_MODELS = {"LinearRegression"}
    REG_METRICS = {
        "r2_score": r2_score,
        "mean_absolute_error": mean_absolute_error, # Fixed spelling typo
        "root_mean_squared_error": root_mean_squared_error,
        "mean_squared_error": mean_squared_error
    }

    def __init__(self, model_name: str, reg_metric: str):
        super().__init__(model_name)
        
        # Validate metric choice
        cleaned_metric = reg_metric.lower().strip()
        if cleaned_metric not in self.REG_METRICS:
            error_msg = f"Invalid Choice: {reg_metric}. Choose from: {list(self.REG_METRICS.keys())}"
            pred_logger.error(json.dumps({"action": "initialization_failed", "error": error_msg}))
            raise ValueError(error_msg)
            
        self.reg_metric = cleaned_metric
        self.model = self.validate_model(model_name)
        
        # Log successful initialization
        pred_logger.info(json.dumps({
            "action": "model_initialized",
            "model_name": self.model_name,
            "metric": self.reg_metric
        }))

    def validate_model(self, model_name: str) -> BaseEstimator:
        if model_name not in self.REG_MODELS:
            error_msg = f"Invalid Choice: {model_name}. Choose from: {self.REG_MODELS}"
            pred_logger.error(json.dumps({"action": "validation_failed", "error": error_msg}))
            raise ValueError(error_msg)
        return LinearRegression() 

    def fit(self, X: np.ndarray, y: np.ndarray) -> None:
        # Replaced print statements with structured entry detailing the matrix dimensions
        pred_logger.info(json.dumps({
            "action": "training_started",
            "model_name": self.model_name,
            "samples": int(X.shape[0]),
            "features": int(X.shape[1]) if len(X.shape) > 1 else 1
        }))
        
        self.model.fit(X, y)
        self.is_trained = True
        
        pred_logger.info(json.dumps({
            "action": "training_completed",
            "model_name": self.model_name,
            "status": "success"
        }))

    def predict(self, X: np.ndarray) -> np.ndarray:
        if not self.is_trained: 
            error_msg = f"You must use the fit() method on {self.model_name} first !!!"
            pred_logger.error(json.dumps({"action": "prediction_failed", "error": error_msg}))
            raise RuntimeError(error_msg)
            
        pred_logger.info(json.dumps({
            "action": "prediction_started",
            "model_name": self.model_name,
            "predict_samples": int(X.shape[0])
        }))
        
        predictions = self.model.predict(X)
        
        pred_logger.info(json.dumps({
            "action": "prediction_completed",
            "model_name": self.model_name
        }))
        return predictions

    def evaluate_metrics(self, y_test: np.ndarray, y_pred: np.ndarray) -> dict[str, float]:
        # Compute dynamic calculation
        raw_score = self.REG_METRICS[self.reg_metric](y_test, y_pred)
        metric_value = round(float(raw_score), 2)
        
        metric_map = {self.reg_metric: metric_value}
        
        # Log validation assessment scores automatically
        pred_logger.info(json.dumps({
            "action": "evaluation_completed",
            "model_name": self.model_name,
            "metrics": metric_map
        }))
        
        return metric_map
    
    def __repr__(self):
        return (f"CustomRegressor(model={self.model_name!r}, "
                f"chosen_metric={self.reg_metric!r}, "
                f"trained={self.is_trained})")


# Create dummy training data 
X_train = np.array([[1, 2], [2, 3], [3, 4], [5, 1], [6, 2], [7, 3]])
y_train = np.array([100,200,300,402,405,610])

X_test = np.array([[1, 1], [6, 4]])
y_test = np.array([95,525])

# Instantiation of the object
regressor_1 = CustomRegressor("LinearRegression","mean_squared_error")
print(regressor_1)
regressor_1.fit(X_train,y_train)
y_pred = regressor_1.predict(X_test)
regressor_1.evaluate_metrics(y_test,y_pred)