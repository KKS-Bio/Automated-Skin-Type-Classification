import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
import os

userName = input("Enter Participant Name: ")
outputName = userName +'Output.txt'
outputFile = './' + outputName
output = open(outputFile, 'w')

def test():
    root = tk.Tk()
    root.withdraw()
    dirname = tk.filedialog.askdirectory(parent=root, initialdir="./", title='Please select a directory')
    root.destroy()
    return (dirname)

def find_database_path():
    root = tk.Tk()
    root.withdraw()
    #dirname = os.chdir(r"path")
    testPath = "/home/gabby/"
    dirname = os.chdir(testPath)
    dirname = os.getcwd()
    root.destroy()
    return (dirname)

def gui(path, j):
    db_path = find_database_path()
    window = tk.Tk()
    window.title("Flowers")
    window.geometry("800x800")
    v = tk.IntVar()
    v.set(8)
    colors = ['#FFDBAC', '#F1C27D', '#E0AC69', '#C68642', '#8D5524', '#533D32']

    def next_window():
        window.destroy()

    def close():
        exit(0)

    def ShowChoice():
        #print(j[:-4], int(v.get()) + 1)
        x = str(j[:-4]) + ", " + str(int(v.get()) + 1) + "\n"
        output.write(x)
        output.flush()
        next_window()

    path = path.rstrip(os.sep)
    file_name = os.path.basename(path).split(".")[0]
    flower_name = file_name.split("_")[0]

    img = ImageTk.PhotoImage(Image.open(path))
    panel1 = tk.Label(window)
    panel2 = tk.Label(window, height=800)
    panel3 = tk.Label(window)
    tk.Label(panel1, image=img, borderwidth=3, relief="solid").pack(side="top")
    tk.Label(panel1, text=file_name, font=("Helvetica", 12)).pack(side="bottom")
    panel1.pack(side="left", fill="none", expand="Yes")
    panel3.pack(side="left", fill="none", expand="Yes")
    panel2.pack(side="right", fill="both", expand="Yes")

    dbpath = os.listdir(db_path)
    img_collection = []
    tk.Label(panel3, text="""Select skin-tone for given face image: """, font=("Helvetica", 15), justify=tk.LEFT,
             padx=20).pack(side="top")
    for val, level in enumerate(colors):
        val = val + 1
        radiobutton = tk.Radiobutton(panel3, text=val, padx=100, variable=v, command=ShowChoice, compound="center",
                                     indicatoron=0, value=val, bg=level, fg="white").pack(fill=tk.X)
    button = tk.Button(panel3, text="Next", command=next_window, bg="green", fg="black")
    button.pack(padx=50, side="top")
    button = tk.Button(panel3, text="Exit", command=close, bg="red", fg="white")
    button.pack(side="top")
    for i in dbpath:
        path_i = i.rstrip(os.sep)
        flower_file_name = os.path.basename(path_i).split(".")[0]
        flw_name = flower_file_name.split("_")[0]

        if flw_name == flower_name:
            image = Image.open(db_path + '/' + i)
            new_image = image.resize((100, 100))
            imgs = ImageTk.PhotoImage(new_image)
            img_collection.append(imgs)
            panel = tk.Label(panel2)
            tk.Label(panel, image=imgs, borderwidth=3, relief="solid", height=100, width=100).pack(side="top")
            tk.Label(panel, text=flower_file_name, font=("Helvetica", 12)).pack(side="bottom")
            panel.pack(side="top", fill="none", expand="Yes")
    window.mainloop()


if __name__ == "__main__":
    in_dir = test()
    path = os.listdir(in_dir)
    for j in path:
        if j == "gui_util.py":
            pass
        elif j == outputName:
            pass
        else:
            gui(in_dir + '/' + j, j)
    output.close()
