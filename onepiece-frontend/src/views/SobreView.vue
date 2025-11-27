<script setup>
const autores = [
  'Filipe Sakaida',
  'Tiago Badan'
]
</script>

<template>
  <main class="page">
    <h1>Sobre o Projeto</h1>

    <section class="card">
      <h2>One Piece TCG – Biblioteca de Cartas</h2>
      <p>
        Este projeto é uma aplicação web para consulta de cartas do
        <strong>One Piece Card Game</strong>, com sistema de login, cadastro de usuários
        e lista de cartas favoritas separada por conta.
      </p>

      <p>
        O sistema foi desenvolvido como parte da disciplina
        <strong>Programação Avançada</strong>, utilizando uma arquitetura full stack:
      </p>

      <ul>
        <li><strong>Frontend:</strong> Vue.js + Vue Router</li>
        <li><strong>Backend:</strong> Flask (Python)</li>
        <li><strong>Banco de dados:</strong> MongoDB Atlas (NoSQL)</li>
        <li><strong>Comunicação:</strong> Web Services REST (JSON)</li>
      </ul>
    </section>

    <section class="card">
      <h2>Autores</h2>
      <ul class="autores">
        <li v-for="nome in autores" :key="nome">
          {{ nome }}
        </li>
      </ul>
    </section>

    <section class="card">
      <h2>Funcionalidades principais</h2>
      <ul>
        <li>Cadastro e login de usuários com senha.</li>
        <li>
          Consulta de cartas do One Piece TCG com busca por nome e exibição de
          imagem, cor, tipo, raridade, expansão, custo, poder e efeitos.
        </li>
        <li>
          Lista de favoritos por usuário, com possibilidade de adicionar, remover
          e escrever nota/comentário para cada carta.
        </li>
        <li>
          Página de detalhes da carta com visual mais completo e botão para
          favoritar.
        </li>
      </ul>
    </section>

    <section class="card">
      <h2>Possíveis melhorias futuras</h2>
      <ul>
        <li>Filtros por cor, expansão e tipo de carta.</li>
        <li>Destaque visual para Leaders, Characters, Events, etc.</li>
        <li>Mais estatísticas sobre o deck / meta do jogo.</li>
      </ul>
    </section>
  </main>
</template>

<style scoped>
.page {
  max-width: 900px;
  margin: 0 auto;
  padding: 1.5rem;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  color: #f5f5f5;
}

h1 {
  text-align: center;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
  color: green;
}

.card {
  background: #111;
  border-radius: 10px;
  border: 1px solid #333;
  padding: 1rem 1.25rem;
  margin-bottom: 1rem;
}

.card h2 {
  margin-top: 0;
  margin-bottom: 0.5rem;
}

.card p {
  margin: 0.25rem 0 0.5rem 0;
}

.card ul {
  padding-left: 1.1rem;
  margin: 0.25rem 0;
}

.autores {
  list-style: disc;
}

.autores li {
  margin: 0.15rem 0;
}
</style>
