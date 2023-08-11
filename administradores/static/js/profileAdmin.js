// sidebar toggle
const btnToggle = document.querySelector(".logo");
const mainContainer = document.querySelector(".container_data");
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
    mainContainer.style.width = "90%";
    mainContainer.style.marginLeft = "10%";
    barOn = true;
    
  } else {
    //console.log("cerrado");
    //btnToggle.classList.remove('activate');
    document.getElementById("sidebar").classList.remove("active");
    barOn = false;
    mainContainer.style.width = "100%";
    mainContainer.style.marginLeft = "0%";
    mainContainer.style.justifyContent = "center";
  }
});
function openNav(){
  console.log("clik");
  if (barOn == false) {
    document.getElementById("sidebar").classList.toggle("active");
    // console.log(document.getElementById('sidebar'));
    // console.log("Abierto");
    mainContainer.style.width = "90%";
    mainContainer.style.marginLeft = "10%";
    barOn = true;
  } else {
    // console.log("cerrado");
    //btnToggle.classList.remove('activate');
    document.getElementById("sidebar").classList.remove("active");
    barOn = false;
    mainContainer.style.width = "100%";
    mainContainer.style.marginLeft = "0%";
    mainContainer.style.justifyContent = "center";
  }
}
openNav();



