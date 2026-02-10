# -*- coding: utf-8 -*-
"""
Created on Thu Feb  5 17:15:55 2026

@author: betul
"""

import tkinter as tk
from tkinter import ttk
import pickle
from tkinter import messagebox
import os
COLORS = {
    "bg": "#F5F7FA",        # genel arka plan (açık gri/mavi)
    "card": "#FFFFFF",      # kart/panel arka planı
    "primary": "#2C3E50",   # koyu mavi-gri (header gibi)
    "accent": "#2E86C1",    # mavi (buton)
    "danger": "#C0392B",    # kırmızı (back)
    "text": "#1F2D3D",      # ana yazı rengi
}
def center_window(win, width=1000, height=600):
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()

    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))

    win.geometry(f"{width}x{height}+{x}+{y}")


window=tk.Tk()
window.geometry("1000x600")
center_window(window, 1000, 600)
window.title("Prediction")
window.resizable(False,False)
window.configure(bg=COLORS["bg"])
window.iconbitmap("assets/appLogo.ico")


home_frame = tk.Frame(window, bg=COLORS["bg"])
anemia_frame = tk.Frame(window, bg=COLORS["bg"])
diabetes_frame = tk.Frame(window, bg=COLORS["bg"])
liver_frame = tk.Frame(window, bg=COLORS["bg"])

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(BASE_DIR, "assets", "logo.png")
try:
    window.logo_img = tk.PhotoImage(file=logo_path)
    window.logo_img = window.logo_img.subsample(8, 8) 

    window.logo_label = tk.Label(home_frame, image=window.logo_img, bg=COLORS["bg"])
    window.logo_label.place(x=250, y=20)
except tk.TclError as e:
    messagebox.showerror("Logo Error", f"Logo yüklenemedi.\n{logo_path}\n\n{e}")
    print("Logo error:", e)
    print("Logo path:", logo_path)
    
for f in (home_frame, anemia_frame, diabetes_frame, liver_frame):
    f.place(x=0, y=0, relwidth=1, relheight=1)

home_frame.tkraise()
label=tk.Label(home_frame,text="WELCOME TO THE DISEASE PREDICTION APP",font="Helvetica 22",bg=COLORS["primary"],fg="white").place(x=180,y=180)
label2=tk.Label(home_frame,text="Please select a disease to predict",font="Times 15",bg=COLORS["bg"],fg=COLORS["text"]).place(x=350,y=300)

def anemiaFunction():
    anemia_frame.tkraise()
    print("anemia")

def diabetesFunction():
    diabetes_frame.tkraise()
    print("diabetes")

def liverFunction():
    liver_frame.tkraise()
    print("liver")
    

button1=tk.Button(home_frame,text="Anemia",width=20,height=2,command=anemiaFunction,bg=COLORS["accent"], fg="white", activebackground="#1F6AA5", activeforeground="white",bd=0).place(x=200,y=400)
button2=tk.Button(home_frame,text="Diabetes",width=20,height=2,command=diabetesFunction,bg=COLORS["accent"], fg="white", activebackground="#1F6AA5", activeforeground="white",bd=0).place(x=400,y=400)
button3=tk.Button(home_frame,text="Liver",width=20,height=2,command=liverFunction,bg=COLORS["accent"], fg="white", activebackground="#1F6AA5", activeforeground="white",bd=0).place(x=600,y=400)
def back():
    home_frame.tkraise()

#anemia screen
label3=tk.Label(anemia_frame,text="Please enter the inputs",font="Times 15").place(x=400,y=100)
gender=tk.StringVar()
gender_comboBox=ttk.Combobox(anemia_frame,textvariable=gender,values=("Female","Male"),state="readonly").place(x=150,y=200)

hemoglobin=tk.Entry(anemia_frame,width=20)
hemoglobin.insert(string="Hemoglobin...",index=0)
hemoglobin.place(x=300,y=200)

mch=tk.Entry(anemia_frame,width=20)
mch.insert(string="MCH...",index=0)
mch.place(x=450,y=200)

