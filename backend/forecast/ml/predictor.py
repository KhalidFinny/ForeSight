import pickle
import pandas as pd
from datetime import timedelta, date

def predict_next_days(days=7):
    with open("forecast/ml/model.pkl", "rb") as f:
        model = pickle.load(f)

    future_dates = [date.today() + timedelta(days=i) for i in range(1, days + 1)]
    future_ordinals = pd.DataFrame([d.toordinal() for d in future_dates], columns=["date_ordinal"])

    preds = model.predict(future_ordinals)

    return [
        {"date": str(future_dates[i]), "prediction": int(max(preds[i], 0))}
        for i in range(days)
    ]
