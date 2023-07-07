// sidebar toggle
const btnToggle = document.querySelector(".logo");
var anchoPantalla = window.innerWidth;
var alturaPantalla = window.innerHeight;
var widgetOn = false;
let barOn = false;

btnToggle.addEventListener("click", function openNav() {
  console.log("clik");
  if (barOn == false) {
    document.getElementById("sidebar").classList.toggle("active");
    // console.log(document.getElementById('sidebar'));
    console.log("Abierto");
    document.getElementById('notifications-all-container').style.width = '75%';
    document.getElementById('notifications-all-container').style.marginLeft= '20%';
    document.getElementById('notifications-all-container2').style.width = '75%';
    document.getElementById('notifications-all-container2').style.marginLeft= '20%';
    barOn = true;
  } else {
    console.log("cerrado");
    document.getElementById('notifications-all-container').style.width = '80%';
    document.getElementById('notifications-all-container').style.marginLeft= '10%';
    document.getElementById('notifications-all-container2').style.width = '80%';
    document.getElementById('notifications-all-container2').style.marginLeft= '10%';
    //btnToggle.classList.remove('activate');
    document.getElementById("sidebar").classList.remove("active");
    barOn = false;
  }
});


function openNav() {
  console.log("clik");
  if (barOn == false) {
    document.getElementById("sidebar").classList.toggle("active");
    // console.log(document.getElementById('sidebar'));
    console.log("Abierto");
    document.getElementById('notifications-all-container').style.width = '75%';
    document.getElementById('notifications-all-container').style.marginLeft= '20%';
    document.getElementById('notifications-all-container2').style.width = '75%';
    document.getElementById('notifications-all-container2').style.marginLeft= '20%';
    barOn = true;
  } else {
    console.log("cerrado");
    //btnToggle.classList.remove('activate');
    document.getElementById('notifications-all-container').style.width = '80%';
    document.getElementById('notifications-all-container').style.marginLeft= '10%';
    document.getElementById('notifications-all-container2').style.width = '80%';
    document.getElementById('notifications-all-container2').style.marginLeft= '10%';
    document.getElementById("sidebar").classList.remove("active");
    barOn = false;;
  }
}
openNav();


        document.addEventListener('DOMContentLoaded', function() {
            var elems = document.querySelectorAll('.dropdown-trigger');
            var instances = M.Dropdown.init(elems, {
                constrainWidth: false,
                coverTrigger: false
            });
            });