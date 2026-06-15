<template>
  <section class="dashboard-view">
    <section class="dashboard-top">
      <header class="dashboard-header">
        <div class="dashboard-header-copy">
          <p class="dashboard-command">
            <span>&gt;</span>
            <strong>mygit.analytics</strong>
          </p>
          <h1>Dashboard</h1>
          <div class="dashboard-summary" aria-label="Alcance del analisis">
            <span class="dashboard-summary-chip">Perfil publico</span>
            <span class="dashboard-summary-chip">Repositorios</span>
            <span class="dashboard-summary-chip">Lenguajes</span>
            <span class="dashboard-summary-chip">Actividad</span>
          </div>
          <p v-if="localUser" class="dashboard-session-chip">
            <span>[local.session]</span>
            <span class="terminal-prompt" aria-hidden="true">&gt;</span>
            <strong>{{ localUser }}</strong>
          </p>
        </div>

        <div class="dashboard-ready" aria-label="Estado del dashboard">
          <span class="status-dot"></span>
          <span>console.ready</span>
        </div>
      </header>

      <section class="search-panel" aria-labelledby="dashboard-search-title">
        <div class="section-heading">
          <div>
            <Search :size="17" aria-hidden="true" />
            <h2 id="dashboard-search-title">profile.lookup</h2>
          </div>
          <span class="status-chip status-chip-ready">{{ loading ? '[RUNNING]' : '[READY]' }}</span>
        </div>

        <form class="terminal-search" @submit.prevent="searchUser">
          <label for="github-username">Usuario de GitHub</label>
          <div class="terminal-search-row">
            <div class="terminal-input">
              <span class="terminal-prompt" aria-hidden="true">&gt;</span>
              <input id="github-username" v-model="username" type="text"
                placeholder="mygit analyze Majestic-Pako" autocomplete="off"/>
            </div>
            <button type="submit":disabled="loading" title="Buscar perfil"
              aria-label="Buscar perfil">
              <Search :size="18" aria-hidden="true" />
            </button>
          </div>
        </form>
      </section>
    </section>

    <section v-if="error || sourceMessage" class="dashboard-state" aria-label="Estado de la consulta">
      <p v-if="error" class="state-message state-message-error">
        <AlertCircle :size="17" aria-hidden="true" />
        <span>{{ error }}</span>
      </p>

      <p v-if="sourceMessage" class="state-message">
        <Database :size="17" aria-hidden="true" />
        <span>{{ sourceMessage }}</span>
        <span v-if="result?.metadata?.cached_at" class="state-separator">|</span>
        <small v-if="result?.metadata?.cached_at">
          Cache: {{ formatDate(result.metadata.cached_at) }}
        </small>
      </p>
    </section>

    <template v-if="result">
      <article class="profile-card" aria-label="Perfil cargado">
        <div class="profile-avatar-frame">
          <img :src="result.profile.avatar_url" :alt="result.profile.username" />
        </div>

        <div class="profile-info">
          <div class="profile-heading">
            <span class="status-chip status-chip-ok">
              <CheckCircle2 :size="15" aria-hidden="true" />
              profile.loaded
            </span>
            <h2>{{ result.profile.name || result.profile.username }}</h2>
            <p class="username">@{{ result.profile.username }}</p>
          </div>

          <p v-if="result.profile.bio" class="profile-bio">{{ result.profile.bio }}</p>

          <a :href="result.profile.html_url" target="_blank" rel="noreferrer" class="github-link">
            <Github :size="17" aria-hidden="true" />
            Ver perfil en GitHub
          </a>
        </div>
      </article>

      <section class="dashboard-section" aria-labelledby="metrics-title">
        <div class="section-heading">
          <div>
            <BarChart3 :size="17" aria-hidden="true" />
            <h2 id="metrics-title">quick.metrics</h2>
          </div>
        </div>

        <div class="metrics-grid">
          <article class="metric-card">
            <span class="metric-icon"><FolderGit2 :size="18" aria-hidden="true" /></span>
            <div class="metric-copy">
              <span class="metric-label">Repositorios publicos</span>
              <strong>{{ result.profile.public_repos }}</strong>
            </div>
          </article>

          <article class="metric-card">
            <span class="metric-icon"><User :size="18" aria-hidden="true" /></span>
            <div class="metric-copy">
              <span class="metric-label">Followers</span>
              <strong>{{ result.profile.followers }}</strong>
            </div>
          </article>

          <article class="metric-card">
            <span class="metric-icon"><Activity :size="18" aria-hidden="true" /></span>
            <div class="metric-copy">
              <span class="metric-label">Following</span>
              <strong>{{ result.profile.following }}</strong>
            </div>
          </article>

          <article class="metric-card metric-card-source">
            <span class="metric-icon"><Database :size="18" aria-hidden="true" /></span>
            <div class="metric-copy">
              <span class="metric-label">Fuente / Cache</span>
              <strong class="metric-source">{{ sourceMessage || 'Estado disponible' }}</strong>
              <small v-if="result?.metadata?.cached_at">
                <Clock :size="14" aria-hidden="true" />
                {{ formatDate(result.metadata.cached_at) }}
              </small>
            </div>
          </article>
        </div>
      </section>

      <section class="repositories-preview" aria-labelledby="repositories-preview-title">
        <div class="section-heading">
          <div>
            <FolderGit2 :size="17" aria-hidden="true" />
            <h2 id="repositories-preview-title">repositories.preview</h2>
          </div>
          <span class="status-chip" :class="{ 'status-chip-ok': hasRepositories }">
            {{ hasRepositories ? '[OK]' : '[PENDING]' }}
          </span>
        </div>

        <div class="repositories-preview-body">
          <div class="repositories-preview-copy">
            <p>Modulo conectado a los repositorios publicos incluidos en la respuesta del perfil.</p>
            <div class="chip-list">
              <span class="status-chip status-chip-ready">[READY] layout.2cols</span>
              <span class="status-chip" :class="{ 'status-chip-ok': hasRepositories }">
                {{ hasRepositories ? '[OK] repositories.data' : '[PENDING] repositories.data' }}
              </span>
            </div>
            <p v-if="hasRepositories" class="repositories-count">
              Mostrando {{ featuredRepositories.length }} de {{ repositoriesCount }} repositorios analizados.
            </p>
          </div>

          <div v-if="hasRepositories" class="repo-placeholder-grid" aria-label="Repositorios destacados">
            <article v-for="repository in featuredRepositories"
              :key="`${repository.name}-${repository.url || repository.updatedAt || repository.language}`"
              class="repo-card">
              <div class="repo-card-header">
                <a v-if="repository.url":href="repository.url" target="_blank"
                  rel="noreferrer" class="repo-name">
                  {{ repository.name }}
                </a>
                <strong v-else class="repo-name">{{ repository.name }}</strong>
                <span v-if="repository.isFork" class="repo-fork-label">fork</span>
              </div>
              <p class="repo-description">{{ repository.description }}</p>
              <div class="repo-meta-row">
                <span>{{ repository.language }}</span>
                <span>{{ repository.stars }} stars</span>
                <span>{{ repository.forks }} forks</span>
                <span v-if="repository.updatedAt">Updated {{ formatShortDate(repository.updatedAt) }}</span>
              </div>
            </article>
          </div>

          <div v-else class="repositories-empty">
            <strong>repositories.empty</strong>
            <p>Todavia no hay repositorios disponibles dentro de la respuesta del backend.</p>
          </div>
        </div>
      </section>

      <section class="secondary-modules" aria-labelledby="modules-title">
        <div class="section-heading section-heading-light">
          <div>
            <Code2 :size="17" aria-hidden="true" />
            <h2 id="modules-title">secondary.modules</h2>
          </div>
          <span class="status-chip">[PENDING]</span>
        </div>

        <div class="dashboard-modules-grid">
          <article class="dashboard-module-card dashboard-module-language">
            <div class="dashboard-module-title">
              <Code2 :size="18" aria-hidden="true" />
              <h3>languages.distribution</h3>
            </div>
            <p>Por lenguaje principal de repositorio.</p>
            <div v-if="languageDistribution.length" class="language-bars">
              <div v-for="language in languageDistribution":key="language.language"
                class="language-row" :style="{ '--language-color': language.color }">
                <div>
                  <span class="language-name">{{ language.language }}</span>
                  <strong>{{ language.percentage }}%</strong>
                </div>
                <span class="language-bar">
                  <span :style="{ width: `${language.percentage}%` }"></span>
                </span>
              </div>
            </div>
            <div v-else class="module-empty">Sin lenguajes disponibles.</div>
            <span class="status-chip" :class="{ 'status-chip-ok': languageDistribution.length }">
              {{ languageDistribution.length ? '[OK] languages.map' : '[PENDING] languages.map' }}
            </span>
          </article>

          <article class="dashboard-module-card dashboard-module-activity">
            <div class="dashboard-module-title">
              <Activity :size="18" aria-hidden="true" />
              <h3>activity.snapshot</h3>
            </div>
            <p>Ultimos repositorios actualizados.</p>
            <div v-if="recentRepositories.length" class="activity-list">
              <div
                v-for="repository in recentRepositories"
                :key="`activity-${repository.name}-${repository.updatedAt}`"
                class="activity-item"
              >
                <strong>{{ repository.name }}</strong>
                <span>{{ formatShortDate(repository.updatedAt) }}</span>
              </div>
            </div>
            <div v-else class="module-empty">Sin fechas de actualizacion disponibles.</div>
            <span class="status-chip" :class="{ 'status-chip-ok': recentRepositories.length }">
              {{ recentRepositories.length ? '[OK] activity.feed' : '[PENDING] activity.feed' }}
            </span>
          </article>

          <article class="dashboard-module-card dashboard-module-status">
            <div class="dashboard-module-title">
              <BarChart3 :size="18" aria-hidden="true" />
              <h3>analysis.status</h3>
            </div>
            <p>Estado del sistema visual.</p>
            <div class="chip-list">
              <span v-for="status in analysisStatus":key="status.label" class="status-chip"
                :class="{
                  'status-chip-ok': status.state === 'ok',
                  'status-chip-ready': status.state === 'ready',
                }">
                {{ status.label }}
              </span>
            </div>
          </article>
        </div>
      </section>
    </template>

    <article v-else class="empty-state">
      <div class="empty-terminal">
        <span>&gt;</span>
        <strong>waiting.for.search</strong>
      </div>
      <h2>Ingresa un usuario para iniciar el analisis.</h2>
      <p>El dashboard todavia no muestra metricas reales porque no hay un perfil cargado.</p>

      <div class="chip-list" aria-label="Estado de modulos">
        <span class="status-chip status-chip-ok">[OK] Perfil general</span>
        <span class="status-chip">[PENDING] Repositorios</span>
        <span class="status-chip">[PENDING] Lenguajes</span>
      </div>
    </article>
  </section>
</template>

<script setup>
// Iconos de Lucide Owo
import {
  Activity,AlertCircle,BarChart3,CheckCircle2,Clock,Code2,
  Database,FolderGit2,Github,Search,User,
} from 'lucide-vue-next'
import { useDashboardViewModel } from '../viewModels/useDashboardViewModel'
import '../styles/dashboard.css'

const {
  localUser,username,loading,error,result,sourceMessage,
  featuredRepositories,repositoriesCount, languageDistribution,
  recentRepositories,hasRepositories,analysisStatus,
  searchUser,formatDate, formatShortDate,
} = useDashboardViewModel()
</script>
