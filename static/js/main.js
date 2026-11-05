/*-----------------------------------------------------------------------
 *                           variables
* ------------------------------------------------------------------------*/
const sidebar = document.querySelector('#sidebar');
const backdrop = document.querySelector('#sidebar-backdrop');
const btnToggleSidebar = document.querySelector('[data-sidebar-toggle]');
// filtre dynamique
const inputSearch = document.querySelector('#memberSearch');
const memberItems = document.querySelectorAll('.member-item');
// purple menu dropdown
const purpleBtn = document.querySelector('#purple-btn');
const purpleBox = document.querySelector('#purple-box');
// header menu purple
const btnProfileMenu = document.querySelector('#profile-menu-btn');
const dropdownProfile = document.querySelector('#dropdown-profile');
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
function openModal(modalId,modalTitle='') {
    let modal = document.getElementById(modalId);
    let modalBox = modal.querySelector('.modal-box');

    modalBox.querySelector('#modalInfo') ? modalBox.querySelector('#modalInfo').textContent = modalTitle : ''
    clearTimeout(closeTimeout);

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