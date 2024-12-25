To get the dataset used in EDA process and model file, make sure get a Kaggle API to retrieve dataset from kaggle.
the EDA process uses raw_data.csv, stack regressor file uses cleaned_dataset.csv.

This model stacks Random Forest Tree, XGBoost, LGBMRegressor, after fitting the final model on the 300k rows dataset, it achieves:
```Python
r2_xgb = 0.988
r2_lgbm = 0.979
r2_forest = 0.987
r2_stack = 0.989
Accuracy = 0.921
```
