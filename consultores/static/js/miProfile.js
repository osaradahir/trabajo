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
const updateInformationExperience = document.querySelector(
  "#update-information-experience"
);

const cancelInformationExperience = document.querySelector(
  "#cancel-information-experience"
);
var anchoPantalla = window.innerWidth;
var alturaPantalla = window.innerHeight;
var widgetOn = false;
let barOn = false;
let viewExperiencias = 0;
let viewCurso = 0;
var previousWidth = window.innerWidth;
document.getElementById("ageFinish").value = "";
document.getElementById("ageInit").value = "";
const tokenP = "pruebas";
const token = "";
var longPressTimer;
var inicio = 0;
var final = 3;
openNav();
viewExperiencia(viewExperiencias);
viewCursos(viewCurso);
controlTableSAP(inicio, final);

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

function viewExperiencia(view) {
  console.log(view);
  var containerCursos = document.querySelectorAll(
    '[id^="container-data-experience-show-"]'
  );
  // Recorre los elementos encontrados
  for (var i = 0; i < containerCursos.length; i++) {
    var elemento = containerCursos[i];

    if (view >= containerCursos.length) {
      document.getElementById("experience-container-end").style.display =
        "block";
    }
    // Aplica el estilo "display: none" a todos los elementos excepto el primero
    if (i !== view) {
      elemento.style.display = "none";
    } else {
      elemento.style.display = "";
    }
  }
}


updateInformationExperience.addEventListener("click", function () {
  console.log("Hola")
  var currentContainer = document.getElementById(
    `container-data-experience-show-${viewExperiencias + 1}`
  );

  if(currentContainer != null){
    var currentContainer = document.getElementById(
      `container-data-experience-show-${viewExperiencias + 1}`
    );
    console.log(currentContainer);
    document.getElementById("puestoExperiencia").value =
      currentContainer.querySelector("#puesto").value;
    document.getElementById("puestoEmpresa").value =
      currentContainer.querySelector("#empresa").value;
    document.getElementById("experiencia-saber").value =
      currentContainer.querySelector("#experiencia-saber-show").value;

  }


  if (widgetOn == false) {
    var containerCursos = document.querySelectorAll(
      '[id^="container-data-experience-show-"]'
    );
    // Recorre los elementos encontrados
    for (var i = 0; i < containerCursos.length; i++) {
      var elemento = containerCursos[i];
      elemento.style.display = "none";
    }
    if(currentContainer == null){
      try {
        document.getElementById("experience-container").style.display = "none";
      } catch (error) {
        document.getElementById('experience-container-end').style.display = "none";
        console.error("Ha ocurrido un error al ocultar el elemento:", error);
      }      
    }
    document.getElementById("button-experience").style.display = "none";
    document.getElementById("container-data-experience").style.display = "";
    document.getElementById("button-experience-update").style.display = "";
  }
  widgetOn = true;
});

