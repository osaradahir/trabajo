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

document.addEventListener("DOMContentLoaded", function () {
  var elems = document.querySelectorAll(".dropdown-trigger");
  var instances = M.Dropdown.init(elems, {
    hover: true,
  });
});

editProfileUserInformation.addEventListener("click", function () {
  if (widgetOn == false) {
    let containerEditInformationProfile = document.querySelector(
      ".input-information-user-profile"
    );
    containerEditInformationProfile.style.display = "block";
    let informationUserProfile = document.querySelector(
      ".information-user-profile"
    );
    informationUserProfile.style.display = "none";
    let informationUserBotommsCv = document.querySelector(
      ".information-user-botomms-cv"
    );
    informationUserBotommsCv.style.display = "none";
    widgetOn = true;
  }
});

cancelEditingInformationProfile.addEventListener("click", function () {
  let containerEditInformationProfile = document.querySelector(
    ".input-information-user-profile"
  );
  containerEditInformationProfile.style.display = "none";
  let informationUserProfile = document.querySelector(
    ".information-user-profile"
  );
  informationUserProfile.style.display = "block";
  let informationUserBotommsCv = document.querySelector(
    ".information-user-botomms-cv"
  );
  informationUserBotommsCv.style.display = "flex";
  widgetOn = false;
});

editContactUserInformation.addEventListener("click", function () {
  if (widgetOn == false) {
    if (anchoPantalla <= 616) {
      let containerEditExperience = document.querySelector(
        ".container-edit-experience"
      );
      containerEditExperience.style.display = "block";

      let contactInfo = document.querySelector(".contact-info");
      contactInfo.style.display = "none";

      let contactButton = document.querySelector(".contact-button");
      contactButton.style.display = "none";

      let divInformationContactExperience = document.querySelector(
        ".information-contact-experience"
      );
      divInformationContactExperience.style.height = "1100px";

      let divContact = document.querySelector(
        "div.information-contact-experience div.contact"
      );
      divContact.style.paddingLeft = "0px";
      divContact.style.height = "650px";

      let divContactTittle = document.querySelector(".data-contact-tittle");
      divContactTittle.style.paddingLeft = "20px";
    } else {
      let containerEditExperience = document.querySelector(
        ".container-edit-experience"
      );
      containerEditExperience.style.display = "block";

      let contactInfo = document.querySelector(".contact-info");
      contactInfo.style.display = "none";

      let contactButton = document.querySelector(".contact-button");
      contactButton.style.display = "none";

      let divInformationContactExperience = document.querySelector(
        ".information-contact-experience"
      );
      divInformationContactExperience.style.height = "650px";

      let divContact = document.querySelector(
        "div.information-contact-experience div.contact"
      );
      divContact.style.paddingLeft = "0px";
      divContact.style.height = "650px";
      let divContactTittle = document.querySelector(".data-contact-tittle");
      divContactTittle.style.paddingLeft = "20px";
    }
    widgetOn = true;
  }
});

cancelEditingInformationContact.addEventListener("click", function () {
  let containerEditExperience = document.querySelector(
    ".container-edit-experience"
  );
  containerEditExperience.style.display = "none";

  let contactInfo = document.querySelector(".contact-info");
  contactInfo.style.display = "block";

  let contactButton = document.querySelector(".contact-button");
  contactButton.style.display = "flex";

  let divInformationContactExperience = document.querySelector(
    ".information-contact-experience"
  );
  divInformationContactExperience.style.height = "350px";

  let divContact = document.querySelector(
    "div.information-contact-experience div.contact"
  );
  divContact.style.paddingLeft = "20px";
  divContact.style.height = "350px";

  let divContactTittle = document.querySelector(".data-contact-tittle");
  divContactTittle.style.paddingLeft = "0px";

  let divLenguajes = document.querySelector(
    ".information-contact-experience#lenguajes"
  );
  divLenguajes.style.marginTop = "30px";

  widgetOn = false;
});

