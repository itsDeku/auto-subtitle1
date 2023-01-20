from tkinter import *
from tkinter import filedialog
import os
import ffmpeg
import whisper
import tempfile
import warnings
from .utils import filename, write_srt





def submit(input_dir,output_dir,model_name,output_str,sub_only):  
    
    if model_name.endswith(".en"):
        warnings.warn(f"{model_name} is an English-only model, forcing English detection.")
    audios = get_audio(input_dir)
    model = whisper.load_model(model_name)
 
    subtitles = get_subtitles(
        audios, output_str or sub_only, output_dir, lambda audio_path: model.transcribe(input_dir)
    )
    if sub_only:
        return

    # bash command to download a youtube video with `youtube-dl` and save it as `video.mp4`:
    # youtube-dl -f 22 -o video.mp4 https://www.youtube.com/watch?v=QH2-TGUlwu4

    for path, srt_path in subtitles.items():
        out_path = os.path.join(output_dir, f"{filename(path)}.mp4")
        print(f"Adding subtitles to {filename(path)}...")
        stderr = ffmpeg.concat(video.filter('subtitles', srt_path, force_style="OutlineColour=&H40000000,BorderStyle=3"), audio, v=1, a=1).output(out_path).run(quiet=True, overwrite_output=True)
        print(f"Saved subtitled video to {os.path.abspath(out_path)}.")


          

def get_subtitles(audio_paths: list, output_srt: bool, output_dir: str, transcribe: callable):
    srt_path = output_dir if output_srt else tempfile.gettempdir()
    subtitles_path = {}

    for path, audio_path in audio_paths.items():
        srt_path = os.path.join(srt_path, f"{filename(path)}.srt")

        print(
            f"Generating subtitles for {filename(path)}... This might take a while."
        )

        warnings.filterwarnings("ignore")
        result = transcribe(audio_path)
        warnings.filterwarnings("default")

        with open(srt_path, "w", encoding="utf-8") as srt:
            write_srt(result["segments"], file=srt)

        subtitles_path[path] = srt_path

    return subtitles_path

def get_audio(paths):
    temp_dir = tempfile.gettempdir()

    audio_paths = {}
    print( os.path.splitext(os.path.basename(paths))[0])
   
    print(f"Extracting audio from {filename(paths)}...")
    output_path = os.path.join(temp_dir, f"{filename(paths)}.wav")
    ffmpeg.input(paths).output(
        output_path,
        acodec="pcm_s16le", ac=1, ar="16k"
    ).run(quiet=True, overwrite_output=True)

    audio_paths[paths] = output_path

    return audio_paths


def open_Input(obj):
   file = filedialog.askopenfile(mode='r')
   if file:
      filepath = os.path.abspath(file.name)
      obj.delete(0,'end')
      obj.insert(0,str(filepath))
def open_Output(obj):
   file = filedialog.askdirectory()
   if file:
      filepath = os.path.abspath(file)
      obj.delete(0,'end')
      obj.insert(0,str(filepath))

def Tk_Window():
# Create object
    root = Tk()
# Adjust size
    root.geometry( "550x250" )
    root.title("auto subtitle")
    

    input_dir = Label(root,text="enter the input directory: ")
    input_dir.grid(row=0,column=0,sticky=W)
    in_dir = Entry(root,width=50)
    in_dir.grid(row=0,column=1,padx=5,sticky=W)
    in_brow = Button(root, text="Browse", command=lambda :open_Input(in_dir))
    in_brow.grid(row=0,column=2,sticky=W)
    output_dir = Label(root,text="enter the output directory: ")
    output_dir.grid(row=1,column=0,sticky=W)
    out_dir = Entry(root,width=50)
    out_dir.grid(row=1,column=1,padx=5,sticky=W)
    out_brow = Button(root, text="Browse", command=lambda :open_Output(out_dir))
    out_brow.grid(row=1,column=2,sticky=W)

    # Dropdown menu options
    options = [
        "tiny.en",
        "tiny",
        "base.en",
        "base",
        "small.en",
        "small",
        "medium.en",
        "medium",
        "large-v1",
        "large-v2",
        "large"
    ]


    sel_model = Label(root,text="select the model: ")
    sel_model.grid(row=2,column=0,sticky=W)
    srt_model = StringVar()
    srt_model.set( "tiny.en" )
    model_drop = OptionMenu( root , srt_model , *options )
    model_drop.grid(row=2,column=1,sticky=W)
    
    out_str = BooleanVar() 
    str_only = BooleanVar()
    Checkbutton3 = BooleanVar()
    
    
    output_str = Checkbutton(root, text = "whether to output the .srt file along with the video files (default: False)", variable = out_str, onvalue = 1, offvalue = 0)
    
    sub_only = Checkbutton(root, text = "whether to only generate the .srt file and not create overlayed video (default: False)", variable = str_only, onvalue = 1, offvalue = 0)
    
    verbose = Checkbutton(root, text = " whether to print out the progress and debug messages (default: False)", variable = Checkbutton3, onvalue = 1, offvalue = 0)  
        
    output_str.grid(row=3,columnspan=3,sticky=W)  
    sub_only.grid(row=4,columnspan=3,sticky=W)  
    verbose.grid(row=5,columnspan=3,sticky=W)
    submit_btn = Button(root, text="Convert",command=lambda : submit(in_dir.get(),out_dir.get(),srt_model.get(),out_str.get(),str_only.get()))
    submit_btn.grid(row=6,columnspan=3,pady=5)


    root.mainloop()

