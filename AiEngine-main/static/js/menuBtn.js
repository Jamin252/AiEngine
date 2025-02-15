// When a menu item is clicked, perform the corresponding action
const menuItems = document.querySelectorAll('#more-menu .menu-item')
menuItems.forEach(item => {
    item.addEventListener('click', () => {
        console.log('Clicked:', item.textContent)
        moreMenu.classList.add('hidden')
    })
})

// When clicking anywhere else on the document, hide the menu
document.addEventListener('click', () => {
    moreMenu.classList.add('hidden')
})