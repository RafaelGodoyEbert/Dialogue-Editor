# Dialogue Editor by RafaGodoy & Krisp
[English](https://github.com/RafaelGodoyEbert/Dialogue-Editor/blob/main/README.md) [Português](https://github.com/RafaelGodoyEbert/Dialogue-Editor/blob/main/README_portuguese.md)

![image (1)](https://github.com/RafaelGodoyEbert/Dialogue-Editor/assets/78083427/325c9804-068e-41fa-a404-2416097b527a)

## About the Project

**Dialogue Editor** is a tool for editing interactive dialogues, created by Rafael Godoy & Krisp. This application allows you to load dialogues from text files, display them, and edit them directly in a graphical interface. Additionally, you can translate the dialogues into different languages and overlay text on images.

## Features

- **Load and Save Dialogues**: Open and save text files containing dialogues.
- **Text Editing**: Edit the dialogues directly in the graphical interface.
- **Search Filter**: Search for specific dialogues.
- **Translation**: Translate dialogues using Google Translate.
- **Text Overlay on Images**: Load an image and overlay text on it.
- **Page Navigation**: Navigate between different pages of dialogue.
- **Font and Text Color Selection**: Customize the font and text color.

## How to Use

### Requirements

- Python 3.x
- Libraries:
  - `tkinter`
  - `Pillow`
  - `googletrans`
  - `tqdm`
  - `i18n`

### Installation

1. Clone the repository:

```bash
git clone https://github.com/RafaelGodoyEbert/Dialogue-Editor
cd dialogue-editor
```

2. Install the dependencies:

```bash
pip install -r requirements.txt
```

### Running the Application

To start the application, run the following command:

```bash
python dialogue_editor.py
```

### Interface Usage

1. **Load Dialogues**: Go to the `File` menu and select `Load Dialogues` to load a text file containing dialogues.
2. **Load Image**: Go to the `File` menu and select `Load Image` to load an image.
3. **Load Font**: Go to the `File` menu and select `Load Font` to load a custom font.
4. **Save Dialogues**: Use the `Save` or `Save As` options in the `File` menu to save the edits made to the dialogues.
5. **Translation**: Select the source and target languages in the comboboxes and click `Translate File` to translate the entire file or `Translate Line` to translate a specific line.
6. **Navigation**: Use the `Previous Page` and `Next Page` buttons to navigate between the dialogue pages. (If applicable)
7. **Customization**: Use the `Font Size` and `Text Position` entries to adjust the appearance of the text overlay on the image.

## Credits

Created by: Rafael Godoy & Krisp

- **GitHub**: [RafaelGodoyEbert](https://github.com/RafaelGodoyEbert)
- **X (Twitter)**: [GodoyEbert](https://twitter.com/GodoyEbert)
- **YouTube**: [Godoyy](https://youtube.com/@Godoyy)
- **Email**: rafaelgodebert@gmail.com

**Support the project:**

- **PIX**: rafaelgodebert@gmail.com
- **PayPal**: [Click here](https://www.paypal.com/donate?hosted_button_id=XXXXX)

## License

This project is licensed under the terms of the GPL license. See the [LICENSE](LICENSE) file for more details.
