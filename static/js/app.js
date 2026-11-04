document.addEventListener('DOMContentLoaded',()=>{

    const btnToggleSidebar = document.querySelector('[data-sidebar-toggle]');
    const sidebar = document.querySelector('#sidebar');
    const backdrop = document.querySelector('#sidebar-backdrop');

    const inputSearch = document.querySelector('#memberSearch');
    const memberItems = document.querySelectorAll('.member-item');
    // header menu purple
    const btnProfileMenu = document.querySelector('#profile-menu-btn');
    const dropdownProfile = document.querySelector('#dropdown-profile');
    // purple menu dropdown
    const purpleBtn = document.querySelector('#purple-btn');
    const purpleBox = document.querySelector('#purple-box');
    // modal purple control
    let closeTimeout = null;

    /*-----------------------------------------------------------------------
    *                           function
    * ------------------------------------------------------------------------*/
    // sidebar
    function openSidebar() {
        sidebar.classList.remove('-translate-x-full');

        backdrop.classList.remove('opacity-0');
        backdrop.classList.remove('pointer-events-none');
        btnToggleSidebar.setAttribute('aria-expanded','true');
    }
    function closeSidebar() {
        sidebar.classList.add('-translate-x-full');

        backdrop.classList.add('opacity-0');
        backdrop.classList.add('pointer-events-none');
        btnToggleSidebar.setAttribute('aria-expanded','false');
    }
    // dynamique search
    function searchFilter(e) {
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
    }
    // purple menu
    function openPurple(purpleBox,purpleBtn) {
        purpleBox.classList.remove('hidden');
        requestAnimationFrame(()=>{
            purpleBox.classList.remove('opacity-0','scale-95','-translate-y-2');
            purpleBox.classList.add('opacity-100','scale-100','translate-y-0');
        });
        purpleBtn.setAttribute('aria-expanded','true');
    }
    function closePurple(purpleBox,purpleBtn) {
        purpleBox.classList.remove('opacity-100','scale-100','translate-y-0');
        purpleBox.classList.add('opacity-0','scale-95','-translate-y-2');
        setTimeout(()=>{
            purpleBox.classList.add('hidden');
        },200);
        purpleBtn.setAttribute('aria-expanded','false');
    }
    // modal purple control
    function openModal(modalId,modalTitle) {
        let modal = document.getElementById(modalId);
        let modalBox = modal.querySelector('.modal-box');
        modalBox.querySelector('.modal-title').textContent = modalTitle
        clearTimeout(closeTimeout)
        modal.classList.remove('pointer-events-none','opacity-0');
        modal.classList.add('opacity-100')
        if (modalBox) {
            modalBox.classList.remove('scale-95', 'opacity-0');
            modalBox.classList.add('scale-100', 'opacity-100');
        }
    }
    function closeModal(modalId) {
        let modal = document.getElementById(modalId);
        let modalBox = modal.querySelector('.modal-box');
        clearTimeout(closeTimeout)
        if (modalBox) {
            modalBox.classList.remove('scale-100', 'opacity-100');
            modalBox.classList.add('scale-95', 'opacity-0');
        }
        modal.classList.remove('opacity-100');
        modal.classList.add('opacity-0');
        closeTimeout = setTimeout(()=>{
            modal.classList.add('pointer-events-none')
        },300)
    }
    /*-----------------------------------------------------------------------
    *                           main principal
    * ------------------------------------------------------------------------*/
    // Ouvrir / Fermer au clic sidebar sur le bouton
    btnToggleSidebar.addEventListener('click',openSidebar);
    backdrop.addEventListener('click',closeSidebar);

    // form project dynamique filter
    if (inputSearch) {
        inputSearch.addEventListener('input',searchFilter);
    }
    // dropdown menu header
    if (btnProfileMenu) {
        btnProfileMenu.addEventListener('click',()=>{

            if (dropdownProfile.classList.contains('hidden')) {
                openPurple(dropdownProfile,btnProfileMenu)
            } else {
                closePurple(dropdownProfile,btnProfileMenu)
            }
        });
    }
    // dropdown purple menu
    if (purpleBtn) {
        purpleBtn.addEventListener('click',()=>{
            if (purpleBox.classList.contains('hidden')) {
                openPurple(purpleBox,purpleBtn);
            } else {
                closePurple(purpleBox,purpleBtn);
            }
        })
    }

    /*-----------------------------------------------------------------------
    *                           keyboards
    * ------------------------------------------------------------------------*/
    document.addEventListener('keydown',(event)=>{
        // sidebar
        if (event.key === 'Escape' && sidebar.classList.contains('-translate-x-full')) {
            closeSidebar()
        }
        // modal purple control
        if (event.key === 'Escape' && document.querySelectorAll('.fixed.inset-0')) {
            document.querySelectorAll('.fixed.inset-0').forEach((modal)=>{
                if (!modal.classList.contains('pointer-events-none')) {
                    closeModal(modal.id);
                }
            })
        }
    });
    /*-----------------------------------------------------------------------
    *                      HTMX
    * ------------------------------------------------------------------------*/
    document.body.addEventListener('htmx:afterSwap',(event)=>{
       if (event.detail.target.id === 'form-modal') {
            openModal('modal','Nouvelle tâche');
        }
    });
    document.body.addEventListener('taskCreated',(event)=>{
        closeModal('modal')
    })
    /*-----------------------------------------------------------------------
    *                      fermeture clic extérieur
    * ------------------------------------------------------------------------*/
    document.addEventListener('click',(event)=>{
        // dropdown menu profile
        if (!dropdownProfile.contains(event.target) && !btnProfileMenu.contains(event.target)) {
            if (!dropdownProfile.classList.contains('hidden')) closePurple(dropdownProfile,btnProfileMenu);
        }
        // dropdown menu purple
        if (purpleBox && !purpleBox.contains(event.target) && !purpleBtn.contains(event.target)) {
            if (!purpleBox.classList.contains('hidden')) closePurple(purpleBox,purpleBtn);
        }
        // modal purple control
        let openModalBtn = event.target.closest('[data-modal-target]');
        let closeModalBtn = event.target.closest('[data-modal-close]');

        if (openModalBtn) {
            openModal(openModalBtn.getAttribute('data-modal-target'),openModalBtn.getAttribute('aria-label'));
        }
        if (closeModalBtn) {
            closeModal(closeModalBtn.getAttribute('data-modal-close'));
        }
        if ((event.target.id ==='modal' || event.target.id==='modal-confirm') && !event.target.classList.contains('pointer-events-none')) {
            closeModal(event.target.id);
        }


    });

});