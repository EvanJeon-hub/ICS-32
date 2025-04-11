# a4.py
# EVAN-SOOBIN JEON
# ejeon2@uci.edu
# 35377131

"""
a4.py for running main() function and GUI
"""

import tkinter as tk
import frame

PORT = 3001

if __name__ == '__main__':
    main = tk.Tk()
    main.title("ICS 32 Distributed Social Messenger")
    main.geometry("720x480")
    main.option_add('*tearOff', False)
    app = frame.MainApp(main)
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    after_id = main.after(2000, app.check_new)
    print(after_id)
    main.mainloop()
