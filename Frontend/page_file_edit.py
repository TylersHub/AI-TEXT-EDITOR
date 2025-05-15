from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QTextEdit, QLabel
from PyQt6.QtCore import Qt, pyqtSignal
from util_widgets import Page, SideBar, FileEditSideBar, PrimaryButton, LLMSuggestion
from util_widgets import primary_color, secondary_color, dark_text_color

import requests

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

    def get_diff(self, file_content_list: list, new_file_content_list: list) -> tuple[list, dict]:
        color_light = secondary_color.lighter(175).name()
        color_bright = secondary_color.lighter(125).name()

        index = 1
        mapper = {}

        output_words_list = []
        max_len = max(len(file_content_list), len(new_file_content_list))

        for i in range(max_len):
            word1 = file_content_list[i] if i < len(file_content_list) else ""
            word2 = new_file_content_list[i] if i < len(new_file_content_list) else ""

            if word1 == word2:
                output_words_list.append(word1)
            else:
                output_words_list.append(
                    f"<span style='background-color:{color_bright};color:white;'>({index})</span>"
                    f"<span style='background-color:{color_light};'>{word1}</span>"
                    f"<span style='background-color:{color_bright};color:white;'> → </span>"
                    f"<span style='background-color:{color_light};'>{word2}</span>"
                )

                mapper[index] = i
                index += 1

        return (output_words_list, mapper)

    def update_llm_suggestions(self, action: str, diff_index, string_index):
        self.file_edit_side_bar.suggestion_container_layout.removeWidget(self.suggestions[diff_index])
        self.suggestions[diff_index].deleteLater()

        if action == "ACCEPT":
            self.words_list[string_index] = self.new_file_content_list[string_index]

            # Charge 1 token
            self.side_bar.update_token_count_penalty(1)
        else:
            self.words_list[string_index] = self.file_content_list[string_index]

        self.file_editor.setHtml(" ".join(self.words_list))
    
    def generate_llm_suggestions(self, file_content: str):
        self.file_content_list = file_content.split()

        new_file_content = "" # LLM OUTPUT GOES HERE
        self.new_file_content_list = new_file_content.split()

        diff = self.get_diff(self.file_content_list, self.new_file_content_list)
        self.words_list = diff[0]
        self.mapper = diff[1]

        for diff_index, string_index in self.mapper.items():
            suggestion = LLMSuggestion(diff_index, string_index, self.file_content_list[string_index], self.new_file_content_list[string_index])
            suggestion.accept_action_label.clicked.connect(lambda _, di=diff_index, si=string_index: self.update_llm_suggestions("ACCEPT", di, si))
            suggestion.reject_action_label.clicked.connect(lambda _, di=diff_index, si=string_index: self.update_llm_suggestions("REJECT", di, si))
            self.suggestions[diff_index] = suggestion
            self.file_edit_side_bar.suggestion_container_layout.addWidget(suggestion)

        self.file_edit_side_bar.suggestion_container_layout.addStretch()

        self.file_editor.setHtml(" ".join(self.words_list))