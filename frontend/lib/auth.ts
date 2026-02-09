// frontend/lib/auth.ts
// This file would handle client-side interaction with the Better Auth service.
// For the hackathon, we'll simulate some of its functionality.

const BETTER_AUTH_BASE_URL = process.env.NEXT_PUBLIC_BETTER_AUTH_URL || 'http://localhost:8080/auth'; // Placeholder
const TOKEN_STORAGE_KEY = 'better_auth_jwt';

export const loginWithBetterAuth = async (email: string, password: string) => {
    // In a real scenario, this would be a redirect to Better Auth's login page
    // or an API call to their service if they offer direct integration.
    // For now, we'll simulate getting a JWT.
    console.log(`Simulating login for: ${email}`);
    // Simulate API call to Better Auth for a token
    const response = await fetch(`${BETTER_AUTH_BASE_URL}/login`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
    });

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Login failed');
    }

    const { access_token } = await response.json();
    setAuthToken(access_token);
    await syncUserWithBackend(access_token); // Sync user after successful login
    return access_token;
};

export const signupWithBetterAuth = async (email: string, password: string) => {
    // Similar to login, this would typically involve redirecting to Better Auth
    // or calling their API directly.
    console.log(`Simulating signup for: ${email}`);
    // Simulate API call to Better Auth for signup and then token
    const response = await fetch(`${BETTER_AUTH_BASE_URL}/signup`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
    });

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Signup failed');
    }

    const { access_token } = await response.json();
    setAuthToken(access_token);
    await syncUserWithBackend(access_token); // Sync user after successful signup
    return access_token;
};

// Sync user with our backend after Better Auth provides a token
export const syncUserWithBackend = async (token: string) => {
    const response = await fetch('/api/users/sync', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
        },
    });

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to sync user with backend');
    }
    const user = await response.json();
    console.log('User synced with backend:', user);
    return user;
};


export const getAuthToken = (): string | null => {
    if (typeof window !== 'undefined') {
        return localStorage.getItem(TOKEN_STORAGE_KEY);
    }
    return null;
};

export const setAuthToken = (token: string): void => {
    if (typeof window !== 'undefined') {
        localStorage.setItem(TOKEN_STORAGE_KEY, token);
    }
};

export const removeAuthToken = (): void => {
    if (typeof window !== 'undefined') {
        localStorage.removeItem(TOKEN_STORAGE_KEY);
    }
};

export const isAuthenticated = (): boolean => {
    return !!getAuthToken();
};
