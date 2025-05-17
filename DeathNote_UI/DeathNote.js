document.addEventListener('DOMContentLoaded', function() {
    // Elementos del formulario
    const nameInput = document.getElementById('name');
    const surnameInput = document.getElementById('surname');
    const ageInput = document.getElementById('age');
    const registerButton = document.getElementById('registerButton');
    const modal1 = document.getElementById('modal1');
    const modal2 = document.getElementById('modal2');
    const nextButton = document.getElementById('nextButton');
    const confirmButton = document.getElementById('confirmButton');

    // Elementos del modal de detalles
    const detailsModal = document.getElementById('detailsModal');
    const closeDetailsButton = document.getElementById('closeDetailsButton');
    const detailsName = document.getElementById('detailsName');
    const detailsSurname = document.getElementById('detailsSurname');
    const detailsAge = document.getElementById('detailsAge');
    const detailsDeathReason = document.getElementById('detailsDeathReason');
    const detailsSpecifications = document.getElementById('detailsSpecifications');
    const detailsImage = document.getElementById('detailsImage');

    const API_BASE_URL = "http://localhost:8000"; // Cambia esto si el backend está en otro host o puerto

    const ws = new WebSocket("ws://localhost:8000/ws/status");

    // Variable global para saber qué persona se está mostrando en el modal de detalles
    let detailsModalPersonaId = null;

    ws.onopen = () => {
        console.log("WebSocket conectado");
    };

    ws.onmessage = (event) => {
        try {
            const message = JSON.parse(event.data);
            if (message.event === "person_created" && message.data) {
            const data = message.data;
            const entriesContainer = document.querySelector(".entries-container");
            // Evita duplicados
            if (!document.querySelector(`.entry[data-persona-id="${data.uid}"]`)) {
                const newEntry = document.createElement("div");
                newEntry.className = "entry";
                newEntry.dataset.personaId = data.uid;
                newEntry.dataset.name = data.nombre;
                newEntry.dataset.surname = data.apellido;
                newEntry.dataset.age = data.edad;
                newEntry.dataset.deathReason = data.causa_muerte?.causa || "";
                newEntry.dataset.specifications = data.causa_muerte?.detalles || "";
                newEntry.dataset.image = data.foto_url || "https://static.vecteezy.com/system/resources/previews/004/679/264/original/user-add-friend-icon-design-model-free-vector.jpg";
                newEntry.innerHTML = `
                    <div class="entry-info">
                        <span class="entry-name">${data.nombre} ${data.apellido}</span>
                        <span class="entry-age">${data.edad} años</span>
                        <span class="entry-status status-alive">Vivo</span>
                    </div>
                    <div class="entry-image-container">
                        <img class="entry-image" src="${data.foto_url || "https://static.vecteezy.com/system/resources/previews/004/679/264/original/user-add-friend-icon-design-model-free-vector.jpg"}" alt="${data.nombre}">
                    </div>
                `;
                entriesContainer.prepend(newEntry);
            }
        }
            if (message.event === "death_notification" && message.data) {
                const data = message.data;
                const entries = document.querySelectorAll(".entry");
                entries.forEach(entry => {
                    if (entry.dataset.personaId === data.persona_id) {
                        const statusElement = entry.querySelector(".entry-status");
                        if (statusElement) {
                            statusElement.textContent = "Muerto";
                            statusElement.className = "entry-status status-dead";
                        }
                        entry.dataset.deathReason = data.causa_muerte.causa;
                        entry.dataset.specifications = data.causa_muerte.detalles;
                    }
                });
                // Actualiza el modal de detalles si corresponde
                if (
                    detailsModal.style.display === "flex" &&
                    detailsModalPersonaId === data.persona_id
                ) {
                    detailsName.textContent = data.nombre;
                    detailsSurname.textContent = data.apellido;
                    detailsAge.textContent = data.edad ? `${data.edad} años` : "N/A";
                    detailsDeathReason.textContent = data.causa_muerte?.causa || "N/A";
                    detailsSpecifications.textContent = data.causa_muerte?.detalles || "N/A";
                    detailsImage.src = data.foto_url || "https://via.placeholder.com/150";
                }
            }
            if (message.event === "person_updated" && message.data) {
                const data = message.data;
                const entries = document.querySelectorAll(".entry");
                let found = false;
                entries.forEach(entry => {
                    if (entry.dataset.personaId === data.uid) {
                        entry.querySelector(".entry-name").textContent = `${data.nombre} ${data.apellido}`;
                        entry.querySelector(".entry-age").textContent = `${data.edad} años`;
                        entry.querySelector(".entry-status").textContent = data.estado === "muerto" ? "Muerto" : "Vivo";
                        entry.querySelector(".entry-status").className = "entry-status " + (data.estado === "muerto" ? "status-dead" : "status-alive");
                        entry.querySelector(".entry-image").src = data.foto_url || entry.querySelector(".entry-image").src;
                        entry.dataset.name = data.nombre;
                        entry.dataset.surname = data.apellido;
                        entry.dataset.age = data.edad;
                        entry.dataset.deathReason = data.causa_muerte?.causa || "";
                        entry.dataset.specifications = data.causa_muerte?.detalles || "";
                        entry.dataset.image = data.foto_url || entry.dataset.image;
                        found = true;
                    }
                });
                if (!found) {
                    const entriesContainer = document.querySelector(".entries-container");
                    const newEntry = document.createElement("div");
                    newEntry.className = "entry";
                    newEntry.dataset.personaId = data.uid;
                    newEntry.dataset.name = data.nombre;
                    newEntry.dataset.surname = data.apellido;
                    newEntry.dataset.age = data.edad;
                    newEntry.dataset.deathReason = data.causa_muerte?.causa || "";
                    newEntry.dataset.specifications = data.causa_muerte?.detalles || "";
                    newEntry.dataset.image = data.foto_url || "https://static.vecteezy.com/system/resources/previews/004/679/264/original/user-add-friend-icon-design-model-free-vector.jpg";
                    newEntry.innerHTML = `
                        <div class="entry-info">
                            <span class="entry-name">${data.nombre} ${data.apellido}</span>
                            <span class="entry-age">${data.edad} años</span>
                            <span class="entry-status ${data.estado === "muerto" ? "status-dead" : "status-alive"}">${data.estado === "muerto" ? "Muerto" : "Vivo"}</span>
                        </div>
                        <div class="entry-image-container">
                            <img class="entry-image" src="${data.foto_url || "https://static.vecteezy.com/system/resources/previews/004/679/264/original/user-add-friend-icon-design-model-free-vector.jpg"}" alt="${data.nombre}">
                        </div>
                    `;
                    entriesContainer.prepend(newEntry);
                }
                // Actualiza el modal de detalles si corresponde
                if (
                    detailsModal.style.display === "flex" &&
                    detailsModalPersonaId === data.uid
                ) {
                    detailsName.textContent = data.nombre;
                    detailsSurname.textContent = data.apellido;
                    detailsAge.textContent = data.edad ? `${data.edad} años` : "N/A";
                    detailsDeathReason.textContent = data.causa_muerte?.causa || "N/A";
                    detailsSpecifications.textContent = data.causa_muerte?.detalles || "N/A";
                    detailsImage.src = data.foto_url || "https://via.placeholder.com/150";
                }
            }
        } catch (e) {
            console.error("Error procesando mensaje de WebSocket:", e);
        }
    };

    ws.onerror = (error) => {
        console.error("WebSocket error:", error);
    };

    ws.onclose = () => {
        console.warn("WebSocket cerrado");
    };


const wsDeaths = new WebSocket("ws://localhost:8000/ws/deaths");

wsDeaths.onopen = () => {
    console.log("WebSocket de muertes conectado");
};

wsDeaths.onmessage = (event) => {
    try {
        const message = JSON.parse(event.data);
        if (message.event === "death_notification" && message.data) {
            const data = message.data;
            const entries = document.querySelectorAll(".entry");
            entries.forEach(entry => {
                if (entry.dataset.personaId === data.persona_id) {
                    // Actualiza causa y detalles de muerte
                    entry.dataset.deathReason = data.causa_muerte?.causa || "";
                    entry.dataset.specifications = data.causa_muerte?.detalles || "";
                    // Cambia el estado visualmente a "Muerto"
                    const statusElement = entry.querySelector(".entry-status");
                    if (statusElement) {
                        statusElement.textContent = "Muerto";
                        statusElement.className = "entry-status status-dead";
                    }
                }
            });
            // Actualiza el modal de detalles si corresponde
            if (
                detailsModal.style.display === "flex" &&
                detailsModalPersonaId === data.persona_id
            ) {
                detailsName.textContent = data.nombre;
                detailsSurname.textContent = data.apellido;
                detailsDeathReason.textContent = data.causa_muerte?.causa || "N/A";
                detailsSpecifications.textContent = data.causa_muerte?.detalles || "N/A";
                // No actualiza edad ni imagen porque no vienen en la notificación
            }
        }
    } catch (e) {
        console.error("Error procesando mensaje de WebSocket (deaths):", e);
    }
};

wsDeaths.onerror = (error) => {
    console.error("WebSocket error (deaths):", error);
};

wsDeaths.onclose = () => {
    console.warn("WebSocket de muertes cerrado");
};

    // Elementos de la imagen
    const imageButton = document.getElementById('imageButton');
    const imageInput = document.getElementById('imageInput');
    const previewImage = document.getElementById('previewImage');

    // Variables para controlar el estado de los modales
    let deathReasonCompleted = false;
    let specificationsCompleted = false;

    // Función para verificar campos
    function checkFields() {
        const ageValue = ageInput.value.trim();
        const isAgeValid = ageValue !== "" && !isNaN(ageValue) && ageValue >= 1 && ageValue <= 120;
        
        registerButton.disabled = !(
            nameInput.value.trim() !== "" && 
            surnameInput.value.trim() !== "" && 
            isAgeValid
        )
    }

    // Eventos para los campos de texto
    nameInput.addEventListener('input', checkFields);
    surnameInput.addEventListener('input', checkFields);
    ageInput.addEventListener('input', checkFields);

    // Evento para el botón de imagen
    imageButton.addEventListener('click', () => imageInput.click());

    // Evento para cargar la imagen seleccionada
    imageInput.addEventListener('change', (event) => {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                previewImage.src = e.target.result;
            };
            reader.readAsDataURL(file);
        }
    });

    let personaId = null;
    let closeModal1Timeout = null;
    registerButton.addEventListener('click', async () => {
        console.log("Register button clicked");
        registerButton.disabled = true;

        const name = nameInput.value.trim();
        const surname = surnameInput.value.trim();
        const age = ageInput.value.trim();
        const file = imageInput.files[0];

        const formData = new FormData();
        formData.append("nombre", name);
        formData.append("apellido", surname);
        formData.append("edad", age);
        if (file) {
            formData.append("foto", file);
        }

        try {
            const response = await fetch(`${API_BASE_URL}/persona`, {
                method: "POST",
                body: formData,
            });
            if (!response.ok) {
                const errorData = await response.json();
                alert(`Error: ${errorData.detail}`);
                registerButton.disabled = false;
                return;
            }
            const persona = await response.json();
            console.log("Persona creada:", persona);

            personaId = persona.uid;

            if (!file) {
                return; // No abrir modal1
            }

            // Si hay foto, abrir modal1 normalmente
            modal1.style.display = 'flex';
            deathReasonCompleted = false;

            if (closeModal1Timeout) clearTimeout(closeModal1Timeout);
    closeModal1Timeout = setTimeout(() => {
        if (modal1.style.display === 'flex') {
            modal1.style.display = 'none';
        }
   }, 40000);

        } catch (error) {
            console.error("Error al registrar la persona:", error);
            alert("Ocurrió un error al registrar la persona.");
        }
    });

    let causa_primer_model = null;

    let closeModal1Timeout2 = null;
    // Siguiente modal
    nextButton.addEventListener('click', async () => {
        const deathReason = document.getElementById('deathReason').value;
        if (deathReason.trim() === "") {
            alert("Por favor, escribe una razón antes de continuar.");
        } else {
            if (closeModal1Timeout) {
            clearTimeout(closeModal1Timeout);
            closeModal1Timeout = null;
        }
            const causaMuerte = {
                persona_id: personaId,
                causa_muerte: {
                    causa: deathReason
                }
            };

            try {
                const response = await fetch(`${API_BASE_URL}/persona/death`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(causaMuerte),
                });
                if (!response.ok) {
                    const errorData = await response.json();
                    alert(`Error: ${errorData.detail}`);
                    registerButton.disabled = false;
                    return;
                }
                const causa1 = await response.json();
                console.log("Causa añadida:", causa1);
                causa_primer_model = causaMuerte.causa_muerte.causa;
                deathReasonCompleted = true;
                modal1.style.display = 'none';
                modal2.style.display = 'flex';
                specificationsCompleted = false;

                if (closeModal1Timeout2) clearTimeout(closeModal1Timeout2);
    closeModal1Timeout2 = setTimeout(() => {
        if (modal2.style.display === 'flex') {
            modal2.style.display = 'none';
        }
   }, 400000);
            } catch (error) {
                console.error("Error al añadir causa", error);
            }
        }
    });

    // Confirmar y añadir entrada
    confirmButton.addEventListener('click', async () => {
        const name = nameInput.value;
        const surname = nameInput.value;
        const age = ageInput.value;
        const specifications = document.getElementById('specifications').value;
        const deathReason = document.getElementById('deathReason').value;

        if (specifications.trim() === "") {
            alert("Por favor, escribe las especificaciones antes de confirmar.");
        } else {
            if (closeModal1Timeout2) {
            clearTimeout(closeModal1Timeout2);
            closeModal1Timeout2 = null;
        }
            const causaMuerte2 = {
                persona_id: personaId,
                causa_muerte: {
                    causa: causa_primer_model,
                    detalles: specifications
                }
            };

            try {
                const response = await fetch(`${API_BASE_URL}/persona/death`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(causaMuerte2),
                });
                if (!response.ok) {
                    const errorData = await response.json();
                    alert(`Error: ${errorData.detail}`);
                    registerButton.disabled = false;
                    return;
                }
                const causa2 = await response.json();
                console.log("Detalles añadidos:", causa2);

                specificationsCompleted = true;

                // Limpiar formulario
                nameInput.value = '';
                surnameInput.value = '';
                ageInput.value = '';
                document.getElementById('specifications').value = '';
                document.getElementById('deathReason').value = '';
                previewImage.src = "https://static.vecteezy.com/system/resources/previews/004/679/264/original/user-add-friend-icon-design-model-free-vector.jpg";
                imageInput.value = '';

                // Resetear variables de control
                deathReasonCompleted = false;
                specificationsCompleted = false;

                registerButton.disabled = true;
                modal2.style.display = 'none';
            } catch (error) {
                console.error("Error al añadir causa", error);
            }
        }
    });

    // Mostrar detalles al hacer clic en el estado
    document.querySelector(".entries-container").addEventListener("click", (event) => {
        const statusElement = event.target.closest(".entry-status");
        if (statusElement) {
            const entry = statusElement.closest(".entry");
            detailsModalPersonaId = entry.dataset.personaId; // Guarda el id de la persona mostrada
            detailsName.textContent = entry.dataset.name;
            detailsSurname.textContent = entry.dataset.surname;
            detailsAge.textContent = entry.dataset.age ? `${entry.dataset.age} años` : "N/A";
            detailsDeathReason.textContent = entry.dataset.deathReason || "N/A";
            detailsSpecifications.textContent = entry.dataset.specifications || "N/A";
            detailsImage.src = entry.dataset.image || "https://via.placeholder.com/150";

            detailsModal.style.display = "flex";
        }
    });

    // Cerrar modal de detalles
    closeDetailsButton.addEventListener("click", () => {
        detailsModal.style.display = "none";
        detailsModalPersonaId = null; // Limpia el id al cerrar
    });

    // Cerrar modales al hacer clic fuera con verificación
    window.addEventListener('click', (event) => {
        if (event.target === modal1 && !deathReasonCompleted) {
            alert("Por favor complete la acción. Escribe de qué va a morir antes de continuar.");
        } else if (event.target === modal1) {
            modal1.style.display = 'none';
        }
        
        if (event.target === modal2 && !specificationsCompleted) {
            alert("Por favor complete la acción. Escribe las especificaciones antes de continuar.");
        } else if (event.target === modal2) {
            modal2.style.display = 'none';
        }
        
        if (event.target === detailsModal) {
            detailsModal.style.display = 'none';
            detailsModalPersonaId = null;
        }
    });

    // Deshabilitar botón al inicio
    registerButton.disabled = true;

    // Llenar la tabla al cargar la página con los datos actuales
