# run.py
# conda activate DoctorNam 
# python 3.6.9 64bit('kobv4':virtualenv)

from main import app



if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=9000)
    
