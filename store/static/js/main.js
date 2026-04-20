 let lastScroll = 0;
        const navbar = document.getElementById('navbar');

        window.addEventListener('scroll', () => {
            const currentScroll = window.pageYOffset;

            if (currentScroll <= 0) {
                navbar.classList.remove('nav-hidden'); // Top of page
                return;
            }

            if (currentScroll > lastScroll && !navbar.classList.contains('nav-hidden')) {
                // Scrolling Down
                navbar.classList.add('nav-hidden');
            } else if (currentScroll < lastScroll && navbar.classList.contains('nav-hidden')) {
                // Scrolling Up
                navbar.classList.remove('nav-hidden');
            }
            lastScroll = currentScroll;
        });

function goToUrl() {
  window.location.href = "{% url 'profile' %}";
}




document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-input');
    
    // Create the UL element dynamically if it doesn't exist
    let list = document.getElementById('suggestions-list');
    if (!list) {
        list = document.createElement('ul');
        list.id = 'suggestions-list';
        list.className = 'suggestions-list';
        searchInput.parentNode.appendChild(list);
    }

    let timeout = null;

    searchInput.addEventListener('input', function() {
        clearTimeout(timeout);
        const query = this.value.trim();

        if (query.length < 1) {
            list.style.display = 'none';
            return;
        }

        // Wait 300ms after user stops typing to fetch
        timeout = setTimeout(() => {
            fetch(`/search-suggestions/?q=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(data => {
                    list.innerHTML = '';
                    if (data.suggestions.length > 0) {
                        list.style.display = 'block';
                        data.suggestions.forEach(item => {
                            const li = document.createElement('li');
                            li.textContent = item;
                            
                            if (item === "No matches found") {
                                li.className = 'no-match';
                            } else {
                                li.onclick = () => {
                                    // searchInput.value = item;
                                    // list.style.display = 'none';
                                    window.location.href = `/search/?q=${encodeURIComponent(item)}`;
                                    // You can trigger a redirect or form submit here
                                };
                            }
                            list.appendChild(li);
                        });
                    }
                });
        }, 300);
    });

    // Close list when clicking outside
    document.addEventListener('click', (e) => {
        if (!searchInput.contains(e.target) && !list.contains(e.target)) {
            list.style.display = 'none';
        }
    });
});

searchInput.addEventListener('keydown', function(e) {
    if (e.key === 'Enter') {
        e.preventDefault();
        const query = this.value.trim();
        if (query.length > 0) {
            window.location.href = `/search/?q=${encodeURIComponent(query)}`;
        }
    }
});