const btnToggle = document.querySelector(".logo");
const mainContainer = document.querySelector(".container-poyectos");
var widgetOn = false;
let barOn = false;

btnToggle.addEventListener("click", function openNav() {
  console.log("clik");
  if (barOn == false) {
    document.getElementById("sidebar").classList.toggle("active");
    // console.log(document.getElementById('sidebar'));
    console.log("Abierto");
    mainContainer.style.width = "90%";
    mainContainer.style.marginLeft = "10%";
    barOn = true;
  } else {
    console.log("cerrado");
    //btnToggle.classList.remove('activate');
    document.getElementById("sidebar").classList.remove("active");
    barOn = false;
    mainContainer.style.width = "100%";
    mainContainer.style.marginLeft = "0%";
  }
});


function openNav() {
  console.log("clik");
  if (barOn == false) {
    document.getElementById("sidebar").classList.toggle("active");
    // console.log(document.getElementById('sidebar'));
    console.log("Abierto");
    mainContainer.style.width = "90%";
    mainContainer.style.marginLeft = "10%";
    barOn = true;
  } else {
    console.log("cerrado");
    //btnToggle.classList.remove('activate');
    document.getElementById("sidebar").classList.remove("active");
    barOn = false;
    mainContainer.style.width = "100%";
    mainContainer.style.marginLeft = "0%";
  }
}
openNav();


document.addEventListener("DOMContentLoaded", function () {
  var fechaSalidaInput = document.getElementById("date_start");
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
        let fechaEntrada = document.getElementById("date_start").value;
        let fechaSalida = document.getElementById("date-end").value;
        //var fechaNacInput = document.getElementById("fecha-nacimiento").value;
        // console.log(fechaNacInput);

        var dateEntrada = new Date(fechaEntrada);
        var dateSalida = new Date(fechaSalida);
        var fechaHoy = new Date(); // Crear un objeto Date con la fecha y hora actuales
        //var fechaNac = moment(fechaNacInput, "MMM. DD, YYYY, h:mm a");
        //var fechaDate = fechaNac.toDate();
        //fechaDate.setFullYear(fechaDate.getFullYear() + 18);
        //console.log(fechaDate);

        /*if (dateEntrada <= fechaDate) {
          document.getElementById("ageInit").value = "";
          Swal.fire(
            "La fecha de entrada no debe ser menor que tu edad minima requerida"
          );
        }*/

        if (dateEntrada == dateSalida) {
          document.getElementById("date-end").value = "";
          Swal.fire("La fecha de entrada no debe igual que la de salida");
        }
        if (dateEntrada >= dateSalida) {
          document.getElementById("date_start").value = "";
          Swal.fire("La fecha de salida no debe ser menor que la de entrada");
        }

        console.log(fechaHoy);
      }, 1000);
    },
  });
});


document.addEventListener("DOMContentLoaded", function () {
  var fechaSalidaInput = document.getElementById("date-end");
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
        let fechaEntrada = document.getElementById("date_start").value;
        let fechaSalida = document.getElementById("date-end").value;
        //var fechaNacInput = document.getElementById("fecha-nacimiento").value;
        // console.log(fechaNacInput);

        var dateEntrada = new Date(fechaEntrada);
        var dateSalida = new Date(fechaSalida);
        var fechaHoy = new Date(); // Crear un objeto Date con la fecha y hora actuales
        //var fechaNac = moment(fechaNacInput, "MMM. DD, YYYY, h:mm a");
        //var fechaDate = fechaNac.toDate();
        //fechaDate.setFullYear(fechaDate.getFullYear() + 18);
        //console.log(fechaDate);

        /*if (dateEntrada <= fechaDate) {
          document.getElementById("ageInit").value = "";
          Swal.fire(
            "La fecha de entrada no debe ser menor que tu edad minima requerida"
          );
        }*/
        if (dateEntrada == dateSalida) {
          document.getElementById("date-end").value = "";
          Swal.fire("La fecha de entrada no debe igual que la de salida");
        }
        if (dateEntrada >= dateSalida) {
          document.getElementById("date_start").value = "";
          Swal.fire("La fecha de salida no debe ser menor que la de entrada");
        }

        console.log(fechaHoy);
      }, 1000);
    },
  });
});