cancelInformationExperience.addEventListener("click", function () {
  document.getElementById("form-update-experiencia").reset();
  viewExperiencia(viewExperiencias);
  document.getElementById("button-experience").style.display = "";
  document.getElementById("container-data-experience").style.display = "none";
  document.getElementById("button-experience-update").style.display = "none";
  widgetOn = false;
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


function viewCursos(view) {
  console.log(view);
  var containerCursos = document.querySelectorAll('[id^="container-curso-"]');
  // Recorre los elementos encontrados
  for (var i = 0; i < containerCursos.length; i++) {
    var elemento = containerCursos[i];

    if (view >= containerCursos.length) {
      document.getElementById("curso-container-end").style.display = "block";
    }
    // Aplica el estilo "display: none" a todos los elementos excepto el primero
    if (i !== view) {
      elemento.style.display = "none";
    } else {
      elemento.style.display = "";
    }
  }
}

coursesEditButton.addEventListener("click", function () {
  var currentContainer = document.getElementById(
    `container-curso-${viewCurso + 1}`
  );

  if(currentContainer != null){
      var titleNode = currentContainer.querySelector("#title-courses");
    console.log(titleNode);
    document.getElementById("instituteCertificate").value =
      titleNode.childNodes[0].textContent.trim();
    document.getElementById("nameCertificate").value =
      currentContainer.querySelector("#content-courses").textContent;
    document.getElementById("id_certificadoQuery").value =
      currentContainer.querySelector("#id_certificado").value;
  }

  if (widgetOn == false) {
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
  document.getElementById("update-certifcado-cursos").reset();

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
  try {
    document.getElementById("education-saber").value = document.getElementById(
      "educacion-saber-show"
    ).value;
  } catch (error) {
    // Manejar el error aquí
    console.error(error);
  }
  
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
  document.getElementById("form-update-educacion").reset();
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

function comprobar(obj) {
  if (obj.checked) {
    document.getElementById("ageFinish").value = "";
    document.getElementById("ageFinish").style.display = "none";
    document.getElementById("span-study").style.display = "none";
  } else {
    document.getElementById("span-study").style.display = "";
    document.getElementById("ageFinish").value = "";
    document.getElementById("ageFinish").style.display = "";
  }
}


function handleFileSelected(event, kindFile) {
  console.log(kindFile);
  const file = event.target.files[0];
  const rfcValue = document.getElementById("data_rfc").value;
  // Verificar que se haya seleccionado un archivo
  if (file) {
    // Crear una instancia de FormData
    const formData = new FormData();
    formData.append("file", file);
    formData.append("name", kindFile);
    formData.append("rfc", rfcValue);

    // Obtener el token CSRF del formulario
    const csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0]
      .value;
    formData.append("csrfmiddlewaretoken", csrfToken);

    // Realizar la solicitud POST usando fetch
    fetch("upload", {
      method: "POST",
      body: formData,
      headers: {
        "X-CSRFToken": csrfToken,
      },
    })
      .then((response) => {
        const body = document.querySelector("body");
        Swal.fire({
          icon: "success",
          title: "Archivo subido",
          text: "El archivo se envio correctamente",
        }).then((result) => {
          if (result.isConfirmed) {
            window.location.reload();
          }
        });
      })
      .catch((error) => {
        Swal.fire({
          icon: "error",
          title: "Oops...",
          text: "Algo salio mal",
        });
      });
  }
}

async function imageChange(){
  const { value: file } = await Swal.fire({
    title: 'Select image',
    input: 'file',
    inputAttributes: {
      'accept': 'image/*',
      'aria-label': 'Upload your profile picture'
    }
  })
  
  if (file) {
    const reader = new FileReader()
    reader.onload = async (e) => {
      const imageData = e.target.result
      const formData = new FormData()
      formData.append('imagen', file)
      // Obtener el token CSRF del formulario
      const csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0]
      .value;
      formData.append("csrfmiddlewaretoken", csrfToken);
      try {
        const response = await fetch('uploadImage', {
          method: 'POST',
          body: formData,
          headers: {
            "X-CSRFToken": csrfToken,
          },
        })

        if (response.ok) {
          Swal.fire('Listo', 'La imagen se subio correctamente', 'success')
          // Recargar la página después de 3 segundos

        } else {
          Swal.fire('Error', 'Ocurrio un error al subir la imagen', 'error')
        }
        setTimeout(function() {
          location.reload(); // Recargar la página actual
        }, 1000);
      } catch (error) {
        Swal.fire('Error', 'Ocurrio un error al subir la imagen', 'error')
      }
    }
    reader.readAsDataURL(file)
  }
}




document.addEventListener("DOMContentLoaded", function () {
  var dates = document.querySelectorAll("#ageFinish");
  M.Datepicker.init(dates, {
    format: "yyyy-mm-dd",
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
    },
    onClose: function () {
      setTimeout(function () {
        let fechaEntrada = document.getElementById("ageInit").value;
        let fechaSalida = document.getElementById("ageFinish").value;
        var fechaNacInput = document.getElementById("fecha-nacimiento").value;
        console.log(fechaNacInput);
        var dateEntrada = new Date(fechaEntrada);
        var dateSalida = new Date(fechaSalida);
        var fechaHoy = new Date(); // Crear un objeto Date con la fecha y hora actuales
        var fechaNac = moment(fechaNacInput, "MMM. DD, YYYY, h:mm a");
        var fechaDate = fechaNac.toDate();
        fechaDate.setFullYear(fechaDate.getFullYear() + 18);
        console.log(fechaDate);

        if (dateSalida <= fechaDate) {
          document.getElementById("ageFinish").value = "";
          Swal.fire(
            "La fecha de salida no debe ser menor que tu edad minima requerida"
          );
        }

        if (dateSalida == dateEntrada) {
          document.getElementById("ageFinish").value = "";
          Swal.fire("La fecha de entrada no debe ser igual que la de salida");
        }

        if (dateSalida >= fechaHoy) {
          document.getElementById("ageFinish").value = "";
          Swal.fire("La fecha de salida no debe ser mayor a la fecha actual");
        }
        if (dateSalida <= dateEntrada) {
          document.getElementById("ageFinish").value = "";
          Swal.fire(
            "La fecha de salida no debe ser menor a la fecha de entrada"
          );
        }

        console.log(fechaHoy);
      }, 1000);
    },
  });
});

document.addEventListener("DOMContentLoaded", function () {
  var fechaSalidaInput = document.getElementById("ageInit");
  M.Datepicker.init(fechaSalidaInput, {
    format: "yyyy-mm-dd",
    autoClose: true,
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
    },
    onClose: function () {
      setTimeout(function () {
        let fechaEntrada = document.getElementById("ageInit").value;
        let fechaSalida = document.getElementById("ageFinish").value;
        var fechaNacInput = document.getElementById("fecha-nacimiento").value;
        console.log(fechaNacInput);

        var dateEntrada = new Date(fechaEntrada);
        var dateSalida = new Date(fechaSalida);
        var fechaHoy = new Date(); // Crear un objeto Date con la fecha y hora actuales
        var fechaNac = moment(fechaNacInput, "MMM. DD, YYYY, h:mm a");
        var fechaDate = fechaNac.toDate();
        fechaDate.setFullYear(fechaDate.getFullYear() + 18);
        console.log(fechaDate);

        if (dateEntrada <= fechaDate) {
          document.getElementById("ageInit").value = "";
          Swal.fire(
            "La fecha de entrada no debe ser menor que tu edad minima requerida"
          );
        }
        if (dateEntrada >= fechaHoy) {
          document.getElementById("ageInit").value = "";
          console.log(document.getElementById("ageInit").value);
          Swal.fire("La fecha de entrada no debe ser mayor a la fecha actual");
        }
        if (dateEntrada == dateSalida) {
          document.getElementById("ageFinish").value = "";
          Swal.fire("La fecha de entrada no debe igual que la de salida");
        }
        if (dateEntrada >= dateSalida) {
          document.getElementById("ageInit").value = "";
          Swal.fire("La fecha de salida no debe ser mayor que la de entrada");
        }

        console.log(fechaHoy);
      }, 1000);
    },
  });
});

document
  .getElementById("button-information-user-profile")
  .addEventListener("click", function (event) {
    event.preventDefault(); // Evita el comportamiento predeterminado del botón

    // Obtén el formulario
    var form = document.getElementById("update-information-personal");

    // Validar los campos utilizando los patrones
    var inputs = form.querySelectorAll("input[pattern]");
    var valid = true;

    inputs.forEach(function (input) {
      var pattern = new RegExp(input.getAttribute("pattern"));
      var value = input.value;
      
      if (!pattern.test(value)) {
        valid = false;
        // Realiza acciones en caso de que no cumpla con el patrón, como mostrar un mensaje de error
        Swal.fire({
          icon: 'error',
          title: 'Oops...',
          text: 'Constesta los formularios adecuadamente!',
        })
      }
    });

    if (!valid) {
      Swal.fire({
        icon: 'error',
        title: 'Oops...',
        text: 'Constesta los formularios adecuadamente!',
      })
      return;
    }
    // Crea un objeto FormData para recopilar los datos del formulario
    var formData = new FormData(form);

    // Realiza una solicitud HTTP utilizando fetch o XMLHttpRequest
    fetch("updateprofileinformation", {
      method: "POST",
      body: formData,
    })
      .then((response) => {
        if (response.status == 200) {
          Swal.fire({
            icon: "success",
            title: "¡Éxito!",
            text: "Los cambios se han guardado correctamente.",
          }).then((result) => {
            if (result.isConfirmed) {
              window.location.reload();
            }
          });
          form.reset();
        } else {
          Swal.fire({
            icon: "error",
            title: "Oops...",
            text: "Algo salio mal",
          });
        }
      })
      .catch((error) => {
        Swal.fire({
          icon: "error",
          title: "Oops...",
          text: "Algo salio mal",
        });
        form.reset();
      });
  });

function updateEducacion(event) {
  event.preventDefault();
  // Obtén el formulario
  var form = document.getElementById("form-update-educacion");
    // Validar los campos utilizando los patrones
    var inputs = form.querySelectorAll("input[pattern]");
    var valid = true;
  
    inputs.forEach(function (input) {
      var pattern = new RegExp(input.getAttribute("pattern"));
      var value = input.value;
        
      if (!pattern.test(value)) {
        valid = false;
        Swal.fire({
          icon: 'error',
          title: 'Oops...',
          text: 'Constesta los formularios adecuadamente!',
        })
      }
     });
  
    if (!valid) {
      Swal.fire({
        icon: 'error',
        title: 'Oops...',
        text: 'Constesta los formularios adecuadamente!',
      })
      return;
    }
  // Crea un objeto FormData para recopilar los datos del formulario
  var formData = new FormData(form);

  // Realiza una solicitud HTTP utilizando fetch o XMLHttpRequest
  fetch("updateeducacion", {
    method: "POST",
    body: formData,
  })
    .then((response) => {
      if (response.status == 200) {
        Swal.fire({
          icon: "success",
          title: "¡Éxito!",
          text: "Los cambios se han guardado correctamente.",
        }).then((result) => {
          if (result.isConfirmed) {
            window.location.reload();
          }
        });
        form.reset();
      } else {
        Swal.fire({
          icon: "error",
          title: "Oops...",
          text: "Algo salio mal",
        });
      }
    })
    .catch((error) => {
      Swal.fire({
        icon: "error",
        title: "Oops...",
        text: "Algo salio mal",
      });
      form.reset();
    });
}

function updateExperiencia() {
  // Obtén el formulario
  var form = document.getElementById("form-update-experiencia");


  // Validar los campos utilizando los patrones
  var inputs = form.querySelectorAll("input[pattern]");
  var valid = true;

  inputs.forEach(function (input) {
    var pattern = new RegExp(input.getAttribute("pattern"));
    var value = input.value;
      
    if (!pattern.test(value)) {
      valid = false;
      Swal.fire({
        icon: 'error',
        title: 'Oops...',
        text: 'Constesta los formularios adecuadamente!',
      })
    }
   });

  if (!valid) {
    Swal.fire({
      icon: 'error',
      title: 'Oops...',
      text: 'Constesta los formularios adecuadamente!',
    })
    return;
  }

  // Crea un objeto FormData para recopilar los datos del formulario
  var formData = new FormData(form);

  // Realiza una solicitud HTTP utilizando fetch o XMLHttpRequest
  fetch("updateexperiencia", {
    method: "POST",
    body: formData,
  })
    .then((response) => {
      if (response.status == 200) {
        Swal.fire({
          icon: "success",
          title: "¡Éxito!",
          text: "Los cambios se han guardado correctamente.",
        }).then((result) => {
          if (result.isConfirmed) {
            window.location.reload();
          }
        });
        form.reset();
      } else {
        Swal.fire({
          icon: "error",
          title: "Oops...",
          text: "Algo salio mal",
        });
      }
    })
    .catch((error) => {
      Swal.fire({
        icon: "error",
        title: "Oops...",
        text: "Algo salio mal",
      });
      form.reset();
    });
}

function saveKindMoney() {
  // Obtén el formulario
  var form = document.getElementById("update-moneda-cobro");

  // Crea un objeto FormData para recopilar los datos del formulario
  var formData = new FormData(form);

  // Realiza una solicitud HTTP utilizando fetch o XMLHttpRequest
  fetch("updateconsultorinformation", {
    method: "POST",
    body: formData,
  })
    .then((response) => {
      if (response.status == 200) {
        Swal.fire({
          icon: "success",
          title: "¡Éxito!",
          text: "Los cambios se han guardado correctamente.",
        }).then((result) => {
          if (result.isConfirmed) {
            window.location.reload();
          }
        });
        form.reset();
      } else {
        Swal.fire({
          icon: "error",
          title: "Oops...",
          text: "Algo salio mal",
        });
      }
    })
    .catch((error) => {
      Swal.fire({
        icon: "error",
        title: "Oops...",
        text: "Algo salio mal",
      });
      form.reset();
    });
}

function saveCostHour() {
  console.log('Hola');
  // Obtén el formulario
  var form = document.getElementById("update-manera-cobro");

  var hora = document.getElementById('updateHora').value;
  var valorNumerico = parseFloat(hora);

  if(valorNumerico<=0){
    return 0;
  }

  
  var formData = new FormData(form);
  // Realiza una solicitud HTTP utilizando fetch o XMLHttpRequest
  fetch("updateconsultorinformation", {
    method: "POST",
    body: formData,
  })
    .then((response) => {
      if (response.status == 200) {
        Swal.fire({
          icon: "success",
          title: "¡Éxito!",
          text: "Los cambios se han guardado correctamente.",
        }).then((result) => {
          if (result.isConfirmed) {
            window.location.reload();
          }
        });
        form.reset();
      } else {
        Swal.fire({
          icon: "error",
          title: "Oops...",
          text: "Algo salio mal",
        });
      }
    })
    .catch((error) => {
      Swal.fire({
        icon: "error",
        title: "Oops...",
        text: "Algo salio mal",
      });
      form.reset();
    });
}

document
  .getElementById("button-update-rfc")
  .addEventListener("click", function (event) {
    event.preventDefault(); // Evita el comportamiento predeterminado del botón

    // Obtén el formulario
    var form = document.getElementById("update-rfc-honorarios");
    var rfcInput = form.querySelector("input[name='RFC']");
    var rfcValue = rfcInput.value;
    var rfcPattern = /^[A-Z,Ñ&]{3,4}[0-9]{2}[0-1][0-9][0-3][0-9][A-Z,0-9]?[A-Z,0-9]?[0-9,A-Z]?$/;

    if (rfcPattern.test(rfcValue)) {
      // El RFC es válido según el patrón
      console.log("RFC válido");
    
    } else {
      Swal.fire({
        icon: 'error',
        title: 'Oops...',
        text: 'Tu RFC no tiene el formato correcto',
      })
      return;
    }

    // Crea un objeto FormData para recopilar los datos del formulario
    var formData = new FormData(form);

    Swal.fire({
      title: '¿Quieres cambiar tu RFC?',
      text: 'Tu documentacion tambien se borrara',
      showDenyButton: true,
      confirmButtonText: 'Aceptar',
      denyButtonText: `Cancelar`,
    }).then((result) => {
      /* Read more about isConfirmed, isDenied below */
      if (result.isConfirmed) {
        // Realiza una solicitud HTTP utilizando fetch o XMLHttpRequest
        fetch("updateconsultorinformation", {
          method: "POST",
          body: formData,
        })
          .then((response) => {
            if (response.status == 200) {
              Swal.fire({
                icon: "success",
                title: "¡Éxito!",
                text: "Los cambios se han guardado correctamente.",
              }).then((result) => {
                if (result.isConfirmed) {
                  window.location.reload();
                }
              });
              form.reset();
            } else {
              Swal.fire({
                icon: "error",
                title: "Oops...",
                text: "Algo salio mal",
              });
              form.reset();
            }
          })
          .catch((error) => {
            Swal.fire({
              icon: "error",
              title: "Oops...",
              text: "Algo salio mal",
            });
            form.reset();
          });
      } else if (result.isDenied) {
        Swal.fire('No ocurrio ningun cambio', '', 'info')
      }
    })
  });

document
  .getElementById("button-update-contact")
  .addEventListener("click", function (event) {
    event.preventDefault(); // Evita el comportamiento predeterminado del botón

    // Obtén el formulario
    var form = document.getElementById("update-contact-form");
    // Validar los campos utilizando los patrones
    var inputs = form.querySelectorAll("input[pattern]");
    var valid = true;

    inputs.forEach(function (input) {
      var pattern = new RegExp(input.getAttribute("pattern"));
      var value = input.value;
      
      if (!pattern.test(value)) {
        valid = false;
        // Realiza acciones en caso de que no cumpla con el patrón, como mostrar un mensaje de error
        Swal.fire({
          icon: 'error',
          title: 'Oops...',
          text: 'Constesta los formularios adecuadamente!',
        })
      }
    });

    if (!valid) {
      Swal.fire({
        icon: 'error',
        title: 'Oops...',
        text: 'Constesta los formularios adecuadamente!',
      })
      return;
    }
    // Crea un objeto FormData para recopilar los datos del formulario
    var formData = new FormData(form);

    // Realiza una solicitud HTTP utilizando fetch o XMLHttpRequest
    fetch(`updateprofileinformation`, {
      method: "POST",
      body: formData,
    })
      .then((response) => {
        if (response.status == 200) {
          Swal.fire({
            icon: "success",
            title: "¡Éxito!",
            text: "Los cambios se han guardado correctamente.",
          }).then((result) => {
            if (result.isConfirmed) {
              window.location.reload();
            }
          });
          form.reset();
        } else if (response.status == 400) {
          Swal.fire({
            icon: "error",
            title: "Oops...",
            text: "El correo proporcionado ya esta en uso",
          });
          form.reset();
        } else {
          Swal.fire({
            icon: "error",
            title: "Oops...",
            text: "Algo salio mal",
          });
          form.reset();
        }
      })
      .catch((error) => {
        Swal.fire({
          icon: "error",
          title: "Oops...",
          text: "Algo salio mal",
        });
        form.reset();
      });
  });

document
  .getElementById("button-update-idiomas")
  .addEventListener("click", function (event) {
    event.preventDefault(); // Evita el comportamiento predeterminado del botón

    // Obtén el formulario
    var form = document.getElementById("update-idiomas-form");

    // Crea un objeto FormData para recopilar los datos del formulario
    var formData = new FormData(form);

    // Realiza una solicitud HTTP utilizando fetch o XMLHttpRequest
    fetch("updateidiomaconsultor", {
      method: "POST",
      body: formData,
    })
      .then((response) => {
        if (response.status == 200) {
          Swal.fire({
            icon: "success",
            title: "¡Éxito!",
            text: "Los cambios se han guardado correctamente.",
          }).then((result) => {
            if (result.isConfirmed) {
              window.location.reload();
            }
          });
          form.reset();
        } else if (response.status == 400) {
          Swal.fire({
            icon: "error",
            title: "Oops...",
            text: "El correo proporcionado ya esta en uso",
          });
          form.reset();
        } else {
          Swal.fire({
            icon: "error",
            title: "Oops...",
            text: "Algo salio mal",
          });
          form.reset();
        }
      })
      .catch((error) => {
        Swal.fire({
          icon: "error",
          title: "Oops...",
          text: "Algo salio mal",
        });
        form.reset();
      });
  });

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
  console.log(data);
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


function startLongPress(element) {
  longPressTimer = setTimeout(function () {
    console.log("Clic prolongado en:", element.id);
    elemento = element.id;
    Swal.fire({
      title: "¿Estas seguro?",
      text: "Este idioma se borrara de tu experiencia",
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#3085d6",
      cancelButtonColor: "#d33",
      confirmButtonText: "Si, quiero borrarlo",
      cancelButtonText: "Cancelar",
    }).then((result) => {
      if (result.isConfirmed) {
        var csrftoken = Cookies.get("csrftoken");
        fetch("deleteidiomaconsultor", {
          method: "POST",
          headers: {
            "X-CSRFToken": csrftoken,
            "Content-Type": "application/x-www-form-urlencoded", // Agrega este encabezado
          },
          body: "elemento=" + encodeURIComponent(elemento),
        })
          .then((response) => {
            if (response.status == 200) {
              Swal.fire(
                "Eliminado",
                "El idioma se ha borrado de tu experiencia",
                "success"
              );
              setTimeout(() => {
                window.location.reload();
              }, 1000);
            } else {
              Swal.fire({
                icon: "error",
                title: "Oops...",
                text: "Algo salio mal",
              });
            }
          })
          .catch((error) => {
            Swal.fire({
              icon: "error",
              title: "Oops...",
              text: "Algo salio mal",
            });
          });
      }
    });
  }, 600);
}

function endLongPress() {
  clearTimeout(longPressTimer);
}

document.addEventListener("DOMContentLoaded", function () {
  var dates = document.querySelectorAll("#ageFinish2");
  M.Datepicker.init(dates, {
    format: "yyyy-mm-dd",
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
    },
    onClose: function () {
      setTimeout(function () {
        let fechaEntrada = document.getElementById("ageInit2").value;
        let fechaSalida = document.getElementById("ageFinish2").value;
        var fechaNacInput = document.getElementById("fecha-nacimiento").value;
        console.log(fechaNacInput);
        var dateEntrada = new Date(fechaEntrada);
        var dateSalida = new Date(fechaSalida);
        var fechaHoy = new Date(); // Crear un objeto Date con la fecha y hora actuales
        var fechaNac = moment(fechaNacInput, "MMM. DD, YYYY, h:mm a");
        var fechaDate = fechaNac.toDate();
        fechaDate.setFullYear(fechaDate.getFullYear() + 18);
        console.log(fechaDate);

        if (dateSalida <= fechaDate) {
          document.getElementById("ageFinish").value = "";
          Swal.fire(
            "La fecha de salida no debe ser menor que tu edad minima requerida"
          );
        }

        if (dateSalida == dateEntrada) {
          document.getElementById("ageFinish").value = "";
          Swal.fire("La fecha de entrada no debe ser igual que la de salida");
        }

        if (dateSalida >= fechaHoy) {
          document.getElementById("ageFinish").value = "";
          Swal.fire("La fecha de salida no debe ser mayor a la fecha actual");
        }
        if (dateSalida <= dateEntrada) {
          document.getElementById("ageFinish").value = "";
          Swal.fire(
            "La fecha de salida no debe ser menor a la fecha de entrada"
          );
        }

        console.log(fechaHoy);
      }, 1000);
    },
  });
});

