import tkinter as tk
from tkinter import messagebox
import csv
import random
import sqlite3  # Use sqlite3 instead of mysql.connector
from PIL import Image, ImageTk  # Add this import for image support
import os

# --- LOGIN WINDOW ---
def show_login(root):
    login_frame = tk.Frame(root)
    login_frame.pack(expand=True)
    
    # Add logo image at the top
    logo_path = r"C:\Users\ap494\Desktop\ADCA\logo.png"
    if os.path.exists(logo_path):
        logo_img = Image.open(logo_path)
        logo_img = logo_img.resize((120, 120))  # Adjust size as needed
        logo_photo = ImageTk.PhotoImage(logo_img)
        logo_label = tk.Label(login_frame, image=logo_photo)
        logo_label.image = logo_photo  # Keep a reference
        logo_label.pack(pady=10)

    tk.Label(login_frame, text="NET-TECH ACADEMY OF COMPUTER TECHNOLOGY ", font=("Arial", 25, "bold")).pack(pady=10)
    tk.Label(login_frame, text="Username:", font=("Arial", 14)).pack(pady=(20, 5))
    user_entry = tk.Entry(login_frame, font=("Arial", 14))
    user_entry.pack()
    tk.Label(login_frame, text="Password:", font=("Arial", 14)).pack(pady=(15, 5))
    pass_entry = tk.Entry(login_frame, font=("Arial", 14), show="*")
    pass_entry.pack()

    def validate_inputs(*args):
        username = user_entry.get().strip()
        pwd = pass_entry.get().strip()
        if not username or not pwd:
            start_btn.config(state="disabled")
            return
        # CSV check
        csv_path = os.path.join(os.path.dirname(__file__), "students.csv")
        found = False
        if os.path.exists(csv_path):
            with open(csv_path, "r", newline='', encoding="utf-8") as f:
                reader = csv.reader(f)
                for row in reader:
                    if row and row[0] == username and row[1] == pwd:
                        found = True
                        break
        if found:
            start_btn.config(state="normal")
        else:
            start_btn.config(state="disabled")

    user_entry.bind('<KeyRelease>', validate_inputs)
    pass_entry.bind('<KeyRelease>', validate_inputs)

    def start_exam():
        global current_username, current_password
        current_username = user_entry.get().strip()
        current_password = pass_entry.get().strip()
        login_frame.destroy()
        start_quiz(root)

    start_btn = tk.Button(login_frame, text="Start Exam", font=("Arial", 14), command=start_exam, bg="#2196F3", fg="white", state="disabled")
    start_btn.pack(pady=25)

    # Admin User Button
    def open_admin_login():
        admin_login_popup(root)

    admin_btn = tk.Button(login_frame, text="Admin User", font=("Arial", 14), command=open_admin_login, bg="#FF9800", fg="white")
    admin_btn.pack(pady=5)

def admin_login_popup(root):
    popup = tk.Toplevel(root)
    popup.title("Admin Login")
    popup.geometry("350x200")
    tk.Label(popup, text="Admin User ID:", font=("Arial", 12)).pack(pady=10)
    admin_user_entry = tk.Entry(popup, font=("Arial", 12))
    admin_user_entry.pack()
    tk.Label(popup, text="Password:", font=("Arial", 12)).pack(pady=10)
    admin_pass_entry = tk.Entry(popup, font=("Arial", 12), show="*")
    admin_pass_entry.pack()

    def check_admin():
        user = admin_user_entry.get().strip()
        pwd = admin_pass_entry.get().strip()
        if user == "Golu@123" and pwd == "Golu@565453":
            popup.destroy()
            open_student_registration(root)
        else:
            messagebox.showerror("Error", "Invalid Admin credentials!")

    tk.Button(popup, text="Login", font=("Arial", 12), command=check_admin, bg="#2196F3", fg="white").pack(pady=15)

def open_student_registration(root):
    reg_win = tk.Toplevel(root)
    reg_win.title("Student Registration")
    reg_win.geometry("400x300")
    tk.Label(reg_win, text="Add New Student", font=("Arial", 16, "bold")).pack(pady=10)
    tk.Label(reg_win, text="Username:", font=("Arial", 12)).pack(pady=5)
    username_entry = tk.Entry(reg_win, font=("Arial", 12))
    username_entry.pack()
    tk.Label(reg_win, text="Password:", font=("Arial", 12)).pack(pady=5)
    password_entry = tk.Entry(reg_win, font=("Arial", 12))
    password_entry.pack()

    def add_student():
        uname = username_entry.get().strip()
        pwd = password_entry.get().strip()
        if not uname or not pwd:
            messagebox.showerror("Error", "Username and Password required!")
            return
        try:
            add_user(uname, pwd)
            messagebox.showinfo("Success", "Student added successfully!")
            username_entry.delete(0, tk.END)
            password_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"Could not add student: {e}")

    tk.Button(reg_win, text="Add Student", font=("Arial", 12), command=add_student, bg="#4CAF50", fg="white").pack(pady=20)

