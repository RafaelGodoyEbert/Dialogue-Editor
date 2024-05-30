import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont
import re
from googletrans import Translator, constants
import six
from tkinter import ttk
from tqdm import tqdm
import six
from i18n.i18n import I18nAuto
i18n = I18nAuto()

class PageEntry:
    def __init__(self, text, image):
        self.text = text
        self.image = None
        self.image_tk = None        

    def render_text(self, font, color, position):
        # Remove as tags específicas do texto antes de renderizar
        cleaned_text = re.sub(r'\{t\d+\}', '', self.text)

        image = self.image.copy()
        draw = ImageDraw.Draw(image)
        draw.text(position, cleaned_text, font=font, fill=color)
        self.image_tk = ImageTk.PhotoImage(image)
        return self.image_tk

class DialogueEditor:
    def __init__(self, root):
        self.current_page_index = 0
        self.root = root
        self.root.title("Dialogue Editor by RafaGodoy & Krisp")
        self.translator = Translator()
        self.dialogues = []
        self.page_tag = "{np}"
        self.break_tag = "<nl>"
        self.text_color = "black"
        self.font_size = 25
        self.text_position = (10, 10)
        self.file_opened = False
        self.current_index = None
        self.current_page_index = 0
        self.page_entries = []
        self.font = ImageFont.truetype("arial.ttf", self.font_size)
        self.file_path = ''  
        self.file_opened = False 
        
        self.create_menu()
        self.create_widgets()
        
    def search_dialogues(self, event=None):
        search_term = self.search_entry.get().strip().lower()
        if search_term:
            filtered_dialogues = [dialogue for dialogue in self.dialogues if search_term in dialogue.lower()]
            self.dialogue_listbox.delete(0, tk.END)
            for dialogue in filtered_dialogues:
                self.dialogue_listbox.insert(tk.END, dialogue.strip())
        else:
            self.dialogue_listbox.delete(0, tk.END)
            for dialogue in self.dialogues:
                self.dialogue_listbox.insert(tk.END, dialogue.strip())
                
    def create_menu(self):
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)

        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label=i18n("File"), menu=self.file_menu)
        self.file_menu.add_command(label=i18n("Load Dialogues"), command=self.load_dialogues)
        self.file_menu.add_command(label=i18n("Load Image"), command=self.load_image)
        self.file_menu.add_command(label=i18n("Load Font"), command=self.load_font)
        self.file_menu.add_command(label=i18n("Translate File"), command=self.translate_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label=i18n("Save"), command=self.save_file_path, accelerator="Ctrl+S")
        self.file_menu.add_command(label=i18n("Save As..."), command=self.save_as, accelerator="Ctrl+Shift+S")
        self.file_menu.add_separator()
        self.file_menu.add_command(label=i18n("Exit"), command=self.exit_application)
        self.menu.add_command(label=i18n("Credits"), command=self.show_credits)
    
    def show_credits(self):
        credits_window = tk.Toplevel(self.root)
        credits_window.title(i18n("Credits"))

        credits_label = tk.Label(credits_window, text=f"{i18n('Credits')}\n\n{i18n('Created by:')} Rafael Godoy & Krisp \n\nGitHub: RafaelGodoyEbert\nX: GodoyEbert\nYoutube @Godoyy\ne-mail: rafaelgodebert@gmail.com\n\n{i18n('Buy me a coffee:')}\nPIX: rafaelgodebert@gmail.com\nPaypal: ")
        credits_label.pack(padx=50, pady=50)
    
    def save_file_path(self, event=None):
        if not self.file_path:
            self.file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if self.file_path:
            with open(self.file_path, 'w', encoding='utf-8') as file:
                for line in self.dialogues:
                    file.write(line)
            messagebox.showinfo(i18n("Save"), i18n("Dialogues saved successfully."))
            
    def select_all(self, event=None):
        self.dialogue_display.tag_add("sel", "1.0", "end")
        return "break"

    def undo(self, event=None):
        try:
            self.dialogue_display.edit_undo()
        except tk.TclError:
            pass  # Ignora o erro caso não haja nada para desfazer
        return "break"
    
    def create_widgets(self):
        # Frame para conter o rótulo e a entrada de pesquisa
        filter_frame = tk.Frame(self.root)
        filter_frame.pack(side=tk.TOP, padx=5, pady=5, anchor='nw')  # Ancora no canto superior esquerdo
        
        # Rótulo "Filter"
        filter_label = tk.Label(filter_frame, text=i18n("Filter: "))
        filter_label.pack(side=tk.LEFT)
        
        # Entrada de pesquisa
        self.search_entry = tk.Entry(filter_frame)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)  # Ocupa todo o espaço horizontal disponível
        self.search_entry.insert(tk.END, "")  # Alteração do texto para "FILTER"
        self.search_entry.bind("<KeyRelease>", self.search_dialogues)

        frame = tk.Frame(self.root)
        frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.dialogue_listbox = tk.Listbox(frame, width=50)
        self.dialogue_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)  # Use fill=BOTH para preencher toda a janela
        self.dialogue_listbox.bind("<<ListboxSelect>>", self.on_select)
        
        self.scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=self.dialogue_listbox.yview)
        self.scrollbar.pack(side=tk.LEFT, fill=tk.Y)  # Mude para side=LEFT para a barra de rolagem
        
        self.dialogue_listbox.config(yscrollcommand=self.scrollbar.set)

        self.display_frame = tk.Frame(self.root)
        self.display_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.dialogue_display = tk.Text(self.display_frame, wrap=tk.WORD, height=10)
        self.dialogue_display.pack(fill=tk.BOTH, expand=True)
        self.dialogue_display.configure(undo=True)
        # Binding de atalhos de teclado
        self.dialogue_display.bind("<Control-a>", self.select_all)
        self.dialogue_display.bind("<Control-z>", self.undo)
        self.root.bind("<Control-s>", self.save_file_path)
        self.root.bind("<Control-Shift-S>", self.save_as)
        self.dialogue_display.bind("<KeyRelease>", self.update_text_on_image)

        self.image_label = tk.Label(self.display_frame)
        self.image_label.pack()

        self.controls_frame = tk.Frame(self.display_frame)
        self.controls_frame.pack(side=tk.BOTTOM, pady=10)

        self.page_tag_label = tk.Label(self.controls_frame, text=i18n("Page Tag:"))
        self.page_tag_label.grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.page_tag_entry = tk.Entry(self.controls_frame)
        self.page_tag_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        self.page_tag_entry.insert(tk.END, self.page_tag)  
        self.page_tag_entry.bind("<KeyRelease>", self.update_page_tag)  

        self.break_tag_label = tk.Label(self.controls_frame, text=i18n("Break Tag:"))
        self.break_tag_label.grid(row=0, column=2, padx=5, pady=5, sticky='e')
        self.break_tag_entry = tk.Entry(self.controls_frame)
        self.break_tag_entry.grid(row=0, column=3, padx=5, pady=5, sticky='w')
        self.break_tag_entry.insert(tk.END, self.break_tag)  
        self.break_tag_entry.bind("<KeyRelease>", self.update_break_tag)  

        self.font_size_label = tk.Label(self.controls_frame, text=i18n("Font Size:"))
        self.font_size_label.grid(row=0, column=4, padx=5, pady=5, sticky='e')
        self.font_size_entry = tk.Entry(self.controls_frame)
        self.font_size_entry.grid(row=0, column=5, padx=5, pady=5, sticky='w')
        self.font_size_entry.insert(tk.END, self.font_size) 
        self.font_size_entry.bind("<Return>", lambda event: self.update_font_size(self.font_size_entry.get()))

        self.text_position_label = tk.Label(self.controls_frame, text=i18n("Text Position (X, Y):"))
        self.text_position_label.grid(row=0, column=7, padx=5, pady=5, sticky='e')
        self.text_position_entry = tk.Entry(self.controls_frame)
        self.text_position_entry.grid(row=0, column=8, padx=5, pady=5, sticky='w')
        self.text_position_entry.bind("<KeyRelease>", self.update_text_position)  

        self.previous_button = tk.Button(self.controls_frame, text=i18n("Previous Page"), command=self.previous_page_entry)
        self.previous_button.grid(row=1, column=3, padx=(5, 2), pady=5)
        
        self.text_color_button = tk.Button(self.controls_frame, text=i18n("Choose Text Color"), command=self.choose_text_color)
        self.text_color_button.grid(row=1, column=4, padx=5, pady=5)
        
        self.translate_button = tk.Button(self.controls_frame, text=i18n("Translate line"), command=self.translate_text)
        self.translate_button.grid(row=2, column=4, padx=5, pady=5)

        # Adicionando um espaço em branco entre os botões
        #blank_space = tk.Label(self.controls_frame, text=" ")
        #blank_space.grid(row=1, column=4)

        self.next_button = tk.Button(self.controls_frame, text=i18n("Next Page"), command=self.next_page_entry)
        self.next_button.grid(row=1, column=5, padx=(2, 5), pady=5)
        
        # Combobox para selecionar o idioma de origem
        self.source_language_label = tk.Label(filter_frame, text=i18n("Source Language:"))
        self.source_language_label.pack(side=tk.LEFT, padx=(20, 5))

        source_languages = list(constants.LANGUAGES.values())
        self.source_language_combobox = ttk.Combobox(filter_frame, state="readonly", values=source_languages)
        self.source_language_combobox.pack(side=tk.LEFT)
        self.source_language_combobox.set("english")  # Definir o idioma de origem padrão como inglês
        self.source_language_combobox.bind("<<ComboboxSelected>>", None)
        self.source_language_combobox.bind("<Key>", lambda event: self.select_language_by_letter(event, self.source_language_combobox))
        
        # Botão para inverter os idiomas
        self.invert_button = tk.Button(filter_frame, text="⇔", command=self.invert_languages)
        self.invert_button.pack(side=tk.LEFT, padx=5)

        # Combobox para selecionar o idioma de destino
        self.target_language_label = tk.Label(filter_frame, text=i18n("Target Language:"))
        self.target_language_label.pack(side=tk.LEFT, padx=(20, 5))

        target_languages = list(constants.LANGUAGES.values())
        self.target_language_combobox = ttk.Combobox(filter_frame, state="readonly", values=target_languages)
        self.target_language_combobox.pack(side=tk.LEFT)
        self.target_language_combobox.set("portuguese")  # Definir o idioma de destino padrão como português
        self.target_language_combobox.bind("<<ComboboxSelected>>", None)
        self.target_language_combobox.bind("<Key>", lambda event: self.select_language_by_letter(event, self.target_language_combobox))
    
    def invert_languages(self):
        # Função para inverter os idiomas selecionados nas comboboxes
        source_language = self.source_language_combobox.get()
        target_language = self.target_language_combobox.get()

        self.source_language_combobox.set(target_language)
        self.target_language_combobox.set(source_language)

        # Atualizar a tradução após a inversão dos idiomas
        self.translate_file = False

    def select_language_by_letter(self, event, combobox):
        # Função para selecionar automaticamente um idioma ao pressionar uma letra
        letter = event.char.lower()
        
        # Obter a lista de idiomas da combobox atual
        languages = combobox.cget("values")
        
        # Procurar um idioma que comece com a letra pressionada
        for language in languages:
            if language.lower().startswith(letter):
                # Selecionar o idioma encontrado na combobox
                combobox.set(language)
                break 

    def translate_file(self):
        if self.file_opened:
            translated_dialogues = []
            total_lines = len(self.dialogues)
            
            self.progressbar = ttk.Progressbar(self.root, length=200, mode='determinate')
            self.progressbar.place(x=self.root.winfo_width() - 210, y=self.root.winfo_height() - 30)
            
            self.progressbar["maximum"] = total_lines
            for i, line in enumerate(self.dialogues):
                translated_line = self.translate_line_with_tags(line)
                translated_dialogues.append(translated_line)
                self.progressbar["value"] = i + 1
                self.progressbar.update()
            self.dialogues = translated_dialogues
            self.update_displayed_dialogue()  # Adicione esta linha para atualizar a lista de diálogos
            self.progressbar.destroy()
        else:
            messagebox.showerror("Error", "No file opened.")

    # Atualize a função translate_line_with_tags para retornar a linha traduzida
    def translate_line_with_tags(self, line):
        parts = re.split(r'(\{.*?\}|\[.*?\]|\<.*?\>)', line)
        translated_parts = []
        source_language = self.source_language_combobox.get()
        target_language = self.target_language_combobox.get()
        for part in parts:
            if re.match(r'\{.*?\}|\[.*?\]|\<.*?\>', part):
                translated_parts.append(part)
            else:
                try:
                    translation = self.translator.translate(part, dest=target_language, src=source_language)
                    translated_text = translation.text if translation else part
                    translated_parts.append(translated_text)
                except Exception as e:
                    print("Erro na tradução:", str(e))
                    translated_parts.append(part)
        translated_line = ''.join(translated_parts)
        return translated_line

    # Atualize a função update_displayed_dialogue para refletir as alterações feitas durante a tradução
    def update_displayed_dialogue(self):
        self.dialogue_listbox.delete(0, tk.END)
        for line in self.dialogues:
            self.dialogue_listbox.insert(tk.END, line.strip())
        self.display_dialogue(self.dialogues[self.current_index].strip(), keep_current_page=True)
 
    def translate_text(self):
        current_text = self.dialogue_display.get('1.0', tk.END).strip()
        source_language = self.source_language_combobox.get()
        target_language = self.target_language_combobox.get()

        # Dividir o texto em linhas
        lines = current_text.split('\n')

        translated_lines = []
        for line in lines:
            # Dividir cada linha em partes, separando pelas tags {}, [], e <>
            parts = re.split(r'(\{.*?\}|\[.*?\]|\<.*?\>)', line)

            translated_parts = []
            for part in parts:
                # Verificar se a parte é uma tag
                if re.match(r'\{.*?\}|\[.*?\]|\<.*?\>', part):
                    # Se for uma tag, apenas adicione-a à lista de partes traduzidas
                    translated_parts.append(part)
                else:
                    # Se não for uma tag, traduza o texto
                    try:
                        translation = self.translator.translate(part, dest=target_language, src=source_language)
                        translated_text = translation.text if translation else part  # Usar o texto original se a tradução for None
                        translated_parts.append(translated_text)
                    except Exception as e:
                        # Mostrar uma mensagem de erro, mas continuar com o processo de tradução
                        print("Erro na tradução:", str(e))
                        translated_parts.append(part)  # Adicionar o texto original se ocorrer um erro na tradução

            # Juntar as partes traduzidas da linha novamente
            translated_line = ''.join(translated_parts)
            translated_lines.append(translated_line)

        # Juntar as linhas traduzidas novamente
        translated_text = '\n'.join(translated_lines)

        # Atualizar a caixa de diálogo com o texto traduzido
        self.dialogue_display.delete('1.0', tk.END)
        self.dialogue_display.insert(tk.END, translated_text)
        
        # Atualizar a lista de diálogos para refletir o texto traduzido
        if self.current_index is not None:
            self.dialogues[self.current_index] = translated_text + "\n"
            self.dialogue_listbox.delete(self.current_index)
            self.dialogue_listbox.insert(self.current_index, translated_text)

        # Atualizar o texto sobreposto na imagem
        self.display_dialogue(translated_text)

    def update_page_tag(self, event):
        self.page_tag = self.page_tag_entry.get()
        self.display_dialogue(self.dialogue_display.get('1.0', tk.END).strip())

    def update_break_tag(self, event):
        self.break_tag = self.break_tag_entry.get()
        self.display_dialogue(self.dialogue_display.get('1.0', tk.END).strip())

    def load_dialogues(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                self.dialogues = file.readlines()
            self.file_path = file_path  # Atualizar o caminho do arquivo carregado
            self.dialogue_listbox.delete(0, tk.END)
            for line in self.dialogues:
                self.dialogue_listbox.insert(tk.END, line.strip())
            self.file_opened = True  # Marcar que um arquivo foi aberto

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.gif *.webp")])
        if file_path:
            try:
                # Abrir a imagem
                image = Image.open(file_path)

                # Definir o tamanho máximo permitido para a imagem
                max_dimension = 900  # Defina o tamanho máximo desejado para a largura ou altura da imagem

                # Obter as dimensões originais da imagem
                width, height = image.size

                # Verificar qual dimensão (largura ou altura) é maior
                if width > height:
                    # Se a largura for maior, calcular a nova altura mantendo a proporção original
                    new_width = max_dimension
                    new_height = int(height * (max_dimension / width))
                else:
                    # Se a altura for maior ou igual, calcular a nova largura mantendo a proporção original
                    new_width = int(width * (max_dimension / height))
                    new_height = max_dimension

                # Redimensionar a imagem
                image = image.resize((new_width, new_height))

                # Atualizar a imagem exibida
                self.image = image
                self.image_tk = ImageTk.PhotoImage(image)
                self.image_label.config(image=self.image_tk)
            except Exception as e:
                messagebox.showerror("Error", f"Erro ao carregar a imagem: {e}")
        else:
            self.image = None
            
    def on_select(self, event):
        selection = event.widget.curselection()
        if selection:
            self.current_index = selection[0]  # Atualiza o índice atualmente selecionado
            index = self.current_index
            self.dialogue_display.delete('1.0', tk.END)
            self.dialogue_display.insert(tk.END, self.dialogues[index].strip())
            # Redefine a página atual para a primeira página e exibe o diálogo selecionado
            self.current_page_index = 0
            self.display_dialogue(self.dialogues[index].strip(), keep_current_page=True)

    def display_dialogue(self, dialogue, keep_current_page=False):
        page_entries = dialogue.split(self.page_tag)

        self.page_entries = []
        for entry in page_entries:
            break_entries = entry.split(self.break_tag)
            self.page_entries.append([b_entry.strip() for b_entry in break_entries if b_entry.strip()])

        if self.page_entries and not keep_current_page:
            self.current_page_index = 0

        if self.page_entries:
            self.display_current_page()
                
    def display_current_page(self):
        if self.page_entries:
            current_page = self.page_entries[self.current_page_index]
            image = self.image.copy()
            draw = ImageDraw.Draw(image)
            y = self.text_position[1]
            max_width = 0
            
            # Obter a altura da fonte diretamente do atributo self.font.size
            text_height = self.font.size
            
            for line in current_page:
                # Remover todas as tags {} e o prefixo '0xXXXX ='
                line = re.sub(r'(\{.*?\}|\[.*?\]|\<.*?\>|0x[0-9A-Fa-f]+ =)', '', line)
                lines = line.split(self.break_tag)  # Dividir a linha usando a Break Tag
                for l in lines:
                    draw.text((self.text_position[0], y), l, font=self.font, fill=self.text_color)
                    # Usar getlength() para obter a largura do texto
                    text_width = self.font.getlength(l)
                    max_width = max(max_width, text_width)
                    y += text_height  # Incrementa a posição Y para a próxima linha
            self.image_tk = ImageTk.PhotoImage(image)
            self.image_label.config(image=self.image_tk)
        else:
            # Se não houver diálogos carregados, limpe a imagem exibida
            self.image_label.config(image=None)
    
    def load_font(self):
        self.font_path = filedialog.askopenfilename(filetypes=[("Font files", "*.ttf;*.otf")])
        if self.font_path:
            self.font = ImageFont.truetype(self.font_path, self.font_size)

    def update_font_size(self, value):
        self.font_size = int(value)
        if hasattr(self, 'font_path'):
            self.font = ImageFont.truetype(self.font_path, self.font_size)
        else:
            self.font = ImageFont.truetype("arial.ttf", self.font_size)
        self.display_dialogue(self.dialogue_display.get('1.0', tk.END).strip())

    def choose_text_color(self):
        color = colorchooser.askcolor(title=i18n("Choose Text Color"))
        if color:
            self.text_color = color[1]
            self.display_dialogue(self.dialogue_display.get('1.0', tk.END).strip())
    
    def update_text_on_image(self, event):
        current_text = self.dialogue_display.get('1.0', tk.END).strip()
        if self.current_index is not None:
            self.dialogues[self.current_index] = current_text + "\n"
            self.dialogue_listbox.delete(self.current_index)
            self.dialogue_listbox.insert(self.current_index, current_text)
        # Atualiza a exibição do diálogo e mantém a página atual
        self.display_dialogue(current_text, keep_current_page=True)

    def update_text_position(self, event):
        position_str = self.text_position_entry.get()
        try:
            x, y = map(int, position_str.split(","))
            self.text_position = (x, y)
            self.display_dialogue(self.dialogue_display.get('1.0', tk.END).strip())
        except ValueError:
            pass

    def next_page_entry(self, event=None):
        if self.page_entries:
            self.current_page_index = (self.current_page_index + 1) % len(self.page_entries)
            # Atualiza a exibição do diálogo e mantém a página atual
            self.display_current_page()

    def previous_page_entry(self, event=None):
        if self.page_entries:
            self.current_page_index = (self.current_page_index - 1) % len(self.page_entries)
            # Atualiza a exibição do diálogo e mantém a página atual
            self.display_current_page()

    def save_as(self, event=None):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as file:
                for line in self.dialogues:
                    file.write(line)
            self.file_path = file_path  # Atualizar o caminho do arquivo atual
            self.file_opened = True  # Marcar que o arquivo foi aberto/salvo
            messagebox.showinfo("Save As", "Dialogues saved successfully.")

    def exit_application(self):
        if self.file_opened:
            confirm_exit = messagebox.askyesnocancel("Exit", "Do you want to save before exiting?")
            if confirm_exit is True:
                self.save_as()
                self.root.destroy()
            elif confirm_exit is False:
                self.root.destroy()
            else:
                pass
        else:
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = DialogueEditor(root)
    root.geometry("1280x720")  # Define o tamanho da janela principal para 800x600 pixels
    root.mainloop()
    

