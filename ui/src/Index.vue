<template>
  <section class="view index-view">
      <div class="index-ambient index-ambient-left" aria-hidden="true"></div>
      <div class="index-ambient index-ambient-right" aria-hidden="true"></div>

      <div class="index-hero">
        <div class="hero-main">
          <div class="identity-badge">
            <BarChart3 :size="16" aria-hidden="true" />
            <span>MyGit Analyzer</span>
          </div>

          <div class="hero-brand">
            <h1>
              <span>My</span><span>Git</span>
            </h1>
          </div>

          <div class="hero-terminal" aria-label="MyGit Terminal">
            <div class="terminal-shell">
              <span class="shell-user">mygit@analyzer</span><span>:~/profile</span>
            </div>

            <div class="terminal-body">
              <div class="terminal-command">
                <span class="prompt-mark">&gt;</span>
                <span class="command-accent">mygit</span>
                <span>analyze username</span>
                <span class="terminal-cursor" aria-hidden="true"></span>
              </div>

              <div class="analysis-output" aria-label="Salida de analisis simulada">
                <div
                  v-for="step in analysisSteps"
                  :key="step.event"
                  class="analysis-line"
                >
                  <span class="status-token">[OK]</span>
                  <span class="event-token">{{ step.event }}</span>
                  <span class="meta-prompt">&gt;</span>
                  <span class="meta-token">{{ step.meta }}</span>
                </div>
              </div>

              <div class="terminal-output">
                <span>output:</span>
                <strong>dashboard.ready</strong>
              </div>
            </div>
          </div>

          <div class="terminal-actions">
            <button type="button" class="analyze-action" @click="goToLogin">
              <LayoutDashboard :size="18" aria-hidden="true" />
              Analizar perfil
            </button>
            <span class="terminal-hint">
              <span class="terminal-hint-prompt">&gt;</span>
              <span class="terminal-hint-run">run</span>
              <strong class="terminal-hint-target">dashboard.preview</strong>
            </span>
          </div>
        </div>

        <aside class="metrics-panel" aria-label="Metricas de analisis">
          <div class="metrics-panel-header">
            <div>
              <BarChart3 :size="18" aria-hidden="true" />
              <span>Profile snapshot</span>
            </div>
            <strong>status: generated</strong>
          </div>

          <div class="snapshot-rows">
            <div v-for="stat in terminalStats":key="stat.label" class="snapshot-row">
              <span>{{ stat.label }}</span>
              <strong>{{ stat.value }}</strong>
            </div>
          </div>

          <div class="snapshot-output">
            <span>output:</span>
            <strong>dashboard.ready</strong>
          </div>
        </aside>
      </div>
  </section>

  <section class="modules-section" aria-labelledby="modules-title">
      <div class="modules-inner">
        <div class="modules-header">
          <p class="modules-command">
            <span>&gt;</span>
            <strong>modules.loaded</strong>
          </p>
          <h2 id="modules-title">Qué analiza MyGit</h2>
          <p>
            Cada módulo transforma datos públicos de GitHub en información clara para el dashboard.
          </p>
        </div>

        <div class="modules-grid">
          <article
            v-for="module in analysisModules"
            :key="module.tag"
            class="module-card"
            :class="`module-card-${module.variant}`"
          >
            <div class="module-card-header">
              <span class="module-icon">
                <component :is="moduleIconMap[module.icon]" :size="18" aria-hidden="true" />
              </span>
              <span class="module-tag">{{ module.tag }}</span>
            </div>

            <div class="module-card-body">
              <h3>{{ module.title }}</h3>
              <p>{{ module.description }}</p>
            </div>

            <div class="module-status">
              <span>{{ module.status }}</span>
            </div>
          </article>
        </div>
      </div>
  </section>
</template>

<script setup>
import {
  Activity,
  BarChart3,
  Code2,
  FolderGit2,
  LayoutDashboard,
  UserRound,
} from 'lucide-vue-next'
import { useIndexViewModel } from './viewModels/useIndexViewModel'
import './css/Index.css'

const { analysisModules, analysisSteps, goToLogin, terminalStats } = useIndexViewModel()

const moduleIconMap = {
  Activity,
  Code2,
  FolderGit2,
  UserRound,
}
</script>
