import os, sys
import pdfreader

def main(folder_path):
    for pdf_file_path in os.scandir(folder_path):
        with open(pdf_file_path, 'rb') as file:
            viewer = pdfreader.SimplePDFViewer(file)
            viewer.navigate(1)
            viewer.render()
            print(viewer.canvas.strings)

if __name__ == '__main__':
    main(sys.argv[1])
