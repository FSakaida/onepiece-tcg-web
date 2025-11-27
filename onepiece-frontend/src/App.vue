<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// nome do usuário logado
const username = ref('')

// função para ler do localStorage
const loadUserFromStorage = () => {
  username.value = localStorage.getItem('authUsername') || ''
}

// carregar assim que o app subir
onMounted(() => {
  loadUserFromStorage()

  // ouvir evento customizado quando o login mudar
  window.addEventListener('auth-changed', loadUserFromStorage)
})

onBeforeUnmount(() => {
  window.removeEventListener('auth-changed', loadUserFromStorage)
})

// logout: limpa storage e volta pro login
const logout = () => {
  localStorage.removeItem('authToken')
  localStorage.removeItem('authUserId')
  localStorage.removeItem('authUsername')
  loadUserFromStorage()
  router.push('/')
}
</script>

<template>
  <div>
    <nav>
      <div class="left">
        <!-- Só mostra "Login" se NÃO tiver usuário logado -->
        <RouterLink v-if="!username" to="/">Login</RouterLink>
        <RouterLink to="/cards">Cartas</RouterLink>
        <RouterLink to="/favorites">Favoritos</RouterLink>
        <RouterLink to="/sobre">Sobre</RouterLink>
      </div>

      <div class="right">
        <span v-if="username" class="user-info">
          Logado como: <strong>{{ username }}</strong>
        </span>
        <button v-if="username" class="logout-button" @click="logout">
          Sair
        </button>
      </div>
    </nav>

    <RouterView />
  </div>
</template>


<style>
nav {
  padding: 1rem;
  background: #111;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}

.left,
.right {
  display: flex;
  align-items: center;
  gap: 1rem;
}

a {
  color: #4fc08d;
  text-decoration: none;
}

a.router-link-active {
  text-decoration: underline;
}

.user-info {
  color: #f5f5f5;
  font-size: 0.9rem;
}

.logout-button {
  padding: 0.3rem 0.7rem;
  cursor: pointer;
  border-radius: 4px;
  border: 1px solid #ff6b6b;
  background: #220000;
  color: #ffaaaa;
  font-size: 0.85rem;
}

.logout-button:hover {
  background: #330000;
}
</style>