# --- QUIZ CODE MOVED TO FUNCTION ---
def start_quiz(root):
    # 50 Questions
    global questions, question_index, selected_option, user_answers, timer_seconds, timer_id, exam_time_left
    questions = [
        #1
        {
            "question": "कंप्यूटर का जनक किसे कहा जाता है?",
            "options": ["A. चार्ल्स बैबेज", "B. आलन ट्यूरिंग", "C. बिल गेट्स", "D. स्टीव जॉब्स"],
            "answer": "A. चार्ल्स बैबेज"
        },
        #2
        {
            "question": "CPU का मुख्य कार्य क्या है?",
            "options": ["A. डेटा स्टोर करना", "B. प्रोसेसिंग करना", "C. प्रिंट करना", "D. इनपुट लेना"],
            "answer": "B. प्रोसेसिंग करना"
        },
        #3
        {
            "question": "MS Word किस प्रकार का सॉफ्टवेयर है?",
            "options": ["A. Spreadsheet", "B. Word Processor", "C. Database", "D. Presentation"],
            "answer": "B. Word Processor"
        },
        #4
        {
            "question": "इंटरनेट का फुल फॉर्म क्या है?",
            "options": ["A. Interconnected Network", "B. Internal Net", "C. International Net", "D. Integrated Network"],
            "answer": "A. Interconnected Network"
        },
        #5
        {
            "question": "MS Excel में formula शुरू करने के लिए कौन सा चिन्ह प्रयोग होता है?",
            "options": ["A. @", "B. #", "C. =", "D. +"],
            "answer": "C. ="
        },
        #6
        {
            "question": "कंप्यूटर में डेटा को स्थायी रूप से कहाँ स्टोर किया जाता है?",
            "options": ["A. RAM", "B. ROM", "C. Hard Disk", "D. Cache"],
            "answer": "C. Hard Disk"
        },
        #7
        {
            "question": "MS PowerPoint का उपयोग किस लिए किया जाता है?",
            "options": ["A. डॉक्युमेंट लिखने के लिए", "B. डेटा स्टोर करने के लिए", "C. प्रेजेंटेशन बनाने के लिए", "D. कोडिंग के लिए"],
            "answer": "C. प्रेजेंटेशन बनाने के लिए"
        },
        #8
        {
            "question": "कंप्यूटर में 'Input Device' का उदाहरण क्या है?",
            "options": [" A. प्रिंटर", "B. मॉनिटर", "C. कीबोर्ड", "D. स्पीकर"],
            "answer": "C. कीबोर्ड"
        },
        #9
        {
            "question": "WWW का अविष्कार किसने किया?",
            "options": ["A. बिल गेट्स", "B. टिम बर्नर्स-ली", "C. लैरी पेज", "D. चार्ल्स बैबेज"],
            "answer": "B. टिम बर्नर्स-ली"
        },
        #10
        {
            "question": "MS Excel में कॉलम को कैसे दर्शाया जाता है?",
            "options": ["A. संख्या (1, 2, 3...)", "B. अक्षर (A, B, C...)", "C. संख्या और अक्षर दोनों", "D. कोई नहीं"],
            "answer": "B. अक्षर (A, B, C...)"
        },
        #11
        {
            "question": "RAM का पूरा नाम क्या है?",
            "options": ["A. Random Access Memory", "B. Read Access Memory", "C. Run Access Memory", "D. Real Access Memory"],
            "answer": "A. Random Access Memory"
        },
        #12
        {
            "question": "ROM का मुख्य कार्य क्या है?",
            "options": ["A. डेटा प्रोसेस करना", "B. स्थायी डेटा स्टोर करना", "C. प्रिंट करना", "D. नेटवर्किंग"],
            "answer": "B. स्थायी डेटा स्टोर करना"
        },
        #13
        {
            "question": "कंप्यूटर में सबसे तेज़ मेमोरी कौन सी होती है?",
            "options": ["A. RAM", "B. ROM", "C. Cache", "D. Hard Disk"],
            "answer": "C. Cache"
        },
        #14
        {
            "question": "कंप्यूटर वायरस क्या है?",
            "options": ["A. एक हार्डवेयर", "B. एक सॉफ्टवेयर", "C. एक प्रोग्राम जो नुकसान करता है", "D. एक नेटवर्क"],
            "answer": "C. एक प्रोग्राम जो नुकसान करता है"
        },
        #15
        {
            "question": "URL का फुल फॉर्म क्या है?",
            "options": ["A. Uniform Resource Locator", "B. Universal Resource Link", "C. Unified Resource Locator", "D. Uniform Reference Link"],
            "answer": "A. Uniform Resource Locator"
        },
        #16
        {
            "question": "MS PowerPoint में नई स्लाइड जोड़ने की shortcut key क्या है?",
            "options": ["A. Ctrl + N", "B. Ctrl + M", "C. Ctrl + S", "D. Ctrl + P"],
            "answer": "B. Ctrl + M"
        },
        #17
        {
            "question": "कंप्यूटर में 'Output Device' का उदाहरण क्या है?",
            "options": ["A. कीबोर्ड", "B. माउस", "C. मॉनिटर", "D. स्कैनर"],
            "answer": "C. मॉनिटर"
        },   
        #18
        {
            "question": "IP Address का उपयोग किस लिए होता है?",
            "options": ["A. डेटा स्टोर करने के लिए", "B. नेटवर्क पहचान के लिए", "C. प्रिंटिंग के लिए", "D.कोडिंग के लिए"],
            "answer": "B. नेटवर्क पहचान के लिए"
        },
        #19
        {
            "question": "MS Word में 'Bold' करने के लिए कौन सी shortcut key होती है?",
            "options": ["A. Ctrl + B", "B. Ctrl + I", "C. Ctrl + U", "D. Ctrl + P"],
            "answer": "A. Ctrl + B"
        },
        #20
        {
            "question": "कंप्यूटर में सबसे बड़ी मेमोरी कौन सी होती है?",
            "options": ["A. RAM", "B. ROM", "C. Cache", "D. Hard Disk"],
            "answer": "D. Hard Disk"
        },
        #21
        {
            "question": " कंप्यूटर का पूरा नाम क्या है?",
            "options": ["A. Common Operating Machine Purposely Used for Technological and Educational Research", "B. Central Operating Machine", "C. Control Operating Machine", "D. None of these"],
            "answer": "A. Common Operating Machine Purposely Used for Technological and Educational Research"
        },
        #22
        {
            "question": " CPU का फुल फॉर्म क्या है?",
            "options": ["A. Central Process Unit", "B. Central Processing Unit", "C. Control Processing Unit", "D. Central Performance Unit"],
            "answer": "B. Central Processing Unit"
        },
        #23
        {
            "question": " RAM का फुल फॉर्म क्या है?",
            "options": ["A. Random Access Memory", "B. Read Access Memory", "C. Run Access Memory", "D. None of these"],
            "answer": "A. Random Access Memory"
        },
        #24
        {
            "question": " कंप्यूटर की मुख्य भाषा कौन सी होती है?",
            "options": ["A. हाई लेवल लैंग्वेज", "B. लो लेवल लैंग्वेज", "C. मशीन लैंग्वेज", "D. C लैंग्वेज"],
            "answer": "C. मशीन लैंग्वेज"
        },
        #25
        {
            "question": " हार्ड डिस्क किस प्रकार की मेमोरी है?",
            "options": ["A. प्राइमरी मेमोरी", "B. सेकेंडरी मेमोरी", "C. कैश मेमोरी", "D. ROM"],
            "answer": "B. सेकेंडरी मेमोरी"
        },
        #26
        {
            "question": " कंप्यूटर का जनक किसे कहा जाता है?",
            "options": ["A. Charles Babbage", "B. Alan Turing", "C. Bill Gates", "D. Steve Jobs"],
            "answer": "A. Charles Babbage"
        },
        #27
        {
            "question": " Ctrl + C किसके लिए प्रयोग होता है?",
            "options": ["A. कट करने के लिए", "B. पेस्ट करने के लिए", "C. कॉपी करने के लिए", "D. सेव करने के लिए"],
            "answer": "C. कॉपी करने के लिए"
        },
        #28
        {
            "question": " कंप्यूटर में उपयोग होने वाली संख्या प्रणाली क्या है?",
            "options": ["A. दशमलव", "B. बाइनरी", "C. हेक्साडेसिमल", "D. ऑक्टल"],
            "answer": "B. बाइनरी"
        },
        #29
        {
            "question": " प्रोग्रामिंग लैंग्वेज कौन सी होती है?",
            "options": ["A. Java", "B. Python", "C. C++", "D. उपरोक्त सभी"],
            "answer": "D. उपरोक्त सभी"
        },
        #30
        {
            "question": " वेब ब्राउज़र का उदाहरण क्या है?",
            "options": ["A. MS Word", "B. Google Chrome", "C. Paint", "D. Excel"],
            "answer": "B. Google Chrome"
        },
        #31
        {
            "question": " कंप्यूटर की पहली पीढ़ी किस तकनीक पर आधारित थी?",
            "options": ["A. ट्रांजिस्टर", "B. वैक्यूम ट्यूब", "C. IC", "D. माइक्रोप्रोसेसर"],
            "answer": "B. वैक्यूम ट्यूब"
        },
        #32
        {
            "question": " एक बाइट में कितने बिट होते हैं?",
            "options": ["A. 4", "B. 8", "C. 16", "D. 2"],
            "answer": "B. 8"
        },
        #33
        {
            "question": " कंप्यूटर को चालू करने की प्रक्रिया को क्या कहते हैं?",
            "options": ["A. लोडिंग", "B. स्टार्टिंग", "C. बूटिंग", "D. इंस्टॉलिंग"],
            "answer": "C. बूटिंग"
        },
        #34
        {
            "question": " माइक्रोसॉफ्ट वर्ड किस प्रकार का सॉफ्टवेयर है?",
            "options": ["A. सिस्टम सॉफ्टवेयर", "B. एप्लीकेशन सॉफ्टवेयर", "C. यूटिलिटी सॉफ्टवेयर", "D. ऑपरेटिंग सिस्टम"],
            "answer": "B. एप्लीकेशन सॉफ्टवेयर"
        },
        #35
        {
            "question": " कंप्यूटर में वायरस क्या होता है?",
            "options": ["A. हार्डवेयर डिवाइस", "B. ऑपरेटिंग सिस्टम", "C. हानिकारक प्रोग्राम", "D. नेटवर्क"],
            "answer": "C. हानिकारक प्रोग्राम"
        },
        #36
        {
            "question": " MS-DOS का पूरा नाम क्या है?",
            "options": ["A. Microsoft Disk Operating System", "B. Micro Soft Drive Operating System", "C. Microsoft Directory Operating System", "D. None of these"],
            "answer": "A. Microsoft Disk Operating System"
        },
        #37
        {
            "question": " MS-DOS किस प्रकार का ऑपरेटिंग सिस्टम है?",
            "options": ["A. मल्टी-यूज़र", "B. मल्टी-टास्किंग", "C. सिंगल-यूज़र सिंगल-टास्किंग", "D. सिंगल-यूज़र मल्टी-टास्किंग"],
            "answer": "C. सिंगल-यूज़र सिंगल-टास्किंग"
        },
        #38
        {
            "question": " DOS में फाइल का एक्सटेंशन कितने अक्षरों का होता है?",
            "options": ["A. 3 अक्षर", "B. 5 अक्षर", "C. 4 अक्षर", "D. कोई सीमा नहीं"],
            "answer": "A. 3 अक्षर"
        },
        #39
        {
            "question": " DOS में DIR कमांड का प्रयोग किसके लिए होता है?",
            "options": ["A. डायरेक्टरी बनाने के लिए", "B. फाइल को डिलीट करने के लिए", "C. डायरेक्टरी सूची देखने के लिए", "D. फाइल रन करने के लिए"],
            "answer": "C. डायरेक्टरी सूची देखने के लिए"
        },
        #40
        {
            "question": " DOS में फाइल डिलीट करने के लिए किस कमांड का प्रयोग होता है?",
            "options": ["A. REMOVE", "B. ERASE", "C. DELETE", "D. DEL"],
            "answer": "D. DEL"
        },
        #41
        {
            "question": " DOS में सिस्टम को बंद करने की प्रक्रिया को क्या कहते हैं?",
            "options": ["A. स्टार्टअप", "B. शटडाउन", "C. लॉगआउट", "D. रीबूट"],
            "answer": "B. शटडाउन"
        },
        #42
        {
            "question": " DOS में MD कमांड का उपयोग किस लिए होता है?",
            "options": ["A. डायरेक्टरी हटाने के लिए", "B. डायरेक्टरी बनाने के लिए", "C. फाइल खोलने के लिए", "D. सिस्टम बंद करने के लिए"],
            "answer": "B. डायरेक्टरी बनाने के लिए"
        },
        #43
        {
            "question": " DOS का पहला संस्करण किस वर्ष जारी किया गया था?",
            "options": ["A. 1980", "B. 1981", "C. 1985", "D. 1990"],
            "answer": "B. 1981"
        },
        #44
        {
            "question": " DOS में कौन-सी कमांड फाइल कॉपी करने के लिए प्रयोग होती है?",
            "options": ["A. COPY", "B. CP", "C. PASTE", "D. MOVE"],
            "answer": "A. COPY"
        },
        #45
       # {
        #     "question": " DOS का डिफ़ॉल्ट प्रॉम्प्ट क्या होता है?",
        #     "options":["A.C:\>", "B.D:\>", "C.A:\>", "D.C:/"],
        #     "answer": "A"
        # },
        #46
        {
            "question": " DOS किस प्रकार का इंटरफेस प्रदान करता है?",
            "options": ["A. ग्राफिकल यूज़र इंटरफेस", "B. टेक्स्ट बेस्ड इंटरफेस", "C. आइकन बेस्ड", "D. वॉइस बेस्ड"],
            "answer": "B. टेक्स्ट बेस्ड इंटरफेस"
        },
        #47
        {
            "question": " DOS में 'CLS' कमांड क्या करती है?",
            "options": ["A. स्क्रीन क्लियर करती है", "B. फाइल सेव करती है", "C. डायरेक्टरी बदलती है", "D. कोई कार्य नहीं"],
            "answer": "A. स्क्रीन क्लियर करती है"
        },
        #48
        {
            "question": " DOS में XCOPY किस लिए प्रयोग होती है?",
            "options": ["A. फाइल डिलीट करने के लिए", "B. एडवांस कॉपी ऑपरेशन के लिए", "C. डायरेक्टरी बनाने के लिए", "D. फाइल रन करने के लिए"],
            "answer": "B. एडवांस कॉपी ऑपरेशन के लिए"
        },
        #49
        {
            "question": " DOS में फाइल की साइज देखने के लिए किस कमांड का प्रयोग होता है?",
            "options": ["A. SIZE", "B. VOL", "C. DIR", "D. MEM"],
            "answer": "C. DIR"
        },
        #50
        {
            "question": " DOS किस प्रकार का सॉफ्टवेयर है?",
            "options": ["A. सिस्टम सॉफ्टवेयर", "B. एप्लिकेशन सॉफ्टवेयर", "C. यूटिलिटी सॉफ्टवेयर", "D. डिवाइस सॉफ्टवेयर"],
            "answer": "A. सिस्टम सॉफ्टवेयर"
        },
        #51
        {
            "question": " MS Paint किस प्रकार का सॉफ्टवेयर है?",
            "options": ["A. वर्ड प्रोसेसर", "B. ग्राफिक्स प्रोग्राम", "C. डेटाबेस सॉफ्टवेयर", "D. स्प्रेडशीट प्रोग्राम"],
            "answer": "B. ग्राफिक्स प्रोग्राम"
        },
        #52
        {
            "question": " MS Paint में किस टूल का उपयोग आकृति भरने के लिए किया जाता है?",
            "options": ["A. Pencil Tool", "B. Eraser Tool", "C. Fill with color", "D. Pick color"],
            "answer": "C. Fill with colo"
        },
        #53
        {
            "question": " MS Paint में आकृति बनाने के लिए किस टूल का उपयोग होता है?",
            "options": ["A. Magnifier", "B. Shapes", "C. Text Tool", "D. Select"],
            "answer": "B. Shapes"
        },
        #54
        {
            "question": " MS Paint में Undo shortcut key क्या है?",
            "options": ["A. Ctrl + Z", "B. Ctrl + X", "C. Ctrl + C", "D. Ctrl + V"],
            "answer": "A. Ctrl + Z"
        },
        #55
        {
            "question": " MS Paint में फाइल को सेव करने के लिए किस मेनू का उपयोग किया जाता है?",
            "options": ["A. Home", "B. View", "C. File", "D. Edit"],
            "answer": "C. File"
        },
        #56
        {
            "question": " MS Paint में एक चित्र को zoom करने के लिए किस टूल का प्रयोग करते हैं?",
            "options": ["A. Pencil", "B. Magnifier", "C. Brush", "D. Color Picker"],
            "answer": "B. Magnifier"
        },
        #57
        {
            "question": " MS Paint में छवि को मिटाने के लिए कौन सा टूल प्रयोग होता है?",
            "options": ["A. Brush", "B. Eraser", "C. Fill Tool", "D. Shapes"],
            "answer": "B. Eraser"
        },
        #58
        {
            "question": " MS Paint का default file format क्या होता है?",
            "options": ["A. .jpg", "B. .bmp", "C. .gif", "D. .png"],
            "answer": "B. .bmp"
        },
        #59
        {
            "question": " MS Paint में Text जोड़ने के लिए किस टूल का प्रयोग किया जाता है?",
            "options": ["A. Text Tool", "B. Brush Tool", "C. Line Tool", "D. Select Tool"],
            "answer": "A. Text Tool"
        },
        #60
        {
            "question": " Color Picker टूल का उपयोग किसके लिए होता है?",
            "options": ["A. रंग भरने के लिए", "B. किसी रंग को चुनने के लिए", "C. चित्र मिटाने के लिए", "D. आकर बनाने के लिए"],
            "answer": "B. किसी रंग को चुनने के लिए"
        },
        #61
        {
            "question": " MS Paint को खोलने के लिए कौन सा shortcut उपयोग होता है?",
            "options": ["A. Win + P", "B. Win + R और फिर 'mspaint'", "C. Ctrl + M", "D. Alt + P"],
            "answer": "B. Win + R और फिर 'mspaint'"
        },
        #62
        {
            "question": " MS Paint में चित्र को उल्टा करने के लिए कौन सा विकल्प प्रयोग होता है?",
            "options": ["A. Resize", "B. Rotate", "C. Flip Horizontal", "D. Crop"],
            "answer": "C. Flip Horizontal"
        },
        #63
        {
            "question": " MS Paint में selection tool का उपयोग क्यों किया जाता है?",
            "options": ["A. रंग भरने के लिए", "B. टेक्स्ट जोड़ने के लिए", "C. किसी भाग को चुनने के लिए", "D. आकृति बनाने के लिए"],
            "answer": "C. किसी भाग को चुनने के लिए"
        },
        #64
        {
            "question": " MS Paint में किस टूल से freehand drawing की जाती है?",
            "options": ["A. Pencil Tool", "B. Shape Tool", "C. Text Tool", "D. Color Tool"],
            "answer": "A. Pencil Tool"
        },
        #65
        {
            "question": " MS Paint किस ऑपरेटिंग सिस्टम में उपलब्ध होता है?",
            "options": ["A. macOS", "B. Linux", "C. Windows", "D. Android"],
            "answer": "C. Windows"
        },
        #66
        {
            "question": " Notepad क्या है?",
            "options": ["A. Word Processor", "B. ग्राफिक्स टूल", "C. टेक्स्ट एडिटर", "D. Spreadsheet"],
            "answer": "C. टेक्स्ट एडिटर"
        },
        #67
        {
            "question": " Notepad किस ऑपरेटिंग सिस्टम का हिस्सा होता है?",
            "options": ["A. Windows", "B. Linux", "C. MacOS", "D. Android"],
            "answer": "A. Windows"
        },
        #68
        {
            "question": " Notepad में किस प्रकार की फाइल सेव होती है?",
            "options": ["A. .doc", "B. .txt", "C. .xls", "D. .ppt"],
            "answer": "B. .txt"
        },
        #69
        {
            "question": " Notepad में टेक्स्ट को सेव करने की shortcut key क्या है?",
            "options": ["A. Ctrl + S", "B. Ctrl + C", "C. Ctrl + V", "D. Ctrl + X"],
            "answer": "A. Ctrl + S"
        },
        #70
        {
            "question": " Notepad का उपयोग किस लिए होता है?",
            "options": ["A. चित्र बनाने के लिए", "B. वीडियो एडिटिंग के लिए", "C. सिंपल टेक्स्ट एडिटिंग के लिए", "D. स्प्रेडशीट बनाने के लिए"],
            "answer": "C. सिंपल टेक्स्ट एडिटिंग के लिए"
        },
        #71
        {
            "question": " Notepad में फॉन्ट बदलने का विकल्प कहाँ मिलता है?",
            "options": ["A. Edit मेन्यू", "B. Format मेन्यू", "C. View मेन्यू", "D. File मेन्यू"],
            "answer": "B. Format मेन्यू"
        },
        #72
        {
            "question": " Notepad में cut command की shortcut key क्या है?",
            "options": ["A. Ctrl + C", "B. Ctrl + X", "C. Ctrl + V", "D. Ctrl + Z"],
            "answer": "B. Ctrl + X"
        },
        #73
        {
            "question": " Notepad में नया दस्तावेज़ खोलने की shortcut key क्या है?",
            "options": ["A. Ctrl + O", "B. Ctrl + N", "C. Ctrl + P", "D. Ctrl + F"],
            "answer": "B. Ctrl + N"
        },
        #74
        {
            "question": " Notepad में find करने की shortcut key क्या है?",
            "options": ["A. Ctrl + F", "B. Ctrl + E", "C. Ctrl + G", "D. Ctrl + H"],
            "answer": "A. Ctrl + F"
        },
        #75
        {
            "question": " Notepad में print करने की shortcut key क्या है?",
            "options": ["A. Ctrl + P", "B. Ctrl + S", "C. Ctrl + T", "D. Ctrl + R"],
            "answer": "A. Ctrl + P"
        },
        #76
        {
            "question": " Notepad में undo करने की shortcut key क्या है?",
            "options": ["A. Ctrl + Z", "B. Ctrl + U", "C. Ctrl + B", "D. Ctrl + Y"],
            "answer": "A. Ctrl + Z"
        },
        #77
        {
            "question": " Notepad में redo करने की shortcut key क्या है?",
            "options": ["A. Ctrl + Z", "B. Ctrl + R", "C. Ctrl + Y", "D. Ctrl + A"],
            "answer": "C. Ctrl + Y"
        },
        #78
        {
            "question": " Notepad में word wrap का उपयोग किस लिए होता है?",
            "options": ["A. टेक्स्ट को सहेजने के लिए", "B. टेक्स्ट को ऑटोमेटिक लाइन ब्रेक में रखने के लिए", "C. फॉन्ट बदलने के लिए", "D. टेक्स्ट हटाने के लिए"],
            "answer": "B. टेक्स्ट को ऑटोमेटिक लाइन ब्रेक में रखने के लिए"
        },
        #79
        {
            "question": " Notepad की विशेषता क्या है?",
            "options": ["A. यह भारी सॉफ्टवेयर है", "B. इसमें चित्र संपादन किया जा सकता है", "C. यह सरल टेक्स्ट एडिटर है", "D. इसमें विडियो चलाए जा सकते हैं"],
            "answer": "C. यह सरल टेक्स्ट एडिटर है"
        },
        #80
        {
            "question": " Notepad में फाइल खोलने की shortcut key क्या है?",
            "options": ["A. Ctrl + N", "B. Ctrl + O", "C. Ctrl + S", "D. Ctrl + Q"],
            "answer": "B. Ctrl + O"
        },
        #81
        {
            "question": " Windows क्या है?",
            "options": ["A. एप्लिकेशन सॉफ्टवेयर", "B. सिस्टम सॉफ्टवेयर", "C. ग्राफिक्स टूल", "D. डेटाबेस सॉफ्टवेयर"],
            "answer": "B. सिस्टम सॉफ्टवेयर"
        },
        #82
        {
            "question": " Windows का निर्माता कौन है?",
            "options": ["A. Apple", "B. Google", "C. Microsoft", "D. IBM"],
            "answer": "C. Microsoft"
        },
        #83
        {
            "question": " Windows का पहला संस्करण किस वर्ष में लॉन्च हुआ?",
            "options": ["A. 1983", "B. 1985", "C. 1990", "D. 1995"],
            "answer": "B. 1985"
        },
        #84
        {
            "question": " Windows में फाइल्स को संगठित करने के लिए कौन सा टूल होता है?",
            "options": ["A. Task Manager", "B. File Explorer", "C. Paint", "D. Notepad"],
            "answer": "B. File Explorer"
        },
        #85
        {
            "question": " Windows में Taskbar कहाँ होता है?",
            "options": ["A. स्क्रीन के ऊपर", "B. स्क्रीन के नीचे", "C. दोनों", "D. कहीं नहीं"],
            "answer": "B. स्क्रीन के नीचे"
        },
        #86
        {
            "question": " Windows में Copy करने की shortcut key क्या है?",
            "options": ["A. Ctrl + C", "B. Ctrl + V", "C. Ctrl + X", "D. Ctrl + Z"],
            "answer": "A. Ctrl + C"
        },
        #87
        {
            "question": " Windows में Recycle Bin का उपयोग किस लिए किया जाता है?",
            "options": ["A. फाइल्स सेव करने के लिए", "B. डिलीट की गई फाइल्स को रखने के लिए", "C. फोल्डर बनाने के लिए", "D. फाइल्स को ओपन करने के लिए"],
            "answer": "B. डिलीट की गई फाइल्स को रखने के लिए"
        },
        #88
        {
            "question": " Windows में स्क्रीन को बंद करने की shortcut key क्या है?",
            "options": ["A. Alt + F4", "B. Ctrl + S", "C. Ctrl + P", "D. Ctrl + Alt + Del"],
            "answer": "A. Alt + F4"
        },
        #89
        {
            "question": " Windows में Control Panel का उपयोग किसके लिए होता है?",
            "options": ["A. गेम खेलने के लिए", "B. सिस्टम सेटिंग्स करने के लिए", "C. चित्र बनाने के लिए", "D. इंटरनेट ब्राउज़िंग के लिए"],
            "answer": "B. सिस्टम सेटिंग्स करने के लिए"
        },
        #90
        {
            "question": " Windows में कौन सा ब्राउज़र डिफ़ॉल्ट रूप से उपलब्ध होता है?",
            "options": ["A. Chrome", "B. Firefox", "C. Internet Explorer / Edge", "D. Opera"],
            "answer": "C. Internet Explorer / Edge"
        },
        #91
        {
            "question": " Windows 10 के बाद कौन सा संस्करण आया?",
            "options": ["A. Windows XP", "B. Windows 11", "C. Windows Vista", "D. Windows 8"],
            "answer": "B. Windows 11"
        },
        #92
        {
            "question": " Windows में स्क्रीनशॉट लेने की shortcut key क्या है?",
            "options": ["A. Ctrl + Shift", "B. Alt + PrintScreen", "C. PrintScreen", "D. Shift + Tab"],
            "answer": "C. PrintScreen"
        },
        #93
        {
            "question": " Windows में फाइल का एक्सटेंशन क्या दर्शाता है?",
            "options": ["A. फोल्डर का नाम", "B. फाइल का प्रकार", "C. यूज़र का नाम", "D. फाइल साइज"],
            "answer": "B. फाइल का प्रकार"
        },
        #94
        {
            "question": " Windows में MS Word किस श्रेणी का सॉफ्टवेयर है?",
            "options": ["A. सिस्टम सॉफ्टवेयर", "B. एप्लिकेशन सॉफ्टवेयर", "C. ड्राइवर सॉफ्टवेयर", "D. यूटिलिटी सॉफ्टवेयर"],
            "answer": "B. एप्लिकेशन सॉफ्टवेयर"
        },
        #95
        {
            "question": " Windows में Start Menu किसके लिए प्रयोग होता है?",
            "options": ["A. सिस्टम बंद करने के लिए", "B. एप्लिकेशन खोलने के लिए", "C. सेटिंग बदलने के लिए", "D. उपरोक्त सभी"],
            "answer": "D. उपरोक्त सभी"
        },
        #96
        {
            "question": " MS Word किस प्रकार का सॉफ्टवेयर है?",
            "options": ["A. स्प्रेडशीट", "B. वर्ड प्रोसेसर", "C. ग्राफिक्स", "D. डेटाबेस"],
            "answer": "B. वर्ड प्रोसेसर"
        },
        #97
        {
            "question": " MS Word का निर्माण किसने किया?",
            "options": ["A. Apple", "B. Microsoft", "C. IBM", "D. Google"],
            "answer": "B. Microsoft"
        },
        #98
        {
            "question": " MS Word में नया डॉक्युमेंट खोलने की shortcut क्या है?",
            "options": ["A. Ctrl + N", "B. Ctrl + S", "C. Ctrl + P", "D. Ctrl + O"],
            "answer": "A. Ctrl + N"
        },
        #99
        {
            "question": " MS Word में सेव करने की shortcut क्या है?",
            "options": ["A. Ctrl + C", "B. Ctrl + V", "C. Ctrl + S", "D. Ctrl + P"],
            "answer": "C. Ctrl + V"
        },
        #100
        {
            "question": " MS Word में प्रिंट करने की shortcut क्या है?",
            "options": ["A. Ctrl + V", "B. Ctrl + P", "C. Ctrl + Z", "D. Ctrl + X"],
            "answer": "B. Ctrl + P"
        },
        #101
        {
            "question": " MS Word में Text को Bold बनाने की shortcut क्या है?",
            "options": ["A. Ctrl + B", "B. Ctrl + I", "C. Ctrl + U", "D. Ctrl + Z"],
            "answer": "A. Ctrl + B"
        },
        #102
        {
            "question": " MS Word में Italic करने की shortcut क्या है?",
            "options": ["A. Ctrl + B", "B. Ctrl + I", "C. Ctrl + U", "D. Ctrl + A"],
            "answer": "B. Ctrl + I"
        },
        #103
        {
            "question": " MS Word में Underline करने की shortcut क्या है?",
            "options": ["A. Ctrl + B", "B. Ctrl + I", "C. Ctrl + U", "D. Ctrl + C"],
            "answer": "C. Ctrl + U"
        },
        #104
        {
            "question": " MS Word में फॉन्ट साइज बदलने के लिए किस टैब का उपयोग होता है?",
            "options": ["A. Insert", "B. Home", "C. View", "D. Layout"],
            "answer": "B. Home"
        },
        #105
        {
            "question": " MS Word में Header और Footer जोड़ने के लिए कौन सा टैब प्रयोग होता है?",
            "options": ["A. Insert", "B. Home", "C. Review", "D. View"],
            "answer": "A. Insert"
        },
        #106
        {
            "question": " MS Word में Spell Check करने के लिए किस विकल्प का उपयोग होता है?",
            "options": ["A. File", "B. Insert", "C. Review", "D. Layout"],
            "answer": "C. Review"
        },
        #107
        {
            "question": " MS Word में Page Orientation कहाँ से बदलते हैं?",
            "options": ["A. Home", "B. Layout", "C. Insert", "D. Design"],
            "answer": "B. Layout"
        },
        #108
        {
            "question": " MS Word में Table जोड़ने के लिए कौन सा टैब प्रयोग होता है?",
            "options": ["A. Insert", "B. Home", "C. View", "D. References"],
            "answer": "A. Insert"
        },
        #109
        {
            "question": " MS Word का डिफ़ॉल्ट फाइल एक्सटेंशन क्या है?",
            "options": ["A. .txt", "B. .doc", "C. .docx", "D. .pdf"],
            "answer": "C. .docx"
        },
        #110
        {
            "question": " MS Word में Text को Select करने की shortcut क्या है?",
            "options": ["A. Ctrl + A", "B. Ctrl + S", "C. Ctrl + X", "D. Ctrl + Z"],
            "answer": "A. Ctrl + A"
        },
        #111
        {
            "question": " MS Word में Page Number किस टैब से जोड़ते हैं?",
            "options": ["A. View", "B. Review", "C. Insert", "D. File"],
            "answer": "C. Insert"
        },
        #112
        {
            "question": " MS Word में Zoom करने का विकल्प किस टैब में होता है?",
            "options": ["A. Home", "B. Insert", "C. Design", "D. Layout"],
            "answer": "A. Home"
        },
        #113
        {
            "question": " MS Word में Line Spacing कहाँ से बदलते हैं?",
            "options": ["A. Home", "B. Insert", "C. Layout", "D. Review"],
            "answer": "A. Home"
        },
        #114
        {
            "question": " MS Word में Track Changes का उपयोग किस कार्य में होता है?",
            "options": ["A. फॉन्ट बदलने में", "B. टेबल बनाने में", "C. बदलावों को देखने में", "D. चित्र जोड़ने में"],
            "answer": "C. बदलावों को देखने में"
        },
        #115
        {
            "question": " MS Word में फाइल को PDF के रूप में सेव करने के लिए क्या करना चाहिए?",
            "options": ["A. Ctrl + Shift + P", "B. Export > Create PDF", "C. Print", "D. File > Exit"],
            "answer": "B. Export > Create PDF"
        },
        #116
        {
            "question": " MS Excel किस प्रकार का सॉफ़्टवेयर है?",
            "options": ["A. डेटाबेस", "B. स्प्रेडशीट", "C. वर्ड प्रोसेसर", "D. ग्राफिक्स"],
            "answer": "B. स्प्रेडशीट"
        },
        #117
        {
            "question": " MS Excel का निर्माण किस कंपनी ने किया है?",
            "options": ["A. Google", "B. Apple", "C. Microsoft", "D. IBM"],
            "answer": "C. Microsoft"
        },
        #118
        {
            "question": " MS Excel में Cell का पता किससे बनता है?",
            "options": ["A. Row + Column", "B. Column + Row", "C. Sheet + Cell", "D. File + Sheet"],
            "answer": "B. Column + Row"
        },
        #119
        {
            "question": " Excel में एक वर्कबुक में कितनी वर्कशीट हो सकती हैं?",
            "options": ["A. 255", "B. 10", "C. 100", "D. जितनी चाहें"],
            "answer": "D. जितनी चाहें"
        },
        #120
        {
            "question": " Excel में SUM फ़ंक्शन का उपयोग किसके लिए होता है?",
            "options": ["A. जोड़ने के लिए", "B. घटाने के लिए", "C. गुणा करने के लिए", "D. विभाजन करने के लिए"],
            "answer": "A. जोड़ने के लिए"
        },
        #121
        {
            "question": " Excel में डिफ़ॉल्ट फाइल एक्सटेंशन क्या होता है?",
            "options": ["A. .txt", "B. .xlsx", "C. .docx", "D. .ppt"],
            "answer": "B. .xlsx"
        },
        #122
        {
            "question": " Excel में सेल को चुनने की शॉर्टकट कुंजी क्या है?",
            "options": ["A. Ctrl + A", "B. Ctrl + C", "C. Ctrl + S", "D. Ctrl + X"],
            "answer": "A. Ctrl + A"
        },
        #123
        # {
        #     "question": " Excel में फ़ॉर्मूला किस प्रतीक से शुरू होता है?",
        #     "options": ["A. @", "B. =", "C. #", "D. $"],
        #     "answer": "B"
        # },
        #124
        {
            "question": " Excel में डेटा को ग्राफ में दिखाने के लिए किस विकल्प का उपयोग होता है?",
            "options": ["A. Table", "B. Chart", "C. Sort", "D. Filter"],
            "answer": "B. Chart"
        },
        #125
        {
            "question": " Excel में Text को Merge करने का विकल्प किस टैब में होता है?",
            "options": ["A. Insert", "B. Layout", "C. Home", "D. Review"],
            "answer": "C. Home"
        },
        #126
        {
            "question": " Excel में MAX फ़ंक्शन क्या करता है?",
            "options": ["A. सबसे बड़ा मान देता है", "B. सबसे छोटा मान देता है", "C. जोड़ता है", "D. फ़िल्टर करता है"],
            "answer": "A. सबसे बड़ा मान देता है"
        },
        #127
        {
            "question": " Excel में COUNTIF फ़ंक्शन का उपयोग किस लिए होता है?",
            "options": ["A. जोड़ने के लिए", "B. शर्त के अनुसार गिनती के लिए", "C. डेटा हटाने के लिए", "D. रंग बदलने के लिए"],
            "answer": "B. शर्त के अनुसार गिनती के लिए"
        },
        #128
        {
            "question": " Excel में Conditional Formatting किस कार्य के लिए होता है?",
            "options": ["A. सेल्स को फॉर्मेट करने के लिए", "B. सेल के डेटा पर आधारित रंग बदलने के लिए", "C. टेबल बनाने के लिए", "D. फ़ॉर्मूला लागू करने के लिए"],
            "answer": "B. सेल के डेटा पर आधारित रंग बदलने के लिए"
        },
        #129
        {
            "question": " Excel में Autofill विकल्प किसके लिए प्रयोग होता है?",
            "options": ["A. फॉर्मूला बदलने के लिए", "B. डेटा को दोहराने के लिए", "C. ग्राफ बनाने के लिए", "D. डेटा छुपाने के लिए"],
            "answer": "B. डेटा को दोहराने के लिए"
        },
        #130
        {
            "question": " Excel में Pivot Table किस कार्य के लिए होता है?",
            "options": ["A. डेटा विश्लेषण के लिए", "B. फॉर्मूला लिखने के लिए", "C. सॉर्टिंग के लिए", "D. सेल मर्ज करने के लिए"],
            "answer": "A. डेटा विश्लेषण के लिए"
        },
        #131
        {
            "question": " Excel में Cell में Hyperlink जोड़ने का विकल्प किस टैब में होता है?",
            "options": ["A. Data", "B. Insert", "C. View", "D. Review"],
            "answer": "B. Insert"
        },
        #132
        {
            "question": " Excel में IF फ़ंक्शन का प्रयोग कब होता है?",
            "options": ["A. डेटा जोड़ने के लिए", "B. ग्राफ बनाने के लिए", "C. Logical condition पर काम करने के लिए", "D. पेज सेटअप के लिए"],
            "answer": "C. Logical condition पर काम करने के लिए"
        },
        #133
        {
            "question": " Excel में Wrap Text किस कार्य के लिए होता है?",
            "options": ["A. टेक्स्ट को छिपाने के लिए", "B. टेक्स्ट को रंगने के लिए", "C. टेक्स्ट को सेल में फिट करने के लिए", "D. कोई विकल्प नहीं"],
            "answer": "C. टेक्स्ट को सेल में फिट करने के लिए"
        },
        #134
        {
            "question": " Excel में डेटा को छाँटने के लिए किस विकल्प का प्रयोग होता है?",
            "options": ["A. Sort", "B. Filter", "C. Table", "D. Chart"],
            "answer": "A. Sort"
        },
        #135
        {
            "question": " Excel में स्पेलिंग चेक करने के लिए किस शॉर्टकट का प्रयोग होता है?",
            "options": ["A. F7", "B. Ctrl + P", "C. F2", "D. Shift + S"],
            "answer": "A. F7"
        },
        #136
        {
            "question": " SUM फ़ंक्शन का उपयोग किसके लिए किया जाता है?",
            "options": ["A. जोड़ने के लिए", "B. घटाने के लिए", "C. गुणा करने के लिए", "D. विभाजन करने के लिए"],
            "answer": "A. जोड़ने के लिए"
        },
        #137
        {
            "question": " AVERAGE फ़ंक्शन किस कार्य के लिए होता है?",
            "options": ["A. अधिकतम निकालने के लिए", "B. औसत निकालने के लिए", "C. जोड़ने के लिए", "D. घटाने के लिए"],
            "answer": "B. औसत निकालने के लिए"
        },
        #138
        {
            "question": " MAX फ़ंक्शन किसके लिए होता है?",
            "options": ["A. सबसे छोटा नंबर", "B. सबसे बड़ा नंबर", "C. दो नंबर जोड़ना", "D. नंबर गिनना"],
            "answer": "B. सबसे बड़ा नंबर"
        },
        #139
        {
            "question": " MIN फ़ंक्शन क्या करता है?",
            "options": ["A. सबसे बड़ा नंबर देता है", "B. सेल को खाली करता है", "C. सबसे छोटा नंबर देता है", "D. कुछ नहीं"],
            "answer": "C. सबसे छोटा नंबर देता है"
        },
        #140
        {
            "question": " COUNT फ़ंक्शन किसके लिए उपयोग होता है?",
            "options": ["A. जोड़ने के लिए", "B. टेक्स्ट गिनने के लिए", "C. नंबर वाले सेल गिनने के लिए", "D. औसत निकालने के लिए"],
            "answer": "C. नंबर वाले सेल गिनने के लिए"
        },
        #141
        {
            "question": " COUNTIF फ़ंक्शन क्या करता है?",
            "options": ["A. शर्त अनुसार गिनती करता है", "B. टेक्स्ट जोड़ता है", "C. टाइम निकालता है", "D. डेटा हटाता है"],
            "answer": "A. शर्त अनुसार गिनती करता है"
        },
        #142
        {
            "question": " IF फ़ंक्शन किस लिए होता है?",
            "options": ["A. ग्राफ बनाने के लिए", "B. टेक्स्ट जोड़ने के लिए", "C. शर्त के अनुसार परिणाम देने के लिए", "D. रंग बदलने के लिए"],
            "answer": "C. शर्त के अनुसार परिणाम देने के लिए"
        },
        #145
        {
            "question": " CONCAT फ़ंक्शन किस कार्य के लिए प्रयोग होता है?",
            "options": ["A. दो टेक्स्ट जोड़ने के लिए", "B. नंबर घटाने के लिए", "C. फॉर्मूला हटाने के लिए", "D. चित्र जोड़ने के लिए"],
            "answer": "A. दो टेक्स्ट जोड़ने के लिए"
        },
        #146
        {
            "question": " TODAY() फ़ंक्शन क्या दिखाता है?",
            "options": ["A. वर्तमान समय", "B. वर्तमान तारीख", "C. वर्ष", "D. दिन नाम"],
            "answer": "B. वर्तमान तारीख"
        },
        #147
        {
            "question": " NOW() फ़ंक्शन क्या return करता है?",
            "options": ["A. केवल तारीख", "B. केवल समय", "C. वर्तमान तारीख और समय", "D. कुछ नहीं"],
            "answer": "C. वर्तमान तारीख और समय"
        },
        #148
        {
            "question": " ROUND() फ़ंक्शन का उपयोग किसलिए होता है?",
            "options": ["A. संख्या को पास के पूरे नंबर तक राउंड करने के लिए", "B. टेक्स्ट राउंड करने के लिए", "C. वर्कशीट राउंड करने के लिए", "D. कुछ नहीं"],
            "answer": "A. संख्या को पास के पूरे नंबर तक राउंड करने के लिए"
        },
        #149
        {
            "question": " VLOOKUP फ़ंक्शन किस काम आता है?",
            "options": ["A. डेटा कॉपी करने के लिए", "B. वर्टिकल रूप में डेटा सर्च करने के लिए", "C. पेज नंबर निकालने के लिए", "D. रोटेशन करने के लिए"],
            "answer": "B. वर्टिकल रूप में डेटा सर्च करने के लिए"
        },
        #150
        {
            "question": " HLOOKUP किस प्रकार से डेटा खोजता है?",
            "options": ["A. वर्टिकल रूप से", "B. होरिज़ॉन्टल रूप से", "C. डायगोनली", "D. रिवर्स में"],
            "answer": "B. होरिज़ॉन्टल रूप से"
        },
        #151
        {
            "question": " TEXT() फ़ंक्शन किसके लिए प्रयोग होता है?",
            "options": ["A. नंबर को टेक्स्ट में बदलने के लिए", "B. चित्र जोड़ने के लिए", "C. ग्राफ बनाने के लिए", "D. फॉर्मूला हटाने के लिए"],
            "answer": "A. नंबर को टेक्स्ट में बदलने के लिए"
        },
        #152
        {
            "question": " LEFT() फ़ंक्शन क्या करता है?",
            "options": ["A. टेक्स्ट के दाएं हिस्से को देता है", "B. टेक्स्ट के बाएं हिस्से को देता है", "C. पूरा टेक्स्ट देता है", "D. टेक्स्ट हटा देता है"],
            "answer": "B. टेक्स्ट के बाएं हिस्से को देता है"
        },
        #153
        {
            "question": " RIGHT() फ़ंक्शन किसके लिए प्रयोग होता है?",
            "options": ["A. बाएं हिस्से को निकालने के लिए", "B. दाएं हिस्से को निकालने के लिए", "C. पूरे टेक्स्ट को हटाने के लिए", "D. सेल की लोकेशन बताने के लिए"],
            "answer": "B. दाएं हिस्से को निकालने के लिए"
        },
        #154
        {
            "question": " MID() फ़ंक्शन किसका उपयोग करता है?",
            "options": ["A. टेक्स्ट के बीच के हिस्से को निकालने के लिए", "B. पूर्ण टेक्स्ट वापस करने के लिए", "C. डेट हटाने के लिए", "D. कुछ नहीं"],
            "answer": "A. टेक्स्ट के बीच के हिस्से को निकालने के लिए"
        },
        #156
        {
            "question": " LEN() फ़ंक्शन क्या बताता है?",
            "options": ["A. टेक्स्ट की लंबाई", "B. टेक्स्ट की चौड़ाई", "C. फाइल का नाम", "D. टाइम"],
            "answer": "A. टेक्स्ट की लंबाई"
        },
        #157
        {
            "question": " ISNUMBER() फ़ंक्शन क्या करता है?",
            "options": ["A. डेटा को रंगता है", "B. यह जांचता है कि सेल में नंबर है या नहीं", "C. सेल हटा देता है", "D. टेक्स्ट बदलता है"],
            "answer": "B. यह जांचता है कि सेल में नंबर है या नहीं"
        },
        #158
        {
            "question": " PROPER() फ़ंक्शन क्या करता है?",
            "options": ["A. सभी अक्षरों को छोटा बनाता है", "B. सभी अक्षरों को बड़ा बनाता है", "C. हर शब्द के पहले अक्षर को बड़ा करता है", "D. सभी को हटाता है"],
            "answer": "C. हर शब्द के पहले अक्षर को बड़ा करता है"
        },
        #159
        {
            "question": " MS PowerPoint क्या है?",
            "options": ["A. डेटाबेस सॉफ़्टवेयर", "B. स्प्रेडशीट सॉफ़्टवेयर", "C. प्रेजेंटेशन सॉफ़्टवेयर", "D. ग्राफिक्स सॉफ़्टवेयर"],
            "answer": "C. प्रेजेंटेशन सॉफ़्टवेयर"
        },
        #160
        {
            "question": " PowerPoint का निर्माण किसने किया?",
            "options": ["A. Google", "B. Microsoft", "C. IBM", "D. Apple"],
            "answer": "B. Microsoft"
        },
        #161
        {
            "question": " PowerPoint स्लाइड में टेक्स्ट जोड़ने के लिए किसका उपयोग होता है?",
            "options": ["A. WordArt", "B. Placeholder", "C. Shape", "D. Header"],
            "answer": "B. Placeholder"
        },
        #162
        {
            "question": " नई स्लाइड जोड़ने की shortcut key क्या है?",
            "options": ["A. Ctrl + N", "B. Ctrl + M", "C. Ctrl + S", "D. Ctrl + D"],
            "answer": "B. Ctrl + M"
        },
        #163
        {
            "question": " PowerPoint में स्लाइड शो शुरू करने की shortcut क्या है?",
            "options": ["A. F5", "B. F2", "C. F10", "D. F7"],
            "answer": "A. F5"
        },
        #164
        {
            "question": " PowerPoint का default file extension क्या है?",
            "options": ["A. .ppt", "B. .pptx", "C. .docx", "D. .xlsx"],
            "answer": "B. .pptx"
        },
        #165
        {
            "question": " PowerPoint में चित्र जोड़ने के लिए कौन सा टैब प्रयोग होता है?",
            "options": ["A. File", "B. Design", "C. Insert", "D. Slide Show"],
            "answer": "C. Insert"
        },
        #166
        {
            "question": " PowerPoint में एनिमेशन जोड़ने के लिए कौन सा टैब प्रयोग होता है?",
            "options": ["A. Home", "B. Review", "C. Animations", "D. View"],
            "answer": "C. Animations"
        },
        #167
        {
            "question": " Transition क्या है?",
            "options": ["A. स्लाइड्स के बीच बदलाव का प्रभाव", "B. टेक्स्ट को हाइलाइट करने का तरीका", "C. Background बदलना", "D. Font बदलना"],
            "answer": "A. स्लाइड्स के बीच बदलाव का प्रभाव"
        },
        #168
        {
            "question": " PowerPoint में स्लाइड डुप्लिकेट करने की shortcut क्या है?",
            "options": ["A. Ctrl + M", "B. Ctrl + D", "C. Ctrl + N", "D. Ctrl + P"],
            "answer": "B. Ctrl + D"
        },
        #169
        {
            "question": " नोट्स जोड़ने का विकल्प किस व्यू में दिखता है?",
            "options": ["A. Slide Sorter View", "B. Normal View", "C. Reading View", "D. Outline View"],
            "answer": "B. Normal View"
        },
        #170
        {
            "question": " PowerPoint में एक पूरी प्रेजेंटेशन को कैसे सेव करते हैं?",
            "options": ["A. Ctrl + V", "B. Ctrl + S", "C. Ctrl + Z", "D. Ctrl + C"],
            "answer": "B. Ctrl + S"
        },
        #171
        {
            "question": " PowerPoint में फाइल को PDF में सेव करने का विकल्प कहाँ होता है?",
            "options": ["A. View", "B. Export", "C. Design", "D. Slide Show"],
            "answer": "B. Export"
        },
        #172
        {
            "question": " MS PowerPoint में Slide Master का उपयोग किसलिए होता है?",
            "options": ["A. टेक्स्ट लिखने के लिए", "B. सभी स्लाइड्स के लेआउट को नियंत्रित करने के लिए", "C. ग्राफ बनाने के लिए", "D. ऑडियो जोड़ने के लिए"],
            "answer": "B. सभी स्लाइड्स के लेआउट को नियंत्रित करने के लिए"
        },
        #173
        {
            "question": " PowerPoint में ऑडियो जोड़ने के लिए कौन सा टैब होता है?",
            "options": ["A. Review", "B. Insert", "C. Design", "D. File"],
            "answer": "B. Insert"
        },
        #174
        {
            "question": " Slide Show को बंद करने के लिए कौन सी कुंजी दबाई जाती है?",
            "options": ["A. Esc", "B. Ctrl", "C. F5", "D. Enter"],
            "answer": "A. Esc"
        },
        #175
        {
            "question": " PowerPoint में SmartArt किसके लिए प्रयोग होता है?",
            "options": ["A. ऑडियो जोड़ने के लिए", "B. डेटा को विज़ुअल रूप में दिखाने के लिए", "C. Background बदलने के लिए", "D. स्लाइड हटाने के लिए"],
            "answer": "B. डेटा को विज़ुअल रूप में दिखाने के लिए"
        },
        #176
        {
            "question": " PowerPoint में Slide की Background बदलने के लिए कौन सा टैब प्रयोग होता है?",
            "options": ["A. Home", "B. Insert", "C. Design", "D. View"],
            "answer": "C. Design"
        },
        #177
        {
            "question": " PowerPoint में Review टैब का उपयोग किसलिए होता है?",
            "options": ["A. ग्राफिक्स जोड़ने के लिए", "B. टिप्पणी और स्पेलिंग जांच के लिए", "C. स्लाइड शो चलाने के लिए", "D. ऑडियो रिकॉर्ड करने के लिए"],
            "answer": "B. टिप्पणी और स्पेलिंग जांच के लिए"
        },
        #178
        {
            "question": " PowerPoint में Zoom करने का विकल्प किस टैब में होता है?",
            "options": ["A. Insert", "B. View", "C. File", "D. Home"],
            "answer": "B. View"
        },

        
    ]
    # Shuffle questions for random order
    random.shuffle(questions)
    questions = questions[:100]

    # GUI Setup
    global progress_frame, progress_canvas, question_label, options, timer_label, nav_frame, prev_btn, finish_btn, next_btn, status_label
    question_index = 0
    selected_option = tk.StringVar()
    user_answers = [None] * len(questions)
    exam_time_left = 5400  # 90 minutes in seconds
    timer_id = None

    # Widgets
    progress_frame = tk.Frame(root)
    progress_frame.pack(side="top", pady=20)
    progress_canvas = tk.Canvas(progress_frame, width=30*len(questions), height=40, highlightthickness=0, bg=root.cget('bg'))
    progress_canvas.pack()

    question_label = tk.Label(root, text="", font=("Arial", 18), wraplength=1000, justify="left")
    question_label.pack(pady=20)

    options = [tk.Radiobutton(root, text="", variable=selected_option, font=("Arial", 18), value="", anchor="w", justify="left") for _ in range(4)]
    for opt in options:
        opt.pack(fill="x", padx=20)

    timer_label = tk.Label(root, text="", font=("Arial", 12), fg="red")
    timer_label.pack()

    nav_frame = tk.Frame(root)
    nav_frame.pack(pady=10)

    prev_btn = tk.Button(nav_frame, text="⏮ Previous", command=lambda: navigate(-1), font=("Arial", 12))
    prev_btn.grid(row=0, column=0, padx=10)

    finish_btn = tk.Button(nav_frame, text="🏁 Finish", command=lambda: finish_quiz(), font=("Arial", 12), bg="green", fg="white")
    finish_btn.grid(row=0, column=1, padx=10)

    next_btn = tk.Button(nav_frame, text="⏭ Next", command=lambda: navigate(1), font=("Arial", 12))
    next_btn.grid(row=0, column=2, padx=10)

    status_label = tk.Label(progress_frame, text="", font=("Arial",18 ), fg="blue")
    status_label.pack(pady=2)

    load_question()
    update_status()
    update_exam_timer()  # Start the exam timer

