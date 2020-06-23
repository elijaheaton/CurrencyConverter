from CurrencyConverter import set_up
from PIL import ImageTk
import tkinter as tk


class Application(tk.Frame):
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("406x230")
        self.root.title('Currency Converter')
        self.root.resizable(0, 0)

        self.canvas = tk.Canvas(width=400, height=150, bg='blue')
        self.canvas.grid(column='0', row='0')
        self.image = ImageTk.PhotoImage(file='money.gif')
        self.canvas.create_image(0, 0, image=self.image, anchor='nw')
        tk.Frame.__init__(self, self.root)

        self.data = set_up()
        self.input_text = tk.Text(self, height=1, width=55)
        self.input_amount = tk.Entry(self)
        self.output_amount = tk.Entry(self, state='readonly')

        self.convert_to_selection = tk.StringVar(self, 'GBP')
        self.convert_from_selection = tk.StringVar(self, 'EUR')
        self.convert_to = tk.OptionMenu(self, self.convert_from_selection,
                                        *self.data.index.tolist())
        self.convert_from = tk.OptionMenu(self, self.convert_to_selection,
                                          *self.data.index.tolist())
        self.create_widgets()

    def create_widgets(self):
        self.input_text.insert('1.0', 'Input your currency in the left box and hit enter.')
        self.input_text.configure(state='disabled')
        self.input_text.grid(column='0', columnspan='2', row='0')

        self.input_amount.grid(column='0', row='2')
        self.convert_from.grid(column='0', row='3')

        self.output_amount.grid(column='1', row='2')
        self.convert_to.grid(column='1', row='3')

        self.root.bind('<Return>', self.parse)
        self.grid()

    def parse(self, event):
        self.output_amount.configure(state='normal')
        self.output_amount.delete(0, len(self.output_amount.get()))
        try:
            self.output_amount.insert(0, "{:.2f}".format(self.convert().iloc[0]))
        except ValueError:
            self.output_amount.insert(0, 'That can not be converted.')
        self.output_amount.configure(state='readonly')

    def convert(self):
        c_to = self.convert_to_selection.get()
        c_from = self.convert_from_selection.get()
        factor = self.data.loc[c_from] / self.data.loc[c_to]
        return float(self.input_amount.get()) * factor

    def start(self):
        self.root.mainloop()


Application().start()
