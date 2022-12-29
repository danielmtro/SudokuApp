import SudokuProgram
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout

class MainApp(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        self.icon = "icon.png"
        self.lstsols = []

        self.row = 1
        self.col = 1

        self.map =[[None for j in range(9)] for i in range(9)] 
         
        main_layout = BoxLayout(orientation = "vertical")

        sudokubox = [
            ["", "", ""],
            ["", "", ""],
            ["", "", ""]
        ]

        # for row in sudokubox:
        #     h_layout = BoxLayout()
        #     for col in row:
        #         sol = TextInput(background_color = (1, 1, 1, 1), foreground_color = "black")
        #         h_layout.add_widget(sol)
        #         self.lstsols.append(sol)

        #     main_layout.add_widget(h_layout)

        glayout = GridLayout(rows = 9, cols = 9, row_default_height = 30, size_hint_y = 7, size_hint_x = 0.7, pos_hint = {'right': 0.85})
        for i in range(9):
            self.lstsols.append([])
            for j in range(9):
                sol = TextInput(background_color = (1, 1, 1, 1), foreground_color = "black", height = 150, readonly = True, halign = "center", font_size = 25, font_name = "Comic")
                glayout.add_widget(sol)
                self.lstsols[i].append(sol)

        main_layout.add_widget(glayout)

        self.solution = TextInput(background_color = "black", foreground_color = "white")
        
        

        buttons = [
            ["7", "8", "9"],
            ["4", "5", "6"],
            ["1", "2", "3"]
        ]

        for row in buttons:
            h_layout = BoxLayout()
            for label in row:
                button = Button(
                    text = label, font_size = 30, background_color = "grey", pos_hint = {"center_x": 0.5, "center_y": 0.5}
                )
                button.bind(on_press = self.on_button_press  )
                h_layout.add_widget(button)
            main_layout.add_widget(h_layout)
        
        hlayout = BoxLayout()
        next_button = Button(
            text = "NEXT", font_size = 30, background_color = "grey", pos_hint = {"center_x": 0.5, "center_y": 0.5}
        )
        next_button.bind(on_press = self.on_next)
        hlayout.add_widget(next_button)

        prev_button = Button(
            text = "PREV", font_size = 30, background_color = "grey", pos_hint = {"center_x": 0.5, "center_y": 0.5}
        )
        prev_button.bind(on_press = self.on_prev)
        hlayout.add_widget(prev_button)

        main_layout.add_widget(hlayout)



        equal_button = Button(
            text = "SOLVE", font_size = 30, background_color = "grey", pos_hint = {"center_x": 0.5, "center_y": 0.5}
        )
        equal_button.bind(on_press = self.on_solution)
        main_layout.add_widget(equal_button)

        return main_layout

    def on_button_press(self, instance):
        button_text = instance.text
        self.lstsols[self.row - 1][self.col - 1].text = button_text
        return
    

    def on_next(self, instance):
        current = self.lstsols[self.row - 1][self.col - 1].text
        try:
            self.map[self.row - 1][self.col - 1] = int(current)
        except:
            self.map[self.row - 1][self.col - 1] = None

        self.col += 1
        if self.col == 10:
            self.col = 1
            self.row += 1
        
        if self.row == 10:
            self.col = 1
            self.row = 1

        self.lstsols[self.row - 1][self.col - 1].text = "_"

    

    def on_solution(self, instance):

        sudoku = SudokuProgram.Graph()
        result = SudokuProgram.Graph()
        SudokuProgram.addTemplate(self.map, sudoku)

        # template1 = [
        #     [None, 3, 5, 2, 6, 9, 7, 8, 1],
        #     [6, 8, 2, 5, 7, 1, 4, 9, 3],
        #     [1, 9, 7, 8, 3, 4, 5, 6, 2],
        #     [8, 2, 6, 1, 9, 5, 3, 4, 7],
        #     [3, 7, 4, 6, 8, 2, 9, 1, 5],
        #     [9, 5, 1, 7, 4, 3, 6, 2, 8],
        #     [5, 1, 9, 3, 2, 6, 8, 7, 4],
        #     [2, 4, 8, 9, 5, 7, 1, 3, 6],
        #     [7, 6, 3, 4, 1, 8, 2, 5, 9]
        # ]

        # SudokuProgram.addTemplate(template1, sudoku)
        SudokuProgram.canSolve(sudoku, result)

        if not result.isComplete():
            return

        resultmap = result.getMatrix()
        #print(resultmap)

        for row in range(9):
            for col in range(9):
                self.lstsols[row][col].text = str(resultmap[row + 1][col + 1])

        return

    def on_prev(self, instance):

        current = self.lstsols[self.row - 1][self.col - 1].text
        try:
            self.map[self.row - 1][self.col - 1] = int(current)
        except:
            self.map[self.row - 1][self.col - 1] = None

        self.col -= 1
        if self.col == 0:
            self.col = 9
            self.row -= 1
        
        if self.row == 0:
            self.col = 9
            self.row = 9

        self.lstsols[self.row - 1][self.col - 1].text = "_"
        return

if __name__ == "__main__":
    app = MainApp()
    app.run()
 