async function cargarPersonas() {
    try {
        const response = await fetch("http://localhost:8000/personas");
        if (!response.ok) {
            throw new Error("No se pudo obtener la lista de personas");
        }
        const personas = await response.json();
        const entriesContainer = document.querySelector(".entries-container");
        entriesContainer.innerHTML = ""; // Limpia la tabla antes de llenarla

        personas.forEach(data => {
            if (!document.querySelector(`.entry[data-persona-id="${data.uid}"]`)) {
                const newEntry = document.createElement("div");
                newEntry.className = "entry";
                newEntry.dataset.personaId = data.uid;
                newEntry.dataset.name = data.nombre;
                newEntry.dataset.surname = data.apellido;
                newEntry.dataset.age = data.edad;
                newEntry.dataset.deathReason = data.causa_muerte?.causa || "";
                newEntry.dataset.specifications = data.causa_muerte?.detalles || "";
                newEntry.dataset.image = data.foto_url || "https://static.vecteezy.com/system/resources/previews/004/679/264/original/user-add-friend-icon-design-model-free-vector.jpg";
                newEntry.innerHTML = `
                    <div class="entry-info">
                        <span class="entry-name">${data.nombre} ${data.apellido}</span>
                        <span class="entry-age">${data.edad} años</span>
                        <span class="entry-status ${data.estado === "muerto" ? "status-dead" : "status-alive"}">${data.estado === "muerto" ? "Muerto" : "Vivo"}</span>
                    </div>
                    <div class="entry-image-container">
                        <img class="entry-image" src="${data.foto_url || "https://static.vecteezy.com/system/resources/previews/004/679/264/original/user-add-friend-icon-design-model-free-vector.jpg"}" alt="${data.nombre}">
                    </div>
                `;
                entriesContainer.prepend(newEntry);
            }
        });
    } catch (e) {
        console.error("Error cargando personas:", e);
    }
}

// Llama la función al cargar la página
cargarPersonas();
});