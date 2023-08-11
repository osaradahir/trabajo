document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('select');
    var instances = M.FormSelect.init(elems, options);

    var dates = document.querySelectorAll('.datepicker');
    M.Datepicker.init(dates, {
        format: 'mmmm/yy',
        setDefaultDate: true,
        defaultDate: new Date(2000, 0, 1),
        autoClose: true,
        showClearBtn: true,
        firstDay: 1,
        minDate: new Date(1979, 1, 12),
        maxDate: new Date(2043, 1, 12),
    });

    var dropdowns = document.querySelectorAll('.dropdown-trigger');
    var dropdownOptions = {
        constrainWidth: false,
        coverTrigger: false
    };
    var dropdownInstances = M.Dropdown.init(dropdowns, dropdownOptions);

    var showButton = document.getElementById('showButton');
    var content = document.getElementById('content');

    showButton.addEventListener('click', function(){
        if (content.classList.contains('hidden-content')){
            content.classList.remove('hidden-content');
            showButton.textContent ="Ocultar";
        } else {
            content.classList.add('hidden-content');
            showButton.textContent = "Agregar Requerimiento";
        }
    });

    var mostrarBtn = document.getElementById("mostrarBtn");
    var ocultarBtn = document.getElementById("ocultarBtn");
    var contenidoOculto = document.getElementById("contenidoOculto");

    mostrarBtn.addEventListener("click", function() {
        contenidoOculto.style.display = "block";
    });

    ocultarBtn.addEventListener("click", function() {
        contenidoOculto.style.display = "none";
    });
});