mchc=tk.Entry(anemia_frame,width=20)
mchc.insert(string="MCHC...",index=0)
mchc.place(x=600,y=200)

mcv=tk.Entry(anemia_frame,width=20)
mcv.insert(string="MCV...",index=0)
mcv.place(x=750,y=200)
anemia_risk_var = tk.DoubleVar(value=0)

anemia_bar = ttk.Progressbar(anemia_frame, orient="horizontal", length=320,mode="determinate", maximum=100, variable=anemia_risk_var)
anemia_bar.place(x=320, y=390)
anemia_result_label = tk.Label(anemia_frame, text="Anemia Risk: %0.00", font=("Helvetica", 12))
anemia_result_label.place(x=340, y=420)



def anemiaPredict():
    genderValue=gender.get()
    if(genderValue=="Male"):
        genderValue=0
    elif(genderValue=="Female"):
        genderValue=1
    else:
        messagebox.showerror("Gender Error", "Please select a gender!")
        return
    hemoglobinValue=hemoglobin.get()
    mchValue=mch.get()
    mchcValue=mchc.get()
    mcvValue=mcv.get()
    try:
        hemoglobinValue = float(hemoglobinValue)
        mchValue = float(mchValue)
        mchcValue = float(mchcValue)
        mcvValue = float(mcvValue)

    except ValueError:
        messagebox.showerror("Value Error", "Please enter numeric values!")
        return
    
    anemia_model=pickle.load(open("anemia_model","rb"))
    x=[[genderValue,hemoglobinValue,mchValue,mchcValue,mcvValue]]
    prob = anemia_model.predict_proba(x)
    risk = prob[0][1]
    result=f"Anemia Risk: %{risk*100:.2f}"
    risk_percent = risk * 100
    anemia_risk_var.set(risk_percent)
    anemia_result_label.config(text=f"Anemia Risk: %{risk_percent:.2f}")
    alert=tk.Label(anemia_frame,text="This is NOT a medical diagnosis. Please consult a doctor.",font=("Helvetica", 8),fg="red").place(x=340,y=470)
    
    # renk (isteğe bağlı)
    if risk_percent < 33:
        anemia_result_label.config(fg="green")
    elif risk_percent < 66:
        anemia_result_label.config(fg="orange")
    else:
        anemia_result_label.config(fg="red")

    
anemia_button=tk.Button(anemia_frame,text="Predict",activebackground="green",height=2,width=20,command=anemiaPredict).place(x=300,y=300)
back_button=tk.Button(anemia_frame,text="Back",activebackground="red",height=2,width=20,command=back).place(x=500,y=300)


#diabetes screen
label4=tk.Label(diabetes_frame,text="Please enter the inputs",font="Times 15").place(x=400,y=100)

pregnancies=tk.Entry(diabetes_frame,width=20)
pregnancies.insert(string="Pregnancies...",index=0)
pregnancies.place(x=200,y=200)

Glucose=tk.Entry(diabetes_frame,width=20)
Glucose.insert(string="Glucose...",index=0)
Glucose.place(x=350,y=200)

BloodPressure=tk.Entry(diabetes_frame,width=20)
BloodPressure.insert(string="BloodPressure...",index=0)
BloodPressure.place(x=500,y=200)

SkinThickness=tk.Entry(diabetes_frame,width=20)
SkinThickness.insert(string="SkinThickness...",index=0)
SkinThickness.place(x=650,y=200)

Insulin=tk.Entry(diabetes_frame,width=20)
Insulin.insert(string="Insulin...",index=0)
Insulin.place(x=200,y=250)

BMI=tk.Entry(diabetes_frame,width=20)
BMI.insert(string="BMI...",index=0)
BMI.place(x=350,y=250)

DiabetesPedigreeFunction=tk.Entry(diabetes_frame,width=20)
DiabetesPedigreeFunction.insert(string="DiabetesPedigreeFunction...",index=0)
DiabetesPedigreeFunction.place(x=500,y=250)
          
