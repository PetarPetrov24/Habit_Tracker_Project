document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.delete-btn').forEach(button => {
        button.addEventListener('click', function (e) {
            e.preventDefault()
            const habitId = this.getAttribute('data-habit-id')
            if (confirm('Are you sure you want to delete this habit?')) {
                fetch(`${deleteUrlPattern}${habitId}/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                        'X-Requested-With': 'XMLHttpRequest',
                        'Content-Type': 'application/json',
                    },
                })
                    .then(res => res.json())
                    .then(data => {
                        if (data.status === 'success') {
                            console.log(data);
                            const habitElement = document.getElementById(`habit-${habitId}`);
                            if (habitElement) {
                                habitElement.remove();
                            }
                        } else {
                            alert('Something went wrong: ' + data.message);
                        }
                    });
            }
        })
    })
})