function openCreateModal() {
    document.getElementById("modalTitle").innerText = "Add New Pet";
    document.getElementById("petForm").action = "{{ url_for('admin.admin_dashboard') }}";
    document.getElementById("petForm").reset();
    document.getElementById("petModal").style.display = "block";
}

function openEditModal(animalId) {
    document.getElementById("modalTitle").innerText = "Edit Pet";
    document.getElementById("petForm").action = "/pets/" + animalId + "/edit";
    document.getElementById("petModal").style.display = "block";
}

function closeModal() {
    document.getElementById("petModal").style.display = "none";
}

window.onclick = function(event) {
    const modal = document.getElementById("petModal");
    if (event.target === modal) {
        modal.style.display = "none";
    }
}
