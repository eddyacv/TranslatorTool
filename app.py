import tkinter as tk
from tkinter import filedialog, messagebox
from processor import process_folder


def select_input_folder():
    folder = filedialog.askdirectory()
    input_var.set(folder)


def select_output_folder():
    folder = filedialog.askdirectory()
    output_var.set(folder)


def start():
    input_folder = input_var.get()
    output_folder = output_var.get()

    if not input_folder or not output_folder:
        messagebox.showerror("Error", "Selecciona carpeta origen y carpeta destino.")
        return

    process_folder(
        input_folder=input_folder,
        output_folder=output_folder,
        generate_subs=subs_var.get(),
        burn_subs=burn_var.get(),
        generate_audio=audio_var.get(),
        replace_original_audio=replace_audio_var.get()
    )

    messagebox.showinfo("Finalizado", "Proceso terminado correctamente.")


root = tk.Tk()
root.title("Traductor de videos a español")
root.geometry("600x350")

input_var = tk.StringVar()
output_var = tk.StringVar()

subs_var = tk.BooleanVar(value=True)
burn_var = tk.BooleanVar(value=True)
audio_var = tk.BooleanVar(value=False)
replace_audio_var = tk.BooleanVar(value=False)

tk.Label(root, text="Carpeta padre origen").pack()
tk.Entry(root, textvariable=input_var, width=70).pack()
tk.Button(root, text="Seleccionar carpeta origen", command=select_input_folder).pack(pady=5)

tk.Label(root, text="Carpeta de salida").pack()
tk.Entry(root, textvariable=output_var, width=70).pack()
tk.Button(root, text="Seleccionar carpeta destino", command=select_output_folder).pack(pady=5)

tk.Checkbutton(root, text="Generar subtítulos en español", variable=subs_var).pack(anchor="w", padx=40)
tk.Checkbutton(root, text="Incrustar subtítulos al video", variable=burn_var).pack(anchor="w", padx=40)
tk.Checkbutton(root, text="Generar audio en español", variable=audio_var).pack(anchor="w", padx=40)
tk.Checkbutton(root, text="Reemplazar audio original por español", variable=replace_audio_var).pack(anchor="w", padx=40)

tk.Button(root, text="Procesar videos", command=start, height=2, width=25).pack(pady=20)

root.mainloop()