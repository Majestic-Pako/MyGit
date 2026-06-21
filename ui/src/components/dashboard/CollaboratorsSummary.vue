<template>
  <article class="dashboard-module-card collaborators-summary">
    <header class="collaborators-header">
      <div class="dashboard-module-title">
        <UsersRound :size="18" aria-hidden="true" />
        <div>
          <h3>collaboration.pattern</h3>
          <p>Señal estimada sobre los repositorios analizados</p>
        </div>
      </div>
      <span class="status-chip" :class="{ 'status-chip-ok': summary.contributors.length }">
        {{ summary.contributors.length ? '[OK] signal.detected' : '[LIMITED] signal.data' }}
      </span>
    </header>

    <div class="collaborators-overview">
      <section class="collaboration-pattern" :class="`is-${summary.pattern.key}`">
        <span class="collaboration-pattern-icon" aria-hidden="true">
          <Network :size="25" />
        </span>
        <div>
          <span class="collaboration-eyebrow">patron.detectado</span>
          <h4>{{ summary.pattern.label }}</h4>
          <p>{{ summary.pattern.feedback }}</p>
        </div>
      </section>

      <dl class="collaboration-metrics" aria-label="Resumen estadístico de colaboración">
        <div>
          <dt>Contributors</dt>
          <dd>{{ summary.totalContributors }}</dd>
        </div>
        <div>
          <dt>Repos analizados</dt>
          <dd>{{ summary.repositoriesAnalyzed }}</dd>
        </div>
        <div>
          <dt>Posibles externos</dt>
          <dd>{{ summary.externalContributors }}</dd>
        </div>
        <div>
          <dt>Contribuciones</dt>
          <dd>{{ summary.totalContributions }}</dd>
        </div>
      </dl>
    </div>

    <section class="collaboration-comparison" aria-label="Comparación entre propietario y contributors externos">
      <div class="collaboration-section-heading">
        <div>
          <GitCompareArrows :size="16" aria-hidden="true" />
          <h4>owner.vs.external</h4>
        </div>
        <small>según {{ summary.comparisonBasis }}</small>
      </div>

      <div v-if="summary.hasComparisonData" class="collaboration-share">
        <div class="collaboration-share-labels">
          <span><i class="is-owner"></i> Propietario <strong>{{ summary.ownerPercentage }}%</strong></span>
          <span><i class="is-external"></i> Externos <strong>{{ summary.externalPercentage }}%</strong></span>
        </div>
        <div class="collaboration-share-bar" aria-hidden="true">
          <span class="owner-segment" :style="{ width: `${summary.ownerPercentage}%` }"></span>
          <span class="external-segment" :style="{ width: `${summary.externalPercentage}%` }"></span>
        </div>
      </div>
      <p v-else class="collaborators-empty">Sin datos suficientes para comparar participaciones.</p>
    </section>

    <section class="collaboration-ranking-block">
      <div class="collaboration-section-heading">
        <div>
          <ListOrdered :size="16" aria-hidden="true" />
          <h4>contributors.by.repository</h4>
        </div>
        <small>frecuencia principal · contribuciones secundarias</small>
      </div>

      <ol v-if="summary.contributors.length" class="collaborators-ranking" aria-label="Ranking de colaboradores por repositorio">
        <li v-for="(contributor, index) in summary.contributors" :key="contributor.username">
          <span class="collaborator-position">{{ String(index + 1).padStart(2, '0') }}</span>
          <div class="collaborator-identity">
            <div>
              <strong>@{{ contributor.username }}</strong>
              <span v-if="contributor.isOwner" class="owner-badge">owner</span>
            </div>
            <small>{{ contributor.contributions }} contrib.</small>
          </div>
          <span class="collaborator-frequency-bar" aria-hidden="true">
            <span :style="{ width: `${contributor.frequencyPercentage}%` }"></span>
          </span>
          <strong class="collaborator-repositories">
            {{ contributor.repositoryCount }} {{ contributor.repositoryCount === 1 ? 'repo' : 'repos' }}
          </strong>
        </li>
      </ol>
      <p v-else class="collaborators-empty">Sin contributors disponibles en la muestra.</p>
    </section>
  </article>
</template>

<script setup>
import { GitCompareArrows, ListOrdered, Network, UsersRound } from 'lucide-vue-next'
import '../../css/CollaboratorsSummary.css'

defineProps({
  summary: {
    type: Object,
    required: true,
  },
})
</script>
