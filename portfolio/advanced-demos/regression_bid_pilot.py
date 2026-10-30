#!/usr/bin/env python3
"""Local, leakage-aware 5-model regression evaluation. Synthetic demo is NOT client data.

Usage:
  python regression_bid_pilot.py --self-test
  python regression_bid_pilot.py --demo --output report.json
  python regression_bid_pilot.py --csv dataset.csv --target TargetColumn --output report.json
  python regression_bid_pilot.py --csv data.csv --target target --time-col timestamp --output report.json

Install in a project-local environment:
  python -m pip install numpy pandas scikit-learn
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

try:
    import numpy as np
    import pandas as pd
    from sklearn.compose import ColumnTransformer
    from sklearn.dummy import DummyRegressor
    from sklearn.ensemble import ExtraTreesRegressor, HistGradientBoostingRegressor, RandomForestRegressor
    from sklearn.impute import SimpleImputer
    from sklearn.linear_model import ElasticNet, Ridge
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
    from sklearn.model_selection import KFold, TimeSeriesSplit, cross_val_score, train_test_split
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import OneHotEncoder, StandardScaler
except ImportError as exc:
    raise SystemExit("Missing dependency: " + str(exc) +
                     "\nInstall using: python -m pip install numpy pandas scikit-learn")


def synthetic_data(rows: int, seed: int = 42) -> pd.DataFrame:
    if rows < 80:
        raise ValueError("Synthetic demo requires at least 80 rows")
    rng = np.random.default_rng(seed)
    a = rng.standard_normal((rows, 19))
    w = np.array([3.0, -2.0, 1.5, 0.8] + [0.0] * 15)
    group = rng.choice(["A", "B", "C"], size=rows)
    target = a @ w + np.where(group == "A", 2.0, -0.8) + rng.normal(0, 0.65, rows)
    df = pd.DataFrame(a, columns=["x" + str(i + 1) for i in range(19)])
    df.loc[::23, "x3"] = np.nan
    df["category"] = group  # 19 numeric + 1 categorical: exactly 20 features
    df["target"] = target
    return df


def evaluate(frame: pd.DataFrame, target: str, time_col: str | None = None,
             seed: int = 42, self_check: bool = False) -> dict:
    if target not in frame:
        raise ValueError("Target column not found: " + target)
    if time_col and (time_col not in frame or time_col == target):
        raise ValueError("Invalid time column")
    df = frame.copy()
    original = len(df)
    if time_col:
        df["_evaluation_time"] = pd.to_datetime(df[time_col], errors="coerce", utc=True)
        df = df.dropna(subset=["_evaluation_time"]).sort_values("_evaluation_time")
    df[target] = pd.to_numeric(df[target], errors="coerce")
    df = df.dropna(subset=[target])
    df = df.drop_duplicates(subset=[c for c in df if c != "_evaluation_time"])
    df = df.reset_index(drop=True)
    if len(df) < 80:
        raise ValueError("At least 80 usable, nonduplicate labeled rows are required")
    features = [c for c in df if c not in {target, time_col, "_evaluation_time"}]
    X = df[features].copy()
    y = df[target].astype(float)
    if not np.isfinite(y.to_numpy()).all():
        raise ValueError("Target contains infinite values")
    invalid_features = [c for c in features if not (
        pd.api.types.is_numeric_dtype(X[c]) or pd.api.types.is_object_dtype(X[c])
        or isinstance(X[c].dtype, pd.CategoricalDtype)
        or pd.api.types.is_bool_dtype(X[c]))]
    if invalid_features:
        raise ValueError("Unsupported feature dtypes; encode these columns first: " + str(invalid_features))
    numeric = list(X.select_dtypes(include=[np.number]).columns)
    categorical = [c for c in features if c not in numeric]
    if not numeric and not categorical:
        raise ValueError("No features")
    if categorical:
        X[categorical] = X[categorical].astype("string").fillna("missing").astype(str)
    steps = []
    if numeric:
        steps.append(("numbers", Pipeline([
            ("fill", SimpleImputer(strategy="median")),
            ("scale", StandardScaler())
        ]), numeric))
    if categorical:
        steps.append(("categories", Pipeline([
            ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
        ]), categorical))
    # A fresh Pipeline is constructed for each model and CV fold: preprocessing fits on training only.
    def make_pipeline(regressor):
        return Pipeline([
            ("preprocess", ColumnTransformer(steps, remainder="drop", sparse_threshold=0)),
            ("model", regressor)
        ])

    ids = np.arange(len(df))
    if time_col:
        cut = int(len(df) * 0.8)
        train_idx, test_idx = ids[:cut], ids[cut:]
        cv = TimeSeriesSplit(n_splits=3)
        split_type = "chronological_80_20"
    else:
        train_idx, test_idx = train_test_split(ids, test_size=0.2, random_state=seed)
        cv = KFold(n_splits=3, shuffle=True, random_state=seed)
        split_type = "random_80_20"
    assert len(set(train_idx) & set(test_idx)) == 0
    xt, xv = X.iloc[train_idx], X.iloc[test_idx]
    yt, yv = y.iloc[train_idx], y.iloc[test_idx]
    models = {
        "Ridge": Ridge(alpha=1.0),
        "ElasticNet": ElasticNet(alpha=0.01, l1_ratio=0.5, max_iter=4000, random_state=seed),
        "RandomForest": RandomForestRegressor(n_estimators=64, min_samples_leaf=2, n_jobs=2, random_state=seed),
        "ExtraTrees": ExtraTreesRegressor(n_estimators=64, min_samples_leaf=2, n_jobs=2, random_state=seed),
        "HistGradientBoosting": HistGradientBoostingRegressor(max_iter=85, learning_rate=0.07, random_state=seed),
        "DummyMeanBaseline": DummyRegressor(strategy="mean"),
    }
    metrics = {}
    for name, reg in models.items():
        pipe = make_pipeline(reg)
        scores = -cross_val_score(pipe, xt, yt, cv=cv,
                                  scoring="neg_root_mean_squared_error", n_jobs=1,
                                  error_score="raise")
        pipe.fit(xt, yt)
        prediction = pipe.predict(xv)
        metrics[name] = {
            "cv_rmse_mean": round(float(np.mean(scores)), 6),
            "cv_rmse_std": round(float(np.std(scores)), 6),
            "holdout_mae": round(float(mean_absolute_error(yv, prediction)), 6),
            "holdout_rmse": round(float(np.sqrt(mean_squared_error(yv, prediction))), 6),
            "holdout_r2": round(float(r2_score(yv, prediction)), 6),
        }
    choices = {name: value for name, value in metrics.items() if name != "DummyMeanBaseline"}
    selected = min(choices, key=lambda name: choices[name]["cv_rmse_mean"])
    if self_check:
        assert len(choices) == 5
        assert len(train_idx) + len(test_idx) == len(df)
        assert all(np.isfinite(x["holdout_rmse"]) for x in metrics.values())
        assert all(np.isfinite(x["cv_rmse_mean"]) for x in metrics.values())
        assert metrics[selected]["cv_rmse_mean"] <= max(x["cv_rmse_mean"] for x in choices.values())
    return {
        "data_provenance": "synthetic demonstration" if self_check else "user-provided CSV or explicit --demo",
        "row_count_input": original,
        "row_count_usable": len(df),
        "n_features": len(features),
        "numeric_features": len(numeric),
        "categorical_features": len(categorical),
        "target": target,
        "validation": split_type,
        "training_rows": len(train_idx),
        "untouched_holdout_rows": len(test_idx),
        "selection_rule": "minimum 3-fold training-only cross-validation RMSE",
        "selected_model_by_cv": selected,
        "metrics": metrics,
        "limitations": [
            "Exploratory demonstration only; synthetic data does not validate a client dataset.",
            "Check units, sample dependency, outliers and domain-specific leakage before any contract.",
            "Reported holdout scores are not a promise of future or production performance.",
            "Verify group/time leakage, data rights and representativeness for real customer data."
        ]
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--demo", action="store_true", help="Use generated, non-client synthetic data")
    group.add_argument("--csv", type=Path, help="Local CSV (never uploaded)")
    group.add_argument("--self-test", action="store_true", help="Fast synthetic checks")
    parser.add_argument("--target", default="target")
    parser.add_argument("--time-col", default=None, help="Use chronological split, excluding timestamp from model features")
    parser.add_argument("--output", type=Path, help="Save JSON evaluation report")
    parser.add_argument("--rows", type=int, default=5000, help="Rows for synthetic --demo")
    args = parser.parse_args()
    frame = synthetic_data(330 if args.self_test else args.rows) if (args.demo or args.self_test) else pd.read_csv(args.csv)
    result = evaluate(frame, args.target, args.time_col, self_check=args.self_test or args.demo)
    if args.demo:
        result["data_provenance"] = "synthetic demonstration"
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    if args.self_test:
        print("SELF_TEST_PASS: five regressors + baseline; no train/holdout overlap.")


if __name__ == "__main__":
    main()
