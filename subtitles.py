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

def save_whisper_as_srt(whisper_output, original_file_path, parent_window=None, status_callback=None, return_content=False):
    """
    Save Whisper output as SRT.
    If return_content is True, returns the SRT content as a string.
    Otherwise, prompts the user to save the file and returns True/False.
    """
    if not whisper_output:
        if status_callback:
            status_callback("No transcription data available to convert to SRT.", "red")
        return "" if return_content else False

    srt_content = whisper_to_srt(whisper_output)

    if return_content:
        return srt_content

    if not original_file_path:
        if status_callback:
            status_callback("Original file path is missing, cannot suggest a save name.", "red")
        original_file_path = "transcription.txt"

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
