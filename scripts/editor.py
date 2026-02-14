import sys
import re
import locale
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QPushButton, QListWidget, QTextEdit,
    QComboBox, QFileDialog, QColorDialog, QMessageBox, QProgressBar,
    QFrame, QSplitter, QScrollArea, QMenu, QSizePolicy, QApplication
)

from PySide6.QtGui import (
    QPixmap, QImage, QFont, QColor, QAction, QIcon, QPalette
)
from PySide6.QtCore import Qt, Signal, Slot, QTimer

from PIL import Image, ImageTk, ImageDraw, ImageFont
from PIL.ImageQt import ImageQt
from googletrans import constants
from i18n.i18n import I18nAuto
from scripts.translation import TranslationService
from scripts.config import load_config, save_config
import os

i18n = I18nAuto()

class DialogueEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dialogue Editor Premium - by RafaGodoy & Krisp")
        self.resize(1280, 800)
        
        # Load Config
        self.config = load_config()
        
        # State
        self.translation_service = TranslationService()
        self.dialogues = []
        self.page_tag = self.config.get("page_tag", "{np}")
        self.break_tag = self.config.get("break_tag", "<nl>")
        self.text_color = QColor(self.config.get("text_color", "black"))
        self.font_size = self.config.get("font_size", 25)
        self.line_height = self.config.get("line_height", 30.0)
        self.text_position = tuple(self.config.get("text_position", [10, 10]))
        
        self.file_opened = False
        self.current_index = -1
        self.current_page_index = 0
        self.page_entries = []
        self.original_page_entries = [] # For comparison
        self.image = None
        self.last_image_path = self.config.get("last_image_path", "")
        self.font_path = self.config.get("font_path", "arial.ttf")
        
        self.comparison_mode = False
        
        # Load last image if exists
        if self.last_image_path and os.path.exists(self.last_image_path):
            try:
                self.image = Image.open(self.last_image_path)
            except:
                self.last_image_path = ""

        try:
            self.pil_font = ImageFont.truetype(self.font_path, self.font_size)
        except:
            self.font_path = "arial.ttf"
            self.pil_font = ImageFont.truetype(self.font_path, self.font_size)
            
        self.file_path = ''

        # Theme system
        self.theme_mode = self.config.get("theme_mode", "light")
        self.themes = {
            "light": {
                "bg": "#f3f4f6", "sidebar": "#ffffff", "card": "#ffffff", 
                "text": "#1f2937", "dim_text": "#4b5563", "border": "#e5e7eb",
                "accent": "#4f46e5", "accent_hover": "#4338ca", "accent_dim": "#eef2ff",
                "input_bg": "#ffffff", "render_bg": (255, 255, 255)
            },
            "dark": {
                "bg": "#111827", "sidebar": "#1f2937", "card": "#1f2937", 
                "text": "#f9fafb", "dim_text": "#9ca3af", "border": "#374151",
                "accent": "#6366f1", "accent_hover": "#818cf8", "accent_dim": "#312e81",
                "input_bg": "#374151", "render_bg": (55, 65, 81)
            },
            "mocha": {
                "bg": "#1e1e2e", "sidebar": "#181825", "card": "#181825", 
                "text": "#cdd6f4", "dim_text": "#a6adc8", "border": "#313244",
                "accent": "#cba6f7", "accent_hover": "#f5c2e7", "accent_dim": "#2d223d",
                "input_bg": "#313244", "render_bg": (49, 50, 68)
            }
        }
        
        self.setup_ui()
        self.apply_styles()
        self.create_menu()
        
        # Initial render if image loaded
        if self.image:
            QTimer.singleShot(100, self.display_current_page)

    def setup_ui(self):

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Top Bar (Filter & Languages) - ADJUSTED HEIGHT
        top_bar = QFrame()
        top_bar.setObjectName("topBar")
        top_bar.setFixedHeight(80)
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(15, 0, 15, 0)
        top_layout.setSpacing(10)
        top_layout.setAlignment(Qt.AlignVCenter)
        
        top_layout.addWidget(QLabel(i18n("Filter: ")))
        self.search_entry = QLineEdit()
        self.search_entry.setPlaceholderText(i18n("Search dialogues..."))
        self.search_entry.textChanged.connect(self.search_dialogues)
        top_layout.addWidget(self.search_entry)
        
        top_layout.addSpacing(10)
        top_layout.addWidget(QLabel(i18n("Source:")))
        self.source_lang_combo = QComboBox()
        langs = sorted(list(constants.LANGUAGES.values()))
        self.source_lang_combo.addItems(langs)
        self.source_lang_combo.setCurrentText(self.config.get("source_lang", "english"))
        top_layout.addWidget(self.source_lang_combo)
        
        self.invert_btn = QPushButton("⇄")
        self.invert_btn.setObjectName("invertBtn")
        self.invert_btn.setFixedWidth(40)
        self.invert_btn.setFixedHeight(35)
        self.invert_btn.clicked.connect(self.invert_languages)
        top_layout.addWidget(self.invert_btn)

        
        top_layout.addWidget(QLabel(i18n("Target:")))
        self.target_lang_combo = QComboBox()
        self.target_lang_combo.addItems(langs)
        self.target_lang_combo.setCurrentText(self.config.get("target_lang", "portuguese"))
        top_layout.addWidget(self.target_lang_combo)
        
        main_layout.addWidget(top_bar, 0)


        # Main Splitter (Left: List, Right: Editor)
        self.splitter = QSplitter(Qt.Horizontal)
        
        # Left Panel (List)
        self.listbox = QListWidget()
        self.listbox.currentRowChanged.connect(self.on_select)
        self.splitter.addWidget(self.listbox)
        
        # Right Panel (Editor Content)
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(10, 10, 10, 10)
        
        # Dual Text Editors (Original vs Target)
        editor_layout = QHBoxLayout()
        editor_layout.setSpacing(10)
        
        # Original Text (Read-only)
        self.text_display_left = QTextEdit()
        self.text_display_left.setFixedHeight(120)
        self.text_display_left.setReadOnly(True)
        self.text_display_left.setPlaceholderText(i18n("Original Text..."))
        self.text_display_left.setObjectName("editorLeft")
        self.text_display_left.setVisible(False) # Start hidden
        editor_layout.addWidget(self.text_display_left, 1)
        
        # Target Text (Editable)
        self.text_display_right = QTextEdit()
        self.text_display_right.setFixedHeight(120)
        self.text_display_right.textChanged.connect(self.update_text_on_image)
        self.text_display_right.setPlaceholderText(i18n("Translate to Portuguese here..."))
        self.text_display_right.setObjectName("editorRight")
        editor_layout.addWidget(self.text_display_right, 1)
        
        right_layout.addLayout(editor_layout, 0)
        
        self.image_container = QFrame()
        self.image_container.setObjectName("imagePreview")
        self.image_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        container_layout = QHBoxLayout(self.image_container)
        container_layout.setContentsMargins(5,5,5,5)
        container_layout.setSpacing(10)
        
        self.image_label_left = QLabel()
        self.image_label_left.setAlignment(Qt.AlignCenter)
        self.image_label_left.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.image_label_left.setVisible(False)
        container_layout.addWidget(self.image_label_left, 1) # Add stretch factor 1

        self.image_label_right = QLabel()
        self.image_label_right.setAlignment(Qt.AlignCenter)
        self.image_label_right.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        container_layout.addWidget(self.image_label_right, 1) # Add stretch factor 1
        
        right_layout.addWidget(self.image_container, 1)
        
        # Controls Grid - AT BOTTOM
        controls_group = QFrame()
        controls_group.setObjectName("controlsFrame")
        controls_grid = QGridLayout(controls_group)
        controls_grid.setContentsMargins(0, 10, 0, 0)
        
        # Row 0
        controls_grid.addWidget(QLabel(i18n("Page Tag:")), 0, 0)
        self.page_tag_entry = QLineEdit(self.page_tag)
        self.page_tag_entry.textChanged.connect(self.update_page_tag)
        controls_grid.addWidget(self.page_tag_entry, 0, 1)
        
        controls_grid.addWidget(QLabel(i18n("Break Tag:")), 0, 2)
        self.break_tag_entry = QLineEdit(self.break_tag)
        self.break_tag_entry.textChanged.connect(self.update_break_tag)
        controls_grid.addWidget(self.break_tag_entry, 0, 3)
        
        controls_grid.addWidget(QLabel(i18n("Font Size:")), 0, 4)
        self.font_size_entry = QLineEdit(str(self.font_size))
        self.font_size_entry.editingFinished.connect(self.update_font_size)
        controls_grid.addWidget(self.font_size_entry, 0, 5)

        # Row 1
        controls_grid.addWidget(QLabel(i18n("Line Height:")), 1, 0)
        self.line_height_entry = QLineEdit(str(self.line_height))
        self.line_height_entry.textChanged.connect(self.update_line_height)
        controls_grid.addWidget(self.line_height_entry, 1, 1)
        
        controls_grid.addWidget(QLabel(i18n("Position (X,Y):")), 1, 2)
        self.pos_entry = QLineEdit(f"{self.text_position[0]},{self.text_position[1]}")
        self.pos_entry.textChanged.connect(self.update_text_position)
        controls_grid.addWidget(self.pos_entry, 1, 3)
        
        self.color_btn = QPushButton(i18n("Text Color"))
        self.color_btn.setObjectName("secondaryBtn")
        self.color_btn.clicked.connect(self.choose_text_color)
        controls_grid.addWidget(self.color_btn, 1, 4)

        # Row 2 (Buttons)
        btn_layout = QHBoxLayout()
        self.prev_btn = QPushButton(i18n("Previous"))
        self.prev_btn.clicked.connect(self.previous_page_entry)
        self.next_btn = QPushButton(i18n("Next"))
        self.next_btn.clicked.connect(self.next_page_entry)
        self.translate_line_btn = QPushButton(i18n("Translate Line"))
        self.translate_line_btn.clicked.connect(self.translate_text_command)
        
        self.compare_btn = QPushButton(i18n("Compare"))
        self.compare_btn.setObjectName("secondaryBtn")
        self.compare_btn.setCheckable(True)
        self.compare_btn.clicked.connect(self.toggle_comparison)

        btn_layout.addWidget(self.prev_btn)
        btn_layout.addWidget(self.next_btn)
        btn_layout.addWidget(self.compare_btn)
        btn_layout.addWidget(self.translate_line_btn)
        controls_grid.addLayout(btn_layout, 2, 0, 1, 6)
        
        right_layout.addWidget(controls_group, 0)
        
        self.splitter.addWidget(right_panel)
        self.splitter.setStretchFactor(0, 2)
        self.splitter.setStretchFactor(1, 4)
        
        main_layout.addWidget(self.splitter, 1)

        
        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)

    def save_current_config(self):
        self.config["page_tag"] = self.page_tag
        self.config["break_tag"] = self.break_tag
        self.config["text_color"] = self.text_color.name()
        self.config["font_size"] = self.font_size
        self.config["line_height"] = self.line_height
        self.config["text_position"] = list(self.text_position)
        self.config["font_path"] = self.font_path
        self.config["source_lang"] = self.source_lang_combo.currentText()
        self.config["target_lang"] = self.target_lang_combo.currentText()
        self.config["theme_mode"] = self.theme_mode
        # Only save path if we have one
        if hasattr(self, 'last_image_path') and self.last_image_path:
            self.config["last_image_path"] = self.last_image_path
        save_config(self.config)


    def apply_styles(self):
        c = self.themes.get(self.theme_mode, self.themes["light"])
        self.setStyleSheet(f"""
            QMainWindow {{ background-color: {c['bg']}; }}
            
            QMenuBar {{
                background-color: {c['sidebar']};
                color: {c['text']};
                border-bottom: 1px solid {c['border']};
                font-size: 13px;
                padding: 4px;
            }}
            QMenuBar::item {{
                padding: 4px 10px;
                background: transparent;
                border-radius: 4px;
            }}
            QMenuBar::item:selected {{
                background-color: {c['bg']};
            }}
            QMenu {{
                background-color: {c['sidebar']};
                color: {c['text']};
                border: 1px solid {c['border']};
                padding: 5px;
            }}
            QMenu::item {{
                padding: 6px 25px;
                border-radius: 4px;
            }}
            QMenu::item:selected {{
                background-color: {c['accent']};
                color: white;
            }}

            #topBar {{ 
                background-color: {c['card']}; 
                border-bottom: 1px solid {c['border']}; 
                padding: 10px 15px; 
            }}
            
            #controlsFrame {{ 
                background-color: {c['card']}; 
                border-top: 1px solid {c['border']}; 
                padding: 20px; 
            }}

            #imagePreview {{ 
                background-color: {c['input_bg'] if self.theme_mode != "light" else "#ffffff"}; 
                border: 1px solid {c['border']};
                border-radius: 4px;
            }}

            QMessageBox, QDialog {{
                background-color: {c['card']};
                color: {c['text']};
            }}
            QMessageBox QLabel {{
                color: {c['text']};
            }}

            QLabel {{ 
                color: {c['dim_text']}; 
                font-weight: 600; 
                font-size: 12px;
            }}

            QLineEdit, QComboBox, QTextEdit {{ 
                border: 1px solid {c['border']}; 
                border-radius: 6px; 
                padding: 8px; 
                background-color: {c['input_bg']}; 
                color: {c['text']};
                font-size: 13px;
            }}
            
            QListWidget {{
                border-right: 1px solid {c['border']};
                background-color: {c['sidebar']};
                color: {c['text']};
                font-size: 11px;
                outline: none;
            }}

            QLineEdit:focus, QTextEdit:focus, QComboBox:focus {{ 
                border-color: {c['accent']}; 
                background-color: {c['input_bg']};
            }}

            QListWidget::item {{
                padding: 10px;
                border-bottom: 1px solid {c['border']};
                color: {c['dim_text']};
            }}
            QListWidget::item:selected {{ 
                background-color: {c['accent_dim']}; 
                color: {c['accent']}; 
                border-left: 4px solid {c['accent']};
                font-weight: bold;
            }}

            QPushButton {{ 
                background-color: {c['accent']}; 
                color: #ffffff; 
                border: none; 
                border-radius: 6px; 
                padding: 10px 20px; 
                font-weight: bold;
                font-size: 12px;
            }}
            QPushButton:hover {{ 
                background-color: {c['accent_hover']}; 
            }}
            QPushButton:pressed {{ 
                background-color: {c['accent']}; 
            }}
            
            QPushButton#invertBtn {{
                padding: 0px;
                font-size: 18px;
            }}
            
            QPushButton#secondaryBtn {{
                background-color: {c['input_bg']};
                color: {c['dim_text']};
                border: 1px solid {c['border']};
            }}
            QPushButton#secondaryBtn:hover {{
                background-color: {c['bg']};
                border-color: {c['dim_text']};
            }}

            #editorLeft {{
                border: 2px solid #ef4444;
            }}
            #editorRight {{
                border: 2px solid #10b981;
            }}

            QProgressBar {{
                border: 1px solid {c['border']};
                border-radius: 10px;
                text-align: center;
                color: {c['text']};
                height: 12px;
                background-color: {c['bg']};
            }}
            QProgressBar::chunk {{
                background-color: {c['accent']};
                border-radius: 10px;
            }}

            QSplitter::handle {{
                background-color: {c['border']};
            }}
            QSplitter::handle:horizontal {{
                width: 1px;
            }}
        """)


    def create_menu(self):
        menu_bar = self.menuBar()
        
        file_menu = menu_bar.addMenu(i18n("File"))
        
        load_diag_act = QAction(i18n("Load Dialogues"), self)
        load_diag_act.triggered.connect(self.load_dialogues)
        file_menu.addAction(load_diag_act)
        
        load_img_act = QAction(i18n("Load Image"), self)
        load_img_act.triggered.connect(self.load_image)
        file_menu.addAction(load_img_act)
        
        load_font_act = QAction(i18n("Load Font"), self)
        load_font_act.triggered.connect(self.load_font)
        file_menu.addAction(load_font_act)
        
        translate_file_act = QAction(i18n("Translate File"), self)
        translate_file_act.triggered.connect(self.translate_file_command)
        file_menu.addAction(translate_file_act)
        
        file_menu.addSeparator()
        
        save_act = QAction(i18n("Save"), self)
        save_act.setShortcut("Ctrl+S")
        save_act.triggered.connect(self.save_file_path)
        file_menu.addAction(save_act)
        
        save_as_act = QAction(i18n("Save As..."), self)
        save_as_act.setShortcut("Ctrl+Shift+S")
        save_as_act.triggered.connect(self.save_as)
        file_menu.addAction(save_as_act)
        
        file_menu.addSeparator()
        
        exit_act = QAction(i18n("Exit"), self)
        exit_act.triggered.connect(self.close)
        file_menu.addAction(exit_act)
        
        # View Menu for Themes
        view_menu = menu_bar.addMenu(i18n("View"))
        
        light_theme_act = QAction(i18n("Light Theme"), self)
        light_theme_act.triggered.connect(lambda: self.change_theme("light"))
        view_menu.addAction(light_theme_act)
        
        dark_theme_act = QAction(i18n("Dark Theme"), self)
        dark_theme_act.triggered.connect(lambda: self.change_theme("dark"))
        view_menu.addAction(dark_theme_act)
        
        mocha_theme_act = QAction(i18n("Mocha Theme"), self)
        mocha_theme_act.triggered.connect(lambda: self.change_theme("mocha"))
        view_menu.addAction(mocha_theme_act)

        help_menu = menu_bar.addMenu(i18n("Help"))
        credits_act = QAction(i18n("Credits"), self)
        credits_act.triggered.connect(self.show_credits)
        help_menu.addAction(credits_act)

    def change_theme(self, mode):
        self.theme_mode = mode
        self.apply_styles()
        self.display_current_page() # Re-render image with new theme background
        self.save_current_config()


    def search_dialogues(self):
        term = self.search_entry.text().strip().lower()
        self.listbox.clear()
        for diag in self.dialogues:
            if not term or term in diag.lower():
                self.listbox.addItem(diag.strip())

    def invert_languages(self):
        src = self.source_lang_combo.currentText()
        tgt = self.target_lang_combo.currentText()
        self.source_lang_combo.setCurrentText(tgt)
        self.target_lang_combo.setCurrentText(src)

    def on_select(self, row):
        if row < 0: return
        self.current_index = row
        text = self.dialogues[row].strip()
        orig_text = self.original_dialogues[row].strip()
        
        # Update both displays
        self.text_display_left.setPlainText(orig_text)
        
        self.text_display_right.blockSignals(True)
        self.text_display_right.setPlainText(text)
        self.text_display_right.blockSignals(False)
        
        self.current_page_index = 0
        self.display_dialogue(text, orig_text, keep_current_page=True)

    def update_text_on_image(self):
        if self.current_index < 0: return
        text = self.text_display_right.toPlainText()
        self.dialogues[self.current_index] = text + "\n"
        item = self.listbox.item(self.current_index)
        if item:
            item.setText(text.strip())
        # Re-fetch original for comparison consistency
        orig_text = self.original_dialogues[self.current_index].strip()
        self.display_dialogue(text, orig_text, keep_current_page=True)

    def display_dialogue(self, dialogue, original=None, keep_current_page=False):
        # Current dialogue
        if self.page_tag:
            self.page_entries = [p.split(self.break_tag) if self.break_tag else [p] for p in dialogue.split(self.page_tag)]
        else:
            self.page_entries = [[b.strip() for b in dialogue.split(self.break_tag)] if self.break_tag else [dialogue]]
        
        # Cleanup page entries
        self.page_entries = [[line.strip() for line in page if line.strip()] for page in self.page_entries]

        # Original dialogue
        if original:
            if self.page_tag:
                self.original_page_entries = [p.split(self.break_tag) if self.break_tag else [p] for p in original.split(self.page_tag)]
            else:
                self.original_page_entries = [[b.strip() for b in original.split(self.break_tag)] if self.break_tag else [original]]
            self.original_page_entries = [[line.strip() for line in page if line.strip()] for page in self.original_page_entries]
        else:
            self.original_page_entries = []

        if not keep_current_page:
            self.current_page_index = 0
            
        self.display_current_page()


    def display_current_page(self):
        if self.image is None:
            self.image_label_left.clear()
            self.image_label_right.clear()
            return

        c = self.themes.get(self.theme_mode, self.themes["light"])
        bg_rgb = c.get("render_bg", (255, 255, 255))

        # Comparison Mode logic
        if self.comparison_mode:
            self.image_label_left.setVisible(True)
            # Render Original (Left)
            if self.original_page_entries:
                pix_orig = self.render_text_to_pixmap(self.original_page_entries, self.text_color, bg_rgb)
                self.set_pixmap_to_label(self.image_label_left, pix_orig)
            else:
                self.image_label_left.clear()
            
            # Render Current (Right)
            if self.page_entries:
                pix_curr = self.render_text_to_pixmap(self.page_entries, self.text_color, bg_rgb)
                self.set_pixmap_to_label(self.image_label_right, pix_curr)
            else:
                self.image_label_right.clear()
        else:
            self.image_label_left.setVisible(False)
            if self.page_entries:
                pix_curr = self.render_text_to_pixmap(self.page_entries, self.text_color, bg_rgb)
                self.set_pixmap_to_label(self.image_label_right, pix_curr)
            else:
                self.image_label_right.clear()

    def render_text_to_pixmap(self, entries, color, bg_rgb):
        # Handle transparent PNGs
        if self.image.mode in ('RGBA', 'LA') or (self.image.mode == 'P' and 'transparency' in self.image.info):
            img_copy = Image.new("RGB", self.image.size, bg_rgb)
            img_copy.paste(self.image, mask=self.image.split()[3] if self.image.mode == 'RGBA' else None)
        else:
            img_copy = self.image.copy().convert("RGB")
            
        current_page = entries[self.current_page_index % len(entries)]
        draw = ImageDraw.Draw(img_copy)
        y = self.text_position[1]
        rgb_color = (color.red(), color.green(), color.blue())

        for line in current_page:
            clean_line = re.sub(r'(\{.*?\}|\[.*?\]|\<.*?\>|0x[0-9A-Fa-f]+ =)', '', line)
            sub_lines = clean_line.split(self.break_tag) if self.break_tag else [clean_line]
            for sl in sub_lines:
                draw.text((self.text_position[0], y), sl, font=self.pil_font, fill=rgb_color)
                y += self.line_height
        
        return QPixmap.fromImage(ImageQt(img_copy))

    def set_pixmap_to_label(self, label, pixmap):
        if not label.size().isEmpty():
            scaled = pixmap.scaled(label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            label.setPixmap(scaled)
        else:
            label.setPixmap(pixmap)

    def toggle_comparison(self):
        self.comparison_mode = self.compare_btn.isChecked()
        
        # Toggle visibility immediately to trigger layout recalculation
        self.text_display_left.setVisible(self.comparison_mode)
        self.image_label_left.setVisible(self.comparison_mode)
        
        # Clear left label if leaving comparison to ensure clean state
        if not self.comparison_mode:
            self.image_label_left.clear()

        # Refresh visuals with a delay to allow layout to finish resizing
        QTimer.singleShot(100, self.display_current_page)


    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Use a small timer to re-render after layout stabilizes
        QTimer.singleShot(50, self.display_current_page)

    def update_page_tag(self):
        self.page_tag = self.page_tag_entry.text()
        self.display_dialogue(self.text_display_right.toPlainText(), self.text_display_left.toPlainText(), True)
        self.save_current_config()

    def update_break_tag(self):
        self.break_tag = self.break_tag_entry.text()
        self.display_dialogue(self.text_display_right.toPlainText(), self.text_display_left.toPlainText(), True)
        self.save_current_config()

    def update_font_size(self):
        try:
            val = int(self.font_size_entry.text())
            if val > 0:
                self.font_size = val
                self.pil_font = ImageFont.truetype(self.font_path, self.font_size)
                self.display_current_page()
                self.save_current_config()
        except: pass

    def update_line_height(self):
        try:
            val = float(self.line_height_entry.text())
            if val > 0:
                self.line_height = val
                self.display_current_page()
                self.save_current_config()
        except: pass

    def update_text_position(self):
        try:
            txt = self.pos_entry.text()
            x, y = map(int, txt.split(","))
            self.text_position = (x, y)
            self.display_current_page()
            self.save_current_config()
        except: pass

    def next_page_entry(self):
        if self.page_entries:
            self.current_page_index = (self.current_page_index + 1) % len(self.page_entries)
            self.display_current_page()

    def previous_page_entry(self):
        if self.page_entries:
            self.current_page_index = (self.current_page_index - 1) % len(self.page_entries)
            self.display_current_page()

    def choose_text_color(self):
        color = QColorDialog.getColor(self.text_color, self, i18n("Choose Text Color"))
        if color.isValid():
            self.text_color = color
            self.display_current_page()
            self.save_current_config()

    def load_dialogues(self):
        path, _ = QFileDialog.getOpenFileName(self, i18n("Load Dialogues"), "", "Text files (*.txt)")
        if path:
            with open(path, 'r', encoding='utf-8') as f:
                self.dialogues = f.readlines()
            self.original_dialogues = list(self.dialogues) # Store original state
            self.file_path = path
            self.file_opened = True
            self.search_dialogues()
            # Auto-select first item
            if self.listbox.count() > 0:
                self.listbox.setCurrentRow(0)

    def load_image(self):
        path, _ = QFileDialog.getOpenFileName(self, i18n("Load Image"), "", "Images (*.jpg *.png *.gif *.webp)")
        if path:
            try:
                img = Image.open(path)
                self.image = img
                self.last_image_path = path
                self.display_current_page()
                self.save_current_config()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load image: {e}")

    def load_font(self):
        path, _ = QFileDialog.getOpenFileName(self, i18n("Load Font"), "", "Fonts (*.ttf *.otf)")
        if path:
            self.font_path = path
            self.pil_font = ImageFont.truetype(self.font_path, self.font_size)
            self.display_current_page()
            self.save_current_config()

    def save_file_path(self):
        if not self.file_path:
            self.save_as()
        else:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                for line in self.dialogues:
                    f.write(line)
            QMessageBox.information(self, i18n("Save"), i18n("Dialogues saved successfully."))

    def save_as(self):
        path, _ = QFileDialog.getSaveFileName(self, i18n("Save As..."), "", "Text files (*.txt)")
        if path:
            self.file_path = path
            self.save_file_path()

    def translate_file_command(self):
        if not self.file_opened:
            QMessageBox.warning(self, i18n("Error"), i18n("No file opened."))
            return
            
        self.progress_bar.setVisible(True)
        self.progress_bar.setMaximum(len(self.dialogues))
        self.progress_bar.setValue(0)
        
        source_lang = self.source_lang_combo.currentText()
        target_lang = self.target_lang_combo.currentText()
        
        translated = []
        for i, line in enumerate(self.dialogues):
            translated.append(self.translation_service.translate_line_with_tags(line, source_lang, target_lang))
            self.progress_bar.setValue(i + 1)
            QApplication.processEvents()
            
        self.dialogues = translated
        self.search_dialogues()
        self.progress_bar.setVisible(False)
        self.save_current_config()

    def translate_text_command(self):
        if self.current_index < 0: return
        text = self.text_display_right.toPlainText()
        source_lang = self.source_lang_combo.currentText()
        target_lang = self.target_lang_combo.currentText()
        
        translated = self.translation_service.translate_text(text, source_lang, target_lang)
        self.text_display_right.setPlainText(translated)
        self.update_text_on_image()

    def show_credits(self):
        msg = f"{i18n('Created by:')} Rafael Godoy & Krisp\n\nGitHub: RafaelGodoyEbert\nYouTube: @Godoyy\nEmail: rafaelgodebert@gmail.com"
        QMessageBox.about(self, i18n("Credits"), msg)

    def closeEvent(self, event):
        self.save_current_config()
        if self.file_opened:
            ret = QMessageBox.question(self, i18n("Exit"), i18n("Save before exiting?"), 
                                     QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if ret == QMessageBox.Yes:
                self.save_file_path()
                event.accept()
            elif ret == QMessageBox.No:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

