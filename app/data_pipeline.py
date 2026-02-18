import pandas as pd
from app.data_api import fetch_mandi_data


def get_dataframe(
    commodity=None,
    state=None,
    district=None,
    limit=500
):

    data = fetch_mandi_data(
        commodity=commodity,
        state=state,
        district=district,
        limit=limit
    )

    df = pd.DataFrame(data)

    return df
