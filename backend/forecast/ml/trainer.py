import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle
from inventory.models import SalesRecord

def train_model():
    qs = SalesRecord.objects.all().order_by("date").values("product_id", "quantity", "date")

    if qs.count() < 10:
        raise Exception("Not enough data to train model")

    df = pd.DataFrame(qs)
    df['date_ordinal'] = pd.to_datetime(df['date']).map(pd.Timestamp.toordinal)

    X = df[['date_ordinal']]
    y = df['quantity']

    model = LinearRegression()
    model.fit(X, y)

    with open("forecast/ml/model.pkl", "wb") as f:
        pickle.dump(model, f)

    return "Model trained successfully"
