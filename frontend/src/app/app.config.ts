import { ApplicationConfig } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideHttpClient, withInterceptors } from '@angular/common/http';
import { routes } from './app.routes';
import { authInterceptor } from './interceptors/auth.interceptor';

export const appConfig: ApplicationConfig = {
  providers: [
    // ✅ Active le routing avec nos routes
    provideRouter(routes),
    
    // ✅ Active HttpClient avec notre interceptor
    provideHttpClient(
      withInterceptors([authInterceptor])
      // Toutes les requêtes HTTP passeront par authInterceptor
    ),
  ]
};