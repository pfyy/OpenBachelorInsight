import pandas as pd
from sklearn.model_selection import train_test_split, GroupShuffleSplit
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report,
)
import lightgbm as lgb


def print_metrics(clf: lgb.LGBMClassifier, X, y):
    print("----------")

    y_pred = clf.predict(X)
    y_pred_proba = clf.predict_proba(X)[:, 1]

    acc = accuracy_score(y, y_pred)
    pre = precision_score(y, y_pred)
    rec = recall_score(y, y_pred)
    f1 = f1_score(y, y_pred)

    auc = roc_auc_score(y, y_pred_proba)

    cm = confusion_matrix(y, y_pred)

    print("accuracy_score:", acc)
    print("precision_score:", pre)
    print("recall_score:", rec)
    print("f1_score:", f1)
    print("roc_auc_score:", auc)
    print(
        f"confusion_matrix:\n{cm}",
    )
    print(f"classification_report:\n{classification_report(y, y_pred)}")


def main():
    df_orig = pd.read_csv("csv/multiOperationMatch_act3enemyduel_01b.csv")
    df_aug = pd.read_csv("csv/multiOperationMatch_act3enemyduel_01b_aug.csv")

    df_orig["group_id"] = df_orig.index

    df = pd.concat([df_orig, df_aug], axis=0, ignore_index=True)

    groups = df["group_id"]

    df["label"] = df["label"].replace(-1, 0)

    X = df.drop(columns=["label", "group_id"])
    y = df["label"]

    gss = GroupShuffleSplit(n_splits=1, test_size=0.1, random_state=42)
    train_idx, test_idx = next(gss.split(X, y, groups=groups))

    test_idx = test_idx[test_idx < len(df_orig)]

    X_train = X.iloc[train_idx]
    y_train = y.iloc[train_idx]
    X_test = X.iloc[test_idx]
    y_test = y.iloc[test_idx]

    clf = lgb.LGBMClassifier(
        objective="binary",
        random_state=42,
        n_estimators=1000,
        num_leaves=255,
    )
    clf.fit(X_train, y_train)

    print_metrics(clf, X_train, y_train)
    print_metrics(clf, X_test, y_test)

    clf.booster_.save_model("src/openbachelori/models/baseline_lgb/model.txt")


if __name__ == "__main__":
    main()
