import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import CardsView from '../views/CardsView.vue'
import FavoritesView from '../views/FavoritesView.vue'
import CardDetailView from '../views/CardDetailView.vue'
import SobreView from '../views/SobreView.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [  
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/cards',
      name: 'cards',
      component: CardsView
    },
    {
      path: '/cards/:cardId',
      name: 'card-detail',
      component: CardDetailView,
      props: true
    },
    {
      path: '/favorites',
      name: 'favorites',
      component: FavoritesView
    },
    {
      path: '/sobre',
      name: 'sobre',
      component: SobreView
    }

  ]
})

export default router
