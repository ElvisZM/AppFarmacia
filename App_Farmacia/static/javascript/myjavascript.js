/*alert("¡P.Sur Pharmacy, tu farmacia de confianza!")*/

function eliminar() {
    var x = confirm("¿Está seguro que quiere eliminar este Producto?");
    if (x){
        return true;
    }
    else{
        return false;
    }
}