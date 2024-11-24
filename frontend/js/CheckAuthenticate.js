import API from './lib/api.js';
import LocalStorage from "./lib/LocalStorage.js";

async function CheckAuthenticate() {
    const publicPaths = ['/auth/login.html'];
    const currentPath = window.location.pathname;

    if (publicPaths.includes(currentPath)) {
        return false;
    }

    try {
        const token = LocalStorage.getItem('token');
        if (!token) {
            throw new Error('No token found');
        }

        const response = await API.get('auth/validate');
        return response.status === 200;
    } catch (error) {
        console.error('Authentication check failed:', error.message);
        window.location.href = '/auth/login.html';
        return false;
    }
}

CheckAuthenticate();