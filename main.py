#import library
#FastAPI -> class
from fastapi import FastAPI, HTTPException
import pandas as pd

#create instance/object
app = FastAPI()

#define api_key
apiKey = "keretakuda1547"

#define endpoint data
#@object
@app.get("/")
def root():
    return {"message": "Hello World"}

#define
@app.get("/data")
def get_data():
    #read data dari file csv
    df = pd.read_csv("data.csv")
    #convert dataframe to dictionary
    #pilihannya ada 2: .to_json atau .to_dict
    return df.to_json(orient='records')
#url: http://127.0.0.1:8000/

@app.get("/data/{id}")
def get_data_by_id(id: int):
    #read data dari file csv
    df = pd.read_csv("data.csv")

    #filter berdasarkan id ada 2 cara: df[kondisi] atau df.query(kondisi)
    #memanggil kolom: df['id] atau df.id
    filter = df[df.id == id]

    #condition if else for filterring
    #kondisi 1: Jika data tidak ditemukan atau tidak ada data yang cocok
    if len(filter) == 0:
        #return pesan error
        #format HTTPException (status_code, detail=None, headers=None)
        raise HTTPException(status_code=404, detail='Data tidak ditemukan!')
    
    #jika data ditemukan:
    else:
    #convert dataframe to dictionary
    #pilihannya ada 2: .to_json atau .to_dict
        return filter.to_json(orient='records')

@app.get("/data/name/{fullname}")
def get_data_by_id(fullname: str):
    #read data dari file csv
    df = pd.read_csv("data.csv")

    #filter berdasarkan id ada 2 cara: df[kondisi] atau df.query(kondisi)
    #memanggil kolom: df['id] atau df.id
    #mengubah menjadi case-insensitive
    filter = df[df.fullname.str.lower() == fullname.lower()]

    #condition if else for filterring
    #kondisi 1: Jika data tidak ditemukan atau tidak ada data yang cocok
    if len(filter) == 0:
        #return pesan error
        #format HTTPException (status_code, detail=None, headers=None)
        raise HTTPException(status_code=404, detail='Data tidak ditemukan!')
    
    #jika data ditemukan:
    else:
    #convert dataframe to dictionary
    #pilihannya ada 2: .to_json atau .to_dict
        return filter.to_json(orient='records')


#define endpoint for updating data
@app.post('/input_data/')
def add_data(update_df: dict):
    df = pd.read_csv("data.csv")

    #define new id for new data
    id = len(df) + 1


    #assign new id to column id in new df named update_df
    update_df['id'] = id

    #create new df beccause we will use concat
    new_df = pd.DataFrame([update_df])

    #menggabungkan data lama dengan data baru (df to update_df)
    df= pd.concat([df, new_df], ignore_index=True)

    #Save updated DataFrame back to csv
    df.to_csv('data.csv', index=False)

    return df.to_dict(orient='records')