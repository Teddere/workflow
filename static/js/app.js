document.addEventListener('DOMContentLoaded',
    ()=>{
        const toggle = document.querySelector('[data-sidebar-toggle]');
        const sidebar = document.getElementById('sidebar');
        const backdrop = document.getElementById('sidebar-backdrop');
        const btnProfile = document.getElementById('btn-profile-menu');
        const profileBox = document.getElementById('profile-menu');

        const purpleBox = document.querySelector('#purple');
        const purpleBtn = document.querySelector('#purple-btn');

        const searchInput = document.getElementById('memberSearch');
        const memberItems = document.querySelectorAll('.member-item');

        const modalBox = document.getElementById('modal-box');
        const modalContent = document.querySelector('#modal-content');
        const openModalBtn = document.getElementById('open-modal-btn');
        const closeModalBtn = document.querySelector('#close-modal-btn');
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
        // purple
        function openPurple(modalBox,btnModal){
            modalBox.classList.remove('hidden');
            requestAnimationFrame(()=>{
                modalBox.classList.remove('opacity-0','scale-95','-translate-y-2');
                modalBox.classList.add('opacity-100','scale-100','translate-y-0');
            });
            btnModal.setAttribute('aria-expanded','true');
        }
        function closePurple(modalBox,btnModal){
            modalBox.classList.remove('opacity-100','scale-100','translate-y-0');
            modalBox.classList.add('opacity-0','scale-95','-translate-y-2');
            setTimeout(()=>{
                modalBox.classList.add('hidden');
            },200)
            btnModal.setAttribute('aria-expanded','false');
        }

        // modal
        let closeTimeout=null;
        function openModal() {
            clearTimeout(closeTimeout)
            modalBox.classList.remove('pointer-events-none');
            modalBox.classList.remove('opacity-0');
            modalBox.classList.add('opacity-100');
            openModalBtn.setAttribute('aria-expanded', 'true')
        }
        function closeModal() {
            modalBox.classList.remove('opacity-100');
            modalBox.classList.add('opacity-0');
            clearTimeout(closeTimeout)

            closeTimeout = setTimeout(()=>{
                modalBox.classList.add('pointer-events-none')
            },300)
        }
        // Ouvrir / Fermer au clic sur le bouton menu
        toggle?.addEventListener('click',openSidebar);
        // Fermer la sidebar
        backdrop?.addEventListener('click',closeSidebar)
        document.addEventListener('keydown',(event)=>{
            if (event.key === 'Escape' && !sidebar.classList.contains('-translate-x-full')) {
                closeSidebar();
            }
            if (event.key === 'Escape' && !modalBox.classList.contains('pointer-events-none')){
                closeModal()
            }
        })

        // profile menu
        btnProfile.addEventListener('click',()=>{
            if (profileBox.classList.contains('hidden')) {
                 openPurple(profileBox,btnProfile)
            } else {
               closePurple(profileBox,btnProfile)
            }
        });

        // purple
            if (purpleBtn) {
                purpleBtn.addEventListener('click',()=>{
                    if (purpleBox.classList.contains('hidden')) {
                        openPurple(purpleBox,purpleBtn)
                    } else {
                        closePurple(purpleBox,purpleBtn)
                    }
                })
            }

        // form project (members)
            if (memberItems) {
                memberItems.forEach((item)=>{
                    const checkbox = item.querySelector('input[type="checkbox"]');
                    const checkboxIcon = item.querySelector('i');

                    if (checkbox && checkbox.checked) {
                        checkboxIcon.classList.remove('text-white')
                    }
                    item.addEventListener('click',()=>{
                        checkbox.checked = !checkbox.checked;
                        checkbox.checked ? checkboxIcon.classList.remove('text-white'): checkboxIcon.classList.add('text-white')
                    })
                })
            }
        // form project dynamique filter
        if (searchInput) {
            searchInput.addEventListener('input',(e)=>{
                const query = e.target.value.toLowerCase();

                memberItems.forEach((item)=>{
                    const name = item.getAttribute('data-name') || '';
                    const email = item.getAttribute('data-email') || '';

                    if (name.includes(query) || email.includes(query)) {
                        item.style.display = 'block';
                    } else {
                        item.style.display = 'none';
                    }
                });
            })
        }

        // modal
            if (openModalBtn) {
                openModalBtn.addEventListener('click',openModal);
            }
            if (closeModalBtn) {
                closeModalBtn.addEventListener('click',closeModal)
            }
            if (modalBox) {
                modalBox.addEventListener('click',closeModal)
            }

        // fermeture clic extérieur
        document.addEventListener('click',(event)=>{
            // profile menu
            if (!profileBox.contains(event.target) && !btnProfile.contains(event.target))
            {
                if(!profileBox.classList.contains('hidden')) closePurple(profileBox,btnProfile);
            }
            // purple
            if(purpleBox && !purpleBox.contains(event.target) && !purpleBtn.contains(event.target)){
                if (!purpleBox.classList.contains('hidden')) closePurple(purpleBox,purpleBtn)
            }

        });

    }
);