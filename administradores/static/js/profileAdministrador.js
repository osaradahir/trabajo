// sidebar toggle
const btnToggle = document.querySelector(".logo");
const mainContainer = document.querySelector(".container_data");
const myDataName = document.querySelector(".my-data-name");
var anchoPantalla = window.innerWidth;
var alturaPantalla = window.innerHeight;

var widgetOn = false;

let barOn = false;
btnToggle.addEventListener("click", function openNav() {
  console.log("clik");
  if (barOn == false) {
    document.getElementById("sidebar").classList.toggle("active");
    // console.log(document.getElementById('sidebar'));
    //console.log("Abierto");
    mainContainer.style.width = "68%";
    myDataName.style.width = "78%";
    mainContainer.style.marginLeft = "18%";
    mainContainer.style.marginRight = "13%";
    mainContainer.style.justifyContent = "initial";
    barOn = true;
    if(previousWidth <= 620){
      //console.log(previousWidth);
      document.getElementById("sidebar").style.height = '4250px';
    }
  } else {
    //console.log("cerrado");
    //btnToggle.classList.remove('activate');
    document.getElementById("sidebar").classList.remove("active");
    barOn = false;
    mainContainer.style.width = "100%";
    mainContainer.style.marginLeft = "0%";
    mainContainer.style.justifyContent = "center";
    myDataName.style.width = "86%";
  }
});
function openNav(){
  console.log("clik");
  if (barOn == false) {
    document.getElementById("sidebar").classList.toggle("active");
    // console.log(document.getElementById('sidebar'));
    // console.log("Abierto");
    mainContainer.style.width = "68%";
    myDataName.style.width = "78%";
    mainContainer.style.marginLeft = "18%";
    mainContainer.style.marginRight = "13%";
    mainContainer.style.justifyContent = "initial";
    barOn = true;
  } else {
    // console.log("cerrado");
    //btnToggle.classList.remove('activate');
    document.getElementById("sidebar").classList.remove("active");
    barOn = false;
    mainContainer.style.width = "100%";
    mainContainer.style.marginLeft = "0%";
    mainContainer.style.justifyContent = "center";
    myDataName.style.width = "86%";
  }
}
openNav();
document.addEventListener("DOMContentLoaded", function () {
  var elems = document.querySelectorAll(".dropdown-trigger");
  var instances = M.Dropdown.init(elems, {
    hover: true,
  });
});




function openFileExplorerForCv() {


}

function openFileExplorerForINE() {
  
}

function openFileExplorerForActa() {
  
}

function openFileExplorerForPasaporte() {
  
}

function openFileExplorerForComprobante() {
  
}

function openFileExplorerForCartaRecomendacion() {
  
}

function openFileExplorerForF3() {
  
}

// console.log("Ancho de la pantalla: " + anchoPantalla);
// console.log("Altura de la pantalla: " + alturaPantalla);

var previousWidth = window.innerWidth;

function handleWindowResize() {
  var currentWidth = window.innerWidth;

  if (
    (previousWidth >= 600 && currentWidth < 600) ||
    (previousWidth < 600 && currentWidth >= 600)
  ) {
    // Si el tamaño previo era mayor o igual a 600 y el tamaño actual es menor a 600, o viceversa, recargar la página
    location.reload();
  }

  previousWidth = currentWidth;
}

// Agregar el listener al evento resize
//window.addEventListener("resize", handleWindowResize);
