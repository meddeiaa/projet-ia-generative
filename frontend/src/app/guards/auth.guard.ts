import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { AuthService } from '../services/auth.service';

export const authGuard: CanActivateFn = (route, state) => {
  /**
   * Guard de protection des routes
   * 
   * CanActivateFn = fonction qui décide si on peut accéder à une route
   * 
   * Retourne :
   * ├── true  → accès autorisé
   * └── UrlTree → redirige vers une autre page
   */
  
  const authService = inject(AuthService);
  const router = inject(Router);

  if (authService.isAuthenticated()) {
    // ✅ Utilisateur connecté → accès autorisé
    return true;
  }

  // ❌ Non connecté → redirige vers login
  // On sauvegarde l'URL demandée pour y revenir après login
  return router.createUrlTree(['/login'], {
    queryParams: { returnUrl: state.url }
  });
};