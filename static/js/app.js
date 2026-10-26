document.addEventListener('DOMContentLoaded',
    ()=>{
        const toggle = document.querySelector('[data-sidebar-toggle]');
        const sidebar = document.getElementById('sidebar');
        const backdrop = document.getElementById('sidebar-backdrop');
        const btnProfile = document.getElementById('btn-profile-menu');
        const profileBox = document.getElementById('profile-menu');
        // function
        // sidebar
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
        // pop profile
        function openMenuProfile(){
            profileBox.classList.remove('hidden');
            requestAnimationFrame(()=>{
                profileBox.classList.remove('opacity-0','scale-95','-translate-y-2');
                profileBox.classList.add('opacity-100','scale-100','translate-y-0');
            });
            btnProfile.setAttribute('aria-expanded','true');
        }
        function closeMenuProfile(){
            profileBox.classList.remove('opacity-100','scale-100','translate-y-0');
            profileBox.classList.add('opacity-0','scale-95','-translate-y-2');
            setTimeout(()=>{
                profileBox.classList.add('hidden');
            },200)
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

        // profile menu
        btnProfile.addEventListener('click',(event)=>{
            if (profileBox.classList.contains('hidden')) {
                openMenuProfile();
            } else {
                closeMenuProfile();
            }
        });

        // fermeture clic extérieur
        document.addEventListener('click',(event)=>{
            // profile menu
            if (!profileBox.contains(event.target) && !btnProfile.contains(event.target))
            {
                if(!profileBox.classList.contains('hidden')) closeMenuProfile();
            }
        });

    }
);