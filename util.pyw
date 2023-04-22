# Utilities
# image:resizer,compresser
# video:resizer

# Inititalization
from customtkinter import filedialog,BOTH,X,Y,CTkButton,CTkLabel,LEFT,CTk,CTkFrame,CTkToplevel,TOP,CTkSlider,HORIZONTAL,IntVar,StringVar,CTkComboBox,CTkProgressBar
from tkinter import messagebox
import cv2,os
from vidgear.gears import WriteGear
from PIL import ImageTk,Image
import moviepy.editor as mp

root = CTk()
root.geometry("700x140")
try:
	root.iconbitmap("chrotilsIcon.ico")
except:pass
root.resizable(0,0)
root.title("chrotils")

# Frames
homeFrame = CTkFrame(root)

# Logic
def homeLoader():
    homeFrame.pack(fill=BOTH,padx=10,pady=10,ipadx=10,ipady=10)
    imageButton.pack(side=LEFT,padx=20)
    videoButton.pack(side=LEFT,padx=20)

def useLoader():
    match comboVal.get():
        case "Image Resizer":return imageResizerLoader()
        case "Image Compressor":return imageCompressorLoader()
        case "Video Resizer":return videoResizerLoader()
        # case "Video Compressor":return videoCompressorLoader()
        case _:messagebox.showerror("chrotils","No such utility found, select a valid one")
    
def imageComboLoader():
    combo.pack_forget()
    comboVal.set("Image Resizer")
    combo.configure(values=["Image Resizer","Image Compressor"])
    useButton.pack(pady=10)
    combo.pack()

def imageResizerLoader():
    global imageResizerWindow,imageResizerImportButton
    imageResizerWindow = CTkToplevel()
    imageResizerWindow.title("Image Resizer")
    imageResizerWindow.geometry("800x300")
    imageResizerImportButton = CTkButton(imageResizerWindow,text="import image",command=lambda:fileImport("imageResizer"))
    imageResizerImportButton.pack(padx=20,pady=20,side=TOP)

    imageResizerWindow.mainloop()

def fileImport(util):
        match util:
            case "imageResizer":
                imageFile = filedialog.askopenfilename(filetypes=[("Image Files",".png .jpg .jpeg")])
                if type(imageFile)==type(""):imageResizer(imageFile)
            case "imageCompressor":
                imageFile = filedialog.askopenfilename(filetypes=[("Image Files",".png .jpg .jpeg")])
                if type(imageFile)==type(""):imageCompressor(imageFile)  
            case "videoResizer":
                videoFile = filedialog.askopenfilename(filetypes=[("Video Files",".mkv .mp4")])
                if type(videoFile)==type(""):videoResizer(videoFile)
            case "videoCompressor":
                videoFile = filedialog.askopenfilename(filetypes=[("Video Files",".mkv .mp4")])
                if type(videoFile)==type(""):videoCompressor(videoFile)

