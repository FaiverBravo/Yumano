//--------------MENÚ ANIMADO------------//

let boton = document.getElementById("icono");
let enlaces = document.getElementById("enlaces");
let contador = 0;

boton.addEventListener("click",function(){
    if(contador == 0){
        enlaces.className = ('enlaces dos');
        contador=1;
    }else{
        enlaces.classList.remove('dos');
        enlaces.className = ('enlaces uno');
        contador = 0;
    }
})

window.addEventListener('resize', function(){
    if(screen.width > 750){
        contador=0;
        enlaces.classList.remove('dos');
        enlaces.className = ('enlaces uno');

    }
})

window.addEventListener('click',function(e){
    console.log(e.target);
    if(cerrado==false){
        let span = document.querySelector('.links-header');
        if(e.target == span){
            contador=0;
        }
    }
});


