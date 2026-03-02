"""
Lucky Day Lotto Model Architecture Template
Compatible with the feature blueprint in features_blueprint.py

Provides:
- LightGBM multi-label model
- PyTorch MLP multi-label model
- Training loops
- Prediction utilities
"""

import numpy as np
import pandas as pd

# LightGBM
import lightgbm as lgb

# PyTorch
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader


# ============================================================
# 1. DATASET WRAPPER (shared by both models)
# ============================================================

class LottoDataset(Dataset):
    def __init__(self, df, feature_cols, target_cols):
        self.X = df[feature_cols].astype(np.float32).values
        self.y = df[target_cols].astype(np.float32).values

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]


# ============================================================
# 2. LIGHTGBM MULTI-LABEL MODEL
# ============================================================

class LightGBMMultiLabel:
    """
    Trains 45 independent LightGBM binary classifiers.
    Each predicts P(number i appears in next draw).
    """

    def __init__(self, feature_cols, target_cols, params=None):
        self.feature_cols = feature_cols
        self.target_cols = target_cols
        self.models = {}

        self.params = params or {
            "objective": "binary",
            "learning_rate": 0.05,
            "num_leaves": 31,
            "feature_fraction": 0.9,
            "bagging_fraction": 0.8,
            "bagging_freq": 5,
            "verbose": -1,
        }

    def fit(self, df_train, df_valid=None):
        X_train = df_train[self.feature_cols]
        y_train = df_train[self.target_cols]

        if df_valid is not None:
            X_valid = df_valid[self.feature_cols]
            y_valid = df_valid[self.target_cols]
        else:
            X_valid = None
            y_valid = None

        for i, target in enumerate(self.target_cols, start=1):
            print(f"Training LightGBM model for number {i}...")

            train_data = lgb.Dataset(X_train, label=y_train[target])

            if df_valid is not None:
                valid_data = lgb.Dataset(X_valid, label=y_valid[target])
                model = lgb.train(
                    self.params,
                    train_data,
                    valid_sets=[valid_data],
                    num_boost_round=500,
                    early_stopping_rounds=50,
                    verbose_eval=False,
                )
            else:
                model = lgb.train(
                    self.params,
                    train_data,
                    num_boost_round=300,
                    verbose_eval=False,
                )

            self.models[target] = model

    def predict_proba(self, df):
        X = df[self.feature_cols]
        preds = np.zeros((len(df), len(self.target_cols)))

        for idx, target in enumerate(self.target_cols):
            preds[:, idx] = self.models[target].predict(X)

        return preds

    def predict_top5(self, df):
        proba = self.predict_proba(df)
        top5 = np.argsort(-proba, axis=1)[:, :5] + 1  # numbers 1–45
        return top5


# ============================================================
# 3. PYTORCH MLP MULTI-LABEL MODEL
# ============================================================

class MLP(nn.Module):
    def __init__(self, input_dim, output_dim=45):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 256),
            nn.ReLU(),
            nn.Dropout(0.2),

            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Dropout(0.2),

            nn.Linear(128, output_dim),
            nn.Sigmoid(),  # multi-label probabilities
        )

    def forward(self, x):
        return self.net(x)


class PyTorchMultiLabel:
    def __init__(self, feature_cols, target_cols, lr=1e-3, batch_size=64, epochs=20):
        self.feature_cols = feature_cols
        self.target_cols = target_cols
        self.lr = lr
        self.batch_size = batch_size
        self.epochs = epochs

        self.model = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    def fit(self, df_train, df_valid=None):
        train_ds = LottoDataset(df_train, self.feature_cols, self.target_cols)
        train_loader = DataLoader(train_ds, batch_size=self.batch_size, shuffle=True)

        input_dim = len(self.feature_cols)
        output_dim = len(self.target_cols)

        self.model = MLP(input_dim, output_dim).to(self.device)
        optimizer = torch.optim.Adam(self.model.parameters(), lr=self.lr)
        criterion = nn.BCELoss()

        for epoch in range(self.epochs):
            self.model.train()
            total_loss = 0

            for X, y in train_loader:
                X = X.to(self.device)
                y = y.to(self.device)

                optimizer.zero_grad()
                preds = self.model(X)
                loss = criterion(preds, y)
                loss.backward()
                optimizer.step()

                total_loss += loss.item()

            print(f"Epoch {epoch+1}/{self.epochs} — Loss: {total_loss:.4f}")

    def predict_proba(self, df):
        self.model.eval()
        X = df[self.feature_cols].astype(np.float32).values
        X = torch.tensor(X).to(self.device)

        with torch.no_grad():
            preds = self.model(X).cpu().numpy()

        return preds

    def predict_top5(self, df):
        proba = self.predict_proba(df)
        top5 = np.argsort(-proba, axis=1)[:, :5] + 1
        return top5


# ============================================================
# 4. TRAINING PIPELINE (CHRONOLOGICAL SPLIT)
# ============================================================

def train_models(df, feature_cols, target_cols, model_type="lightgbm"):
    df = df.sort_values("draw_date").reset_index(drop=True)

    split_idx = int(len(df) * 0.8)
    df_train = df.iloc[:split_idx]
    df_valid = df.iloc[split_idx:]

    if model_type == "lightgbm":
        model = LightGBMMultiLabel(feature_cols, target_cols)
    else:
        model = PyTorchMultiLabel(feature_cols, target_cols)

    model.fit(df_train, df_valid)
    return model