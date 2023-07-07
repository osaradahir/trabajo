var showButton = document.getElementById('showButton');
var content = document.getElementById('content');

showButton.addEventListener('click', function(){
    if (content.classList.contains('hidden-content')){
        content.classList.remove('hidden-content');
        showButton.textContent ="Ocultar filtros";
    } else {
        content.classList.add('hidden-content');
        showButton.textContent = "Mas filtros"
    }
});

$(document).ready(function(){
    $('.tabs').tabs();
    });

$(document).ready(function(){
    $('select').formSelect();
});

var elem = document.querySelector('.collapsible.expandable');
var instance = M.Collapsible.init(elem, {
  accordion: false
});

$(document).ready(function(){
    $('.tooltipped').tooltip();
  });

      // Agregar el listener al evento resize
      window.addEventListener("resize", aparece);
      function aparece() {
        var anchoPantalla = window.innerWidth;
        if (anchoPantalla <= 500){
          console.log("shsh")
          
          
          var test =document.querySelectorAll('#user1')
          for(var i=0;i<test.length;i++)
          {
              test[i].style.width = '';
              test[i].style.marginLeft = '0px';
              test[i].style.marginRight = '0px';
          }
        }
        else {
          console.log("jjjh")
          var test =document.querySelectorAll('#user1');
          for(var i=0;i<test.length;i++)
          {
              test[i].style.width = '23%';
              test[i].style.marginLeft = '9px';
              test[i].style.marginRight = '9px';
          }
        }
      }
      aparece();
  
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
//openNav();