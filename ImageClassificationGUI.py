import PySimpleGUI as sg
import os
import matplotlib
import shutil
import csv

home = os.getcwd()
large = (800, 600)

def get_classes():
    # for _dir in set_directory(home):
    #     print(_dir)
    return set_directory(home)

def set_directory(directory):
    os.chdir(directory)
    directories = filter(os.path.isdir, os.listdir(os.getcwd()))
    _dirs = list(directories)
    return _dirs

def get_folders():
    folders = list()
    for i, _class in enumerate(get_classes()):
        folders.append(sg.Button(str(i) + " - " + _class))
    return folders

def get_layout_c():
    layout = [[
        sg.Column(classification()),
        sg.VSeperator(),
        sg.Column(image_viewer()),
    ]]
    return layout

def get_layout_r():
    layout = [[
        sg.Column(regression()),
        sg.VSeperator(),
        sg.Column(image_viewer()),
    ]]
    return layout

def image_viewer():
    image_viewer = [[sg.Text("Choose")],
        [sg.Text(size=(40,1), key="text_key")],
        [sg.Image(size=large, key="image_key")]]
    return image_viewer

def classification():
    classification = [[sg.Text("Classification", key="error_key"),],
    [
        sg.Text("Image Folder"),
        sg.In(size=(20, 1), enable_events=True, key="folder_key"),
        sg.FolderBrowse(),
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40, 20), key="file_key"
        )
    ], get_folders(),
    [
        sg.Button("next"),
        sg.Button("prev"),
    ]]
    return classification

def regression():
    regression = [[sg.Text("Regression", key="error_key"),],

    [
        sg.Text("Image Folder"),
        sg.In(size=(20, 1), enable_events=True, key="folder_key"),
        sg.FolderBrowse(),
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40, 20), key="file_key"
        )
    ],
    [
        sg.Button("next"),
        sg.Button("prev"),
    ],
    [
        sg.Slider(range=(1, 1000), orientation='h',size=(25,15), default_value=500, pad=(5,0)),
        sg.Button("Save", enable_events=True, key="save_slide")
    ],
    [
        sg.In(size=(32,10), pad=(5,0)),
        sg.Button("Save", enable_events=True, key="save_in")
    ]]
    return regression

# def draw_figure(canvas, figure):
#     figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
#     figure_canvas_agg.draw()
#     figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
#     return figure_canvas_agg

def prog(classif):
    if classif:
        layout = get_layout_c()
    else:
        layout = get_layout_r()
    window = sg.Window("Demo",
        layout,
        location=(0,0),
        finalize=True,
        element_justification="center",
        font="Helvetica 10",
        return_keyboard_events=True
        )
    return window

def primary():
    layout = [[
        sg.Button("Classification", key="C"),
        sg.Button("Regression", key="R"),
    ]]
    window = sg.Window("Demo",
        layout,
        location=(0,0),
        finalize=True,
        element_justification="center",
        font="Helvetica 10"
        )
    while True:
        event, values = window.read()
        if event == "C":
            window.close()
            secondary(True)
            break
        elif event == "R":
            window.close()
            secondary(False)
            break
        return

def secondary(classif):
    if not classif:
        start(classif)
        return
    layout = [[
        sg.Text("Classification Directory"),
        sg.In(size=(25, 1), enable_events=True, key="dest_key"),
        sg.FolderBrowse(),
    ]]
    window = sg.Window("Demo",
        layout,
        location=(0,0),
        finalize=True,
        element_justification="center",
        font="Helvetica 10"
        )
    while True:
        event, values = window.read()
        if event == "dest_key":
            global home
            dest = values["dest_key"]
            home = dest
            window.close()
            start(classif)
            break
        return

