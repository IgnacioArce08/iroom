<?php
// Obtén el nombre del país desde la solicitud GET
$pais = isset($_GET['pais']) ? $_GET['pais'] : '';

// Verifica si se proporcionó un país y si existe el archivo correspondiente
if ($pais && file_exists("datos_ciudades/{$pais}.txt")) {
    // Lee el contenido del archivo de ciudades
    $ciudades = file("datos_ciudades/{$pais}.txt", FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);

    // Devuelve las opciones de ciudad como HTML
    foreach ($ciudades as $ciudad) {
        echo "<option value=\"{$ciudad}\">{$ciudad}</option>";
    }
} else {
    // Devuelve un mensaje de error si no se proporciona un país válido
    echo "<option value=\"\">Selecciona un país válido</option>";
}
?>