import os
import datetime

# Used to add timestampts to log messages saved to files
def log_message(message):
	curr_time = datetime.datetime.now()
	curr_time = curr_time.strftime("%Y-%m-%d %H:%M")
	return curr_time + ' - ' + message + '\n'

READ_LINE_LIMIT = 20

# Folder for each note_type property
NOTE_TYPE_FOLDERS = {
	"  - script_log": "zc_script_logs",
	"  - documentation_note": "documentation_notes",
	"  - general_note": "general_notes",
	"  - meeting_note": "meeting_notes",
	"  - project": "projects",
	"  - task": "tasks",
	"  - topic": "topics"
}

# Creation of the log file
vault_root = input("Input vault root path: ")
os.chdir(vault_root)
source_folder = os.path.join(vault_root, '1_to_organize')
log_folder = os.path.join(vault_root, 'zc_script_logs')

datetime_now = datetime.datetime.now()
current_timestamp = datetime_now.strftime("%Y%m%d_%H%M")
current_date = datetime_now.strftime("%Y-%m-%d")
execution_log_file_path = os.path.join(log_folder, current_timestamp + '_python_file_mover.md' )
execution_log = open(execution_log_file_path, 'w')


# Property header for log file
execution_log.write(f"""---
date: {current_date}
note_type:
  - script_log
cssclasses:
  - script_log
---
Execution log:
```log
""")


file_list = [os.path.join(source_folder, file) for file in os.listdir(os.path.join(source_folder)) if os.path.isfile(os.path.join(source_folder, file))]

total_files_moved = 0
files_not_moved = []

# Loop that moves files
for file in file_list:
	file_name = os.path.basename(file)
	opened_file = open(file)
	content = opened_file.read().splitlines()
	opened_file.close()
	execution_log.write(log_message(f"'{file_name}' | ").replace("\n", ''))

	for line_num, line_content in enumerate(content):
		if line_num > READ_LINE_LIMIT:
			execution_log.write(f"Reached line {line_num} without finding property 'note_type'\n")
			files_not_moved.append(f"'{file_name}' | Property note_type not found")
			break

		if line_content == 'note_type:':
			try: folder = NOTE_TYPE_FOLDERS[content[line_num + 1]]
			except:
				execution_log.write("Note type did not match any criteria\n")
				files_not_moved.append(f"'{file_name}' | Note type found: '{content[line_num + 1]}'")
				break

			try:
				os.rename(file, os.path.join(vault_root, folder, file_name))
				execution_log.write(f"Sucessfully moved to '{folder}'\n")
				total_files_moved += 1
				break
			except Exception as err:
				if type(err) == FileExistsError:
					execution_log.write(f"Could not move note. Note already exists in '{folder}'\n")
				else:
					execution_log.write(str(type(err).__name__) + " | " + str(err) + "\n")
					files_not_moved.append(f"'{file_name}' | Targeted folder: '{folder}'")
				break


execution_log.write('\n')
execution_log.write(log_message(f"End of notes\n"))
execution_log.write(log_message(f"Total notes moved: {total_files_moved}"))
execution_log.write(log_message(f"Total notes not moved: {len(files_not_moved)}\n"))

# Cria task caso hajam notas que nao foram movidas
if len(files_not_moved) >= 1:
	execution_log.write(log_message(f"List of notes not moved"))
	file_list_string = '\n'.join(files_not_moved)
	execution_log.write(file_list_string)
	execution_log.write('\n\n')

	execution_log.write(log_message(f"Creating task to check notes that were not moved"))
	task_note_path = os.path.join(vault_root, '0_inbox', current_timestamp + ' Verificar arquivos nao movidos.md')
	task_note = open(task_note_path, 'w')
	task_note.write(f"""---
date: {current_date}
status: false
projects:
  - "[[This vault]]"
topics:
meetings:
tasks:
scope:
  - personal
tags:
  - "#generated_by_script"
aliases:
note_type:
  - task
cssclasses:
  - task
---
Lista de notas que nao foram movidas:
- [ ] """)
	file_list_checklist = '\n- [ ] '.join(files_not_moved)
	task_note.write(file_list_checklist)
	task_note.close()
else:
	execution_log.write(log_message(f"All notes moved successfully"))

execution_log.write(log_message(f"End of script"))
execution_log.write(r"```")
execution_log.close()