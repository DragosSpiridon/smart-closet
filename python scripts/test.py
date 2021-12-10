import pandas as pd

database = pd.read_csv("Clothes_database.csv") # import clothing items database

for i in range(len(database)):
    if (database.at[i,'Style'] == 'Casual' or database.at[i,'Style'] == 'Classy-casual'):
        database.drop(i,inplace=True)

database.reset_index(drop=True, inplace=True)

print(database)