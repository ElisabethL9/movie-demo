document.addEventListener('DOMContentLoaded', () => {
    const movieRows = document.querySelectorAll('.movie-row');
    
    movieRows.forEach(row => {
        let isDown = false;
        let startX;
        let scrollLeft;

        row.addEventListener('mousedown', (e) => {
            isDown = true;
            row.classList.add('active');
            startX = e.pageX - row.offsetLeft;
            scrollLeft = row.scrollLeft;
        });

        row.addEventListener('mouseleave', () => {
            isDown = false;
            row.classList.remove('active');
        });

        row.addEventListener('mouseup', () => {
            isDown = false;
            row.classList.remove('active');
        });

        row.addEventListener('mousemove', (e) => {
            if (!isDown) return;
            e.preventDefault();
            const x = e.pageX - row.offsetLeft;
            const walk = (x - startX) * 2;
            row.scrollLeft = scrollLeft - walk;
        });
    });
}); 