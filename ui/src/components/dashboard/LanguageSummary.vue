<template>
  <article class="dashboard-module-card language-summary">
    <header class="language-summary-header">
      <div class="dashboard-module-title">
        <Code2 :size="18" aria-hidden="true" />
        <div>
          <h3>languages.analysis</h3>
          <p>Distribucion del codigo analizado</p>
        </div>
      </div>
      <span class="status-chip" :class="{ 'status-chip-ok': summary.languages.length }">
        {{ summary.languages.length ? '[OK] data.mapped' : '[PENDING] data.mapped' }}
      </span>
    </header>

    <template v-if="summary.languages.length">
      <div class="language-summary-overview">
        <section class="language-chart-panel" aria-label="Distribucion porcentual de lenguajes">
          <div
            class="language-donut"
            role="img"
            :aria-label="donutLabel"
            :style="{ '--donut-gradient': summary.donutGradient }"
          >
            <div class="language-donut-center">
              <strong>{{ formatPercentage(summary.primary.percentage) }}%</strong>
              <span>{{ summary.primary.language }}</span>
            </div>
          </div>
          <p><strong>{{ summary.totalLanguages }}</strong> lenguajes detectados</p>
        </section>

        <section class="language-primary-panel" :style="{ '--primary-language-color': summary.primary.color }">
          <span class="language-primary-eyebrow">Lenguaje dominante</span>
          <div class="language-primary-heading">
            <span class="language-primary-icon" :class="{ 'is-generic': !primaryMeta.icon }" aria-hidden="true">
              <Icon v-if="primaryMeta.icon" :icon="primaryMeta.icon" />
              <FileCode2 v-else :size="25" />
            </span>
            <div>
              <h4>{{ summary.primary.language }}</h4>
              <strong>{{ formatPercentage(summary.primary.percentage) }}%</strong>
            </div>
          </div>
          <p class="language-summary-feedback">{{ summary.feedback }}</p>
        </section>
      </div>

      <div class="language-ranking-block">
        <div class="language-ranking-heading">
          <span>ranking.by.usage</span>
          <span>share</span>
        </div>
        <ol class="language-summary-ranking" aria-label="Ranking de lenguajes">
        <li
          v-for="(language, index) in displayLanguages"
          :key="language.language"
          :style="{ '--language-color': language.color }"
        >
          <div class="language-summary-row">
            <span class="language-rank-name">
              <span class="language-rank-icon" aria-hidden="true">
                <Icon v-if="language.meta.icon" :icon="language.meta.icon" />
                <FileCode2 v-else :size="14" />
              </span>
              <b>{{ String(index + 1).padStart(2, '0') }}</b>
              {{ language.language }}
              <small v-if="language.groupedCount">+{{ language.groupedCount }} lenguajes</small>
            </span>
            <strong>{{ formatPercentage(language.percentage) }}%</strong>
          </div>
        </li>
        </ol>
      </div>
    </template>

    <p v-else class="language-summary-empty">Sin lenguajes disponibles.</p>
  </article>
</template>

<script setup>
import { computed } from 'vue'
import { Icon } from '@iconify/vue'
import { Code2, FileCode2 } from 'lucide-vue-next'
import { getLanguageMeta } from '../../utils/languageIcons'
import '../../css/LanguageSummary.css'

const props = defineProps({
  summary: {
    type: Object,
    required: true,
  },
})

const donutLabel = computed(() => props.summary.chartLanguages
  .map((language) => `${language.language}: ${formatPercentage(language.percentage)}%`)
  .join(', '))
const primaryMeta = computed(() => getLanguageMeta(props.summary.primary?.language))
const displayLanguages = computed(() => props.summary.chartLanguages.map((language) => ({
  ...language,
  meta: getLanguageMeta(language.language),
})))

function formatPercentage(value) {
  const percentage = Number(value)
  return Number.isFinite(percentage)
    ? percentage.toLocaleString(undefined, { maximumFractionDigits: 1 })
    : '0'
}
</script>
