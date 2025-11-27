<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const card = ref(null)
const loading = ref(false)
const error = ref(null)

// popup
const popupVisible = ref(false)
const popupMessage = ref('')

const showPopup = (msg) => {
  popupMessage.value = msg
  popupVisible.value = true
  setTimeout(() => {
    popupVisible.value = false
  }, 2000)
}

const fetchCard = async () => {
  loading.value = true
  error.value = null

  const token = localStorage.getItem('authToken')
  if (!token) {
    router.push('/')
    return
  }

  const cardId = route.params.cardId

  try {
    const res = await fetch(`http://127.0.0.1:5000/api/cards/${encodeURIComponent(cardId)}`)

    if (!res.ok) {
      throw new Error('Erro ao buscar carta')
    }

    card.value = await res.json()
  } catch (err) {
    error.value = err.message || 'Erro desconhecido'
  } finally {
    loading.value = false
  }
}

const addFavorite = async () => {
  if (!card.value) return

  const userId = localStorage.getItem('authUserId')
  if (!userId) {
    showPopup('Faça login novamente.')
    router.push('/')
    return
  }

  try {
    const res = await fetch('http://127.0.0.1:5000/api/favorites', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-User-Id': userId
      },
      body: JSON.stringify({ card_id: card.value.card_id })
    })

    const data = await res.json()

    if (!res.ok) {
      throw new Error(data.error || 'Erro ao favoritar')
    }

    if (data.message) {
      showPopup(data.message)
    } else {
      showPopup(`Carta ${card.value.card_id} adicionada aos favoritos`)
    }
  } catch (err) {
    showPopup(err.message || 'Erro ao favoritar')
  }
}

onMounted(() => {
  fetchCard()
})
</script>

<template>
  <main class="page">
    <button class="back-button" @click="router.push('/cards')">
      ← Voltar para lista
    </button>

    <p v-if="loading">Carregando carta...</p>
    <p v-if="error" class="error">{{ error }}</p>

    <section v-if="card && !loading && !error" class="card-detail">
      <div class="image-column">
        <img
          v-if="card.card_image"
          :src="card.card_image"
          :alt="card.card_name"
          class="card-image"
        />
        <button class="fav-button" @click="addFavorite">
          ⭐ Favoritar
        </button>
      </div>

      <div class="info-column">
        <h1>{{ card.card_name }}</h1>
        <p><strong>card_id:</strong> {{ card.card_id }}</p>
        <p><strong>Código:</strong> {{ card.card_code }}</p>
        <p><strong>Cor:</strong> {{ card.card_color }}</p>
        <p><strong>Tipo:</strong> {{ card.card_type }}</p>
        <p><strong>Raridade:</strong> {{ card.card_rarity }}</p>
        <p><strong>Expansão:</strong> {{ card.card_expansion }}</p>
        <p v-if="card.card_cost !== null"><strong>Custo:</strong> {{ card.card_cost }}</p>
        <p v-if="card.card_power !== null"><strong>Poder:</strong> {{ card.card_power }}</p>
        <p v-if="card.card_counter !== null"><strong>Counter:</strong> {{ card.card_counter }}</p>

        <p v-if="card.card_banned">
          <strong>Banlist:</strong> {{ card.card_banned }}
        </p>

        <div v-if="card.card_effect" class="block">
          <h2>Efeito</h2>
          <p>{{ card.card_effect }}</p>
        </div>

        <div v-if="card.card_trigger" class="block">
          <h2>Trigger</h2>
          <p>{{ card.card_trigger }}</p>
        </div>
      </div>
    </section>

    <div v-if="popupVisible" class="popup">
      {{ popupMessage }}
    </div>
  </main>
</template>

<style scoped>
.page {
  max-width: 1000px;
  margin: 0 auto;
  padding: 1.5rem;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  color: #f5f5f5;
}

.back-button {
  margin-bottom: 1rem;
  padding: 0.4rem 0.8rem;
  cursor: pointer;
  border-radius: 4px;
  border: 1px solid #4fc08d;
  background: #003322;
  color: #a8ffd2;
  font-size: 0.85rem;
}

.back-button:hover {
  background: #005533;
}

.card-detail {
  display: grid;
  grid-template-columns: minmax(0, 320px) minmax(0, 1fr);
  gap: 1.5rem;
  background: #111;
  border-radius: 10px;
  border: 1px solid #333;
  padding: 1rem;
}

.image-column {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
}

.card-image {
  width: 100%;
  max-width: 320px;
  border-radius: 8px;
  object-fit: cover;
  box-shadow: 0 0 12px rgba(0, 0, 0, 0.7);
}

.fav-button {
  padding: 0.4rem 0.9rem;
  cursor: pointer;
  border-radius: 4px;
  border: 1px solid #ffd700;
  background: #222;
  color: #ffd700;
  font-size: 0.9rem;
}

.fav-button:hover {
  background: #333;
}

.info-column h1 {
  margin-top: 0;
  margin-bottom: 0.5rem;
  font-size: 1.4rem;
}

.info-column p {
  margin: 0.15rem 0;
}

.block {
  margin-top: 0.75rem;
  padding: 0.5rem;
  background: #181818;
  border-radius: 6px;
}

.block h2 {
  margin: 0 0 0.25rem 0;
  font-size: 1rem;
}

.error {
  color: #ff6b6b;
}

/* popup */
.popup {
  position: fixed;
  bottom: 1rem;
  right: 1rem;
  background: #222;
  color: #ffd700;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  border: 1px solid #ffd700;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
  z-index: 1000;
  font-size: 0.9rem;
}
</style>
