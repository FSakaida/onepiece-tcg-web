<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const mode = ref('login') // 'login' ou 'register'
const username = ref('')
const password = ref('')
const message = ref('')
const error = ref('')

// estado para saber se já está logado
const alreadyLogged = ref(false)
const currentUser = ref('')

const switchMode = (newMode) => {
  mode.value = newMode
  message.value = ''
  error.value = ''
}

const handleLogin = async () => {
  message.value = ''
  error.value = ''

  try {
    const res = await fetch('http://127.0.0.1:5000/api/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        username: username.value,
        password: password.value
      })
    })

    const data = await res.json()

    if (!res.ok || !data.success) {
      throw new Error(data.error || 'Erro ao fazer login')
    }

    // Salva o "token" (user_id) e info do usuário
    localStorage.setItem('authToken', data.token)
    localStorage.setItem('authUserId', data.user_id)
    localStorage.setItem('authUsername', data.username)

    // avisa o App.vue que o login mudou
    window.dispatchEvent(new Event('auth-changed'))

    router.push('/cards')
  } catch (err) {
    error.value = err.message || 'Erro desconhecido'
  }
}

const handleRegister = async () => {
  message.value = ''
  error.value = ''

  try {
    const res = await fetch('http://127.0.0.1:5000/api/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        username: username.value,
        password: password.value
      })
    })

    const data = await res.json()

    if (!res.ok || !data.success) {
      throw new Error(data.error || 'Erro ao cadastrar')
    }

    message.value = 'Cadastro realizado com sucesso! Agora faça login.'
    mode.value = 'login'
    password.value = ''
  } catch (err) {
    error.value = err.message || 'Erro desconhecido'
  }
}

// ao carregar a tela, checar se já tem login
onMounted(() => {
  const token = localStorage.getItem('authToken')
  const storedUser = localStorage.getItem('authUsername')

  if (token && storedUser) {
    alreadyLogged.value = true
    currentUser.value = storedUser
  }
})
</script>

<template>
  <div class="shell">
    <main class="page">
      <section class="brand">
        <div class="logo-circle">
          <span class="logo-text">OP</span>
        </div>
        <h1>One Piece TCG</h1>
        <p class="subtitle">Biblioteca de cartas com login e favoritos por conta</p>
        <p class="desc">
          Faça login ou crie uma conta para consultar cartas, marcar favoritas
          e salvar anotações por usuário.
        </p>
      </section>

      <!-- BLOCO "JÁ LOGADO" -->
      <section v-if="alreadyLogged" class="auth-card">
        <h2>Você já está logado</h2>
        <p class="logged-text">
          Sessão ativa como <strong>{{ currentUser }}</strong>.
        </p>

        <div class="logged-actions">
          <button @click="router.push('/cards')">
            Ver cartas
          </button>
          <button @click="router.push('/favorites')">
            Ver favoritos
          </button>
        </div>

        <p class="hint">
          Use o botão <strong>Sair</strong> no topo para trocar de conta.
        </p>
      </section>

      <!-- BLOCO LOGIN / CADASTRO -->
      <section v-else class="auth-card">
        <div class="tabs">
          <button
            :class="{ active: mode === 'login' }"
            @click="switchMode('login')"
          >
            Entrar
          </button>
          <button
            :class="{ active: mode === 'register' }"
            @click="switchMode('register')"
          >
            Cadastrar
          </button>
        </div>

        <div class="form">
          <label>
            Usuário
            <div class="input-wrapper">
              <input
                v-model="username"
                type="text"
                placeholder="Digite seu usuário"
              />
            </div>
          </label>

          <label>
            Senha
            <div class="input-wrapper">
              <input
                v-model="password"
                type="password"
                placeholder="Digite sua senha"
              />
            </div>
          </label>

          <button
            v-if="mode === 'login'"
            class="primary-btn"
            @click="handleLogin"
          >
            Entrar
          </button>

          <button
            v-else
            class="primary-btn"
            @click="handleRegister"
          >
            Criar conta
          </button>

          <p v-if="message" class="message">{{ message }}</p>
          <p v-if="error" class="error">{{ error }}</p>

          <p class="small-hint" v-if="mode === 'register'">
            Após o cadastro, use o mesmo usuário e senha para fazer login.
          </p>
        </div>
      </section>
    </main>
  </div>
</template>

<style scoped>
/* zera margem do body pra não aparecer barra branca em volta */
:global(body) {
  margin: 0;
  background: #020617;
}

