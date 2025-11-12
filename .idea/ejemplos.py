# linea para que apaezca el texto del entry ya seleccionado en azul
self.entry_precio_venta_pesos.bind('<FocusIn>', lambda x: self.entry_precio_venta_pesos.selection_range(0, END))