Age=tk.Entry(diabetes_frame,width=20)
Age.insert(string="Age...",index=0)
Age.place(x=650,y=250)        
diabetes_risk_var = tk.DoubleVar(value=0)

diabetes_bar = ttk.Progressbar(diabetes_frame, orient="horizontal",length=320, mode="determinate",maximum=100, variable=diabetes_risk_var)
diabetes_bar.place(x=320, y=440)
diabetes_result_label = tk.Label(diabetes_frame, text="Diabetes Risk: %0.00", font=("Helvetica", 12))
diabetes_result_label.place(x=330, y=470)


def diabetesPredict():
    pregnanciesValue=pregnancies.get()
    glucoseValue=Glucose.get()
    bloodPresureValue=BloodPressure.get()
    skinThicknessValue=SkinThickness.get()
    InsulinValue=Insulin.get()
    BMIValue=BMI.get()
    pedigreeValue=DiabetesPedigreeFunction.get()
    ageValue=Age.get()

    try:
        pregnanciesValue = float(pregnanciesValue)
        glucoseValue = float(glucoseValue)
        bloodPresureValue = float(bloodPresureValue)
        skinThicknessValue = float(skinThicknessValue)
        InsulinValue = float(InsulinValue)
        BMIValue = float(BMIValue)
        pedigreeValue = float(pedigreeValue)
        ageValue = float(ageValue)

    except ValueError:
        messagebox.showerror("Value Error", "Please enter numeric values!")
        return
    
    diabetes_model=pickle.load(open("diabetes_model","rb"))
    x2=[[pregnanciesValue,glucoseValue,bloodPresureValue,skinThicknessValue,InsulinValue,BMIValue,pedigreeValue,ageValue]]
    prob_diabetes = diabetes_model.predict_proba(x2)
    risk_diabates = prob_diabetes[0][1]
    result2=f"Diabetes Risk: %{risk_diabates*100:.2f}"
    risk_percent = risk_diabates * 100
    diabetes_risk_var.set(risk_percent)
    diabetes_result_label.config(text=f"Diabetes Risk: %{risk_percent:.2f}")
    alert2=tk.Label(diabetes_frame,text="This is NOT a medical diagnosis. Please consult a doctor.",font=("Helvetica", 8),fg="red").place(x=340,y=520)
    
    if risk_percent < 33:
        diabetes_result_label.config(fg="green")
    elif risk_percent < 66:
        diabetes_result_label.config(fg="orange")
    else:
        diabetes_result_label.config(fg="red")

    
diabetes_button=tk.Button(diabetes_frame,text="Predict",activebackground="green",height=2,width=20,command=diabetesPredict).place(x=300,y=350)
back_button2=tk.Button(diabetes_frame,text="Back",activebackground="red",height=2,width=20,command=back).place(x=500,y=350)

#liver screen
label5=tk.Label(liver_frame,text="Please enter the inputs",font="Times 15").place(x=400,y=100)

Age2=tk.Entry(liver_frame,width=20)
Age2.insert(string="Age...",index=0)
Age2.place(x=200,y=170)

gender2=tk.StringVar()
gender_comboBox2=ttk.Combobox(liver_frame,textvariable=gender2,values=("Female","Male"),state="readonly").place(x=350,y=170)

TotalBilirubin=tk.Entry(liver_frame,width=20)
TotalBilirubin.insert(string="TotalBilirubin...",index=0)
TotalBilirubin.place(x=500,y=170)

DirectBilirubin=tk.Entry(liver_frame,width=20)
DirectBilirubin.insert(string="DirectBilirubin...",index=0)
DirectBilirubin.place(x=650,y=170)

AlkphosAlkalinePhosphotase=tk.Entry(liver_frame,width=20)
AlkphosAlkalinePhosphotase.insert(string="AlkphosAlkalinePhosphotase...",index=0)
AlkphosAlkalinePhosphotase.place(x=200,y=220)

