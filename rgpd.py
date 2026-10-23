import pandas as pd
clients = pd.read_csv("dim_client.csv")
print(len(clients), clients["email"].nunique())
