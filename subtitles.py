"""
Minimal function to transform Whisper's bracketed output to SRT format
"""

import os
import re
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox

def whisper_to_srt(whisper_output):
    """
    Convert Whisper output to SRT format with minimal changes.
    """
    # Split into lines and process each line
    lines = whisper_output.strip().split('\n')
    srt_parts = []
    
    counter = 1
    for line in lines:
        # Match the timestamp pattern
        match = re.match(r'\[(\d{2}:\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}:\d{2}\.\d{3})\] (.*)', line.strip())
        if match:
            start_time, end_time, text = match.groups()
            
            # Convert dots to commas
            start_time = start_time.replace('.', ',')
            end_time = end_time.replace('.', ',')
            
            # Format as SRT entry
            srt_parts.append(f"{counter}")
            srt_parts.append(f"{start_time} --> {end_time}")
            srt_parts.append(f"{text.strip()}")
            srt_parts.append("")  # Empty line
            
            counter += 1
    
    return "\n".join(srt_parts)

def save_whisper_as_srt(whisper_output, original_file_path, parent_window=None, status_callback=None):
    """Save Whisper output as SRT with minimal conversion."""
    if not whisper_output or not original_file_path:
        if status_callback:
            status_callback("No transcription data available", "red")
        return False
    
    # Prepare file dialog
    filetypes = [('SubRip Subtitle', '*.srt')]
    initial_filename = os.path.splitext(os.path.basename(original_file_path))[0] + '.srt'
    initial_dir = os.path.dirname(original_file_path)
    
    save_path = filedialog.asksaveasfilename(
        title="Save SRT Subtitle File",
        defaultextension=".srt",
        initialfile=initial_filename,
        initialdir=initial_dir,
        filetypes=filetypes,
        parent=parent_window
    )
    
    if save_path:
        try:
            srt_content = whisper_to_srt(whisper_output)
            with open(save_path, 'w', encoding='utf-8') as srt_file:
                srt_file.write(srt_content)
            if status_callback:
                status_callback(f"SRT file saved to {save_path}", "green")
            return True
        except Exception as e:
            error_msg = f"Error saving SRT file: {str(e)}"
            if status_callback:
                status_callback(error_msg, "red")
            else:
                messagebox.showerror("SRT Saving Error", error_msg)
            return False
    else:
        if status_callback:
            status_callback("SRT file saving cancelled", "blue")
        return False