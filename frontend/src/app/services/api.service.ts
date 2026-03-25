import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';

// ===== INTERFACES =====
// Définir la structure des données

export interface GenerateRequest {
  prompt: string;
}

export interface GenerateResponse {
  success: boolean;
  result: string;
}

// ===== SERVICE =====

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  
  // URL du backend
  private baseUrl = 'http://localhost:8000';

  // Injection de HttpClient
  constructor(private http: HttpClient) { }

  // ===== MÉTHODES =====

  /**
   * Génère du texte à partir d'un prompt
   */
  generateText(prompt: string): Observable<GenerateResponse> {
    const url = `${this.baseUrl}/generate/text`;
    const body: GenerateRequest = { prompt };
    
    return this.http.post<GenerateResponse>(url, body)
      .pipe(
        catchError(this.handleError)
      );
  }

  /**
   * Génère une image à partir d'un prompt
   */
  generateImage(prompt: string): Observable<GenerateResponse> {
    const url = `${this.baseUrl}/generate/image`;
    const body: GenerateRequest = { prompt };
    
    return this.http.post<GenerateResponse>(url, body)
      .pipe(
        catchError(this.handleError)
      );
  }

  /**
   * Génère une vidéo à partir d'un prompt
   * Retourne un Blob (fichier binaire)
   */
  generateVideo(prompt: string): Observable<Blob> {
    const url = `${this.baseUrl}/generate/video`;
    const body: GenerateRequest = { prompt };
    
    return this.http.post(url, body, {
      responseType: 'blob'  // Recevoir comme fichier binaire
    }).pipe(
      catchError(this.handleError)
    );
  }

  /**
   * Gestion des erreurs
   */
  private handleError(error: HttpErrorResponse) {
    let errorMessage = 'Une erreur est survenue';
    
    if (error.error instanceof ErrorEvent) {
      // Erreur côté client
      errorMessage = `Erreur: ${error.error.message}`;
    } else {
      // Erreur côté serveur
      errorMessage = `Erreur ${error.status}: ${error.message}`;
    }
    
    console.error(errorMessage);
    return throwError(() => new Error(errorMessage));
  }
}