editLanguajesUserInformation.addEventListener("click", function () {
  if (widgetOn == false) {
    if (anchoPantalla > 616) {
      let divLenguajes = document.querySelector(
        "div.information-contact-experience#lenguajes"
      );
      divLenguajes.style.height = "360px";

      let languajesContainer = document.querySelector(".languajes-container");
      languajesContainer.style.display = "block";

      let contactInfo = document.querySelector("#languajes-description");
      contactInfo.style.display = "none";

      let editLanguajesUserInformation = document.querySelector(
        "#edit-languajes-user-information"
      );
      editLanguajesUserInformation.style.display = "none";
    } else {
      let divLenguajes = document.querySelector(
        "div.information-contact-experience#lenguajes"
      );
      divLenguajes.style.height = "900px";
      //divLenguajes.style.backgroundColor = "green"
      let divContact = document.querySelector(
        "#information-contact-experience-contact"
      );
      divContact.style.height = "350px";

      let languajesContainer = document.querySelector(".languajes-container");
      languajesContainer.style.display = "block";

      let contactInfo = document.querySelector("#languajes-description");
      contactInfo.style.display = "none";

      let editLanguajesUserInformation = document.querySelector(
        "#edit-languajes-user-information"
      );
      editLanguajesUserInformation.style.display = "none";
    }
    widgetOn = true;
  }
});

cancelEditingInformationLanguajes.addEventListener("click", function () {
  let divLenguajes = document.querySelector(
    "div.information-contact-experience#lenguajes"
  );
  if (anchoPantalla <= 616) {
    let editLanguajesUserInformationDos = document.querySelector(
      "#information-contact-experience-contact"
    );
    editLanguajesUserInformationDos.style.height = "250px";

    let editLanguajesUserInformationTres = document.querySelector(
      "#information-contact-experience-contact-experience"
    );
    editLanguajesUserInformationTres.style.height = "250px";
    divLenguajes.style.height = "550px";
  } else {
    divLenguajes.style.height = "260px";
    
  }

  let languajesContainer = document.querySelector(".languajes-container");
  languajesContainer.style.display = "none";

  let contactInfo = document.querySelector("#languajes-description");
  contactInfo.style.display = "block";

  let editLanguajesUserInformation = document.querySelector(
    "#edit-languajes-user-information"
  );
  editLanguajesUserInformation.style.display = "block";

  widgetOn = false;
});

editFactoryInformationActivate.addEventListener("click", function () {
  if (widgetOn == false) {
    let factoryContainer = document.querySelector("#inputs-show-factury");
    factoryContainer.style.display = "none";

    let factoryEditContainer = document.querySelector("#input-edit-factury");
    factoryEditContainer.style.display = "block";

    let buttonRfc = document.querySelector(".buttons-rfc#buttons-show");
    buttonRfc.style.display = "none";
    widgetOn = true;
  }
});

coursesEditButton.addEventListener("click", function () {
  if (widgetOn == false) {
    console.log("olalalalalalal");
    let coursesEditContainer = document.querySelector(
      "#courses-edit-container"
    );
    coursesEditContainer.style.display = "block";

    let coursesShowContainer = document.querySelector(
      "#courses-show-container"
    );
    coursesShowContainer.style.display = "none";

    coursesEditContainer.style.height = "680px";

    let sidebar = document.querySelector("#sidebar.active");

    if (sidebar) {
      sidebar.style.height = "2400px";
    } else {
      console.log(
        "El componente de la barra lateral no se encuentra en el documento."
      );
    }

    if (anchoPantalla <= 616) {
      let containerModuls = document.querySelector(".courses-moduls");
      containerModuls.style.marginTop = "-30px";
    }
    widgetOn = true;
  }
});

coursesEditButtonCancel.addEventListener("click", function () {
  let coursesEditContainer = document.querySelector("#courses-edit-container");
  coursesEditContainer.style.display = "none";

  let coursesShowContainer = document.querySelector("#courses-show-container");
  coursesShowContainer.style.display = "block";
  coursesShowContainer.style.height = "250px";

  let sidebar = document.querySelector("#sidebar.active");

  if (sidebar) {
    sidebar.style.height = "2400px";
  } else {
    console.log(
      "El componente de la barra lateral no se encuentra en el documento."
    );
  }
  widgetOn = false;
});

