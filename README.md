Basic GUI for quickly sorting photos into labeled classification folders.

Program requires PySimpleGUI pip install, must be run as a .py in Python 3.
Should display an option to choose a classification directory. This is the destination directory that contains labeled folders for your selected images to be sorted into. After a classification directory is chosen, you must choose the source folder containing the images you intend to sort. After the destination and source are chosen, just click on one of the displayed image names and sort each image by clicking on the associated label button, or by typing the zero-indexed number corresponding to the desired category. Only 10 classifications (0 - 9) will be supported for the numbered sorting. Program needs to be restarted in order to sort into a new classification directory, but you should be able to change the source directory the same way it was initialized.


The size of the primary window is set with the tuple "large" at the top of the file, resizing hasn't been added yet.
