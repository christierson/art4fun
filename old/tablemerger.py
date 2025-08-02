from tkinter import *
from tabledata import FileTable
from tkinter import filedialog


# t = TableData()

# t.read_table(
#     path="Lagerlista.txt",
#     id_col="Artikelnr",
#     cols={
#         "Benämning": "Benämning",
#         "Antal i lager": "I lager",
#     },
# )
# t.read_table(
#     path="Artikelstatistik.txt",
#     id_col="Art.nr",
#     cols={
#         "Benämning": "Benämning",
#         "Antal": "Sålt",
#     },
# )


# print(t.data)
# t.filter_incomplete()
# t.save_table()


class SimpleFormApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Form")
        self.table = FileTable()

        self.cols = []
        self.id_col = ""

        # # File dialog button
        self.file_button = Button(
            root, text="Select File", command=self.open_file_dialog
        )
        self.file_button.pack(pady=10)

        self.form_frame = Frame(root)

        self.set_id_button = Button(
            self.form_frame, text="Set as identifier column", command=self.set_id_col
        )
        self.set_id_button.pack(pady=5)

        self.id_col_var = StringVar()
        self.id_col_var.set("Identifier column:")
        self.id_col_label = Label(
            self.form_frame, textvariable=self.id_col_var, justify="left"
        )
        self.id_col_label.pack(pady=10)

        # Listbox to show added strings (hidden initially)
        self.listbox = Listbox(self.form_frame, height=5)
        self.listbox.pack(pady=10)

        # Dictionary to hold translations (editable text fields for each item)
        self.translations = {}

        # # Frame to hold the list and the second column
        # self.list_frame = Frame(self.form_frame)
        # self.list_frame.grid(row=2, column=0, columnspan=2, pady=10)

        # # self.item_label = Label(
        # #     self.list_frame, text="Item", font=("Arial", 10, "bold")
        # # )
        # # self.item_label.grid(row=0, column=0, padx=10)
        # # self.translation_label = Label(
        # #     self.list_frame, text="Translation", font=("Arial", 10, "bold")
        # # )
        # # self.translation_label.grid(row=0, column=1, padx=10)

        # # # List of items
        # # self.item_entries = []
        # # self.translation_entries = []

        # self.remove_button = Button(
        #     self.form_frame, text="Remove from List", command=self.remove_from_list
        # )
        # self.remove_button.pack(pady=5)

        # # Hide the form frame initially
        # self.form_frame.pack_forget()

        # ######################################
        # # self.table.read_table("Artikelstatistik.txt")
        # # self.form_frame.pack(pady=10)  # Show the hidden form elements
        # # self.set_cols(self.table.cols)

    def open_file_dialog(self):
        file_path = filedialog.askopenfilename()
        if file_path:  # If a file is selected, show the rest of the form
            self.table.read_table(file_path)
            self.form_frame.pack(pady=10)  # Show the hidden form elements
            # self.set_cols(self.table.cols)

    def set_cols(self, cols):
        for col in cols:
            self.cols.append(col)
            self.listbox.insert(END, col)

    def remove_from_list(self):
        selected_indices = self.listbox.curselection()
        for i in selected_indices[::-1]:  # Remove selected items in reverse order
            self.listbox.delete(i)
            del self.cols[i]

    def set_id_col(self):
        (index,) = self.listbox.curselection()
        self.id_col = self.cols[index]
        self.id_col_var.set(f"Identifier column: {self.id_col}")

    def submit(self):
        print("submit")


# Create the application window
root = Tk()
app = SimpleFormApp(root)
root.mainloop()