editEducationUserInformation.addEventListener("click", function () {
  if (widgetOn == false) {
    let educationContainer = document.querySelector(
      "#data-experience-show-container"
    );
    educationContainer.style.display = "none";

    let educationEditContainer = document.querySelector(
      "#data-experience-edit-container"
    );
    educationEditContainer.style.display = "block";

    let buttonExperienceStudy = document.querySelector(
      ".button-experience-study"
    );
    buttonExperienceStudy.style.display = "none";
    if (anchoPantalla <= 616) {
      let containerExperienceStudy = document.querySelector(
        "div.information-contact-experience#lenguajes"
      );
      containerExperienceStudy.style.height = "900px";
      let containerExperienceExperience = document.querySelector(
        "div#data-experience-edit-container"
      );
      containerExperienceExperience.style.height = "340px";
      let containerExperience = document.querySelector(
        "div#information-contact-experience-contact-experience"
      );
      containerExperience.style.height = "390px";
    } else {
      let containerExperienceStudy = document.querySelector(
        "div.information-contact-experience#lenguajes"
      );
      containerExperienceStudy.style.height = "450px";
    }
    widgetOn = true;
  }
});

cancelEditingInformationEstudy.addEventListener("click", function () {
  let divLenguajes = document.querySelector(
    "div.information-contact-experience#lenguajes"
  );
  divLenguajes.style.height = "900px";
  let divContact = document.querySelector(
    "#information-contact-experience-contact"
  );

  let educationContainer = document.querySelector(
    "#data-experience-show-container"
  );
  educationContainer.style.display = "block";

  let educationEditContainer = document.querySelector(
    "#data-experience-edit-container"
  );
  educationEditContainer.style.display = "none";

  let buttonExperienceStudy = document.querySelector(
    ".button-experience-study"
  );
  buttonExperienceStudy.style.display = "flex";

  if (anchoPantalla <= 616) {
    let containerExperienceStudy = document.querySelector(
      "div.information-contact-experience#lenguajes"
    );
    containerExperienceStudy.style.height = "600px";
  } else {
    let containerExperienceStudy = document.querySelector(
      "div.information-contact-experience#lenguajes"
    );
    containerExperienceStudy.style.height = "250px";
  }
  widgetOn = false;
});

function editRowSapId(id) {
  console.log("Botón presionado: " + id);

  let form = document.querySelector(`#sap-form-${id}`);
  //form.style.display = "block";
  // form.style.width = "100%";

  let formTrEdit = document.querySelector(`#sap-form-edit-${id}`);
  formTrEdit.style.display = "";
  formTrEdit.style.width = "100%";

  let formTrShow = document.querySelector(`#sap-form-show-${id}`);
  formTrShow.style.display = "none";
}

function changeKindMoney() {
  let showContainer = document.querySelector("#money-kind-show");
  showContainer.style.display = "none";

  let editContainer = document.querySelector("#money-kind-edit");
  editContainer.style.display = "flex";

  let editContainerSelect = document.querySelector("#selectMoneda");
  editContainerSelect.style.display = "block";

  let editButton = document.querySelector("#button-edit");
  editButton.style.display = "none";

  let showButton = document.querySelector("#button-save");
  showButton.style.display = "";
}

function saveKindMoney() {
  let showContainer = document.querySelector("#money-kind-show");
  showContainer.style.display = "";

  let editContainer = document.querySelector("#money-kind-edit");
  editContainer.style.display = "none";

  let editButton = document.querySelector("#button-edit");
  editButton.style.display = "";

  let showButton = document.querySelector("#button-save");
  showButton.style.display = "none";
}

