import PySimpleGUI as sg
import os
import matplotlib
import shutil

home = os.getcwd()
large = (1000, 1000)

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

def get_layout():
    file_list_column = [
        [
            sg.Text("Errors Will Appear Here", key="error_key"),
        ],
        [
            sg.Text("Image Folder"),
            sg.In(size=(25, 1), enable_events=True, key="folder_key"),
            sg.FolderBrowse(),
        ],
        [
            sg.Listbox(
                values=[], enable_events=True, size=(40, 20), key="file_key"
            )
        ],
            get_folders()
        ,
        [
            sg.Button("next"),
            sg.Button("prev"),
        ]
    ]
    image_viewer_column = [
        [sg.Text("Choose")],
        [sg.Text(size=(40,1), key="text_key")],
        [sg.Image(size=large, key="image_key")],
    ]
    layout = [
        [
            sg.Column(file_list_column),
            sg.VSeperator(),
            sg.Column(image_viewer_column),
        ]
    ]
    return layout

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg

def prog():
    layout = get_layout()
    window = sg.Window("Demo",
        layout,
        location=(0,0),
        finalize=True,
        element_justification="center",
        font="Helvetica 10",
        return_keyboard_events=True
        )
    return window

def initial():
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
            start()
            break
        return

def start():
    window = prog()
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == "folder_key":
            folder = values["folder_key"]
            try:
                file_list = os.listdir(folder)
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
        elif event in get_classes() or event in [str(i) for i in range(10)]:
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
        try:
            window["file_key"].update(fnames)
            window["error_key"].update(filename)
        except:
            pass
    window.close()

def move(src, _class, img):
    dest = home + '/' + _class + '/' + img
    shutil.move(src, dest)
    return

if __name__=='__main__':
    initial()
