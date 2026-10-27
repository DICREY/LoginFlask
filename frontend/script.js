document.addEventListener('DOMContentLoaded',() =>  {
    
    const pass = document.getElementById('pass')
    const slash = document.getElementById('slash')

    // toggle password
    document.getElementById('toggle').addEventListener('click', () => {
        const oculto = pass.type === 'password'
        pass.type = oculto ? 'text' : 'password'
        slash.style.display = oculto ? 'none' : ''
    })

    // darkmode
    document.getElementById('theme').addEventListener('click', () => {
        document.documentElement.classList.toggle('dark')
    })
})        