function changeCostHour() {
  let showContainer = document.querySelector("#hour-kind-show");
  showContainer.style.display = "none";

  let editContainer = document.querySelector("#hour-kind-edit");
  editContainer.style.display = "flex";

  let editButton = document.querySelector("#button-edit-hour");
  editButton.style.display = "none";

  let showButton = document.querySelector("#button-save-hour");
  showButton.style.display = "";
}

function saveCostHour() {
  let showContainer = document.querySelector("#hour-kind-show");
  showContainer.style.display = "";

  let editContainer = document.querySelector("#hour-kind-edit");
  editContainer.style.display = "none";

  let editButton = document.querySelector("#button-edit-hour");
  editButton.style.display = "";

  let showButton = document.querySelector("#button-save-hour");
  showButton.style.display = "none";
}

function openFileExplorerForCv() {
  let fileInputCV = document.getElementById("fileInputCV");
  fileInputCV.click();
}

function openFileExplorerForINE() {
  let fileInputINE = document.getElementById("fileInputINE");
  fileInputINE.click();
}

function openFileExplorerForActa() {
  let fileInputActaNacimiento = document.getElementById(
    "fileInputActaNacimiento"
  );
  fileInputActaNacimiento.click();
}

function openFileExplorerForPasaporte() {
  let fileInputPasaporte = document.getElementById("fileInputPasaporte");
  fileInputPasaporte.click();
}

function openFileExplorerForComprobante() {
  let fileInputComprobanteDomicilio = document.getElementById(
    "fileInputComprobanteDomicilio"
  );
  fileInputComprobanteDomicilio.click();
}

function openFileExplorerForCartaRecomendacion() {
  let fileInputCartaRecomendacion = document.getElementById(
    "fileInputCartaRecomendacion"
  );
  fileInputCartaRecomendacion.click();
}

