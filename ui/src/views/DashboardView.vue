<template>
  <section class="view">
    <h1>Dashboard</h1>

    <form class="search-form" @submit.prevent="searchUser">
      <label for="github-username">Usuario de GitHub</label>
      <div class="search-row">
        <input
          id="github-username"
          v-model="username"
          type="text"
          placeholder="agus"
          autocomplete="off"
        />
        <button type="submit" :disabled="loading">
          {{ loading ? 'Buscando...' : 'Buscar' }}
        </button>
      </div>
    </form>

    <p v-if="error" class="error-message">{{ error }}</p>

    <article v-if="result" class="profile-card">
      <img :src="result.profile.avatar_url" :alt="result.profile.username" />

      <div class="profile-info">
        <h2>{{ result.profile.name || result.profile.username }}</h2>
        <p class="username">@{{ result.profile.username }}</p>
        <p v-if="result.profile.bio">{{ result.profile.bio }}</p>

        <dl class="profile-stats">
          <div>
            <dt>Repositorios</dt>
            <dd>{{ result.profile.public_repos }}</dd>
          </div>
          <div>
            <dt>Followers</dt>
            <dd>{{ result.profile.followers }}</dd>
          </div>
          <div>
            <dt>Following</dt>
            <dd>{{ result.profile.following }}</dd>
          </div>
        </dl>

        <a :href="result.profile.html_url" target="_blank" rel="noreferrer">
          Ver perfil en GitHub
        </a>
      </div>
    </article>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import { getGithubUser } from '../services/githubAnalysisService'

const username = ref('')
const loading = ref(false)
const error = ref('')
const result = ref(null)

async function searchUser() {
  loading.value = true
  error.value = ''
  result.value = null

  try {
    result.value = await getGithubUser(username.value)
  } catch (err) {
    error.value = err.message || 'Ocurrio un error inesperado.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.search-form {
  display: grid;
  gap: 10px;
  margin-top: 24px;
}

.search-form label {
  color: var(--text-strong);
  font-weight: 600;
}

.search-row {
  display: flex;
  gap: 12px;
}

.search-row input {
  width: 100%;
  background: var(--background);
  border: 1px solid var(--border);
  border-radius: 6px;
  color: var(--text);
  font: inherit;
  padding: 10px 12px;
}

.search-row input:focus {
  border-color: var(--primary);
  outline: none;
}

.search-row button {
  background: var(--primary);
  border: 0;
  border-radius: 6px;
  color: var(--background);
  cursor: pointer;
  font: inherit;
  font-weight: 700;
  padding: 10px 18px;
}

.search-row button:disabled {
  cursor: not-allowed;
  opacity: 0.7;
}

.error-message {
  color: #ff7b72;
  margin-top: 18px;
}

.profile-card {
  background: var(--surface-elevated);
  border: 1px solid var(--border);
  border-radius: 8px;
  display: flex;
  gap: 20px;
  margin-top: 24px;
  padding: 20px;
}

.profile-card img {
  border-radius: 50%;
  height: 96px;
  width: 96px;
}

.profile-info {
  display: grid;
  gap: 10px;
}

.profile-info h2 {
  color: var(--text-strong);
  font-size: 24px;
  line-height: 1.2;
  margin: 0;
}

.profile-info p {
  margin: 0;
}

.username {
  color: var(--text-muted);
}

.profile-stats {
  display: flex;
  flex-wrap: wrap;
  gap: 14px;
  margin: 4px 0;
}

.profile-stats div {
  background: var(--background);
  border: 1px solid var(--border-soft);
  border-radius: 6px;
  min-width: 110px;
  padding: 10px;
}

.profile-stats dt {
  color: var(--text-muted);
  font-size: 13px;
}

.profile-stats dd {
  color: var(--text-strong);
  font-size: 20px;
  font-weight: 700;
  margin: 4px 0 0;
}

.profile-info a {
  color: var(--blue-soft);
  font-weight: 600;
}

@media (max-width: 640px) {
  .search-row,
  .profile-card {
    flex-direction: column;
  }

  .search-row button {
    width: 100%;
  }
}
</style>
