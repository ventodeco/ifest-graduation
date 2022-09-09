from flask import Blueprint, render_template, request
import pandas as pd
import joblib
import numpy as np

graduation = Blueprint('graduation',__name__)

predict_graduation = joblib.load("model/rf_model_deploy_compressed.joblib")

@graduation.route("/graduation")
def index():
    data = {
        "title": "Prediksi Kelulusan",
        "selected": "graduation"
    }
    return render_template("graduation/index.html", data=data)

@graduation.route("/graduation/form")
def graduation_page():
    data = {
        "title": "Prediksi Kelulusan",
        "selected": "graduation"
    }
    return render_template("graduation/graduation.html", data=data)

@graduation.route("/graduation/predict", methods=['POST'])
def predict_graduation_page():
    data_form = [
        request.form['Gender'],
        request.form['Tinggal_Dengan'],
        request.form['Status_Kerja'],
        request.form['Biaya'],
        request.form['Alamat'],
        request.form['UKM'],
        request.form['Organisasi_Kampus'],
        request.form['Fakultas'],
    ]

    used_cols = np.array(['Gender', 'Tinggal_Dengan', 'Status_Kerja', 'Biaya', 'Alamat', 'UKM', 'Organisasi_Kampus', 'Fakultas'])

    all_encoding = {"Gender" : {"Wanita":0, "Pria":1},
                "Tinggal_Dengan" : {"Orang Tua":0, "Kos":1},
                "Status_Kerja" : {"Belum":0, "Bekerja":1},
                "Biaya" : {"Orang Tua":0, "Beasiswa":1},
                "Tgl_Daftar_Kuliah" : {2007:0, 2008:1, 2009:2},
                "Alamat" : {"Bekasi":0, "Bogor": 1, "Jakarta": 2, "Karawang": 3, "Serang": 4, "Tangerang": 5},
                "UKM" : {"Tidak":0, "UKM_1":1, "UKM_2":2, "UKM_3": 3, "UKM_4":4},
                "Organisasi_Kampus": {"Tidak":0, "Ya":1},
                "Fakultas": {"DKV":0, "FIKOM":1, "FISIP":2, "FT":3, "FTI":4}
                }

    # Data dijadikan dataframe
    df_new_data = pd.DataFrame(data_form).T
    df_new_data.columns = used_cols
    df_new_predict = df_new_data.replace(all_encoding)
    data_predict = df_new_predict.values.reshape(1,-1)
    prediksi_baru = predict_graduation.predict(data_predict)

    data = {
        "title": "Prediksi Sarjana",
        "selected": "graduation",
        "prediction": prediksi_baru[0]
    }

    return render_template("graduation/graduation_predict.html", data=data)
