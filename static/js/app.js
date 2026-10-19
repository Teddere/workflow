document.addEventListener('DOMContentLoaded',
    ()=>{
        const toggle = document.querySelector('[data-sidebar-toggle]');
        const sidebar = document.getElementById('sidebar');
        const backdrop = document.getElementById('sidebar-backdrop');

        // Ouvrir / Fermer au clic sur le bouton menu
        toggle?.addEventListener('click',toggleSidebar);
        // Fermer la sidebar
        backdrop?.addEventListener('click',toggleSidebar)

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