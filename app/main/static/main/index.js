const deadline = document.getElementById('goal_deadline');

document.querySelectorAll('[data-reflection-dialog]').forEach((button) => {
    const dialog = document.getElementById(button.dataset.reflectionDialog);
    button.addEventListener('click', () => dialog.showModal());
});

document.querySelectorAll('[data-goal-date]').forEach((label) => {
    const value = label.textContent.trim();
    if (!/^\d{4}-\d{2}-\d{2}$/.test(value)) return;

    const date = new Date(value);
    if (Number.isNaN(date.getTime()) || date.toISOString().slice(0, 10) !== value) return;

    label.textContent = date.toLocaleDateString('en-GB', {
        day: 'numeric',
        month: 'long',
        year: 'numeric',
        timeZone: 'UTC',
    });
});

if (deadline) {
    const picker = document.createElement('input');
    picker.type = 'date';
    picker.value = deadline.value;

    if (picker.type === 'date') {
        if (!deadline.value || picker.value === deadline.value) {
            deadline.type = 'date';
        } else {
            const label = document.createElement('label');
            label.htmlFor = 'deadline-picker';
            label.textContent = 'Choose a new deadline';

            picker.id = label.htmlFor;
            const field = document.createElement('span');
            field.className = 'deadline-picker';
            field.append(label, picker);
            deadline.after(field);

            picker.addEventListener('change', () => {
                if (picker.value) {
                    deadline.type = 'date';
                    deadline.value = picker.value;
                    deadline.focus();
                    field.remove();
                }
            });
        }
    }
}
