<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const cards = ref([])
const loading = ref(false)
const error = ref(null)
const searchName = ref('')

const favFeedback = ref('')

// estado do popup
const popupVisible = ref(false)
const popupMessage = ref('')

const showPopup = (msg) => {
  popupMessage.value = msg
  popupVisible.value = true
  setTimeout(() => {
    popupVisible.value = false
  }, 2000) // some depois de 2 segundos
}

const fetchCards = async () => {
  loading.value = true
  error.value = null

  try {
    const params = new URLSearchParams()
    if (searchName.value.trim() !== '') {
      params.append('name', searchName.value.trim())
    }

    const url = `http://127.0.0.1:5000/api/cards?${params.toString()}`
    const res = await fetch(url)

    if (!res.ok) {
      throw new Error('Erro ao buscar cartas')
    }

    cards.value = await res.json()
  } catch (err) {
    error.value = err.message || 'Erro desconhecido'
  } finally {
    loading.value = false
  }
}

const goToCard = (cardId) => {
  router.push(`/cards/${encodeURIComponent(cardId)}`)
}

const addFavorite = async (cardId) => {
  favFeedback.value = ''

  const userId = localStorage.getItem('authUserId')
  if (!userId) {
    error.value = 'Usuário não autenticado'
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
      body: JSON.stringify({ card_id: cardId })
    })

    const data = await res.json()

    if (!res.ok) {
      throw new Error(data.error || 'Erro ao favoritar')
    }

    if (data.message) {
      const msg = data.message + ` (${cardId})`
      favFeedback.value = msg
      showPopup(msg)
    } else {
      const msg = `Carta ${cardId} adicionada aos favoritos`
      favFeedback.value = msg
      showPopup(msg)
    }
  } catch (err) {
    const msg = err.message || 'Erro ao favoritar'
    favFeedback.value = msg
    showPopup(msg)
  }
}

onMounted(() => {
  const token = localStorage.getItem('authToken')
  if (!token) {
    router.push('/')   // não logado? volta pro login
    return
  }

  fetchCards()
})
</script>

<template>
  <main class="page">
    <h1>Cartas One Piece TCG</h1>

    <section class="search">
      <input
        v-model="searchName"
        @keyup.enter="fetchCards"
        type="text"
        placeholder="Buscar por nome (ex: Zoro)"
      />
      <button @click="fetchCards">Buscar</button>
    </section>

    <p v-if="loading">Carregando cartas...</p>
    <p v-if="error" class="error">{{ error }}</p>
    <p v-if="favFeedback" class="fav-feedback">{{ favFeedback }}</p>

    <section v-if="!loading && !error" class="cards-grid">
      <article
        v-for="card in cards"
        :key="card.id"
        class="card card-clickable"
        @click="goToCard(card.card_id)"
      >
        <img
          v-if="card.card_image"
          :src="card.card_image"
          :alt="card.card_name"
          class="card-image"
        />

        <h2>{{ card.card_name }}</h2>
        <p><strong>Código:</strong> {{ card.card_code }}</p>
        <p><strong>card_id:</strong> {{ card.card_id }}</p>
        <p><strong>Cor:</strong> {{ card.card_color }}</p>
        <p><strong>Tipo:</strong> {{ card.card_type }}</p>
        <p><strong>Raridade:</strong> {{ card.card_rarity }}</p>
        <p><strong>Expansão:</strong> {{ card.card_expansion }}</p>
        <p v-if="card.card_cost !== null"><strong>Custo:</strong> {{ card.card_cost }}</p>
        <p v-if="card.card_power !== null"><strong>Poder:</strong> {{ card.card_power }}</p>
        <p class="effect" v-if="card.card_effect">
          <strong>Efeito:</strong> {{ card.card_effect }}
        </p>

        <button
          class="fav-button"
          @click.stop="addFavorite(card.card_id)"
        >
          ⭐ Favoritar
        </button>
      </article>

      <p v-if="cards.length === 0 && !loading">Nenhuma carta encontrada.</p>
    </section>

    <div v-if="popupVisible" class="popup">
      {{ popupMessage }}
    </div>
  </main>
</template>

<style scoped>
.page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1.5rem;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

h1 {
  margin-bottom: 1rem;
}

.search {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.search input {
  flex: 1;
  padding: 0.5rem;
}

.search button {
  padding: 0.5rem 1rem;
  cursor: pointer;
}

.cards-grid {
  display: grid;
  gap: 1rem;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
}

.card {
  border: 1px solid #444;
  border-radius: 8px;
  padding: 0.75rem;
  background: #111;
  color: #f5f5f5;
}

/* tornar o card clicável */
.card-clickable {
  cursor: pointer;
  transition: transform 0.08s ease, box-shadow 0.08s ease, border-color 0.08s ease;
}

.card-clickable:hover {
  transform: translateY(-2px);
  border-color: #4fc08d;
  box-shadow: 0 0 10px rgba(79, 192, 141, 0.3);
}

.card-image {
  width: 100%;
  border-radius: 6px;
  margin-bottom: 0.5rem;
  object-fit: cover;
}

.card h2 {
  margin-top: 0;
  margin-bottom: 0.5rem;
  font-size: 1.1rem;
}

.effect {
  margin-top: 0.5rem;
  font-size: 0.9rem;
}

.error {
  color: #ff6b6b;
}

.fav-button {
  margin-top: 0.5rem;
  padding: 0.4rem 0.8rem;
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

.fav-feedback {
  margin-bottom: 0.5rem;
  color: #ffd700;
  font-size: 0.9rem;
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
