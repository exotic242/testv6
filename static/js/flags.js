
document.querySelectorAll('.status-details-link').forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        const reason = link.getAttribute('data-reason');
        openModal(reason);
    });
});
