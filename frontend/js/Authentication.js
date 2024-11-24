import API from './lib/api.js'
import LocalStorage from './lib/LocalStorage.js'
import Helper from './lib/Helper.js'

const Authentication = {
    async Login(email, password) {
        try {
            const response = await API.post('auth/login', {email, password}, false)

            if (!response.access) {
                throw new Error('Invalid response from server')
            }

            const authUser = Helper.JWTDecode(response.access)
            if (!authUser) {
                throw new Error('Invalid token received')
            }

            LocalStorage.setItem('token', response.access)
            LocalStorage.setItem('authUser', authUser)

            window.location.href = authUser.is_superuser ? '/admin/dashboard.html' : '/user/dashboard.html'

            return true
        } catch (error) {
            throw new Error(`Login failed: ${error.message}`)
        }
    },
    async Logout() {
        try {
            const res = await API.get('auth/logout')

            if (res.status === true) {
                LocalStorage.removeItem('token')
                LocalStorage.removeItem('authUser')
                window.location.href = '/auth/login.html'
            } else {
                throw new Error('Logout failed')
            }

        } catch (error) {
            console.error("Logout error:", error)
            LocalStorage.removeItem('token')
            LocalStorage.removeItem('authUser')
            window.location.href = '/auth/login.html'
        }
    }
}

export default Authentication