function mostrarInfo(info) {
    $("#info").html(info);
    $("#info").fadeIn();
}

function ocultarInfo() {
    $("#info").fadeOut();
}

$(document).ready(function() {
    $(".imagen").hover(
        function() {
            var info = $(this).data("info");
            mostrarInfo(info);
        },
        function() {
            ocultarInfo();
        }
    );
});

        // Función para cambiar el estado de los cuadrados al hacer clic
        function toggleCheckbox(id) {
            const checkbox = document.getElementById(id);
            checkbox.classList.toggle("checked");
        }

        document.getElementById("SensorTemperatura").addEventListener("click", function() {
            toggleCheckbox("SensorTemperatura");
        });

        document.getElementById("SensorHumedad").addEventListener("click", function() {
            toggleCheckbox("SensorHumedad");
        });

        document.getElementById("SensorSonido").addEventListener("click", function() {
            toggleCheckbox("SensorSonido");
        });

        document.getElementById("SensorLuz").addEventListener("click", function() {
            toggleCheckbox("SensorLuz");
        });

        document.getElementById("SensorMovimiento").addEventListener("click", function() {
            toggleCheckbox("SensorMovimiento");
        });

        function verEnGoogleMaps() {
            var localizacion = document.getElementById("localizacion").value;

            localizacion = localizacion.replace(/º/g, '+');
            localizacion = localizacion.replace(/'/g, '+');
            localizacion = localizacion.replace(/"/g, '')
            localizacion = localizacion.replace(/N/g, '+');
            localizacion = localizacion.replace(/S/g, '-');
            localizacion = localizacion.replace(/E/g, '+');
            localizacion = localizacion.replace(/O/g, '-');

            // Genera el enlace a Google Maps
            var enlace = "https://maps.google.com/maps?q=" + localizacion;
            window.open(enlace);
        }

        // Función para actualizar el valor de la barra en tiempo real
        function updateRangeValue(inputId, targetId) {
            var range = document.getElementById(inputId);
            var target = document.querySelector('[data-range-target="' + targetId + '"]');
            
            range.addEventListener('input', function () {
                target.textContent = range.value + '°C';
            });
        }
    
        updateRangeValue('minTemp', 'minTemp');
        updateRangeValue('maxTemp', 'maxTemp');

        function actualizarTemperaturaMedia() {
            var minTempRange = document.getElementById("minTemp");
            var maxTempRange = document.getElementById("maxTemp");
            var temperaturaMediaSpan = document.getElementById("temperaturaMedia");

            var minTempValue = parseFloat(minTempRange.value);
            var maxTempValue = parseFloat(maxTempRange.value);

            var temperaturaMedia = (minTempValue + maxTempValue) / 2;

            temperaturaMediaSpan.innerHTML = temperaturaMedia.toFixed(2) + "°C";

            if (temperaturaMedia < 20 || temperaturaMedia > 26) {
                temperaturaMediaSpan.style.color = "red";
                //alert("La temperatura media está fuera del rango (20-26°C).");
            } else {
                temperaturaMediaSpan.style.color = "green";
            }

        }

        // Agregar un detector de eventos a los elementos de rango
        document.getElementById("minTemp").addEventListener("input", actualizarTemperaturaMedia);
        document.getElementById("maxTemp").addEventListener("input", actualizarTemperaturaMedia)

        var Paises = ["Alemania","Argentina","Australia","Austria","Bélgica","Brasil","Canadá","China","Dinamarca","Egipto","España","Estados Unidos","Finlandia","Francia","Grecia","India","Irlanda","Italia","Japón","México","Noruega","Países Bajos","Polonia","Portugal","Reino Unido","Rusia","Sudáfrica","Suecia","Suiza","Tailandia","Turquía","Ucrania",];

        document.getElementById("enviarDatos").addEventListener("click", function(event) {
        event.preventDefault();

        // Obtiene los valores de los campos
        var country = document.getElementById("Pais").value;
        var ciudad = document.getElementById("Ciudad").value;
        var localizacion = document.getElementById("localizacion").value;
        var mapLink = document.getElementById("mapLink").value;
        var foto = document.getElementById("foto").value;
        var sensorTemperatura = document.getElementById("SensorTemperatura").value;
        var sensorHumedad = document.getElementById("SensorHumedad").value;
        var sensorSonido = document.getElementById("SensorSonido").value;
        var sensorLuz = document.getElementById("SensorLuz").value;
        var sensorMovimiento = document.getElementById("SensorMovimiento").value;
        var minTemp = document.getElementById("minTemp").value;
        var maxTemp = document.getElementById("maxTemp").value;
        var password = document.getElementById("Contraseña").value;
        var Contraseña = document.getElementById("Contraseña");
        var CalidadContraseña = document.getElementById("CalidadContraseña");

        Contraseña.addEventListener("input", function () {
        var password = this.value;

        if (password.length < 6) {
                CalidadContraseña.textContent = "mala";
                CalidadContraseña.style.color = "red";
            } else if (password.length >= 6 && password.length <= 7) {
                CalidadContraseña.textContent = "aceptable";
                CalidadContraseña.style.color = "yellow";
            } else if (password.length >= 8) {
                CalidadContraseña.textContent = "buena";
                CalidadContraseña.style.color = "green";
            }
        });

        if (Paises.includes(country)) {
            
            if (password.length < 6) {
                alert("La contraseña debe tener al menos 6 caracteres.");
            } else if (password.length >= 6 && password.length <= 7) {
                alert("La contraseña tiene una longitud aceptable (6-7 caracteres).");

                        // Almacena los valores en el Local Storage
                        localStorage.setItem("Pais", Pais);
                        localStorage.setItem("Ciudad", ciudad);
                        localStorage.setItem("localizacion", localizacion);
                        localStorage.setItem("mapLink", mapLink);
                        localStorage.setItem("foto", foto);
                        localStorage.setItem("Contraseña", Contraseña);
                        localStorage.setItem("sensorTemperatura", sensorTemperatura);
                        localStorage.setItem("sensorHumedad", sensorHumedad);
                        localStorage.setItem("sensorSonido", sensorSonido);
                        localStorage.setItem("sensorLuz", sensorLuz);
                        localStorage.setItem("sensorMovimiento", sensorMovimiento);
                        localStorage.setItem("minTemp", minTemp);
                        localStorage.setItem("maxTemp", maxTemp);

                        alert("Datos guardados con éxito.");
                        window.location.href = "index.html";

            } else if (password.length >= 8) {
                alert("La contraseña es segura (8 o más caracteres).");

                        // Almacena los valores en el Local Storage
                        localStorage.setItem("Pais", Pais);
                        localStorage.setItem("Ciudad", ciudad);
                        localStorage.setItem("localizacion", localizacion);
                        localStorage.setItem("mapLink", mapLink);
                        localStorage.setItem("foto", foto);
                        localStorage.setItem("Contraseña", Contraseña);
                        localStorage.setItem("sensorTemperatura", sensorTemperatura);
                        localStorage.setItem("sensorHumedad", sensorHumedad);
                        localStorage.setItem("sensorSonido", sensorSonido);
                        localStorage.setItem("sensorLuz", sensorLuz);
                        localStorage.setItem("sensorMovimiento", sensorMovimiento);
                        localStorage.setItem("minTemp", minTemp);
                        localStorage.setItem("maxTemp", maxTemp);

                        alert("Datos guardados con éxito.");
                        window.location.href = "index.html";
            }
            } else {
                alert("El país no corresponde a una serie de países permitidos.");
            }
        });
