document.addEventListener('DOMContentLoaded',
    ()=>{
        const toggle = document.querySelector('[data-sidebar-toggle]');
        const sidebar = document.getElementById('sidebar');
        const backdrop = document.getElementById('sidebar-backdrop');

        // function
        function openSidebar() {
            sidebar.classList.remove('-translate-x-full');

            backdrop.classList.remove('opacity-0');
            backdrop.classList.remove('pointer-events-none');
            toggle.setAttribute('aria-expanded','true');
        }
        function closeSidebar() {
            sidebar.classList.add('-translate-x-full');

            backdrop.classList.add('opacity-0');
            backdrop.classList.add('pointer-events-none');
            toggle.setAttribute('aria-expanded','false');
        }

        // Ouvrir / Fermer au clic sur le bouton menu
        toggle?.addEventListener('click',openSidebar);
        // Fermer la sidebar
        backdrop?.addEventListener('click',closeSidebar)

        document.addEventListener('keydown',(event)=>{
            if (event.key === 'Escape' && !sidebar.classList.contains('-translate-x-full')) {
                closeSidebar();
            }
        })
        function toggleSidebar() {
            sidebar.classList.toggle('-translate-x-full');
            // Gère le backdrop
            if (backdrop) {
                backdrop.classList.toggle('opacity-0');
                backdrop.classList.toggle('pointer-events-none');
            }
        }
    }
);