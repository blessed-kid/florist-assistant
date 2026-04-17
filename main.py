from interface import ImageApp
import tkinterdnd2 as tkdnd

def main():
    root = tkdnd.Tk()
    app = ImageApp(root)
    root.mainloop()
    
if __name__=='__main__':
    main()