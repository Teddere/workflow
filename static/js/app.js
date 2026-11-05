document.addEventListener('DOMContentLoaded',()=>{
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

            const form = document.querySelector('#form-modal form');
            const submitBtn = document.getElementById('modal-submit-btn');

            if (form && submitBtn) {
                submitBtn.setAttribute('form',form.id)
            }
           openModal('modal');
        }
    });

    ['taskCreated','taskUpdated','taskDeleted'].forEach((eventName)=>{
    document.body.addEventListener(eventName,()=>{
            (eventName === 'taskDeleted') ? closeModal('modal-confirm'): closeModal('modal')
        });

    });
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
            openModal(
                openModalBtn.getAttribute('data-modal-target'),
                openModalBtn.getAttribute('aria-label'),
            )
        }
        if (closeModalBtn) {
            closeModal(closeModalBtn.getAttribute('data-modal-close'));
        }
        if ((event.target.id ==='modal' || event.target.id==='modal-confirm') && !event.target.classList.contains('pointer-events-none')) {
            closeModal(event.target.id);
        }


    });

});