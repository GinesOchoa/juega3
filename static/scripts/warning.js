function warning(ID) {
    if (ID == 'delete') {
        if (confirm("¿Borrar este producto del carrito?")) {
            document.getElementById(ID).submit();
        }
    }
    else if (ID == 'clear') {
        if (confirm("¿Borrar todos los productos del carrito?")) {
            document.getElementById(ID).submit();
        }
    }
}