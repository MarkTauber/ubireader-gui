from .app import UBIReaderGUI

def main():
    app = UBIReaderGUI()

    try:
        from tkinterdnd2 import DND_FILES

        app.drop_target_register(DND_FILES)
        app.dnd_bind("<<Drop>>", lambda event: app._set_file(event.data.strip("{}")))

    except ImportError:
        pass

    app.mainloop()

if __name__ == "__main__":
    main()