def start(classif):
    window = prog(classif)
    if not classif:
        regression_list = []
        try:
            dest = os.getcwd() + r'/processed/'
            os.mkdir(dest)
        except FileExistsError as F:
            print(F)
    file_list = []
    img = None
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            try:
                csv_save(regression_list, dest)
                print(regression_list)
            except:
                print("Regression Not Completed")
            break
        elif event == "folder_key":
            folder = values["folder_key"]
            try:
                file_list = os.listdir(folder)
                dest = folder + r'/processed/'
            except:
                file_list = []
            fnames = [
                f
                for f in file_list
                if os.path.isfile(os.path.join(folder, f))
                and f.lower().endswith((".png", ".jpg", ".gif"))
            ]
            window["file_key"].update(fnames)
        elif event == "file_key":
            try:
                img = values["file_key"][0]
                index = fnames.index(img)
                filename = os.path.join(
                    values["folder_key"], img
                )
                window["text_key"].update(filename)
                window["image_key"].update(size=large, filename=filename)
            except:
                pass
        elif event == "prev":
            fnames = [
                f
                for f in file_list
                if os.path.isfile(os.path.join(folder, f))
                and f.lower().endswith((".png", ".jpg", ".gif"))
            ]
            window["file_key"].update(fnames)
            try:
                file_list = os.listdir(folder)
            except:
                file_list = []
            index = fnames.index(img) - 1
            if index < 0:
                index = 0
            img = fnames[index]
            filename = os.path.join(
                values["folder_key"], img
            )
            window["text_key"].update(filename)
            window["image_key"].update(size=large, filename=filename)
        elif event == "next":
            fnames = [
                f
                for f in file_list
                if os.path.isfile(os.path.join(folder, f))
                and f.lower().endswith((".png", ".jpg", ".gif"))
            ]
            window["file_key"].update(fnames)
            try:
                file_list = os.listdir(folder)
            except:
                file_list = []
            index = fnames.index(img) + 1
            if index >= len(fnames):
                index = len(fnames) - 1
            img = fnames[index]
            filename = os.path.join(
                values["folder_key"], img
            )
            window["text_key"].update(filename)
            window["image_key"].update(size=large, filename=filename)
        elif event == "save_slide":
            flt = values[0] / 1000
            print(float)
            fnames = [
                f
                for f in file_list
                if os.path.isfile(os.path.join(folder, f))
                and f.lower().endswith((".png", ".jpg", ".gif"))
            ]
            # img = values["file_key"][0]
            regression_list.append((img, flt))
            filename = os.path.join(
                values["folder_key"], img
            )
            move_r(filename, dest, img)
            window["file_key"].update(fnames)
            try:
                file_list = os.listdir(folder)
            except:
                file_list = []
            index = fnames.index(img)
            fnames = [
                f
                for f in file_list
                if os.path.isfile(os.path.join(folder, f))
                and f.lower().endswith((".png", ".jpg", ".gif"))
            ]
            if index >= len(fnames):
                index = len(fnames) - 1
            img = fnames[index]
            filename = os.path.join(
                values["folder_key"], img
            )
            window["file_key"].update(fnames)
            window["text_key"].update(filename)
            window["image_key"].update(size=large, filename=filename)
        elif event == "save_in":
            flt = int(values[1]) / 1000
            print(flt)
            window[1].update('')
            fnames = [
                f
                for f in file_list
                if os.path.isfile(os.path.join(folder, f))
                and f.lower().endswith((".png", ".jpg", ".gif"))
            ]
            # img = values["file_key"][0]
            regression_list.append((img, flt))
            filename = os.path.join(
                values["folder_key"], img
            )
            move_r(filename, dest, img)
            window["file_key"].update(fnames)
            try:
                file_list = os.listdir(folder)
            except:
                file_list = []
            index = fnames.index(img) # + 1
            fnames = [
                f
                for f in file_list
                if os.path.isfile(os.path.join(folder, f))
                and f.lower().endswith((".png", ".jpg", ".gif"))
            ]
            if index >= len(fnames):
                index = len(fnames) - 1
            img = fnames[index]
            filename = os.path.join(
                values["folder_key"], img
            )
            window["file_key"].update(fnames)
            window["text_key"].update(filename)
            window["image_key"].update(size=large, filename=filename)
        elif event in get_classes() or event in [str(i) for i in range(10)]:
            if not classif:
                continue
            try:
                c = get_classes()
                if event in c:
                    move(filename, event, img)
                else:
                    if int(event) < len(c):
                        move(filename, c[int(event)], img)
                    else:
                        continue
                if index + 1 <= len(fnames) - 1:
                    img = fnames[index + 1]
                elif index - 1 >= 0:
                    img = fnames[index - 1]
                else:
                    img = None
                del fnames[index]
                filename = values["folder_key"] + '/' + img
                window["image_key"].update(size=large, filename=filename)
                window["file_key"].update(fnames)
            except:
                window["error_key"].update("!!!No Image Chosen!!!")
                print("No Image Chosen")
        # try:
        #     window["file_key"].update(fnames)
        #     window["error_key"].update(filename)
        # except:
        #     print("ERROR 353")
    window.close()

def move(src, _class, img):
    dest = home + '/' + _class + '/' + img
    shutil.move(src, dest)
    return

def csv_save(tuple_list, d):
    try:
        try:
            f = open(d + r'reg_save.csv', 'a+')
            writer = csv.writer(f)
        except:
            f = open(d + r'reg_save.csv', 'a')
            writer = csv.writer(f)
    except:
        print("ERROR 371")
        e = sys.exc_info()[0]
        print(e)
    for row in tuple_list:
        writer.writerow(row)
    f.close()
    return

def move_r(src, d, img):
    dest = d + img
    try:
        shutil.move(src, dest)
    except FileNotFoundError as f:
        print("Initializing File")
        os.mkdir(d)
        shutil.move(src, dest)
    return

if __name__=='__main__':
    primary()
