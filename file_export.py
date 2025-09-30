# file_export.py
import os
from tkinter import filedialog, messagebox, Button, Frame
import tkinter as tk  # Import tkinter here

def create_export_button(parent, app):
    """Creates the export transcription button."""
    export_frame = Frame(parent)  # No need to pack here
    export_button = Button(
        export_frame,
        text="Export Transcription",
        command=lambda: export_transcription(app),  # Pass app instance
        font=("Arial", 12),
        state=tk.DISABLED  # Initially disabled
    )
    export_button.pack(fill="x", padx=10, pady=5)
    return export_frame, export_button  # Return both frame and button

def export_transcription(app):
    """
    Export the transcription.
    If SRT is enabled and diarization is not enabled, convert Whisper output to SRT using save_whisper_as_srt.
    If SRT and diarization are both enabled, export the already-processed diarized text.
    Otherwise, export plain text.
    """
    # Update current_text from the transcription textbox.
    if hasattr(app, 'transcription_box'):
        app.current_text = app.transcription_box.get("1.0", tk.END).strip()

    if not app.current_text:
        # Nothing to export.
        return

    if app.srt_var.get():
        app.debug_print("Exporting as SRT")
        initial_filename = os.path.splitext(os.path.basename(app.file_path))[0] + '.srt'
        initial_dir = os.path.dirname(app.file_path)
        save_path = filedialog.asksaveasfilename(
            title="Save Transcription as SRT File",
            defaultextension=".srt",
            initialfile=initial_filename,
            initialdir=initial_dir,
            filetypes=[('SRT File', '*.srt'), ('All Files', '*.*')],
            parent=app.root
        )
        if save_path:
            try:
                with open(save_path, 'w', encoding='utf-8') as out_f:
                    out_f.write(export_content)
                app.update_status(f"SRT file saved to {save_path}", "green")
            except Exception as e:
                msg = f"Error saving SRT file: {str(e)}"
                app.update_status(msg, "red")
                messagebox.showerror("SRT Saving Error", msg)
        else:
            app.update_status("SRT file saving cancelled", "blue")
    else:
        app.debug_print("Exporting as plain text (.txt)")
        initial_filename = os.path.splitext(os.path.basename(app.file_path))[0] + '.txt'
        initial_dir = os.path.dirname(app.file_path)
        save_path = filedialog.asksaveasfilename(
            title="Save Transcription as Text File",
            defaultextension=".txt",
            initialfile=initial_filename,
            initialdir=initial_dir,
            filetypes=[('Text File', '*.txt'), ('All Files', '*.*')],
            parent=app.root
        )
        if save_path:
            try:
                with open(save_path, 'w', encoding='utf-8') as out_f:
                    out_f.write(app.current_text)
                app.update_status(f"Plain text file saved to {save_path}", "green")
            except Exception as e:
                msg = f"Error saving text file: {str(e)}"
                app.update_status(msg, "red")
                messagebox.showerror("TXT Saving Error", msg)
        else:
            app.update_status("Text file saving cancelled", "blue")
