import pandas as pd
from features_blueprint import BLUEPRINT, build_feature_matrix
from lotto_model import train_models

# 1. Load raw data
df_raw = pd.read_csv("lucky_day_lotto.csv")

# 2. Build full feature matrix
df = build_feature_matrix(df_raw)

# 3. Train model (LightGBM or PyTorch)
model = train_models(
    df,
    feature_cols=BLUEPRINT.all_features,
    target_cols=BLUEPRINT.targets,
    model_type="lightgbm",   # or "pytorch"
)

# 4. Predict next draw
next_row = df.tail(1)
predicted = model.predict_top5(next_row)
print("Predicted numbers:", predicted)