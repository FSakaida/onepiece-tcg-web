<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const favorites = ref([])
const loading = ref(false)
const error = ref(null)
const feedback = ref('')

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

const fetchFavorites = async () => {
  loading.value = true
  error.value = null

  const userId = localStorage.getItem('authUserId')
  if (!userId) {
    error.value = 'Usuário não autenticado'
    showPopup('Faça login novamente.')
    loading.value = false
    router.push('/')
    return
  }

  try {
    const res = await fetch('http://127.0.0.1:5000/api/favorites', {
      headers: {
        'X-User-Id': userId
      }
    })

    if (!res.ok) {
      throw new Error('Erro ao buscar favoritos')
    }

    favorites.value = await res.json()
  } catch (err) {
    error.value = err.message || 'Erro desconhecido'
  } finally {
    loading.value = false
  }
}

const removeFavorite = async (favId) => {
  feedback.value = ''

  const userId = localStorage.getItem('authUserId')
  if (!userId) {
    error.value = 'Usuário não autenticado'
    showPopup('Faça login novamente.')
    router.push('/')
    return
  }

  try {
    const res = await fetch(`http://127.0.0.1:5000/api/favorites/${favId}`, {
      method: 'DELETE',
      headers: {
        'X-User-Id': userId
      }
    })

    const data = await res.json()

    if (!res.ok) {
      throw new Error(data.error || 'Erro ao remover favorito')
    }

    favorites.value = favorites.value.filter(f => f.id !== favId)
    feedback.value = 'Favorito removido com sucesso.'
    showPopup('Favorito removido com sucesso.')
  } catch (err) {
    const msg = err.message || 'Erro ao remover favorito'
    feedback.value = msg
    showPopup(msg)
  }
}

// UPDATE: salvar a nota do favorito
const saveFavoriteNote = async (fav) => {
  feedback.value = ''

  const userId = localStorage.getItem('authUserId')
  if (!userId) {
    error.value = 'Usuário não autenticado'
    showPopup('Faça login novamente.')
    router.push('/')
    return
  }

  try {
    const res = await fetch(`http://127.0.0.1:5000/api/favorites/${fav.id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'X-User-Id': userId
      },
      body: JSON.stringify({ note: fav.note || '' })
    })

    const data = await res.json()

    if (!res.ok) {
      throw new Error(data.error || 'Erro ao atualizar favorito')
    }

    feedback.value = 'Nota atualizada com sucesso.'
    showPopup('Nota atualizada com sucesso.')
  } catch (err) {
    const msg = err.message || 'Erro ao atualizar favorito'
    feedback.value = msg
    showPopup(msg)
  }
}

onMounted(() => {
  const token = localStorage.getItem('authToken')
  if (!token) {
    router.push('/') // não logado? volta pro login
    return
  }

  fetchFavorites()
})
</script>

<template>
  <main class="page">
    <h1>Favoritos</h1>

    <p v-if="loading">Carregando favoritos...</p>
    <p v-if="error" class="error">{{ error }}</p>
    <p v-if="feedback" class="feedback">{{ feedback }}</p>

    <section v-if="!loading && !error" class="cards-grid">
      <article
        v-for="fav in favorites"
        :key="fav.id"
        class="card"
      >
        <h2>{{ fav.card?.card_name || fav.card_id }}</h2>
        <p><strong>card_id:</strong> {{ fav.card_id }}</p>

        <img
          v-if="fav.card && fav.card.card_image"
          :src="fav.card.card_image"
          :alt="fav.card.card_name"
          class="card-image"
        />

        <p v-if="fav.card"><strong>Cor:</strong> {{ fav.card.card_color }}</p>
        <p v-if="fav.card"><strong>Tipo:</strong> {{ fav.card.card_type }}</p>
        <p v-if="fav.card"><strong>Raridade:</strong> {{ fav.card.card_rarity }}</p>
        <p v-if="fav.card"><strong>Expansão:</strong> {{ fav.card.card_expansion }}</p>

        <!-- CAMPO DE NOTA / COMENTÁRIO -->
        <label class="note-label">
          Nota / Comentário:
          <textarea
            v-model="fav.note"
            rows="2"
            placeholder="Escreva algo sobre esta carta..."
          />
        </label>

        <div class="buttons">
          <button class="save-button" @click="saveFavoriteNote(fav)">
            Salvar nota
          </button>

          <button class="remove-button" @click="removeFavorite(fav.id)">
            Remover dos favoritos
          </button>
        </div>
      </article>

      <p v-if="favorites.length === 0 && !loading">
        Você ainda não tem favoritos.
      </p>
    </section>

    <!-- POPUP / TOAST -->
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

.card-image {
  width: 100%;
  border-radius: 6px;
  margin-bottom: 0.5rem;
  object-fit: cover;
}

.error {
  color: #ff6b6b;
}

.feedback {
  color: #4fc08d;
  margin-bottom: 0.5rem;
}

.note-label {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  margin-top: 0.5rem;
  font-size: 0.9rem;
}

textarea {
  resize: vertical;
  padding: 0.4rem;
  font-family: inherit;
  font-size: 0.9rem;
  background: #222;
  color: #f5f5f5;
  border-radius: 4px;
  border: 1px solid #555;
}

.buttons {
  display: flex;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.save-button {
  padding: 0.4rem 0.8rem;
  cursor: pointer;
  border-radius: 4px;
  border: 1px solid #4fc08d;
  background: #003322;
  color: #a8ffd2;
  font-size: 0.9rem;
}

.save-button:hover {
  background: #005533;
}

.remove-button {
  padding: 0.4rem 0.8rem;
  cursor: pointer;
  border-radius: 4px;
  border: 1px solid #ff6b6b;
  background: #220000;
  color: #ffaaaa;
  font-size: 0.9rem;
}

.remove-button:hover {
  background: #330000;
}

/* POPUP NO CANTINHO */
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