document.addEventListener("DOMContentLoaded", function () {
  var fechaSalidaInput = document.getElementById("ageInit2");
  M.Datepicker.init(fechaSalidaInput, {
    format: "yyyy-mm-dd",
    autoClose: true,
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
    },
    onClose: function () {
      setTimeout(function () {
        let fechaEntrada = document.getElementById("ageInit2").value;
        let fechaSalida = document.getElementById("ageFinish2").value;
        var fechaNacInput = document.getElementById("fecha-nacimiento").value;
        console.log(fechaNacInput);

        var dateEntrada = new Date(fechaEntrada);
        var dateSalida = new Date(fechaSalida);
        var fechaHoy = new Date(); // Crear un objeto Date con la fecha y hora actuales
        var fechaNac = moment(fechaNacInput, "MMM. DD, YYYY, h:mm a");
        var fechaDate = fechaNac.toDate();
        fechaDate.setFullYear(fechaDate.getFullYear() + 18);
        console.log(fechaDate);

        if (dateEntrada <= fechaDate) {
          document.getElementById("ageInit").value = "";
          Swal.fire(
            "La fecha de entrada no debe ser menor que tu edad minima requerida"
          );
        }
        if (dateEntrada >= fechaHoy) {
          document.getElementById("ageInit").value = "";
          console.log(document.getElementById("ageInit").value);
          Swal.fire("La fecha de entrada no debe ser mayor a la fecha actual");
        }
        if (dateEntrada == dateSalida) {
          document.getElementById("ageFinish").value = "";
          Swal.fire("La fecha de entrada no debe igual que la de salida");
        }
        if (dateEntrada >= dateSalida) {
          document.getElementById("ageInit").value = "";
          Swal.fire("La fecha de salida no debe ser mayor que la de entrada");
        }

        console.log(fechaHoy);
      }, 1000);
    },
  });
});