# --- REST OF THE QUIZ FUNCTIONS (unchanged) ---
def load_question():
    selected_option.set(user_answers[question_index])
    q = questions[question_index]
    question_label.config(text=f"Q{question_index+1}:{q['question']}")
    for i in range(4):
        options[i].config(text=q['options'][i], value=q['options'][i])
    # Enable Finish button only on last question
    if question_index == len(questions) - 1:
        finish_btn.config(state="normal")
    else:
        finish_btn.config(state="disabled")
    update_status()

# Remove countdown and update_timer for per-question timer

def update_exam_timer():
    global exam_time_left, timer_id
    mins, secs = divmod(exam_time_left, 60)
    timer_label.config(text=f"⏳ Time Left: {mins:02d}:{secs:02d}")
    if exam_time_left > 0:
        exam_time_left -= 1
        timer_id = root.after(1000, update_exam_timer)
    else:
        finish_quiz()

# Remove per-question timer logic from submit_answer and navigate

def submit_answer(manual=True):
    global question_index
    selected = selected_option.get()
    user_answers[question_index] = selected
    if not manual:
        question_index += 1
        if question_index < len(questions):
            load_question()
        else:
            finish_quiz()
    update_status()

def navigate(direction):
    global question_index
    user_answers[question_index] = selected_option.get()
    question_index += direction
    if question_index < 0:
        question_index = 0
    elif question_index >= len(questions):
        question_index = len(questions) - 1
    load_question()
    update_status()

