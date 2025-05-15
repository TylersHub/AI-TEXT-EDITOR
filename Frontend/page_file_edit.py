from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QTextEdit, QLabel
from PyQt6.QtCore import Qt, pyqtSignal
from Frontend.util_widgets import Page, SideBar, FileEditSideBar, PrimaryButton, LLMSuggestion
from Frontend.util_widgets import primary_color, secondary_color, dark_text_color
from llm.llm_api import generate_with_ollama

import difflib

import requests
import json

class FileEditPage(Page):
    def __init__(self, session_token, account_type, user_id, file_id, edit_mode, new_file):
        super().__init__()

        self.session_token = session_token
        self.account_type = account_type
        self.user_id = user_id
        self.file_id = file_id
        self.edit_mode = edit_mode
        self.new_file = new_file

        self.central_layout = QHBoxLayout(self)
        self.central_layout.setContentsMargins(0, 0, 0, 0)
        self.central_layout.setSpacing(0)

        self.side_bar = SideBar(account_type, user_id)
        self.central_layout.addWidget(self.side_bar, stretch=1)

        self.body_layout = QVBoxLayout()
        self.body_layout.setContentsMargins(0, 32, 0, 32)
        self.body_layout.setSpacing(32)
        self.central_layout.addLayout(self.body_layout, stretch=3)

        self.file_edit_side_bar = FileEditSideBar(user_id, file_id, new_file, edit_mode)
        self.central_layout.addWidget(self.file_edit_side_bar, stretch=1)

        self.body_header = QLabel("Edit File")
        self.body_header.setStyleSheet(f"color: {dark_text_color.name()}; font-size: 32px; font-weight: 600;")
        self.body_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.body_layout.addWidget(self.body_header)

        if edit_mode == "self":
            self.file_editor = QTextEdit(self.file_edit_side_bar.file_content)
            self.file_editor.setStyleSheet(
                f"color: {dark_text_color.name()};"
                f"background-color: {primary_color.darker(110).name()};"
                "padding: 0 4px;"
                "border-top: 2px solid;"
                "border-bottom: 2px solid;"
                "font-size: 16px;"
            )
            self.body_layout.addWidget(self.file_editor)


        elif edit_mode == "llm":
            self.suggestions = {}
            file_content = self.file_edit_side_bar.file_content

            self.file_editor = QTextEdit()
            self.file_editor.setStyleSheet(
                f"color: {dark_text_color.name()};"
                f"background-color: {primary_color.darker(110).name()};"
                "padding: 0 4px;"
                "border-top: 2px solid;"
                "border-bottom: 2px solid;"
                "font-size: 16px;"
            )
            self.file_editor.setReadOnly(True)
            self.body_layout.addWidget(self.file_editor)

            self.generate_llm_suggestions(file_content)
        else:
            print(f"Error (FileEditPage init): Wrong edit mode '{edit_mode}' provided")
            self.side_bar.navigate_to_home.emit()

        # Call-To-Action
        if account_type == "FREE":
            self.exit_button = PrimaryButton("Exit")
            self.exit_button.clicked.connect(self.discard_file)
            self.body_layout.addWidget(self.exit_button)
            self.body_layout.setAlignment(self.exit_button, Qt.AlignmentFlag.AlignHCenter)
        else:
            self.action_button_layout = QHBoxLayout()
            self.action_button_layout.setContentsMargins(0, 0, 0, 0)
            self.action_button_layout.setSpacing(0)
            self.body_layout.addLayout(self.action_button_layout)

            self.action_button_layout.addStretch()

            self.discard_button = PrimaryButton("Discard")
            self.discard_button.clicked.connect(self.discard_file)
            self.action_button_layout.addWidget(self.discard_button)

            self.action_button_layout.addStretch()

            self.save_button = PrimaryButton("Save")
            self.save_button.clicked.connect(self.save_file)
            self.action_button_layout.addWidget(self.save_button)

            self.action_button_layout.addStretch()

        if not new_file:
            self.file_edit_side_bar.delete_file_button.clicked.connect(self.delete_file)

    def delete_file(self):
        try:
            headers = {"Content-Type": "application/json"}
            
            response = requests.delete(f"http://127.0.0.1:5000/documents/{self.file_id}?user_id={self.user_id}", headers=headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error discarding file: {e}")

        self.side_bar.navigate_to_home.emit()
    
    def discard_file(self):
        if self.new_file:
            try:
                headers = {"Content-Type": "application/json"}
                
                response = requests.delete(f"http://127.0.0.1:5000/documents/{self.file_id}?user_id={self.user_id}", headers=headers)
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                print(f"Error discarding file: {e}")

        self.side_bar.navigate_to_home.emit()

    def save_file(self):
        file_name = self.file_edit_side_bar.name_text_box.text()
        file_content = self.file_editor.toPlainText()

        try:
            input_data = {"title": file_name, "content": file_content}
            headers = {"Content-Type": "application/json"}
            
            response = requests.put(f"http://127.0.0.1:5000/documents/{self.file_id}?user_id={self.user_id}", json=input_data, headers=headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error saving file: {e}")

        self.side_bar.navigate_to_home.emit()

    def get_diff(self, original_text: str, corrected_text: str) -> tuple[list[str], dict[int, int]]:
        original_words = original_text.split()
        corrected_words = corrected_text.split()

        matcher = difflib.SequenceMatcher(None, original_words, corrected_words)
        color_light = secondary_color.lighter(175).name()
        color_bright = secondary_color.lighter(125).name()

        output_words = []
        mapper = {}
        suggestion_index = 1

        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == 'equal':
                output_words.extend(corrected_words[j1:j2])
            else:
                for j, word in enumerate(corrected_words[j1:j2]):
                    output_words.append(
                        f"<span style='background-color:{color_bright};color:white;'>({suggestion_index})</span> "
                        f"<span style='background-color:{color_light};'>{word}</span>"
                    )
                    mapper[suggestion_index] = j1 + j
                    suggestion_index += 1

        return output_words, mapper


    def update_llm_suggestions(self, action: str, diff_index, string_index):
        suggestion_widget = self.suggestions.pop(diff_index, None)
        if suggestion_widget:
            self.file_edit_side_bar.suggestion_container_layout.removeWidget(suggestion_widget)
            suggestion_widget.deleteLater()

        if action == "ACCEPT":
            self.words_list[string_index] = self.new_file_content_list[string_index]
            self.side_bar.update_token_count_penalty(1)
        else:
            self.words_list[string_index] = self.file_content_list[string_index]

        self.file_editor.setHtml(" ".join(self.words_list))


    def generate_llm_suggestions(self, file_content: str):

        try:
            prompt = (
                "Instructions:\n"
                "1. Replace each word in the blacklist with asterisks — one asterisk per letter. For example, \"yellow\" becomes \"******\".\n"
                "2. Do not censor any words that are not in the blacklist.\n"
                "3. Fix all grammar, punctuation, and clarity issues in the text.\n"
                "4. Output only the corrected and censored paragraph — no extra explanation.\n\n"
                "Example:\n"
                "Input: I seen the yellow sky and it dont look normal.\n"
                "Output: I saw the ****** sky, and it didn't look normal.\n\n"
                f"Input: {file_content}\n"
                "Output:"
            )

            print("🧠 Prompt sent to LLM:\n", prompt)  # optional debug
            new_file_content = generate_with_ollama(prompt=prompt, model="llama3:8b", stream=False).strip()
            print("✅ LLM response received.")  # optional debug

        except Exception as e:
            print(f"❌ Error contacting LLM: {e}")
            new_file_content = file_content

        self.file_content_list = file_content.split()
        self.new_file_content_list = new_file_content.split()

        self.words_list, self.mapper = self.get_diff(file_content, new_file_content)

        for diff_index, string_index in self.mapper.items():
            if string_index >= len(self.new_file_content_list):
                print(f"⚠️ Skipping invalid diff index {diff_index}: string_index {string_index} out of range")
                continue

            original = self.file_content_list[string_index] if string_index < len(self.file_content_list) else ""
            corrected = self.new_file_content_list[string_index]
            suggestion = LLMSuggestion(diff_index, string_index, original, corrected)

            suggestion.accept_action_label.clicked.connect(lambda _, di=diff_index, si=string_index: self.update_llm_suggestions("ACCEPT", di, si))
            suggestion.reject_action_label.clicked.connect(lambda _, di=diff_index, si=string_index: self.update_llm_suggestions("REJECT", di, si))

            self.suggestions[diff_index] = suggestion
            self.file_edit_side_bar.suggestion_container_layout.addWidget(suggestion)

        self.file_edit_side_bar.suggestion_container_layout.addStretch()
        self.file_editor.setHtml(" ".join(self.words_list))

