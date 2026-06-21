<template>
    <section class="auth-view">
        <div class="auth-glow auth-glow-green" aria-hidden="true"></div>
        <div class="auth-glow auth-glow-orange" aria-hidden="true"></div>

        <div class="auth-layout">
        <section class="auth-copy" aria-labelledby="login-heading">
            <div class="terminal-pill" aria-hidden="true">
            <span class="terminal-path">~/mygit</span>
            <span class="terminal-symbol">$</span>
            <span class="terminal-action">init session</span>
            <span class="terminal-cursor"></span>
            </div>

            <div class="auth-heading">
            <p class="auth-eyebrow">Local workspace</p>
            <h1 id="login-heading">Activa tu workspace local</h1>
            <p>Una sesion simple para personalizar el dashboard y mantener el flujo de analisis en tu navegador.</p>
            </div>

            <div class="tech-list" aria-label="Estado tecnico de la sesion">
            <div class="tech-row tech-row-green">
                <span class="tech-icon" aria-hidden="true">o</span>
                <span class="tech-label">localhost</span>
                <span class="tech-status">ONLINE</span>
            </div>
            <div class="tech-row tech-row-orange">
                <span class="tech-icon" aria-hidden="true">#</span>
                <span class="tech-label">JSON cache</span>
                <span class="tech-status">LOCAL</span>
            </div>
            <div class="tech-row tech-row-green">
                <span class="tech-icon" aria-hidden="true">+</span>
                <span class="tech-label">GitHub API</span>
                <span class="tech-status">READY</span>
            </div>
            <div class="tech-row tech-row-orange">
                <span class="tech-icon" aria-hidden="true">&gt;</span>
                <span class="tech-label">dashboard.ready</span>
                <span class="tech-status">NEXT</span>
            </div>
            </div>
        </section>

        <section class="auth-form-column" aria-label="Inicio de sesion local">
            <aside class="login-card" aria-label="Formulario de sesion local">
            <header class="login-card-header">
                <p class="login-eyebrow">MYGIT LOCAL</p>
            <h2>{{ isRegisterMode ? 'Crear cuenta' : 'Iniciar sesión' }}</h2>
            <p>{{ isRegisterMode
                ? 'Creá tu usuario para guardar búsquedas en MyGit.'
                : 'Ingresá a MyGit para continuar al dashboard.' }}</p>
            </header>

            <div class="session-preview" aria-label="Vista previa de sesion">
                <span class="session-dot" aria-hidden="true"></span>
                <span class="session-path">
                localhost / <strong>{{ localUsername || 'usuario' }}</strong>
                </span>
            </div>

            <form class="login-form" @submit.prevent="submitLogin" novalidate>
                <div class="field">
                <label for="local-username" class="field-label">Usuario</label>
                <div class="terminal-input" :class="{ 'terminal-input-error': error }">
                    <span class="input-prompt" aria-hidden="true">&gt;_</span>
                    <input id="local-username" v-model="localUsername" type="text"
                    placeholder="Agus" autocomplete="username" class="field-input"
                    spellcheck="false"/>
                </div>
                </div>

                <div class="field">
                <label for="password" class="field-label">Contraseña</label>
                <div class="terminal-input" :class="{ 'terminal-input-error': error }">
                    <span class="input-prompt" aria-hidden="true">&gt;_</span>
                    <input id="password" v-model="password" type="password"
                    placeholder="••••••••" :autocomplete="isRegisterMode ? 'new-password' : 'current-password'"
                    class="field-input"/>
                </div>
                </div>

                <div v-if="isRegisterMode" class="field">
                <label for="confirm-password" class="field-label">Confirmar contraseña</label>
                <div class="terminal-input" :class="{ 'terminal-input-error': error }">
                    <span class="input-prompt" aria-hidden="true">&gt;_</span>
                    <input id="confirm-password" v-model="confirmPassword" type="password"
                    placeholder="••••••••" autocomplete="new-password" class="field-input"/>
                </div>
                </div>

                <p v-if="error" class="error-message" role="alert">
                <span aria-hidden="true">!</span>
                {{ error }}
                </p>

                <button type="submit" class="btn-primary" :disabled="loading">
                {{ loading ? 'Procesando...' : (isRegisterMode ? 'Registrarse' : 'Entrar') }}
                </button>

                <button type="button" class="auth-mode-link" @click="toggleMode">
                {{ isRegisterMode
                    ? '¿Ya tenés cuenta? Iniciar sesión'
                    : '¿No tenés cuenta? Crear cuenta' }}
                </button>
            </form>
            </aside>

            <RouterLink to="/" class="back-icon-link" aria-label="Volver al inicio"
            title="Volver al inicio">&lt;</RouterLink>
        </section>
        </div>
    </section>
</template>

<script setup>
import { useLoginViewModel } from '../../viewModels/useLoginViewModel'
import '../../css/Login.css'
const {
    localUsername, password, confirmPassword, isRegisterMode,
    loading, error, toggleMode, submitLogin,
} = useLoginViewModel()
</script>
