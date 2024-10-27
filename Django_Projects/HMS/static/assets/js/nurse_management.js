function filterNurses() {
    var department = document.getElementById('department').value;
    var shift = document.getElementById('shift').value;
    var cards = document.getElementsByClassName('nurse-card');

    for (var i = 0; i < cards.length; i++) {
        var card = cards[i];
        var cardDepartment = card.getAttribute('data-department');
        var cardShift = card.getAttribute('data-shift');

        if ((department === 'Department' || department === cardDepartment) &&
            (shift === 'Shift' || shift === cardShift)) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    }
}

function populateUpdateModal(id, name, gender, department, shift, care) {
    document.getElementById('updateNurseId').value = id;
    document.getElementById('updateNurseName').value = name;
    document.getElementById('updateNurseGender').value = gender;
    document.getElementById('updateNurseDepartment').value = department;
    document.getElementById('updateNurseShift').value = shift;
    document.getElementById('updateNurseCare').value = care;
}

document.getElementById('updateNurseForm').addEventListener('submit', function(event) {
    event.preventDefault();
    
    var nurseId = document.getElementById('updateNurseId').value;
    var formData = new FormData(this);

    fetch(`/update_nurse/${nurseId}/`, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        }
    }).then(response => {
        if (response.ok) {
            window.location.reload();
        } else {
            alert('Failed to update nurse details.');
        }
    });
});

function showNurseDetails(profilePicture, name, gender, department, shift, care, experience, certifications, contact, email, address) {
    console.log('Profile Picture:', profilePicture);
    console.log('Name:', name);
    console.log('Gender:', gender);
    console.log('Department:', department);
    console.log('Shift:', shift);
    console.log('Care:', care);
    console.log('Experience:', experience);
    console.log('Certifications:', certifications);
    console.log('Contact:', contact);
    console.log('Email:', email);
    console.log('Address:', address);

    document.getElementById('nurseProfilePicture').src = profilePicture;
    document.getElementById('nurseName').textContent = name;
    document.getElementById('nurseGender').textContent = gender;
    document.getElementById('nurseDepartment').textContent = department;
    document.getElementById('nurseShift').textContent = shift;
    document.getElementById('nurseCare').textContent = care;
    document.getElementById('nurseExperience').textContent = experience;
    document.getElementById('nurseCertifications').textContent = certifications;
    document.getElementById('nurseContact').textContent = contact;
    document.getElementById('nurseEmail').textContent = email;
    document.getElementById('nurseAddress').textContent = address;

    var nurseDetailsModal = new bootstrap.Modal(document.getElementById('nurseDetailsModal'));
    nurseDetailsModal.show();
}

