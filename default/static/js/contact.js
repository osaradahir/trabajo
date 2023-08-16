const tokenP = "pruebas";
const token = "38bf9334-0cba-4550-a079-79ef3534413f";

function queryCP(cp) {
    const selectEstado = document.getElementById("estado");
    const selectColonia = document.getElementById("colonia");
    //selectEstado.innerHTML = "";
    selectColonia.innerHTML = "";
    const url = `https://api.copomex.com/query/info_cp/${cp}?token=${token}`;
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
