document.addEventListener('DOMContentLoaded', function() {
    // Elementos del formulario
    const nameInput = document.getElementById('name');
    const surnameInput = document.getElementById('surname');
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
    const detailsDeathReason = document.getElementById('detailsDeathReason');
    const detailsSpecifications = document.getElementById('detailsSpecifications');
    const detailsImage = document.getElementById('detailsImage');

    const API_BASE_URL = "http://localhost:8000"; // Cambia esto si el backend está en otro host o puerto

    // Elementos de la imagen
    const imageButton = document.getElementById('imageButton');
    const imageInput = document.getElementById('imageInput');
    const previewImage = document.getElementById('previewImage');

    // Variables para controlar el estado de los modales
    let deathReasonCompleted = false;
    let specificationsCompleted = false;

    // Función para verificar campos
    function checkFields() {
        registerButton.disabled = !(nameInput.value.trim() !== "" && surnameInput.value.trim() !== "");
    }

    // Eventos para los campos de texto
    nameInput.addEventListener('input', checkFields);
    surnameInput.addEventListener('input', checkFields);

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
    // Abrir primer modal
    registerButton.addEventListener('click', async () => {
        console.log("Register button clicked");

        registerButton.disabled = true;
        const name = nameInput.value.trim();
        const surname = surnameInput.value.trim();
     const age = parseInt(document.getElementById('age').value); // Asegúrate de tener un campo para la edad
    const file = imageInput.files[0];

    if (!file) {
        alert("Por favor, selecciona una imagen.");
        return;
    }

    const formData = new FormData();
    formData.append("nombre", name);
    formData.append("apellido", surname);
    formData.append("edad", age);
    formData.append("foto", file);

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

        personaId = persona.uid; // Guarda el ID de la persona creada

        // Opcional: Actualiza la UI con la nueva persona
        modal1.style.display = 'flex';
        deathReasonCompleted = false;
    } catch (error) {
        console.error("Error al registrar la persona:", error);
    }
});
let causa_primer_model=null;
    // Siguiente modal
    nextButton.addEventListener('click', async () => {
        const deathReason = document.getElementById('deathReason').value;
        if (deathReason.trim() === "") {
            alert("Por favor, escribe una razón antes de continuar.");
        } else {
            const causaMuerte = {
                persona_id: personaId, // Reemplaza con el ID real de la persona si lo tienes
                causa_muerte: {
                    causa: deathReason
                }
            };

            const formData2 = new FormData();
    formData2.append("persona_id", causaMuerte.persona_id);
    formData2.append("causa", causaMuerte.causa_muerte.causa);

    
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
                causa_primer_model=causaMuerte.causa_muerte.causa;
                
            deathReasonCompleted = true;
            modal1.style.display = 'none';
            modal2.style.display = 'flex';
            specificationsCompleted = false;
        } catch (error) {
            console.error("Error al añadir causa", error);
        }
        }
    });

    // Confirmar y añadir entrada
    confirmButton.addEventListener('click', async () => {
        const name = nameInput.value;
        const surname = surnameInput.value;
        const specifications = document.getElementById('specifications').value;
        const deathReason = document.getElementById('deathReason').value;

        if (specifications.trim() === "") {
            alert("Por favor, escribe las especificaciones antes de confirmar.");
        } else {

            const causaMuerte2 = {
                persona_id: personaId, // Reemplaza con el ID real de la persona si lo tienes
                causa_muerte: {
                    causa: causa_primer_model,
                    detalles: specifications
                }
            };

            const formData3 = new FormData();
            formData3.append("persona_id", causaMuerte2.persona_id);
            formData3.append("causa", causaMuerte2.causa_muerte.causa);
            formData3.append("detalles", causaMuerte2.causa_muerte.detalles);

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
            const entriesContainer = document.querySelector(".entries-container");
            const newEntry = document.createElement("div");
            newEntry.className = "entry";

            const isDefaultImage = previewImage.src.includes("user-add-friend-icon-design-model-free-vector.jpg");
            const status = isDefaultImage ? "Vivo" : "Muerto";
            const statusClass = isDefaultImage ? "status-alive" : "status-dead";

            newEntry.innerHTML = `
                <div class="entry-info">
                    <span class="entry-name">${name} ${surname}</span>
                    <span class="entry-status ${statusClass}">${status}</span>
                </div>
                <div class="entry-image-container">
                    <img class="entry-image" src="${previewImage.src}" alt="${name}">
                </div>
            `;

            // Almacenar datos para el modal de detalles
            newEntry.dataset.name = name;
            newEntry.dataset.surname = surname;
            newEntry.dataset.deathReason = deathReason;
            newEntry.dataset.specifications = specifications;
            newEntry.dataset.image = previewImage.src;

            entriesContainer.appendChild(newEntry);

            // Limpiar formulario
            nameInput.value = '';
            surnameInput.value = '';
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
            detailsName.textContent = entry.dataset.name;
            detailsSurname.textContent = entry.dataset.surname;
            detailsDeathReason.textContent = entry.dataset.deathReason || "N/A";
            detailsSpecifications.textContent = entry.dataset.specifications || "N/A";
            detailsImage.src = entry.dataset.image || "https://via.placeholder.com/150";

            detailsModal.style.display = "flex";
        }
    });

    // Cerrar modal de detalles
    closeDetailsButton.addEventListener("click", () => {
        detailsModal.style.display = "none";
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
        }
    });

    // Deshabilitar botón al inicio
    registerButton.disabled = true;
});