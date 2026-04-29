import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { AuthService } from '../services/auth.service';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  /**
   * Intercepteur HTTP
   * 
   * FONCTIONNEMENT :
   * 1. Récupère le token depuis AuthService
   * 2. Si token existe → clone la requête avec le token
   * 3. Envoie la requête (avec ou sans token)
   * 
   * POURQUOI CLONER LA REQUÊTE ?
   * Les requêtes HTTP sont IMMUABLES (on ne peut pas les modifier)
   * On doit créer une copie avec les nouveaux headers
   */
  
  const authService = inject(AuthService);
  const token = authService.getToken();

  if (token) {
    // Clone la requête et ajoute le header Authorization
    const authReq = req.clone({
      headers: req.headers.set('Authorization', `Bearer ${token}`)
    });
    
    // Envoie la requête avec le token
    return next(authReq);
  }

  // Pas de token → envoie la requête normale (pour login/register)
  return next(req);
};