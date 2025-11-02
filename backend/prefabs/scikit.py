import pandas as pd
from breeze import NodeType
from backend.formatting import add_display_format
from typing import Optional
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import OneHotEncoder


@NodeType(tags=["sklearn"])
def one_hot_encode(
    df: pd.DataFrame,
    column: str,
) -> pd.DataFrame:
    encoder = OneHotEncoder(handle_unknown="ignore")
    encoder.fit(df[[column]])

    df_encoded = pd.DataFrame(
        encoder.transform(df[[column]]).todense(), columns=encoder.categories_[0]
    )

    df = pd.concat([df.drop(columns=[column]), df_encoded], axis=1)

    return df


@NodeType(tags=["sklearn"])
def fit_decision_tree(
    df_x: pd.DataFrame,
    df_y: pd.DataFrame,
):
    model = DecisionTreeClassifier()
    model = model.fit(df_x, df_y)

    return model


@NodeType(tags=["sklearn"])
def predict(
    model: DecisionTreeClassifier,
    df_x: pd.DataFrame,
    predicted_colname: str = "predicted",
):
    df_x = df_x.copy()
    result = pd.Series(model.predict(df_x))
    df_x[predicted_colname] = result
    return df_x
