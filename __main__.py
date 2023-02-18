import tkinter
import tkinter.messagebox
import customtkinter
import csv

from knapsack_solve import main
from properties import Properties

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.cache_data: dict = {}

        self.path: dict = {
            0: "BoySchoolBackpack",
            1: "BoyTravelBackpack",
            2: "GirlSchoolBackpack",
            3: "GirlTravelBackpack"
        }
        self.CSVText = """"""
        self.filenames = [
            "Boy School Backpack",
            "Boy Travel Backpack",
            "Girl School Backpack",
            "Girl Travel Backpack"
        ]
        self.value = 0
        self.oldValue = 0
        self.read_csv_data()

        # configure window
        self.title("Knapsack Menu")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=0, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                                       values=["Dark", "Light", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=1, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=2, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                               values=["80%", "90%", "100%", "110%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.set("100%")
        self.scaling_optionemenu.grid(row=3, column=0, padx=20, pady=(10, 20))

        # create main entry and button
        self.myLabel = customtkinter.CTkLabel(self, text="Select the CSV file:", font=(16, 22))
        self.myLabel.place(relx=0.28, rely=0.1, anchor=tkinter.CENTER)
        self.slider_1 = customtkinter.CTkSlider(self, command=self.slider_callback, from_=0, to=len(self.filenames) - 1)
        self.slider_1.place(relx=0.33, rely=0.37)
        self.slider_1.set(0)

        self.fileLabel = customtkinter.CTkLabel(self, text=f"{self.value + 1}. FIle: {self.filenames[self.value]}",
                                                font=(26, 30))
        self.fileLabel.place(relx=0.42, rely=0.3, anchor=tkinter.CENTER)

        self.pop_size = customtkinter.CTkEntry(self, placeholder_text="Population size = 100", width=140, height=58)
        self.pop_size.place(relx=0.18, rely=0.8)

        self.max_gens = customtkinter.CTkEntry(self, placeholder_text="Max generations = 50", width=140, height=58)
        self.max_gens.place(relx=0.18, rely=0.6)

        self.cross = customtkinter.CTkEntry(self, placeholder_text="Crossover = 0.9", width=140, height=58)
        self.cross.place(relx=0.36, rely=0.6)

        self.mut = customtkinter.CTkEntry(self, placeholder_text="Mutation = 0.1",
                                          width=140, height=58)
        self.mut.place(relx=0.36, rely=0.8)

        self.hall_of_fame_size = customtkinter.CTkEntry(self, placeholder_text="HOF size = 1",
                                                        width=140, height=58)
        self.hall_of_fame_size.place(relx=0.54, rely=0.6)

        self.rand_seed = customtkinter.CTkEntry(self, placeholder_text="Random seed = 42",
                                                width=140, height=58)
        self.rand_seed.place(relx=0.54, rely=0.8)

        self.main_button_1 = customtkinter.CTkButton(master=self, text="START", fg_color="transparent", border_width=2,
                                                     text_color=("gray10", "#DCE4EE"), command=self.start_knapsack)
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # create textbox
        self.textbox = customtkinter.CTkTextbox(self, width=340, height=550, text_color="grey", font=(16, 20))
        self.textbox.grid(row=0, column=3)

        self.textbox.insert("0.0", text=self.CSVText)  # insert at line 0 character 0

        self.textbox.configure(state="disabled")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def slider_callback(self, value):
        val = round(value)
        self.slider_1.set(value)
        self.value = val

        if self.oldValue != val:
            self.fileLabel.destroy()
            self.fileLabel = customtkinter.CTkLabel(self, text=f"{self.value + 1}. FIle: {self.filenames[self.value]}",
                                                    font=(26, 30))
            self.fileLabel.place(relx=0.42, rely=0.3, anchor=tkinter.CENTER)

            self.read_csv_data()
            self.textbox.configure(state='normal')
            self.textbox.delete('0.0', 'end')

            self.textbox.insert("0.0", text=self.CSVText)  # insert at line 0 character 0

            self.textbox.configure(state="disabled")

            self.oldValue = val

    def start_knapsack(self):
        properties = Properties()
        pop_size = self.pop_size.get()
        max_gens = self.max_gens.get()
        cross = self.cross.get()
        mut = self.mut.get()
        hof_size = self.hall_of_fame_size.get()
        rand_seed = self.rand_seed.get()

        print(max_gens)

        properties.POPULATION_SIZE = int(pop_size) if pop_size else 100
        properties.MAX_GENERATIONS = int(max_gens) if max_gens else 50
        properties.P_CROSSOVER = float(cross) if cross else 0.9
        properties.P_MUTATION = float(mut) if mut else 0.1
        properties.HALL_OF_FAME_SIZE = int(hof_size) if hof_size else 1
        properties.RANDOM_SEED = int(rand_seed) if rand_seed else 42

        main(self.value, properties)

    def read_csv_data(self):
        if self.value in self.cache_data:
            self.CSVText = self.cache_data[self.value]
            return

        with open(f"./{self.path[self.value]}.csv", 'r') as file:
            result = [", ".join(row) for row in csv.reader(file)]

        self.CSVText = "\n".join(result)
        self.cache_data[self.value] = self.CSVText


if __name__ == "__main__":
    app = App()
    app.mainloop()