/* fundo geral */
.shell {
  min-height: 100vh;
  box-sizing: border-box;
  background: radial-gradient(circle at top, #1f2937, #020617 55%, #000 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem 1rem;
}

/* conteúdo central */
.page {
  width: 100%;
  max-width: 960px;
  display: grid;
  grid-template-columns: minmax(0, 1.2fr) minmax(0, 1fr);
  gap: 1.5rem;
  align-items: stretch;
  color: #f5f5f5;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

@media (max-width: 768px) {
  .page {
    grid-template-columns: 1fr;
  }
}

/* branding lateral */
.brand {
  padding: 1.5rem;
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.08);
  background: linear-gradient(
    135deg,
    rgba(10, 20, 40, 0.95),
    rgba(20, 40, 80, 0.9)
  );
  box-shadow: 0 18px 45px rgba(0, 0, 0, 0.6);
}

.brand h1 {
  margin: 0.75rem 0 0.25rem;
  font-size: 1.8rem;
  letter-spacing: 0.04em;
}

.subtitle {
  margin: 0;
  font-size: 0.95rem;
  color: #c9d6ff;
}

.desc {
  margin-top: 0.75rem;
  font-size: 0.85rem;
  color: #e5e7eb;
}

.logo-circle {
  width: 56px;
  height: 56px;
  border-radius: 999px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: radial-gradient(circle at 30% 20%, #facc15, #f97316);
  box-shadow: 0 0 18px rgba(250, 204, 21, 0.7);
}

.logo-text {
  font-weight: 800;
  color: #111827;
  letter-spacing: 0.06em;
}

/* cartão principal (login/cadastro ou já logado) */
.auth-card {
  background: rgba(3, 7, 18, 0.96);
  border-radius: 16px;
  border: 1px solid rgba(148, 163, 184, 0.25);
  box-shadow: 0 18px 45px rgba(0, 0, 0, 0.7);
  padding: 1.5rem 1.75rem;
  backdrop-filter: blur(16px);
}

/* abas */
.tabs {
  display: inline-flex;
  padding: 0.2rem;
  border-radius: 999px;
  background: rgba(15, 23, 42, 0.9);
  margin-bottom: 1.25rem;
}

.tabs button {
  flex: 1;
  border: none;
  background: transparent;
  color: #dbeafe;
  font-size: 0.9rem;
  padding: 0.4rem 1rem;
  border-radius: 999px;
  cursor: pointer;
  transition:
    background 0.15s ease,
    color 0.15s ease,
    transform 0.1s ease;
}

.tabs button.active {
  background: linear-gradient(135deg, #4fc08d, #1eaa75);
  color: #041014;
  font-weight: 600;
  transform: translateY(-1px);
}

/* formulário */
.form {
  display: flex;
  flex-direction: column;
  gap: 0.9rem;
}

label {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
  font-size: 0.9rem;
  color: #e5e7eb;
}

.input-wrapper {
  display: flex;
  align-items: center;
  padding: 0.4rem 0.75rem;
  border-radius: 999px;
  border: 1px solid #374151;
  background: #020617;
}

input {
  border: none;
  outline: none;
  flex: 1;
  background: transparent;
  color: #f9fafb;
  font-size: 0.9rem;
}

input::placeholder {
  color: #6b7280;
}

.primary-btn {
  padding: 0.55rem 1rem;
  margin-top: 0.5rem;
  cursor: pointer;
  border-radius: 999px;
  border: none;
  background: linear-gradient(135deg, #4fc08d, #1eaa75);
  color: #041014;
  font-weight: 600;
  font-size: 0.95rem;
  box-shadow: 0 8px 20px rgba(15, 118, 110, 0.5);
  transition:
    transform 0.1s ease,
    box-shadow 0.1s ease,
    filter 0.1s ease;
}

.primary-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 10px 26px rgba(15, 118, 110, 0.7);
  filter: brightness(1.03);
}

.error {
  color: #fca5a5;
  font-size: 0.85rem;
}

.message {
  color: #86efac;
  font-size: 0.85rem;
}

.small-hint {
  font-size: 0.78rem;
  color: #9ca3af;
  margin-top: 0.25rem;
}

/* bloco já logado */
.auth-card h2 {
  margin-top: 0;
  margin-bottom: 0.5rem;
}

.logged-text {
  margin: 0.25rem 0 0.75rem 0;
}

.logged-actions {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
}

.logged-actions button {
  flex: 1;
  padding: 0.5rem 0.8rem;
  cursor: pointer;
  border-radius: 999px;
  border: 1px solid #4fc08d;
  background: #020617;
  color: #bbf7d0;
  font-size: 0.85rem;
  transition:
    background 0.1s ease,
    transform 0.1s ease,
    border-color 0.1s ease;
}

.logged-actions button:hover {
  background: #022c22;
  border-color: #7dd3fc;
  transform: translateY(-1px);
}

.hint {
  font-size: 0.8rem;
  color: #9ca3af;
}
</style>
