import pandas as pd
from breeze import NodeType
from backend.formatting import add_display_format
from typing import Optional
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import OneHotEncoder


@NodeType(tags=["sklearn"])
def create_one_hot_encoder(
    df: pd.DataFrame,
) -> OneHotEncoder:
    encoder = OneHotEncoder(handle_unknown="ignore")
    encoder.fit(df)
    return encoder


@NodeType(tags=["sklearn"])
def one_hot_encode(
    df: pd.DataFrame,
    encoder: OneHotEncoder,
) -> pd.DataFrame:
    return pd.DataFrame(
        encoder.transform(df[["Sex"]]).todense(), columns=encoder.categories_[0]
    )


@NodeType(tags=["sklearn"])
def fit_decision_tree(
    df_x: pd.DataFrame,
    df_y: pd.DataFrame,
):
    model = DecisionTreeClassifier()
    model = model.fit(df_x, df_y)

    return model


def predict(
    model: DecisionTreeClassifier,
    df_x: pd.DataFrame,
    predicted_colname: str = "predicted",
):
    df_x = df_x.copy()
    result = pd.Series(model.predict(df_x))
    df_x[predicted_colname] = result
    return df_x
