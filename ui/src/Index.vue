<template>
    <section class="view index-view">
        <div class="index-content">
        <p class="eyebrow">MyGit</p>
        <h1>Explora perfiles de GitHub</h1>
        <p>
            Inicia con un nombre local para entrar al dashboard y buscar perfiles.
        </p>
        <button type="button" class="primary-action" @click="goToLogin">
            Iniciar búsqueda
        </button>
        </div>
    </section>
</template>

<script setup>
import { useIndexViewModel } from './viewModels/useIndexViewModel'
import './css/Index.css'

const { goToLogin } = useIndexViewModel()
</script>