def imageResizer(file):
    global imageSizeShower
    imageResizerImportButton.pack_forget()
    pilImage = Image.open(file)
    height,width = pilImage.height,pilImage.width
    photoImage = ImageTk.PhotoImage(image=pilImage.resize(size=((200*width)//height,200)))
    thumbnailImageLabel = CTkLabel(imageResizerWindow,image=photoImage,text=None)
    thumbnailImageLabel.pack()
    imageSizeShower = CTkLabel(imageResizerWindow,text=f"{width}x{height}")
    imageSizeShower.pack()
    imageResizeVal.set(int(width*0.8))
    imageResizeHeightEstimator(int(width*0.8),height)
    imageResizerSlider = CTkSlider(imageResizerWindow,from_=30,to=width,variable=imageResizeVal,orientation=HORIZONTAL,command=lambda x:imageResizeHeightEstimator(width,height))
    imageResizerSlider.pack(fill=X)
    imageResizeSave = CTkButton(imageResizerWindow,text="Save",command=lambda:imageResizeSaver(pilImage,file,width,height))
    imageResizeSave.pack()


def imageResizeHeightEstimator(width,height):
    imageSizeShower.configure(text=f"{imageResizeVal.get()}x{(imageResizeVal.get()*height)//width}")

def imageResizeSaver(pilImage,file,width,height):
    fileName = file.split("x")[-1].split(".")[0]+"_resized."+file.split("x")[-1].split(".")[1]
    fp = filedialog.asksaveasfilename(initialdir="/".join(file.split("x")[:-1]),initialfile=fileName)
    if fp!='':
        try:
            pilImage.resize(size=(imageResizeVal.get(),(imageResizeVal.get()*height)//width)).save(fp=fp)
            messagebox.showinfo("imageResizer","Image resized successfully")
        except:
            messagebox.showinfo("imageResizer","Something went wrong")

def imageCompressorLoader():
    global imageCompressorImportButton,imageCompressorWindow
    imageCompressorWindow = CTkToplevel(root)
    imageCompressorWindow.title("Image Compressor")
    imageCompressorWindow.geometry("500x250")
    imageCompressorImportButton = CTkButton(imageCompressorWindow,command=lambda:fileImport("imageCompressor"))
    imageCompressorImportButton.pack()
    imageCompressorWindow.mainloop()

def imageCompressor(file):
    imageCompressorImportButton.pack_forget()
    pilImage = Image.open(file)
    height,width = pilImage.height,pilImage.width
    photoImage = ImageTk.PhotoImage(pilImage.resize(size=((width*200)//height,200)))
    imageCompressorThumbnail = CTkLabel(imageCompressorWindow,image=photoImage,text=None)
    imageCompressorThumbnail.pack()
    imageCompressorSaveButton = CTkButton(imageCompressorWindow,command=lambda:imageCompressorSaver(file,pilImage,height,width),text="Save")
    imageCompressorSaveButton.pack(padx=10,pady=10)

def imageCompressorSaver(file,pilImage,height,width):
    pilImage = pilImage.resize(size=(width,height),resample=Image.Resampling.LANCZOS)
    fileName = file.split("x")[-1].split(".")[0]+"_compressed."+file.split("x")[-1].split(".")[1]
    fp = filedialog.asksaveasfilename(initialdir="/".join(file.split("x")[:-1]),initialfile=fileName)
    if fp!='':
        try:
            pilImage.save(optimize=True,fp=fp)
            messagebox.showinfo("imageCompressor","Image compressed successfully")
        except:
            messagebox.showinfo("imageCompressor","Something went wrong")

def videoComboLoader():
    global combo,comboVal,useButton
    combo.pack_forget()
    comboVal.set("Video Resizer")
    combo.configure(values=["Video Resizer"])
    useButton.pack(pady=10)
    combo.pack()

def videoResizerLoader():
    global videoResizerWindow,videoResizerImportButton
    videoResizerWindow = CTkToplevel()
    videoResizerWindow.title("Video Resizer")
    videoResizerWindow.geometry("800x170")

    videoResizerImportButton = CTkButton(videoResizerWindow,text="import video",command=lambda:fileImport("videoResizer"))
    videoResizerImportButton.pack(padx=20,pady=20,side=TOP)

    videoResizerWindow.mainloop()

def videoResizer(file):
    global videoResizeShower
    if file!="":
        videoResizerImportButton.pack_forget()
        cvInputVideo = cv2.VideoCapture(file)
        outputFileName = file.split("x")[-1].split(".")[0]+"_resized."+file.split("x")[-1].split(".")[1]
        fps = cvInputVideo.get(cv2.CAP_PROP_FPS)
        frames = cvInputVideo.get(cv2.CAP_PROP_FRAME_COUNT)
        width = int(cvInputVideo.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cvInputVideo.get(cv2.CAP_PROP_FRAME_HEIGHT))
        videoResizeShower = CTkLabel(videoResizerWindow,text=f"{width}x{height}")
        videoResizeShower.pack()
        videoResizerSlider = CTkSlider(videoResizerWindow,from_=30,to=width,variable=videoResizeVal,orientation=HORIZONTAL,command=lambda x:videoResizeHeightEstimator(width,height))
        videoResizerSlider.pack(fill=X)
        videoResizeVal.set(int(width*0.8))
        videoResizeHeightEstimator(int(width*0.8),height)
        videoResizedSaver = CTkButton(videoResizerWindow,text="Save video",command=lambda:videoResizeSaver(file,cvInputVideo,outputFileName,fps,width,height))
        videoResizedSaver.pack()

def videoResizeHeightEstimator(width,height):
    videoResizeShower.configure(text=f"{videoResizeVal.get()}x{(videoResizeVal.get()*height)//width}")
    
def videoResizeSaver(file,sourceVideo,outputFileName,fps,width,height):
    global videoResizeProgress
    try:
        newHight = (videoResizeVal.get()*height)//width
        newWidth = videoResizeVal.get()
        fp = filedialog.asksaveasfilename(initialfile=outputFileName)
        tempFp = ""
        if fp!='':
            tempFp="".join(fp.split(".")[:-1])+"_wait."+"".join(fp.split(".")[-1])
            # cvOutputVideo = cv2.VideoWriter(fp,cv2.VideoWriter_fourcc(*"avc1"),fps,(newWidth,newHight))
            cvOutputVideo = WriteGear(output=tempFp,compression_mode=False,logging=False,**{"-fps":fps})
            videoProgressFrame = CTkFrame(videoResizerWindow)
            videoProgressFrame.pack(padx=10,pady=10,fill="x")
            videoResizeProgressShower = CTkLabel(videoProgressFrame,bg_color="transparent",text="0%")
            videoResizeProgressShower.pack(padx=10,pady=10)
            videoResizeProgress = CTkProgressBar(videoProgressFrame,orientation=HORIZONTAL,width=videoResizerWindow.winfo_width())
            videoResizeProgress.pack(padx=10,pady=10,side=LEFT,fill="x")
            frameCount = sourceVideo.get(cv2.CAP_PROP_FRAME_COUNT)
            count = 0
            videoResizeProgress.start()
            videoResizeProgress.set(0)
            while(sourceVideo.isOpened()):
                ret,frame = sourceVideo.read()
                if ret:
                    frame = cv2.resize(frame,(newWidth,newHight))
                    cvOutputVideo.write(frame)
                    count+=1
                    prog = str(count/frameCount*100)[:4]
                    videoResizeProgressShower.configure(text=f"{prog}%")
                    videoResizeProgressShower.update_idletasks()
                    videoResizeProgress.set(count/frameCount)
                    videoResizerWindow.update_idletasks()
                else:break
            videoResizeProgress.stop()
            videoResizeProgress.configure(mode="indeterminate",indeterminate_speed=1)
            videoResizeProgressShower.configure(text="Compiling audio...")
            videoResizeProgress.start()
            videoResizerWindow.update()
            sourceVideo.release()
            cvOutputVideo.close()
            mpInputFile = mp.VideoFileClip(file)
            mpInputAudio = mpInputFile.audio.copy()
        
            mpOutputFile = mp.VideoFileClip(tempFp)
            mpOutputFile.audio = mpInputAudio
            mpOutputFile.write_videofile(filename=fp,fps=fps)

            
            mpInputAudio.close()
            mpInputFile.close()
            mpOutputFile.close()
            os.remove(tempFp)
            videoResizeProgress.stop()
            videoProgressFrame.pack_forget()
            messagebox.showinfo("Video Resizer","Video resized successfully")
            cv2.destroyAllWindows()
    except:
        messagebox.showerror("Video Resizer","Something went wrong")

def videoCompressorLoader():
    global videoCompressorImportButton,videoCompressorWindow
    videoCompressorWindow = CTkToplevel()
    videoCompressorWindow.title("Video Compressor")
    videoCompressorWindow.geometry("800x150")

    videoCompressorImportButton = CTkButton(videoCompressorWindow,text="import video",command=lambda:fileImport("videoCompressor"))
    videoCompressorImportButton.pack(padx=20,pady=20,side=TOP)

    videoCompressorWindow.mainloop()

def videoCompressor(file):
    global videoCompressShower
    if file!="":
        videoCompressorImportButton.pack_forget()
        cvInputVideo = cv2.VideoCapture(file)
        fps = cvInputVideo.get(cv2.CAP_PROP_FPS)
        width = int(cvInputVideo.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cvInputVideo.get(cv2.CAP_PROP_FRAME_HEIGHT))
        outputFileName = file.split("x")[-1].split(".")[0]+"_compressed."+file.split("x")[-1].split(".")[1]
        videoResizedSaver = CTkButton(videoCompressorWindow,text="Save video",command=lambda:videoCompressSaver(file,cvInputVideo,outputFileName,fps,width,height))
        videoResizedSaver.pack(padx=10,pady=10)

def videoCompressSaver(file,sourceVideo,outputFileName,fps,width,height):
    fp = filedialog.asksaveasfilename(initialfile=outputFileName)
    tempFp = ""
    if fp!=tempFp:
        tempFp="".join(fp.split(".")[:-1])+"_wait."+"".join(fp.split(".")[-1])
        cvOutputVideo = WriteGear(output=tempFp,compression_mode=False,logging=False,**{"-fps":fps})
        videoProgressFrame = CTkFrame(videoCompressorWindow)
        videoProgressFrame.pack(padx=10,pady=10,fill="x")
        videoCompressProgressShower = CTkLabel(videoProgressFrame,bg_color="transparent",text="0%")
        videoCompressProgressShower.pack(padx=10,pady=10)
        videoCompressProgress = CTkProgressBar(videoProgressFrame,orientation=HORIZONTAL,width=videoCompressorWindow.winfo_width())
        videoCompressProgress.pack(padx=10,pady=10,side=LEFT,fill="x")
        frameCount = sourceVideo.get(cv2.CAP_PROP_FRAME_COUNT)
        count = 0
        videoCompressProgress.start()
        videoCompressProgress.set(0)
        while(sourceVideo.isOpened()):
            ret,frame = sourceVideo.read()
            if ret:
                # frame = cv2.resize(frame,(width,height),interpolation=Image.Resampling.LANCZOS)
                frame = cv2.resize(frame,(width,height),interpolation=cv2.INTER_AREA,fx=0.5,fy=0.5)
                cvOutputVideo.write(frame)
                count+=1
                prog = str(count/frameCount*100)[:4]
                videoCompressProgressShower.configure(text=f"{prog}%")
                videoCompressProgressShower.update_idletasks()
                videoCompressProgress.set(count/frameCount)
                videoCompressorWindow.update_idletasks()
            else:break
        videoCompressProgress.stop()
        videoCompressProgress.configure(mode="indeterminate",indeterminate_speed=1)
        videoCompressProgressShower.configure(text="Compiling audio...")
        videoCompressProgress.start()
        videoCompressorWindow.update()
        
        sourceVideo.release()
        cvOutputVideo.close()
        mpInputFile = mp.VideoFileClip(file)
        mpInputAudio = mpInputFile.audio.copy()
    
        mpOutputFile = mp.VideoFileClip(tempFp)
        mpOutputFile.audio = mpInputAudio
        mpOutputFile.write_videofile(filename=fp,fps=fps)


        mpInputAudio.close()
        mpInputFile.close()
        mpOutputFile.close()
        os.remove(tempFp)
        videoCompressProgress.stop()
        videoProgressFrame.pack_forget()
        messagebox.showinfo("Video Compressor","Video compressed successfully")
        cv2.destroyAllWindows()



    

# Widgets and vars]
comboVal = StringVar()
imageResizeVal = IntVar()
videoResizeVal = IntVar()
imageButton = CTkButton(homeFrame,width=100,height=100,text="Image",command=imageComboLoader)
videoButton = CTkButton(homeFrame,width=100,height=100,text="Video",command=videoComboLoader)

useButton = CTkButton(homeFrame,command=useLoader,text="Use")
combo = CTkComboBox(homeFrame,state="normal",variable=comboVal)

# Execution
homeLoader()
root.mainloop()
