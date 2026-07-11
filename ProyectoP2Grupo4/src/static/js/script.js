const boton = document.getElementById("enviar");
const input = document.getElementById("mensaje");
const chat = document.querySelector(".chat");

function enviarMensaje() {

    let texto = input.value.trim();

    if (texto === "") return;

    // Mostrar mensaje del usuario
    chat.innerHTML += `
        <div class="mensaje usuario">
            <div class="burbuja">
                ${texto}
            </div>
        </div>
    `;

    input.value = "";

    // Desplazar el chat al final
    chat.scrollTop = chat.scrollHeight;

    // burbuja de "escribiendo..." mientras llega la respuesta
    chat.innerHTML += `
        <div class="mensaje bot escribiendo">
            <div class="burbuja">
                escribiendo...
            </div>
        </div>
    `;
    chat.scrollTop = chat.scrollHeight;

    fetch("/preguntar", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            mensaje: texto
        })
    })

    .then(response => response.json())

    .then(datos => {

        // quitar la burbuja de "escribiendo..."
        const escribiendo = chat.querySelector(".escribiendo");
        if (escribiendo) escribiendo.remove();

        chat.innerHTML += `
            <div class="mensaje bot">
                <div class="burbuja">
                    ${datos.respuesta}
                </div>
            </div>
        `;

        chat.scrollTop = chat.scrollHeight;

    })

    .catch(error => {

        console.error(error);

        const escribiendo = chat.querySelector(".escribiendo");
        if (escribiendo) escribiendo.remove();

        chat.innerHTML += `
            <div class="mensaje bot">
                <div class="burbuja">
                    Ocurrió un error al conectar con el servidor.
                </div>
            </div>
        `;

    });

}

function preguntaRapida(texto) {
    input.value = texto;
    enviarMensaje();
}

boton.addEventListener("click", enviarMensaje);

input.addEventListener("keypress", function(e) {

    if (e.key === "Enter") {

        enviarMensaje();

    }

});