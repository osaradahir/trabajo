// sidebar toggle
const btnToggle = document.querySelector(".logo");
const mainContainer = document.querySelector(".container_data");
const myDataName = document.querySelector(".my-data-name");
const editProfileUserInformation = document.querySelector(
  "#edit-profile-user-information"
);
const cancelEditingInformationProfile = document.querySelector(
  "#cancel-editing-information-profile"
);
const editContactUserInformation = document.querySelector(
  "#edit-contact-user-information"
);
const cancelEditingInformationContact = document.querySelector(
  "#cancel-editing-information-contact"
);

const editLanguajesUserInformation = document.querySelector(
  "#edit-languajes-user-information"
);

const cancelEditingInformationLanguajes = document.querySelector(
  "#cancel-editing-information-languajes"
);

const editFactoryInformationActivate = document.querySelector(
  "#edit-factory-information-activate"
);
const coursesEditButton = document.querySelector("#courses-edit-button");
const coursesEditButtonCancel = document.querySelector(
  "#courses-edit-button-cancel"
);
const editEducationUserInformation = document.querySelector(
  "#edit-education-user-information"
);
const cancelEditingInformationEstudy = document.querySelector(
  "#cancel-editing-information-estudy"
);
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
    mainContainer.style.width = "68%";
    myDataName.style.width = "78%";
    mainContainer.style.marginLeft = "18%";
    mainContainer.style.marginRight = "13%";
    mainContainer.style.justifyContent = "initial";
    barOn = true;
  } else {
    console.log("cerrado");
    //btnToggle.classList.remove('activate');
    document.getElementById("sidebar").classList.remove("active");
    barOn = false;
    mainContainer.style.width = "100%";
    mainContainer.style.marginLeft = "0%";
    mainContainer.style.justifyContent = "center";
    myDataName.style.width = "86%";
  }
});
function openNav() {
  console.log("clik");
  if (barOn == false) {
    document.getElementById("sidebar").classList.toggle("active");
    // console.log(document.getElementById('sidebar'));
    console.log("Abierto");
    mainContainer.style.width = "68%";
    myDataName.style.width = "78%";
    mainContainer.style.marginLeft = "18%";
    mainContainer.style.marginRight = "13%";
    mainContainer.style.justifyContent = "initial";
    barOn = true;
  } else {
    console.log("cerrado");
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