function controlTableSAP(inicio, final) {
  var tablaResultados = document.getElementById('tablaResultados');
  var filas = tablaResultados.querySelectorAll('tr');
  var contador = 0;
  var inicioFilas = inicio; // Límite de filas a mostrar
  var limiteFilas = final; // Límite de filas a mostrar
  
  for (var fila of filas) {
    var id = fila.getAttribute('id');
    var idDeseado = 'sap-form-show-';

    if (fila.id.startsWith(idDeseado)) {
      contador++;
      
      if (contador < inicioFilas || contador > limiteFilas) {
        fila.style.display = 'none';
      } else {
        fila.style.display = 'table-row';
      }
    }
  }
}


document.getElementById('less').addEventListener('click', function(e) {
  e.preventDefault();
  inicio -= 3;
  final -= 2;
  controlTableSAP(inicio, final);
  console.log('less');
  console.log(inicio);
  console.log(final);
});

document.getElementById('more').addEventListener('click', function(e) {
  e.preventDefault();
  inicio += 3;
  final += 2;
  controlTableSAP(inicio, final);
  console.log('more');
  console.log(inicio);
  console.log(final);
});


function updateCertificados(e){
  e.preventDefault();
  // Obtén el formulario
  var form = document.getElementById("update-certifcado-cursos");
  // Validar los campos utilizando los patrones
  var inputs = form.querySelectorAll("input[pattern]");
  var valid = true;

  inputs.forEach(function (input) {
    var pattern = new RegExp(input.getAttribute("pattern"));
    var value = input.value;
      
    if (!pattern.test(value)) {
      valid = false;
      console.log(input.name);
      Swal.fire({
        icon: 'error',
        title: 'Oops...',
        text: 'Constesta los formularios adecuadamente!',
      })
    }
   });

  if (!valid) {
    Swal.fire({
      icon: 'error',
      title: 'Oops...',
      text: 'Constesta los formularios adecuadamente!',
    })
    return;
  } 
  // Crea un objeto FormData para recopilar los datos del formulario
  var formData = new FormData(form);
 
  // Realiza una solicitud HTTP utilizando fetch o XMLHttpRequest
  fetch('updatecertificados', {
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


function addModuleSAP(){
  // Obtén el formulario
  var form = document.getElementById("sap-form-content");
 
  // Crea un objeto FormData para recopilar los datos del formulario
  var formData = new FormData(form);
 
  // Realiza una solicitud HTTP utilizando fetch o XMLHttpRequest
  fetch('updateModulosSAP', {
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

function sendModuleSAP(event,id){
  event.preventDefault();
  var separado = id.split("-");
  // Obtén el formulario
  
  var form = document.getElementById(`sap-form-${separado[1]}`);
  console.log(`sap-form-${separado[1]}`)
  // Crea un objeto FormData para recopilar los datos del formulario
  var formData = new FormData(form);

  var valorCampo1 = formData.get('modulo');
  var valorCampo2 = formData.get('submodulo');
  var valorCampo3 = formData.get('nivel');
  console.log(valorCampo1)
  if (valorCampo1 === null || valorCampo2 === null || valorCampo3 === null) {
    Swal.fire('Debes llenar todos los campos');
  } else {
    // Realiza una solicitud HTTP utilizando fetch o XMLHttpRequest
    fetch('updateModulosSAP', {
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
}