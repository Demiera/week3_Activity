const contentContainer = document.getElementById('content-container')
const loginForm = document.getElementById('login-form')
const searchForm = document.getElementById('search-form')
const baseEndpoint = 'http://127.0.0.1:8000/api'
if (loginForm) {
    loginForm.addEventListener('submit', handleLogin)
}

if (searchForm) {
    searchForm.addEventListener('submit', handleSearch)
}

function handleLogin(event){
    console.log(event)
    event.preventDefault()
    const loginEndpoint = `${baseEndpoint}/token/`
    let loginFromData = new FormData(loginForm)
    let loginObjectData = Object.fromEntries(loginFromData)
    let bodyStr = JSON.stringify(loginObjectData)
    console.log(bodyStr)
    const options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: bodyStr
    }
    fetch(loginEndpoint, options) //promise
    .then(response => {
        console.log(response)
        return response.json()
    })
    .then(authData =>{
        handleAuthData(authData, getProductList)
    })

    .catch(err =>{
        console.log(err)
    })
}

function handleSearch(event){
    console.log(event)
    event.preventDefault()

    let formData = new FormData(searchForm)
    let data = Object.fromEntries(formData)
    let searchParams = new URLSearchParams(data)
    const endpoint = `${baseEndpoint}/search/?${searchParams}`
    const options = {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    }
    fetch(endpoint, options) //promise
    .then(response => {
        console.log(response)
        return response.json()
    })
    .then(data =>{
        writeToContainer(data)
    })

    .catch(err =>{
        console.log(err)
    })
}

function handleAuthData(authData, callback){
    localStorage.setItem('access', authData.access)
    localStorage.setItem('refresh', authData.refresh)
    if(callback){
        callback()
    }
}

function writeToContainer(data){
    if (contentContainer){
        contentContainer.innerHTML = "<pre>" + JSON.stringify(data, null, 4) +"</pre>"
    }
}

function getFetchOptions(method, body){
    return {
        method: method === null ? 'GET' : method,
        headers: {
            'Content-Type':'application/json',
            'Authorization': `Bearer ${localStorage.getItem('access')}`
        },
        body: body ? body : null
    }
}

function isTokenNotValid(jsonData){
    if(jsonData.code && jsonData.code === 'token_not_valid'){
        alert('please login again')
        return false
    }
    return true
}

function getProductList(){
    const endpoint = `${baseEndpoint}/products/`
//    const options = {
//        headers: {
//            'Content-Type':'application/json',
//            'Authorization': `Bearer ${localStorage.getItem('access')}`
//        }
//    }'
    const options = getFetchOptions()
    fetch(endpoint, options)
    .then(response =>{
        return response.json()
    })
    .then(data=>{
        console.log(data)
        const validData = isTokenNotValid(data)
        if (validData){
            writeToContainer(data)
        }
    })

}

getProductList()