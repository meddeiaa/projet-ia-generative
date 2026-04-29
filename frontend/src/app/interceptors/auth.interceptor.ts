import { HttpInterceptorFn, HttpErrorResponse } from '@angular/common/http';
import { inject } from '@angular/core';
import { catchError, throwError } from 'rxjs';
import { AuthService } from '../services/auth.service';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  /**
   * Rôle de cet interceptor :
   * 1. Ajouter automatiquement le token JWT aux requêtes protégées
   * 2. Détecter les erreurs 401 (token expiré / invalide)
   * 3. Déconnecter automatiquement l'utilisateur si la session n'est plus valide
   */

  const authService = inject(AuthService);
  const token = authService.getToken();

  // Routes d'authentification : on ne met pas de token dessus
  const isAuthRoute =
    req.url.includes('/auth/login') ||
    req.url.includes('/auth/register');

  // Si token existe et que ce n'est pas une route d'auth
  const authReq = token && !isAuthRoute
    ? req.clone({
        setHeaders: {
          Authorization: `Bearer ${token}`
        }
      })
    : req;

  return next(authReq).pipe(
    catchError((error: HttpErrorResponse) => {
      /**
       * Si le backend répond 401 :
       * - token expiré
       * - token invalide
       * - utilisateur supprimé de la DB
       *
       * Alors on déconnecte automatiquement l'utilisateur
       */
      if (error.status === 401 && token && !isAuthRoute) {
        console.warn('🔒 Session expirée ou invalide. Déconnexion automatique.');
        authService.logout();
      }

      return throwError(() => error);
    })
  );
};