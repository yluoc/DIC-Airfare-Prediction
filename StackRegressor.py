import numpy as np
import pandas as pd
import pickle as pkl
import warnings
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from sklearn.ensemble import RandomForestRegressor
from mlxtend.regressor import StackingCVRegressor
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import KFold, cross_val_score, train_test_split
from sklearn.preprocessing import RobustScaler, LabelEncoder

warnings.filterwarnings('ignore')

df = pd.read_csv('./Dataset/cleaned_data.csv')
# remove specifal character in database
df.columns = df.columns.str.replace('[^a-zA-Z0-9_]', '_', regex=True)

# encode features
lb_encode = LabelEncoder()
df['airline'] = lb_encode.fit_transform(df['airline'])
df['flight_code'] = lb_encode.fit_transform(df['flight_code'])
df['source_city'] = lb_encode.fit_transform(df['source_city'])
df['time_taken'] = lb_encode.fit_transform(df['time_taken'])
df['stop'] = lb_encode.fit_transform(df['stop'])
df['destinate_city'] = lb_encode.fit_transform(df['destinate_city'])
df['Class'] = lb_encode.fit_transform(df['Class'])
df['dep_time_category'] = lb_encode.fit_transform(df['dep_time_category'])
df['arr_time_category'] = lb_encode.fit_transform(df['arr_time_category'])

X = df.drop(columns=['price', 'idx', 'flight_code'])
y = df.price
X_train, X_test, y_train, y_test =  train_test_split(X, y, test_size=0.2, random_state=42)

kfolds = KFold(n_splits=50, shuffle=True, random_state=100)
def cv_rmse(model):
    return np.sqrt(-cross_val_score(model, X, y, scoring='neg_mean_squared_error', cv=kfolds))

# XGB regressor
xgb3 = XGBRegressor(learning_rate=0.5, 
                    n_estimators=300, 
                    max_depth=6, 
                    min_child_weight=10, 
                    gamma=0, 
                    subsample=0.8, 
                    max_bin=128,
                    colsample_bytree=0.8, 
                    objective='reg:linear', 
                    nthread=4, 
                    scale_pos_weight=1, 
                    seed=27, 
                    reg_alpha=0.0001,
                    tree_method='gpu_hist',
                    device='cuda')

xgb_fit = xgb3.fit(X_train, y_train, eval_set=[(X_test, y_test)], verbose=True)
# print(cv_rmse(xgb_fit).mean())

# LGBM regressor
lgbm_model = LGBMRegressor(objective='regression', 
                           num_leaves=31, 
                           learning_rate=0.05, 
                           n_estimators=300,
                           max_bin=128, 
                           bagging_fraction=0.8, 
                           bagging_freq=5, 
                           feature_fraction=0.8,
                           feature_fraction_seed=9, 
                           bagging_seed=9,
                           min_data_in_leaf=50, 
                           min_sum_hessian_in_leaf=10,
                           reg_alpha=0.1,
                           reg_lambda=0.1)

lgbm_fit = lgbm_model.fit(X_train, y_train, eval_set=[(X_test, y_test)])
# print(cv_rmse(lgbm_model).mean())

# RandomForest regressor
forest= RandomForestRegressor(n_estimators=300, 
                              random_state=42,
                              max_depth=20,
                              min_samples_split=10,
                              min_samples_leaf=5,
                              n_jobs=-1,
                              max_features='sqrt')
forest_fit = forest.fit(X_train, y_train)
# print(cv_rmse(forest_fit).mean())

# Stack the regressor
lightgbm = make_pipeline(RobustScaler(),
                         LGBMRegressor(objective='regression', 
                           num_leaves=31, 
                           learning_rate=0.05, 
                           n_estimators=300,
                           max_bin=128, 
                           bagging_fraction=0.8, 
                           bagging_freq=5, 
                           feature_fraction=0.8,
                           feature_fraction_seed=9, 
                           bagging_seed=9,
                           min_data_in_leaf=50, 
                           min_sum_hessian_in_leaf=10,
                           reg_alpha=0.1,
                           reg_lambda=0.1))

xgboost = make_pipeline(RobustScaler(),
                        XGBRegressor(learning_rate=0.5, 
                    n_estimators=300, 
                    max_depth=6, 
                    min_child_weight=10, 
                    gamma=0, 
                    subsample=0.8, 
                    max_bin=128,
                    colsample_bytree=0.8, 
                    objective='reg:linear', 
                    nthread=4, 
                    scale_pos_weight=1, 
                    seed=27, 
                    reg_alpha=0.0001,
                    tree_method='gpu_hist',
                    device='cuda'))

forest = make_pipeline(RobustScaler(),
                       RandomForestRegressor(n_estimators=300, 
                              random_state=42,
                              max_depth=20,
                              min_samples_split=10,
                              min_samples_leaf=5,
                              n_jobs=-1,
                              max_features='sqrt'))

stack_gen = StackingCVRegressor(regressors=(lightgbm, xgboost, forest),
                                meta_regressor=xgboost, use_features_in_secondary=True)

stackX = np.array(X_train)
stacky = np.array(y_train)

stack_gen_model = stack_gen.fit(stackX, stacky)

stack_gen_preds = stack_gen_model.predict(X_test)
xgb_preds = xgb_fit.predict(X_test)
lgbm_preds = lgbm_fit.predict(X_test)
forest_preds = forest_fit.predict(X_test)
'''
# envalute the model
rmse_forest = np.sqrt(mean_squared_error(y_test, forest_preds))
print('RMSE_FOREST: %f' % (rmse_forest))

rmse_xgb = np.sqrt(mean_squared_error(y_test, xgb_preds))
print('RMSE_XGB: %f' % (rmse_xgb))

rmse_lgbm = np.sqrt(mean_squared_error(y_test, lgbm_preds))
print('RMSE_LGBM: %f' % (rmse_lgbm))

rmse_stack = np.sqrt(mean_squared_error(y_test, stack_gen_preds))
print('RMSE_STACK: %f' % (rmse_stack))

print('r2_xgb' ,r2_score(y_test,xgb_preds) )
print('r2_lgbm' , r2_score(y_test,lgbm_preds) )
print('r2_forest' , r2_score(y_test,forest_preds) )
print('r2_stack' , r2_score(y_test,stack_gen_preds) )

abs_error = abs(stack_gen_preds - y_test)
made = 100*(abs_error / y_test)
accuracy = 100-np.mean(made)

print('Accuracy:', round(accuracy, 2), '%')
'''
# save the model
with open('./StackRegressor.pkl', 'wb') as f:
    pkl.dump(stack_gen_model, f)