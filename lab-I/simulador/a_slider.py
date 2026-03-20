import tkinter as tk
from tkinter import ttk, simpledialog

class Slider(ttk.Frame):
    """Deslizador personalizado que incluye etiqueta, entrada de texto y menú contextual."""

    def __init__(self, parent, label_text, from_, to, value, step=1.0, **kwargs):
        """Crea y posiciona los elementos visuales del deslizador y la entrada numérica."""
        super().__init__(parent, **kwargs)

        self.value_var = tk.DoubleVar(value=value)
        
        self.label = ttk.Label(self, text=label_text)
        self.label.grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        
        self.entry = ttk.Entry(self, textvariable=self.value_var, width=8)
        self.entry.grid(row=0, column=1, sticky=tk.E)
        
        self.scale = tk.Scale(self, from_=from_, to=to, resolution=step, 
                              orient=tk.HORIZONTAL, variable=self.value_var, showvalue=False)
        self.scale.grid(row=1, column=0, columnspan=2, sticky=tk.EW, pady=(2, 5))
        self.columnconfigure(0, weight=1)
        
        self.menu = tk.Menu(self, tearoff=0)
        self.menu.add_command(label="Modificar límite inferior", command=self.change_min)
        self.menu.add_command(label="Modificar límite superior", command=self.change_max)
        self.menu.add_command(label="Modificar paso (resolución)", command=self.change_step)
        
        self.scale.bind("<Button-3>", self.show_menu)
        self.entry.bind("<FocusOut>", self.validate_entry)
        self.entry.bind("<Return>", self.validate_entry)

    def show_menu(self, event):
        """Despliega un menú contextual al hacer clic derecho sobre la escala."""
        self.menu.tk_popup(event.x_root, event.y_root)

    def change_min(self):
        """Solicita al usuario un nuevo valor para el límite inferior de la escala."""
        current_min = self.scale.cget("from")
        new_min = simpledialog.askfloat("Límite Inferior", "Introduce el nuevo límite inferior:", initialvalue=current_min, parent=self)
        if new_min is not None:
            self.scale.config(from_=new_min)

    def change_max(self):
        """Solicita al usuario un nuevo valor para el límite superior de la escala."""
        current_max = self.scale.cget("to")
        new_max = simpledialog.askfloat("Límite Superior", "Introduce el nuevo límite superior:", initialvalue=current_max, parent=self)
        if new_max is not None:
            self.scale.config(to=new_max)

    def change_step(self):
        """Solicita al usuario una nueva resolución (paso) para los incrementos de la escala."""
        current_step = self.scale.cget("resolution")
        new_step = simpledialog.askfloat("Paso / Resolución", "Introduce el nuevo paso del deslizador:", initialvalue=current_step, parent=self)
        if new_step is not None:
            self.scale.config(resolution=new_step)
            
    def validate_entry(self, event):
        """Valida que el texto ingresado manualmente en el campo sea un número válido."""
        try:
            val = float(self.entry.get())
            self.value_var.set(val)
        except ValueError:
            self.value_var.set(self.scale.get())

    def get_value(self):
        """Devuelve el valor numérico actual configurado en el deslizador."""
        return self.value_var.get()