Sgpt=tk.Entry(liver_frame,width=20)
Sgpt.insert(string="SgptAlamineAminotransferase...",index=0)
Sgpt.place(x=350,y=220)

Sgot=tk.Entry(liver_frame,width=20)
Sgot.insert(string="SgotAspartateAminotransferase...",index=0)
Sgot.place(x=500,y=220)
          
TotalProtiens=tk.Entry(liver_frame,width=20)
TotalProtiens.insert(string="TotalProtiens...",index=0)
TotalProtiens.place(x=650,y=220)

ALB=tk.Entry(liver_frame,width=20)
ALB.insert(string="ALBAlbumin...",index=0)
ALB.place(x=350,y=270) 

A_G=tk.Entry(liver_frame,width=20)
A_G.insert(string="AlbuminAndGlobulinRatio...",index=0)
A_G.place(x=500,y=270)  

liver_risk_var = tk.DoubleVar(value=0)

liver_bar = ttk.Progressbar(liver_frame, orient="horizontal",length=320, mode="determinate",maximum=100, variable=liver_risk_var)
liver_bar.place(x=320, y=440)
liver_result_label = tk.Label(liver_frame, text="Liver Disease Risk: %0.00", font=("Helvetica", 12))
liver_result_label.place(x=330, y=470)
    

def liverPredict():
    age2Value=Age2.get()
    gender2Value=gender2.get()
    if(gender2Value=="Male"):
        gender2Value=1
    elif(gender2Value=="Female"):
        gender2Value=0
    else:
        messagebox.showerror("Gender Error", "Please select a gender!")
        return
    TotalBilirubinValue=TotalBilirubin.get()
    DirectBilirubinValue=DirectBilirubin.get()
    AlkphosAlkalinePhosphotaseValue=AlkphosAlkalinePhosphotase.get()
    SgptValue=Sgpt.get()
    SgotValue=Sgot.get()
    TotalProtiensValue=TotalProtiens.get()
    ALBValue=ALB.get()
    A_GValue=A_G.get()

    try:
        age2Value = float(age2Value)
        TotalBilirubinValue = float(TotalBilirubinValue)
        DirectBilirubinValue = float(DirectBilirubinValue)
        AlkphosAlkalinePhosphotaseValue = float(AlkphosAlkalinePhosphotaseValue)
        SgptValue = float(SgptValue)
        SgotValue = float(SgotValue)
        TotalProtiensValue = float(TotalProtiensValue)
        ALBValue = float(ALBValue)
        A_GValue = float(A_GValue)

    except ValueError:
        messagebox.showerror("Value Error", "Please enter numeric values!")
        return
    
    liver_model=pickle.load(open("liver_model","rb"))
    x3=[[age2Value,gender2Value,TotalBilirubinValue,DirectBilirubinValue,AlkphosAlkalinePhosphotaseValue,SgptValue,SgotValue,TotalProtiensValue,ALBValue,A_GValue]]
    prob_liver = liver_model.predict_proba(x3)
    risk_liver = prob_liver[0][1]
    result3=f"Liver Disease Risk: %{risk_liver*100:.2f}"
    risk_percent = risk_liver * 100
    liver_risk_var.set(risk_percent)
    liver_result_label.config(text=f"Liver Disease Risk: %{risk_percent:.2f}")
    alert3=tk.Label(liver_frame,text="This is NOT a medical diagnosis. Please consult a doctor.",font=("Helvetica", 8),fg="red").place(x=340,y=520)
    
    if risk_percent < 33:
        liver_result_label.config(fg="green")
    elif risk_percent < 66:
        liver_result_label.config(fg="orange")
    else:
        liver_result_label.config(fg="red")

    

liver_button=tk.Button(liver_frame,text="Predict",activebackground="green",height=2,width=20,command=liverPredict).place(x=300,y=350)
back_button3=tk.Button(liver_frame,text="Back",activebackground="red",height=2,width=20,command=back).place(x=500,y=350)


window.mainloop()