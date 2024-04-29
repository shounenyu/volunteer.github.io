#連線資料庫
import mysql.connector
con=mysql.connector.connect(
    user="root",
    password="12345678",
    host="localhost",
    database="voldb",
    port=3305
)
print("連線成功")


#網頁架構
from flask import*
app=Flask(
    __name__,
    static_folder="public",
    static_url_path="/"
)
app.secret_key="any string but secret"
#算日期
from datetime import date, timedelta
import calendar
import datetime

#路由
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/signup",methods= ["POST"])
def signup():
    account=request.form["account"]
    password=request.form["password"]
    
    if account=="1111" and password=="1111":
        return render_template("host.html") 
    else:
        return render_template("error.html",message="輸入錯誤")

@app.route("/host")
def host():
     return render_template("host.html")

@app.route("/data")
def data():
  cursor = con.cursor()
  cursor.execute("SELECT * FROM volun")
  result = cursor.fetchall()
  cursor.close()
  return render_template("data.html", data=result)
   
@app.route("/add")
def add():
    return render_template("add.html")

@app.route("/add1", methods=["POST"])
def add1():
    number = request.form["number"]
    volname = request.form["volname"]
    sex = request.form["sex"]
    inday = request.form["inday"]
    birth = request.form["birth"]
    indentyid = request.form["indentyid"]
    phone = request.form["phone"]
    cell = request.form["cell"]
    enman = request.form["enman"]
    enmanphone = request.form["enmanphone"]
    address = request.form["address"]
    email = request.form["email"]
    workday = request.form["workday"]
    workday1 = request.form["workday1"]
    
    cursor = con.cursor()
    cursor.execute("SELECT * FROM volun WHERE volname = %s", (volname,))
    result = cursor.fetchone()
    cursor.execute("SELECT * FROM volun WHERE number = %s", (number,))
    result1 = cursor.fetchone()

    if result is not None:
        return render_template("error.html", message="此人已存在")
    elif result1 is not None:
        return render_template("error.html", message="此號碼已存在")
    else:
        cursor.execute("INSERT INTO volun (number, volname, sex, inday, birth, indentyid, phone, cell, enman, enmanphone, address, email, workday, workday1) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                       (number, volname, sex, inday, birth, indentyid, phone, cell, enman, enmanphone, address, email, workday, workday1,))
        con.commit()
        cursor.execute("INSERT INTO hours (volname) VALUES (%s)", (volname,))
        con.commit()
        cursor.execute("INSERT INTO reason (volname) VALUES (%s)", (volname,))
        return render_template("error.html", message="成功新增")
    
@app.route("/change")
def change():
    cursor = con.cursor()
    cursor.execute("SELECT * FROM volun")
    result = cursor.fetchall()
    cursor.close()
    return render_template("change.html", data=result)

@app.route("/delete", methods=["POST"])
def delete():
    volname = request.form.get("volname")
    cursor = con.cursor()
    cursor.execute("DELETE FROM volun WHERE volname = %s", (volname,))
    con.commit() 
    cursor.execute("DELETE FROM reason WHERE volname = %s", (volname,))
    con.commit() 
    cursor.execute("DELETE FROM hours WHERE volname = %s", (volname,))
    con.commit() 
    return render_template("error.html", message="刪除成功")

@app.route("/update", methods=["POST"])
def update():
    volname = request.form.get("volname")
    number = request.form.get("number")

    # 將原始資料填充到表單欄位
    sex = request.form.get("sex")
    inday = request.form.get("inday")
    birth = request.form.get("birth")
    indentyid = request.form.get("indentyid")
    cell = request.form.get("cell")
    phone = request.form.get("phone")
    enman = request.form.get("enman")
    enmanphone = request.form.get("enmanphone")
    address = request.form.get("address")
    email = request.form.get("email")
    workday = request.form.get("workday")
    workday1 = request.form.get("workday1")

    cursor = con.cursor()
    cursor.execute("UPDATE volun SET sex = %s, inday = %s, birth = %s, indentyid = %s, cell = %s, phone = %s, enman = %s, enmanphone = %s, address = %s, email = %s, workday = %s, workday1 = %s WHERE  volname=%s and number=%s",
    ( sex, inday, birth, indentyid, cell, phone, enman, enmanphone, address, email, workday, workday1,volname,number,))
    con.commit()

    return render_template("error.html", message="更新成功")


@app.route("/workday")
def workday():
  cursor = con.cursor()
  cursor.execute("SELECT volun.number, volun.volname,volun.workday,volun.workday1 FROM volun")
  result = cursor.fetchall()
  cursor.close()
  return render_template("workday.html", data=result)

@app.route("/holiday")
def holiday():
  cursor = con.cursor()
  cursor.execute("SELECT * FROM holiday")
  result = cursor.fetchall()
  cursor.close()
  return render_template("holiday.html", data=result)

@app.route("/holiday1", methods=["POST"])
def day1():
    holiname = request.form.get("holiname")
    holiday = request.form.get("holiday")
    day = request.form.get("day")

    cursor = con.cursor()
    cursor.execute("SELECT * FROM holiday WHERE holiday = %s", (holiday,))
    result = cursor.fetchone()

    if holiday == "" or holiname == ""or day == "":
        return render_template("error.html", message="請輸入完整")
    elif result != None:
        return render_template("error.html", message="節日已存在")
    else:
        cursor.execute("INSERT INTO holiday (holiname, holiday,day) VALUES (%s, %s,%s)", (holiname, holiday,day,))
        con.commit()
        return render_template("error.html", message="新增成功")
    
@app.route("/holiday2", methods=["POST"])
def holiday2():
    holiname = request.form.get("holiname")
    cursor = con.cursor()
    cursor.execute("DELETE FROM holiday WHERE holiname = %s", (holiname,))
    con.commit() 
    return render_template("error.html", message="刪除成功")


    
@app.route("/sign")
def sign():
  cursor = con.cursor()
  cursor.execute("SELECT * FROM reason WHERE reason IS NOT NULL")
  result = cursor.fetchall()
  cursor.close()
  return render_template("sign.html", data=result)

@app.route("/sign1", methods=["POST"])
def sign1():
    volname = request.form.get("volname")
    dayy = request.form.get("dayy")
    reason=request.form.get("reason")
    ty=request.form.get("ty")
    hours=request.form.get("hours")
    cursor = con.cursor()

    cursor.execute("SELECT * FROM volun WHERE volname = %s", (volname,))
    result = cursor.fetchone()
    
    if volname == "" or dayy == "" or reason ==""or ty ==""or hours =="":
        return render_template("error.html", message="請輸入完整")
    elif result == None:
        return render_template("error.html", message="查無此人")
    elif ty == "+":
        cursor.execute("UPDATE hours SET hours = hours + %s WHERE volname=%s",(hours,volname,))
        con.commit()
        cursor.execute("INSERT INTO reason (volname, dayy, reason, ty, hours) VALUES (%s, %s,%s,%s,%s)", (volname,dayy,reason,ty,hours))
        con.commit()
        return render_template("error.html", message="新增成功")
    else:
        cursor.execute("UPDATE hours SET hours = hours - %s WHERE volname=%s",(hours,volname,))
        con.commit()
        cursor.execute("INSERT INTO reason (volname, dayy, reason, ty, hours) VALUES (%s, %s,%s,%s,%s)", (volname,dayy,reason,ty,hours))
        con.commit()
        return render_template("error.html", message="新增成功")
@app.route("/sign2", methods=["POST"])
def sign2():
    volname = request.form.get("volname")
    dayy = request.form.get("dayy")
    reason=request.form.get("reason")
    cursor = con.cursor()
    cursor.execute("DELETE FROM reason WHERE volname = %s and dayy=%s and reason=%s ", (volname,dayy,reason,))
    con.commit() 
    return render_template("error.html", message="刪除成功")


@app.route("/count")
def count():
    cursor = con.cursor()
    cursor.execute("SELECT volname FROM volun")
    volname_data = cursor.fetchall()
    volname_list = [row[0] for row in volname_data]
 

    def count_weekday(year, start_month, end_month, weekdays):
        count = 0
        for month in range(start_month, end_month + 1):
            _, num_days = calendar.monthrange(year, month)
            if month == end_month:
                num_days = date.today().day  # Use current day for the last month
            for day in range(1, num_days + 1):
                current_date = date(year, month, day)
                if current_date.weekday() in weekdays:
                    count += 1
        return count

           

    for volname in volname_list:
       cursor.execute("SELECT ty,hours FROM reason WHERE volname = %s", (volname,))
       ty_data=cursor.fetchall()
       ty_list = [(row[0],row[1])for row in ty_data]
       hou=0
       for ty ,hours in ty_list:
           if ty=="+":
               hou += hours
           else:
               hou -= hours
    print(ty_list)
    return render_template("error.html", message=ty_list)



    

app.run(port=3000)
con.close()#關閉