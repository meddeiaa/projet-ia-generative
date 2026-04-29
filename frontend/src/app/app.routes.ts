import { Routes } from '@angular/router';
import { authGuard } from './guards/auth.guard';

export const routes: Routes = [
  // ======================================================
  // ROUTES PUBLIQUES (sans connexion)
  // ======================================================
  
  {
    path: 'login',
    loadComponent: () =>
      import('./pages/login/login.component')
        .then(m => m.LoginComponent),
    title: 'Connexion - IA Générative'
  },
  {
    path: 'register',
    loadComponent: () =>
      import('./pages/register/register.component')
        .then(m => m.RegisterComponent),
    title: 'Inscription - IA Générative'
  },

  // ======================================================
  // ROUTES PROTÉGÉES (nécessitent connexion)
  // ======================================================
  
  {
    path: 'dashboard',
    loadComponent: () =>
      import('./pages/dashboard/dashboard.component')
        .then(m => m.DashboardComponent),
    canActivate: [authGuard],  // ← Protection !
    title: 'Dashboard - IA Générative'
  },

  // ======================================================
  // REDIRECTIONS
  // ======================================================
  
  {
    path: '',
    redirectTo: '/dashboard',
    pathMatch: 'full'
    // Si URL vide → va sur dashboard
    // AuthGuard redirigera vers login si non connecté
  },
  {
    path: '**',
    redirectTo: '/dashboard'
    // URL inconnue → dashboard
  }
];