function openFileExplorerForF3() {
  let fileInputF3 = document.getElementById("fileInputF3");
  fileInputF3.click();
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
window.addEventListener("resize", handleWindowResize);


function comprobar(obj)
{   
    if (obj.checked){
       document.getElementById("ageFinish").value = "";
       document.getElementById('ageFinish').style.display = "none";
       document.getElementById('span-study').style.display = "none";
   } else{
     document.getElementById('span-study').style.display = "";
     document.getElementById("ageFinish").value = "";
       document.getElementById('ageFinish').style.display = "";
   }     
}
document.getElementById("ageFinish").value = "";
document.getElementById("ageInit").value = "";
function handleFileSelected(event, kindFile) {
 console.log(kindFile)
 const file = event.target.files[0];
 const rfcValue = document.getElementById('data_rfc').value;
 // Verificar que se haya seleccionado un archivo
 if (file) {
   // Crear una instancia de FormData
   const formData = new FormData();
   formData.append('file', file);
   formData.append('name', kindFile);
   formData.append('rfc', rfcValue);


   // Obtener el token CSRF del formulario
   const csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;
   formData.append('csrfmiddlewaretoken', csrfToken);

   // Realizar la solicitud POST usando fetch
   fetch('upload', {
     method: 'POST',
     body: formData,
     headers: {
       'X-CSRFToken': csrfToken
     }
   })
   .then(response => {
     const body = document.querySelector('body');
     Swal.fire({
       icon: 'success',
       title: 'Archivo subido',
       text: 'El archivo se envio correctamente',
     }).then((result) => {
       if (result.isConfirmed) {
         window.location.reload()
       }
     });
   })
   .catch(error => {
     Swal.fire({
       icon: 'error',
       title: 'Oops...',
       text: 'Algo salio mal',
     })
   });
 }
}

document.addEventListener('DOMContentLoaded', function () {
 var dates = document.querySelectorAll('#ageFinish');
 M.Datepicker.init(dates, {
     format: 'yyyy-mm-dd',
     setDefaultDate: true,
     autoClose: true,
     showClearBtn: true,
     firstDay: 1,
     minDate: new Date(1969, 1, 12),
     maxDate: new Date(2023, 11, 31),
     i18n: {
         cancel: "Cancelar",
         clear: "Limpiar",
         done: "Listo",
         today: "Hoy",
         previousMonth: "Mes anterior",
         nextMonth: "Siguiente mes",
         months: [
           "Enero",
           "Febrero",
           "Marzo",
           "Abril",
           "Mayo",
           "Junio",
           "Julio",
           "Agosto",
           "Septiembre",
           "Octubre",
           "Noviembre",
           "Diciembre",
         ],
         monthsShort: [
           "Ene",
           "Feb",
           "Mar",
           "Abr",
           "May",
           "Jun",
           "Jul",
           "Ago",
           "Sep",
           "Oct",
           "Nov",
           "Dic",
         ],
         weekdays: [
           "Domingo",
           "Lunes",
           "Martes",
           "Miércoles",
           "Jueves",
           "Viernes",
           "Sábado",
         ],
         weekdaysShort: ["Dom", "Lun", "Mar", "Mié", "Jue", "Vie", "Sáb"],
         weekdaysAbbrev: ["D", "L", "M", "M", "J", "V", "S"],
       },onClose: function () {
         setTimeout(function () {
           let fechaEntrada = document.getElementById("ageInit").value;
           let fechaSalida = document.getElementById("ageFinish").value;
           var fechaNacInput = document.getElementById('fecha-nacimiento').value;
           console.log(fechaNacInput)
           var dateEntrada = new Date(fechaEntrada);
           var dateSalida = new Date(fechaSalida);
           var fechaHoy = new Date();  // Crear un objeto Date con la fecha y hora actuales
           var fechaNac = moment(fechaNacInput, "MMM. DD, YYYY, h:mm a");
           var fechaDate = fechaNac.toDate();
           fechaDate.setFullYear(fechaDate.getFullYear() + 18);
           console.log(fechaDate);

           if (dateSalida <= fechaDate) {
             document.getElementById("ageFinish").value = "";
             Swal.fire('La fecha de salida no debe ser menor que tu edad minima requerida');
           }

           
           if (dateSalida == dateEntrada) {
             document.getElementById("ageFinish").value = "";
             Swal.fire('La fecha de entrada no debe igual que la de salida');
           }


           if (dateSalida >= fechaHoy) {
             document.getElementById("ageFinish").value = "";
             Swal.fire('La fecha de salida no debe ser mayor a la fecha actual');
           }

           console.log(fechaHoy)
         }, 1000);
       },
 })
})


document.addEventListener("DOMContentLoaded", function () {
       var fechaSalidaInput = document.getElementById("ageInit");
       M.Datepicker.init(fechaSalidaInput, {
         format: "yyyy-mm-dd",
         autoClose: true,
           autoClose:true,
           showClearBtn:true,
           firstDay: 1,
           minDate: new Date(1969,1,12),
           maxDate: new Date(2023,11,31),
           i18n: {
               cancel: "Cancelar",
               clear: "Limpiar",
               done: "Listo",
               today: "Hoy",
               previousMonth: "Mes anterior",
               nextMonth: "Siguiente mes",
               months: [
                 "Enero",
                 "Febrero",
                 "Marzo",
                 "Abril",
                 "Mayo",
                 "Junio",
                 "Julio",
                 "Agosto",
                 "Septiembre",
                 "Octubre",
                 "Noviembre",
                 "Diciembre",
               ],
               monthsShort: [
                 "Ene",
                 "Feb",
                 "Mar",
                 "Abr",
                 "May",
                 "Jun",
                 "Jul",
                 "Ago",
                 "Sep",
                 "Oct",
                 "Nov",
                 "Dic",
               ],
               weekdays: [
                 "Domingo",
                 "Lunes",
                 "Martes",
                 "Miércoles",
                 "Jueves",
                 "Viernes",
                 "Sábado",
               ],
               weekdaysShort: ["Dom", "Lun", "Mar", "Mié", "Jue", "Vie", "Sáb"],
               weekdaysAbbrev: ["D", "L", "M", "M", "J", "V", "S"],
             },
         onClose: function () {
           setTimeout(function () {
           let fechaEntrada = document.getElementById("ageInit").value;
           let fechaSalida = document.getElementById("ageFinish").value;
           var fechaNacInput = document.getElementById('fecha-nacimiento').value;
           console.log(fechaNacInput)

             var dateEntrada = new Date(fechaEntrada);
             var dateSalida = new Date(fechaSalida);
             var fechaHoy = new Date();  // Crear un objeto Date con la fecha y hora actuales
             var fechaNac = moment(fechaNacInput, "MMM. DD, YYYY, h:mm a");
             var fechaDate = fechaNac.toDate();
             fechaDate.setFullYear(fechaDate.getFullYear() + 18);
             console.log(fechaDate);

             if (dateEntrada <= fechaDate) {
               document.getElementById("ageInit").value = "";
               Swal.fire('La fecha de entrada no debe ser menor que tu edad minima requerida');
             }
             if (dateEntrada >= fechaHoy) {
               document.getElementById("ageInit").value = "";
               console.log(document.getElementById("ageInit").value)
               Swal.fire('La fecha de entrada no debe ser mayor a la fecha actual');
             }
             if (dateEntrada == dateSalida) {
               document.getElementById("ageFinish").value = "";
               Swal.fire('La fecha de entrada no debe igual que la de salida');
             }
             if (dateEntrada >= dateSalida) {
               document.getElementById("ageInit").value = "";
               Swal.fire('La fecha de salida no debe ser mayor que la de entrada');
             }

             console.log(fechaHoy)
           }, 1000);
         },
       });
     });

document.getElementById("button-information-user-profile").addEventListener("click", function(event) {
 event.preventDefault(); // Evita el comportamiento predeterminado del botón

 // Obtén el formulario
 var form = document.getElementById("update-information-personal");

 // Crea un objeto FormData para recopilar los datos del formulario
 var formData = new FormData(form);

 // Realiza una solicitud HTTP utilizando fetch o XMLHttpRequest
 fetch('updateprofileinformation', {
   method: 'POST',
   body: formData
 })
 .then(response => {
   if(response.status == 200){
     Swal.fire({
       icon: 'success',
       title: '¡Éxito!',
       text: 'Los cambios se han guardado correctamente.',
     }).then((result) => {
       if (result.isConfirmed) {
         window.location.reload()
       }else{
         Swal.fire({
           icon: 'error',
           title: 'Oops...',
           text: 'Algo salio mal',
         });
       }
     });
     form.reset();
   }
 })
 .catch(error => {
   Swal.fire({
     icon: 'error',
     title: 'Oops...',
     text: 'Algo salio mal',
   });
   form.reset();
 });
});


function saveKindMoney(){
 // Obtén el formulario
 var form = document.getElementById("update-moneda-cobro");

 // Crea un objeto FormData para recopilar los datos del formulario
 var formData = new FormData(form);

 // Realiza una solicitud HTTP utilizando fetch o XMLHttpRequest
 fetch('updateconsultorinformation', {
   method: 'POST',
   body: formData
 })
 .then(response => {
   if(response.status == 200){
     Swal.fire({
       icon: 'success',
       title: '¡Éxito!',
       text: 'Los cambios se han guardado correctamente.',
     }).then((result) => {
       if (result.isConfirmed) {
         window.location.reload()
       }else{
         Swal.fire({
           icon: 'error',
           title: 'Oops...',
           text: 'Algo salio mal',
         });
       }
     });
     form.reset();
   }
 })
 .catch(error => {
   Swal.fire({
     icon: 'error',
     title: 'Oops...',
     text: 'Algo salio mal',
   });
   form.reset();
 });
}


function saveCostHour(){
 // Obtén el formulario
 var form = document.getElementById("update-manera-cobro");

 // Crea un objeto FormData para recopilar los datos del formulario
 var formData = new FormData(form);

 // Realiza una solicitud HTTP utilizando fetch o XMLHttpRequest
 fetch('updateconsultorinformation', {
   method: 'POST',
   body: formData
 })
 .then(response => {
   if(response.status == 200){
     Swal.fire({
       icon: 'success',
       title: '¡Éxito!',
       text: 'Los cambios se han guardado correctamente.',
     }).then((result) => {
       if (result.isConfirmed) {
         window.location.reload()
       }else{
         Swal.fire({
           icon: 'error',
           title: 'Oops...',
           text: 'Algo salio mal',
         });
       }
       form.reset();
     });
     form.reset();
   }
 })
 .catch(error => {
   Swal.fire({
     icon: 'error',
     title: 'Oops...',
     text: 'Algo salio mal',
   });
   form.reset();
 });
}

document.getElementById("button-update-rfc").addEventListener("click", function(event) {
 event.preventDefault(); // Evita el comportamiento predeterminado del botón

 // Obtén el formulario
 var form = document.getElementById("update-rfc-honorarios");

 // Crea un objeto FormData para recopilar los datos del formulario
 var formData = new FormData(form);

 // Realiza una solicitud HTTP utilizando fetch o XMLHttpRequest
 fetch('updateconsultorinformation', {
   method: 'POST',
   body: formData
 })
 .then(response => {
   if(response.status == 200){
     Swal.fire({
       icon: 'success',
       title: '¡Éxito!',
       text: 'Los cambios se han guardado correctamente.',
     }).then((result) => {
       if (result.isConfirmed) {
         window.location.reload()
       }
     });
     form.reset();
   }else{
     Swal.fire({
       icon: 'error',
       title: 'Oops...',
       text: 'Algo salio mal',
     }); 
     form.reset(); 
   }
 })
 .catch(error => {
   Swal.fire({
     icon: 'error',
     title: 'Oops...',
     text: 'Algo salio mal',
   });
   form.reset();
 });
});


document.getElementById("button-update-contact").addEventListener("click", function(event) {
 event.preventDefault(); // Evita el comportamiento predeterminado del botón

 // Obtén el formulario
 var form = document.getElementById("update-contact-form");

 // Crea un objeto FormData para recopilar los datos del formulario
 var formData = new FormData(form);

 // Realiza una solicitud HTTP utilizando fetch o XMLHttpRequest
 fetch('updateprofileinformation', {
   method: 'POST',
   body: formData
 })
 .then(response => {
   if(response.status == 200){
     Swal.fire({
       icon: 'success',
       title: '¡Éxito!',
       text: 'Los cambios se han guardado correctamente.',
     }).then((result) => {
       if (result.isConfirmed) {
         window.location.reload()
       }
     });
     form.reset();
   }else if(response.status == 400){
     Swal.fire({
       icon: 'error',
       title: 'Oops...',
       text: 'El correo proporcionado ya esta en uso',
     });  
     form.reset();

   }
   else{
     Swal.fire({
       icon: 'error',
       title: 'Oops...',
       text: 'Algo salio mal',
     });  
     form.reset();
   }
   
 })
 .catch(error => {
   Swal.fire({
     icon: 'error',
     title: 'Oops...',
     text: 'Algo salio mal',
   });
   form.reset();
 });
});

document.getElementById("button-update-idiomas").addEventListener("click", function(event) {
 event.preventDefault(); // Evita el comportamiento predeterminado del botón

 // Obtén el formulario
 var form = document.getElementById("update-idiomas-form");

 // Crea un objeto FormData para recopilar los datos del formulario
 var formData = new FormData(form);

 // Realiza una solicitud HTTP utilizando fetch o XMLHttpRequest
 fetch('updateidiomaconsultor', {
   method: 'POST',
   body: formData
 })
 .then(response => {
   if(response.status == 200){
     Swal.fire({
       icon: 'success',
       title: '¡Éxito!',
       text: 'Los cambios se han guardado correctamente.',
     }).then((result) => {
       if (result.isConfirmed) {
         window.location.reload();
       }
     });
     form.reset();
   }else if(response.status == 400){
     Swal.fire({
       icon: 'error',
       title: 'Oops...',
       text: 'El correo proporcionado ya esta en uso',
     });  
     form.reset();

   }
   else{
     Swal.fire({
       icon: 'error',
       title: 'Oops...',
       text: 'Algo salio mal',
     });  
     form.reset();
   }
   
 })
 .catch(error => {
   Swal.fire({
     icon: 'error',
     title: 'Oops...',
     text: 'Algo salio mal',
   });
   form.reset();
 });
});


const tokenP = "pruebas";
const token = "";

function queryCP(cp) {
const selectEstado = document.getElementById("estado");
const selectColonia = document.getElementById("colonia");
//selectEstado.innerHTML = "";
selectColonia.innerHTML = "";
const url = `https://api.copomex.com/query/info_cp/${cp}?token=${tokenP}`;
axios
   .get(url)
   .then((response) => {
       if (response.status === 200) {
           // 200 significa que la solicitud fue exitosa
           const resultado = response.data; // Obtener los datos de la respuesta

           // Trabajar con los datos recibidos
           resultado.forEach((data) => {
               llenarSelect(data.response); // Agregar opciones al <select>
           });
       } else {
           console.log("Error en la solicitud:", response.status);
       }
   })
   .catch((error) => {
       console.log("Error en la solicitud:", error.message);
   });
}

function llenarSelect(data) {
const selectEstado = document.getElementById("estado");
const selectColonia = document.getElementById("colonia");
const selectCiudad = document.getElementById("ciudad");
const selectMunicipio = document.getElementById("municipio");

// Limpiar las opciones existentes
selectEstado.innerHTML = "";
selectCiudad.innerHTML = "";
selectMunicipio.innerHTML = "";
//selectCiudad.innerHTML = "";
console.log(data)
const opcion = document.createElement("option");
opcion.value = data.estado;
opcion.textContent = data.estado;
selectEstado.appendChild(opcion);

const opcion2 = document.createElement("option");
opcion2.value = data.asentamiento;
opcion2.textContent = data.asentamiento;
selectColonia.appendChild(opcion2);

const opcion3 = document.createElement("option");
opcion3.value = data.ciudad;
opcion3.textContent = data.ciudad;
selectCiudad.appendChild(opcion3);

const opcion4 = document.createElement("option");
opcion4.value = data.municipio;
opcion4.textContent = data.municipio;
selectMunicipio.appendChild(opcion4);

M.FormSelect.init(selectEstado);
M.FormSelect.init(selectColonia);
M.FormSelect.init(selectCiudad);
M.FormSelect.init(selectMunicipio);
}


var longPressTimer;

function startLongPress(element) {
longPressTimer = setTimeout(function() {
 console.log('Clic prolongado en:', element.id);
 elemento = element.id
 Swal.fire({
   title: '¿Estas seguro?',
   text: "Este idioma se borrara de tu experiencia",
   icon: 'warning',
   showCancelButton: true,
   confirmButtonColor: '#3085d6',
   cancelButtonColor: '#d33',
   confirmButtonText: 'Si, quiero borrarlo',
   cancelButtonText: 'Cancelar'
 }).then((result) => {
   if (result.isConfirmed) {
     var csrftoken = Cookies.get('csrftoken');
     fetch('deleteidiomaconsultor', {
       method: 'POST',
       headers: {
         'X-CSRFToken': csrftoken,
         'Content-Type': 'application/x-www-form-urlencoded'  // Agrega este encabezado
       },
       body:'elemento=' + encodeURIComponent(elemento)
     })
     .then(response => {
       if(response.status == 200){
         Swal.fire(
           'Eliminado',
           'El idioma se ha borrado de tu experiencia',
           'success'
         );
         setTimeout(() => {
           window.location.reload();
         }, 1000);
       }else{
         Swal.fire({
           icon: 'error',
           title: 'Oops...',
           text: 'Algo salio mal',
         });
       }
     })
     .catch(error => {
       Swal.fire({
         icon: 'error',
         title: 'Oops...',
         text: 'Algo salio mal',
       });
     });
   }
 });
}, 600);
}

function endLongPress() {
  clearTimeout(longPressTimer);
}