def show_result():
    correct = sum(1 for i, ans in enumerate(user_answers) if ans == questions[i]['answer'])
    attempted = sum(1 for ans in user_answers if ans)
    left = len(questions) - attempted
    incorrect = attempted - correct
    # Save results to CSV
    with open('quiz_results.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Question Number', 'Question', 'User Answer', 'Correct Answer', 'Status'])
        for i, ans in enumerate(user_answers):
            q = questions[i]
            status = 'Correct' if ans == q['answer'] else 'Incorrect'
            writer.writerow([
                i+1,
                q['question'],
                ans if ans else '',
                q['answer'],
                status
            ])
    # Save summary to student_result.csv
    try:
        global current_username, current_password
        result_path = os.path.join(os.path.dirname(__file__), 'student_result.csv')
        file_exists = os.path.exists(result_path)
        with open(result_path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(['Username', 'Password', 'Attempted', 'Left', 'Correct', 'Incorrect'])
            writer.writerow([
                current_username,
                current_password,
                attempted,
                left,
                correct,
                incorrect
            ])
    except Exception as e:
        messagebox.showerror("File Error", f"Result not saved: {e}")
    messagebox.showinfo("Quiz Over", f"आपका स्कोर: {correct}/{len(questions)}")
    root.quit()

def finish_quiz():
    user_answers[question_index] = selected_option.get()
    update_status()
    show_result()

def update_status():
    total = len(questions)
    attempted = sum(1 for ans in user_answers if ans)
    left = total - attempted
    progress_canvas.delete("all")
    radius = 19
    spacing = 25
    circles_per_row = 5
    cols = (total + circles_per_row - 1) // circles_per_row
    x_offset = spacing
    y_offset = spacing
    for i in range(total):
        col = i // circles_per_row
        row = i % circles_per_row
        x = x_offset + col * (1 * radius + spacing)
        y = y_offset + row * (1 * radius + spacing)
        if i == question_index:
            fill = "#FFD600"
        elif user_answers[i]:
            fill = "#28a745"
        else:
            fill = "#e53935"
        outline = "#888"
        width = 1
        progress_canvas.create_oval(x-radius, y-radius, x+radius, y+radius, fill=fill, outline=outline, width=width)
        progress_canvas.create_text(x, y, text=str(i+1), font=("Arial", 14, "bold"), fill="#222")
    # Adjust canvas size
    progress_canvas.config(
        width=cols * (1 * radius + spacing) + x_offset,
        height=circles_per_row * (1 * radius + spacing) + y_offset
    )
    status_label.config(
        text=f" Attempted: {attempted} | Left: {left} | Total: {total}")

def add_user(username, password):
    # Save to students.csv
    csv_path = os.path.join(os.path.dirname(__file__), "students.csv")
    # Check if username already exists
    exists = False
    if os.path.exists(csv_path):
        with open(csv_path, "r", newline='', encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if row and row[0] == username:
                    exists = True
                    break
    if exists:
        print("Username already exists!")
        return
    with open(csv_path, "a", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([username, password])
    print("User added successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("NET-TECH ACADEMY OF COMPUTER TECHONOLOGY")
    root.state('zoomed')
    show_login(root)
    root.mainloop()
