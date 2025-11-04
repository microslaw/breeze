import pandas as pd
from breeze import NodeType
from backend.formatting import add_display_format, format_for_display
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import r_regression


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

    df = pd.concat(
        [df.drop(columns=[column]).reset_index(drop=True), df_encoded], axis=1
    )

    return df


@NodeType(tags=["sklearn"])
def train_test_split_node_type(
    df: pd.DataFrame,
    test_size: float,
) -> pd.DataFrame:
    return train_test_split(df, test_size=test_size)


@NodeType(tags=["sklearn"])
def get_by_index(indexable, id: int):
    return indexable[id]


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


@NodeType(tags=["sklearn"])
def compute_pearson(df: pd.DataFrame, x_col: str, y_col: str):
    return float(r_regression(df[[x_col]], df[[y_col]]))


add_display_format(
    DecisionTreeClassifier,
    lambda x: f'DecisionTreeClassifier(criterion="{x.criterion}")',
)
add_display_format(
    tuple,
    lambda x: f"Tuple({','.join([format_for_display(type(item)) for item in x])})",
)
