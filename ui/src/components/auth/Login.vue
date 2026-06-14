<template>
    <section class="view auth-view">
        <form class="login-form" @submit.prevent="submitLogin">
        <h1>Ingresar</h1>
        <p>Usa un nombre visible para guardar tu sesión local.</p>

        <label for="local-username">Nombre</label>
        <input
            id="local-username"
            v-model="localUsername"
            type="text"
            placeholder="Agustin"
            autocomplete="name"
        />

        <p v-if="error" class="error-message">{{ error }}</p>

        <button type="submit">Entrar al dashboard</button>
        </form>
    </section>
</template>

<script setup>
import { useLoginViewModel } from '../../viewModels/useLoginViewModel'

const { localUsername, error, submitLogin } = useLoginViewModel()
</script>

<style scoped>
    .auth-view {
    max-width: 520px;
    margin: 0 auto;
}

.login-form {
    display: grid;
    gap: 14px;
}

.login-form p {
    margin-bottom: 8px;
}

.login-form label {
    color: var(--text-strong);
    font-weight: 600;
}

.login-form input {
    background: var(--background);
    border: 1px solid var(--border);
    border-radius: 6px;
    color: var(--text);
    font: inherit;
    padding: 10px 12px;
}

.login-form input:focus {
    border-color: var(--primary);
    outline: none;
}

.login-form button {
    background: var(--primary);
    border: 0;
    border-radius: 6px;
    color: var(--background);
    cursor: pointer;
    font: inherit;
    font-weight: 700;
    padding: 11px 18px;
}
</style>
